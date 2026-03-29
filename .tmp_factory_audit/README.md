# AuditFactory

Audit repo for PROGRAMSTART project factory

## Project Setup

- PROGRAMBUILD variant: product
- Product shape: web app
- USERJOURNEY attached: no

## Start Here

```powershell
uv sync --extra dev
uv run programstart validate --check bootstrap-assets
uv run programstart next
```

Use `programstart recommend` to confirm the current stack and workflow fit before filling stage outputs.
