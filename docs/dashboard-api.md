# Dashboard API

This page documents the internal HTTP contract exposed by `scripts/programstart_serve.py`.

It is an operator surface for the local PROGRAMSTART dashboard, not a public product API.

## Scope

- binds to `127.0.0.1` only
- serves a local operator UI for workflow visibility, signoff, bootstrap, and smoke actions
- only executes whitelisted commands defined in `scripts/programstart_command_registry.py`
- should be treated as an internal contract that may evolve with the dashboard

## Stability Rules

The route set is intentionally small and disciplined, but it is not a semver-style public API.

Use these routes through the bundled dashboard UI or the repo smoke tests. Do not build external automation that assumes long-term compatibility without pinning the repo version.

## GET Routes

### `GET /` and `GET /index.html`

Returns the local dashboard HTML shell.

Intended use:

- human operator access in a browser

### `GET /api/state`

Returns the dashboard state payload assembled from workflow state files, registry data, and selected planning document summaries.

Primary payload areas:

- PROGRAMBUILD active stage and workflow steps
- USERJOURNEY attachment status and active phase when attached
- checklist, progress, and signoff context
- dashboard guidance metadata derived from source docs

Intended use:

- dashboard hydration
- browser smoke tests
- screenshot golden tests

### `GET /api/doc?path=<workspace-relative-path>`

Returns a preview payload for a workspace document.

Expected query parameter:

- `path`: workspace-relative markdown path

Success behavior:

- `200` with a JSON payload containing the resolved preview data

Failure behavior:

- `400` for invalid or unavailable document requests

Intended use:

- previewing planning documents from the dashboard without leaving the operator surface

### `GET /api/health`

Returns a structured health probe report for the workspace.

Success behavior:

- `200` with a JSON payload containing system health data (overall health classification, per-system control file counts, and missing file lists)

Intended use:

- programmatic health checks and monitoring integration

## POST Routes

### `POST /api/run`

Runs a command from the strict dashboard whitelist.

Request body:

```json
{
  "command": "status",
  "args": ["--system", "programbuild"]
}
```

Response shape:

```json
{
  "output": "...command output...",
  "exit_code": 0
}
```

Rules:

- `command` must exist in the whitelist built by `dashboard_allowed_commands()`
- `args` are optional and are filtered to a small allowlist of signoff-related values
- command execution never uses `shell=True`

Whitelisted command keys currently include:

- `state.show`
- `state.show.programbuild`
- `state.show.userjourney`
- `guide.programbuild`
- `guide.userjourney`
- `guide.kickoff`
- `status`
- `validate`
- `validate.workflow-state`
- `log`
- `drift`
- `advance.programbuild.dry`
- `advance.userjourney.dry`
- `advance.programbuild`
- `advance.userjourney`
- `progress`
- `dashboard`
- `smoke.dashboard`
- `smoke.browser`

### `POST /api/bootstrap`

Runs the validated bootstrap flow for a new planning repo.

Request body:

```json
{
  "dest": "C:\\Projects\\SampleRepo",
  "project_name": "SampleRepo",
  "variant": "product",
  "dry_run": false
}
```

Rules:

- `dest` must match the server's safe absolute-path validation
- `project_name` must match the validated name format
- `variant` must be one of `lite`, `product`, or `enterprise`

Response shape:

- same command-style `{ "output": ..., "exit_code": ... }` payload used by other operator actions

### `POST /api/workflow-signoff`

Persists signoff metadata for the active PROGRAMBUILD stage or USERJOURNEY phase.

Request body:

```json
{
  "system": "userjourney",
  "decision": "approved",
  "date": "2026-03-28",
  "notes": "Checkpoint approved"
}
```

Behavior:

- validates JSON input
- writes signoff metadata through the workflow state tooling
- returns `200` on success and `400` on validation or workflow failure

### `POST /api/workflow-advance`

Saves signoff data and attempts to advance the active stage or phase.

Request body:

```json
{
  "system": "programbuild",
  "decision": "approved",
  "date": "2026-03-28",
  "notes": "Advance to next stage",
  "dry_run": true
}
```

Behavior:

- supports dry-run preview of the next transition
- returns the workflow command output and exit code

### `POST /api/uj-phase`

Updates USERJOURNEY implementation-tracker phase status.

Request body:

```json
{
  "phase": "0",
  "status": "Completed",
  "blockers": ""
}
```

Behavior:

- intended only for repos with the USERJOURNEY attachment present
- returns `200` on success and `400` on invalid input or failed update

### `POST /api/uj-slice`

Updates USERJOURNEY execution-slice status in the implementation tracker.

Request body:

```json
{
  "slice": "Slice 1",
  "status": "Selected",
  "notes": "Ready to begin"
}
```

Behavior:

- intended only for repos with the USERJOURNEY attachment present
- returns `200` on success and `400` on invalid input or failed update

## Error Model

Common failures:

- invalid JSON body returns `{ "error": "invalid JSON body" }` with `400`
- invalid document requests return a preview error payload with `400`
- command failures return `{ "output": ..., "exit_code": nonzero }`
- unknown routes return `404`

## Security Notes

- the server listens on loopback only
- command execution is allowlist-based
- bootstrap input is validated for path, project name, and variant
- subprocesses are invoked with argument lists, not a shell string

## Testing Surfaces

The internal dashboard contract is exercised by:

- `scripts/programstart_dashboard_smoke.py`
- `scripts/programstart_dashboard_browser_smoke.py`
- `scripts/programstart_dashboard_golden.py`

Those tests are the practical regression contract for the operator dashboard.
