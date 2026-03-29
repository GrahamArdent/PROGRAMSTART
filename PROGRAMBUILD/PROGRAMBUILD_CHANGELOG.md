# PROGRAMBUILD_CHANGELOG.md

# Program Build Changelog

Tracks changes to the reusable PROGRAMBUILD system itself.

---

## 2026-03-29

- added a scheduled full CI gate workflow to run the heavier nox-based quality lane outside normal PR and push validation
- implemented the three core PROGRAMBUILD specialist roles as workspace agents in `.github/agents/`
- clarified in repository docs that `USERJOURNEY/` remains an optional reference attachment and is not required for every bootstrapped project
- hardened workflow caching and artifact capture, normalized agent/workflow line endings, and reduced bootstrapped nox smoke noise in CI
- adjusted drift policy so `PROGRAMBUILD_CHANGELOG.md` entries do not require concurrent canonical or file-index edits unless authority or inventory actually changes

---

## 2026-03-27

- established PROGRAMBUILD and USERJOURNEY as separate systems with registry-backed validation and drift checks
- added `pb.ps1` PowerShell wrapper and `STATUS_DASHBOARD.md` generation
- added `DECISION_LOG.md` and `POST_LAUNCH_REVIEW.md` as standard PROGRAMBUILD outputs
- added ADR template guidance, gate sign-off log, requirements traceability, external dependency review, and post-launch review stage
- clarified variant-aware expectations so lite, product, and enterprise processes keep different evidence levels

---

Last updated: 2026-03-29
