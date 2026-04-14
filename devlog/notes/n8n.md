# n8n CLI Reference

n8n has a CLI for self-hosted installations. It lets you run workflows, change workflow activation, import or export workflows and credentials, run admin operations, and perform security checks.

## Running the CLI

### npm install

If n8n is installed with npm, the CLI is available directly:

```bash
n8n <command>
```

### Docker install

If n8n is running in Docker, run the CLI inside the container:

```bash
docker exec -u node -it <n8n-container-name> n8n <command>
```

## Common Commands

### Execute a workflow

```bash
n8n execute --id <ID>
```

### Activate or deactivate workflows

```bash
n8n update:workflow --id=<ID> --active=true
n8n update:workflow --id=<ID> --active=false
n8n update:workflow --all --active=true
n8n update:workflow --all --active=false
```

Note: workflow activation changes operate on the database and may require an n8n restart before they take effect.

## Export Commands

### Export workflows

```bash
n8n export:workflow --all
n8n export:workflow --id=<ID> --output=file.json
n8n export:workflow --backup --output=backups/latest/
```

Useful flags:

- `--all`
- `--backup`
- `--id`
- `--output`
- `--pretty`
- `--separate`

### Export credentials

```bash
n8n export:credentials --all
n8n export:credentials --id=<ID> --output=file.json
n8n export:credentials --backup --output=backups/latest/
n8n export:credentials --all --decrypted --output=backups/decrypted.json
```

Warning: `--decrypted` exports secrets in plain text.

### Export entities for database migration

```bash
n8n export:entities --outputDir=./outputs
n8n export:entities --outputDir=./outputs --includeExecutionHistoryDataTables=true
```

## Import Commands

### Import workflows

```bash
n8n import:workflow --input=file.json
n8n import:workflow --separate --input=backups/latest/
```

### Import credentials

```bash
n8n import:credentials --input=file.json
n8n import:credentials --separate --input=backups/latest/
```

Useful flags:

- `--input`
- `--projectId`
- `--userId`
- `--separate`
- `--skipMigrationChecks`

Important: imported workflows and credentials keep their IDs. If matching IDs already exist in the target database, they can be overwritten.

### Import full entities

```bash
n8n import:entities --inputDir ./outputs --truncateTables true
```

This is intended for migrations between supported database types such as SQLite and Postgres.

## Admin and Security Commands

### License

```bash
n8n license:info
n8n license:clear
```

### User management

```bash
n8n user-management:reset
n8n mfa:disable --email=johndoe@example.com
n8n ldap:reset
```

### Community nodes

```bash
n8n community-node --uninstall --package <COMMUNITY_NODE_NAME>
n8n community-node --uninstall --credential <CREDENTIAL_TYPE> --userId <ID>
```

### Security audit

```bash
n8n audit
```

## Practical Notes

- The CLI is mainly documented for self-hosted n8n.
- Be careful with import operations because IDs can collide and overwrite existing records.
- Be careful with decrypted credential exports because they contain sensitive values.
- `update:workflow` changes may not be reflected until n8n restarts.

## Good Backup Pattern

For a safe backup of workflows and credentials:

```bash
n8n export:workflow --backup --output=backups/workflows/
n8n export:credentials --backup --output=backups/credentials/
```

## Source

Official docs:

- https://docs.n8n.io/hosting/cli-commands/
