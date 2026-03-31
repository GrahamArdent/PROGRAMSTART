from __future__ import annotations

import argparse
import os
import re
import shutil
import signal
import socket
import subprocess
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class FactoryScenario:
    slug: str
    project_name: str
    product_shape: str
    needs: tuple[str, ...] = ()
    requires_userjourney: bool = False
    requires_npm: bool = False
    runtime_mode: str = "default"


SCENARIOS = (
    FactoryScenario(slug="cli", project_name="SMOKE CLI", product_shape="CLI tool"),
    FactoryScenario(
        slug="api",
        project_name="SMOKE API",
        product_shape="API service",
        runtime_mode="api_boot",
    ),
    FactoryScenario(
        slug="api_agents",
        project_name="SMOKE API AGENTS",
        product_shape="API service",
        needs=("rag", "agents"),
        runtime_mode="api_modules",
    ),
    FactoryScenario(slug="data", project_name="SMOKE DATA", product_shape="data pipeline"),
    FactoryScenario(
        slug="web",
        project_name="SMOKE WEB",
        product_shape="web app",
        requires_userjourney=True,
        requires_npm=True,
    ),
)


def slugify_project_name(project_name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", project_name.strip()).strip("_").lower()
    return slug or "generated_app"


def npm_executable() -> str:
    return "npm.cmd" if os.name == "nt" else "npm"


def clean_subprocess_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("VIRTUAL_ENV", None)
    return env


def remove_tree(path: Path) -> None:
    if not path.exists():
        return
    last_error: OSError | None = None
    attempts = 6 if os.name == "nt" else 1
    for attempt in range(attempts):
        try:
            shutil.rmtree(path)
            return
        except FileNotFoundError:
            return
        except OSError as exc:
            last_error = exc
            if attempt == attempts - 1:
                raise
            time.sleep(0.5 * (attempt + 1))
    if last_error is not None:
        raise last_error


def run_command(command: list[str], cwd: Path, *, timeout: int = 0) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        env=clean_subprocess_env(),
        capture_output=True,
        text=True,
        check=False,
        timeout=None if timeout <= 0 else timeout,
    )
    output = (result.stdout + result.stderr).strip()
    if result.returncode != 0:
        command_text = " ".join(command)
        detail = output or f"command exited with code {result.returncode}"
        raise RuntimeError(f"{command_text} failed in {cwd}:\n{detail}")
    return output


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def stop_process_tree(process: subprocess.Popen[str]) -> str:
    if process.poll() is None:
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/T", "/F", "/PID", str(process.pid)],
                capture_output=True,
                text=True,
                check=False,
            )
        else:
            os.killpg(process.pid, signal.SIGTERM)
    try:
        stdout, _ = process.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, _ = process.communicate(timeout=15)
    return stdout.strip()


def wait_for_http(url: str, *, expected_text: str, process: subprocess.Popen[str], timeout_seconds: int) -> str:
    deadline = time.time() + timeout_seconds
    last_error = ""
    while time.time() < deadline:
        if process.poll() is not None:
            break
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                body = response.read().decode("utf-8", errors="replace")
            if expected_text in body:
                return body
            last_error = f"response from {url} did not contain expected text: {expected_text}"
        except urllib.error.URLError as exc:
            last_error = str(exc)
        time.sleep(1)
    logs = stop_process_tree(process)
    raise RuntimeError(f"Timed out waiting for {url}. Last error: {last_error}\n{logs}")


def start_server(command: list[str], cwd: Path) -> subprocess.Popen[str]:
    kwargs: dict[str, object] = {
        "cwd": cwd,
        "env": clean_subprocess_env(),
        "stdout": subprocess.PIPE,
        "stderr": subprocess.STDOUT,
        "text": True,
        "start_new_session": True,
    }
    return subprocess.Popen(command, **kwargs)


def create_repo(
    *,
    scenario: FactoryScenario,
    destination: Path,
    workspace: Path,
    program: str,
) -> None:
    command = [
        program,
        "create",
        "--dest",
        str(destination),
        "--project-name",
        scenario.project_name,
        "--product-shape",
        scenario.product_shape,
        "--owner",
        "SMOKE",
        "--force",
    ]
    for need in scenario.needs:
        command.extend(["--need", need])
    if scenario.requires_userjourney:
        command.extend(["--attachment-source", str(workspace / "USERJOURNEY")])
    run_command(command, workspace)


def validate_created_repo(repo_root: Path, scenario: FactoryScenario) -> None:
    run_command(["uv", "sync", "--extra", "dev"], repo_root)
    checks = ["bootstrap-assets", "authority-sync", "planning-references", "workflow-state"]
    if not scenario.requires_userjourney:
        checks.insert(0, "all")
    for check in checks:
        run_command(["uv", "run", "programstart", "validate", "--check", check], repo_root)
    run_command(["uv", "run", "programstart", "prompt-eval", "--json"], repo_root)
    run_command(["uv", "run", "python", "scripts/programstart_cli_smoke.py", "--workspace", "."], repo_root)


def smoke_cli_starter(repo_root: Path, scenario: FactoryScenario) -> None:
    package_name = slugify_project_name(scenario.project_name)
    starter_root = repo_root / "starter" / "cli_tool"
    output = run_command(
        ["uv", "run", "--project", ".", "python", "-m", f"{package_name}.main", "--name", "smoke", "--enthusiasm", "2"],
        starter_root,
    )
    if "hello, smoke!!" not in output:
        raise RuntimeError(f"CLI starter output mismatch in {starter_root}:\n{output}")


