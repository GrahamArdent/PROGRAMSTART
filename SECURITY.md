# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |

## Reporting a Vulnerability

**Do not open public GitHub issues for security vulnerabilities.**

To report a vulnerability, use [GitHub Security Advisories](https://github.com/your-org/PROGRAMSTART/security/advisories/new) or email the maintainers directly with:

- A description of the vulnerability
- Steps to reproduce it
- The potential impact
- Any suggested fix (optional)

We will acknowledge your report within 48 hours and aim to provide a fix or mitigation within 7 days for critical issues.

## Security Design

- The HTTP dashboard server (`programstart_serve.py`) binds to `127.0.0.1` only and is not intended for network exposure.
- All API commands are executed from a strict whitelist; arbitrary shell execution is not possible.
- JSON state files are validated against schemas before writes.
- No secrets or credentials are stored in planning documents.

## Dependency Updates

This project uses Dependabot to monitor dependency vulnerabilities. Security patches are applied as soon as feasible after disclosure.