def smoke_api_server_starter(repo_root: Path) -> None:
    starter_root = repo_root / "starter" / "api_service"
    port = free_port()
    process = start_server(
        [
            "uv",
            "run",
            "--project",
            ".",
            "python",
            "-c",
            (
                "from app.main import app; "
                "import uvicorn; "
                f"uvicorn.run(app, host='127.0.0.1', port={port}, log_level='warning')"
            ),
        ],
        starter_root,
    )
    try:
        body = wait_for_http(
            f"http://127.0.0.1:{port}/health",
            expected_text='"status":"ok"',
            process=process,
            timeout_seconds=45,
        )
        if '"service"' not in body:
            raise RuntimeError(f"API starter response missing service payload:\n{body}")
    finally:
        if process.poll() is None:
            stop_process_tree(process)


def smoke_api_module_starter(repo_root: Path) -> None:
    starter_root = repo_root / "starter" / "api_service"
    output = run_command(
        [
            "uv",
            "run",
            "--project",
            ".",
            "python",
            "-c",
            (
                "from app.config import ServiceSettings; "
                "from app.ai import build_llm_router_hint; "
                "from app.retrieval import retrieval_backend; "
                "from app.workflows import orchestration_plan; "
                "print(ServiceSettings().model_dump()); "
                "print(build_llm_router_hint()); "
                "print(retrieval_backend()); "
                "print(orchestration_plan())"
            ),
        ],
        starter_root,
    )
    if "service_name" not in output or "litellm" not in output or "chromadb" not in output or "temporal" not in output:
        raise RuntimeError(f"API starter output mismatch in {starter_root}:\n{output}")


def smoke_data_starter(repo_root: Path, scenario: FactoryScenario) -> None:
    package_name = slugify_project_name(scenario.project_name)
    starter_root = repo_root / "starter" / "data_pipeline"
    output = run_command(
        ["uv", "run", "--project", ".", "python", "-m", f"{package_name}.main", "sample_input.csv"],
        starter_root,
    )
    if "'rows': 3" not in output or "'total': 65" not in output:
        raise RuntimeError(f"Data pipeline starter output mismatch in {starter_root}:\n{output}")


def smoke_web_starter(repo_root: Path) -> None:
    starter_root = repo_root / "starter" / "web_app"
    run_command([npm_executable(), "install", "--no-audit", "--no-fund"], starter_root, timeout=300)
    run_command([npm_executable(), "run", "build"], starter_root, timeout=300)
    port = free_port()
    process = start_server(
        [npm_executable(), "run", "start", "--", "--hostname", "127.0.0.1", "--port", str(port)],
        starter_root,
    )
    try:
        body = wait_for_http(
            f"http://127.0.0.1:{port}",
            expected_text="recommended product stack",
            process=process,
            timeout_seconds=90,
        )
        if "Workflow-first planning" not in body:
            raise RuntimeError(f"Web starter response missing expected content:\n{body}")
    finally:
        if process.poll() is None:
            stop_process_tree(process)


def smoke_starter_runtime(repo_root: Path, scenario: FactoryScenario, *, require_web_runtime: bool) -> None:
    if scenario.slug == "cli":
        smoke_cli_starter(repo_root, scenario)
        return
    if scenario.runtime_mode == "api_boot":
        smoke_api_server_starter(repo_root)
        return
    if scenario.runtime_mode == "api_modules":
        smoke_api_module_starter(repo_root)
        return
    if scenario.slug == "data":
        smoke_data_starter(repo_root, scenario)
        return
    if scenario.slug == "web":
        npm_path = shutil.which(npm_executable())
        if npm_path is None:
            if require_web_runtime:
                raise RuntimeError("npm was not found, but web runtime smoke is required")
            print("[SKIP] web starter runtime smoke skipped because npm is not available")
            return
        smoke_web_starter(repo_root)
        return
    raise RuntimeError(f"Unsupported scenario: {scenario.slug}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Smoke the one-shot factory path across multiple shapes and starter runtimes.")
    parser.add_argument("--workspace", default=".", help="Workspace root containing PROGRAMSTART.")
    parser.add_argument("--program", default="programstart", help="Programstart executable to invoke.")
    parser.add_argument("--dest-root", default=".tmp_factory_smoke", help="Directory where generated repos are created.")
    parser.add_argument(
        "--require-web-runtime",
        action="store_true",
        help="Fail when npm is unavailable for web starter runtime smoke.",
    )
    args = parser.parse_args(argv)

    workspace = Path(args.workspace).resolve()
    dest_root = (workspace / args.dest_root).resolve()
    dest_root.mkdir(parents=True, exist_ok=True)
    run_root = dest_root / f"run_{int(time.time())}"
    run_root.mkdir(parents=True, exist_ok=False)

    failures = 0
    for scenario in SCENARIOS:
        repo_root = run_root / scenario.slug
        print(f"[CREATE] {scenario.slug} -> {repo_root}")
        try:
            create_repo(scenario=scenario, destination=repo_root, workspace=workspace, program=args.program)
            print(f"[VALIDATE] {scenario.slug}")
            validate_created_repo(repo_root, scenario)
            print(f"[RUNTIME] {scenario.slug}")
            smoke_starter_runtime(repo_root, scenario, require_web_runtime=args.require_web_runtime)
            print(f"[PASS] {scenario.slug}")
        except Exception as exc:  # pragma: no cover - integration failure path
            failures += 1
            print(f"[FAIL] {scenario.slug}: {exc}")

    if failures:
        print(f"\nFactory smoke failed: {failures} scenario(s) failed.")
        return 1

    print(f"\nFactory smoke passed: {len(SCENARIOS)} scenario(s) succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())