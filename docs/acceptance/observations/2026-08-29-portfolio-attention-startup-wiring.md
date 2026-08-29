# PROGRAMSTART Learning Observation — Portfolio Attention Startup Wiring

Date: 2026-08-29  
Related lesson: `PSL-018` — Portfolio Attention Control  
Classification: systemic implementation correction / supporting evidence  
Maturity effect: **none — remains implemented pending a natural later portfolio retest**

## Trigger

Immediately after Portfolio Attention Control merged in PR #69, the operator asked whether the portfolio would update automatically or whether they would need to remember to prompt for updates.

A live read of the merged startup/orchestration surfaces showed a real integration gap:

- `PROGRAMBUILD_PORTFOLIO_CONTROL.md` defined the portfolio method and already said an external row should refresh after project truth changes;
- the always-on repository startup/JIT instructions did not yet define when that reconciliation should happen automatically;
- `programstart-what-next.prompt.md` remained repository-scoped and did not distinguish portfolio-level "what should we work on?" questions;
- `PROGRAMBUILD_PORTFOLIO_CONTROL.md` was indexed in `PROGRAMBUILD_FILE_INDEX.md` but was missing from `config/registry/systems/programbuild.json`, so generated/adopted PROGRAMBUILD surfaces could omit the protocol.

The first implementation therefore solved the method but stopped one integration step short of making it operationally discoverable during normal PROGRAMSTART use.

## Correction

This follow-up keeps the original authority boundary and adds only the missing routing:

1. `.github/copilot-instructions.md` gains **Portfolio Attention Checkpoints** as an always-on startup/JIT rule.
2. Ordinary project turns do not scan or rebuild the portfolio.
3. Meaningful portfolio invalidation events trigger reconciliation of only the current project's external row when an already-authorized writable portfolio workspace is available:
   - milestone/packet merge or closure;
   - blocker or operator-gate change;
   - dependency change;
   - explicit pause/resume;
   - provider/runtime evidence that materially changes the next action or attention class.
4. Unavailable/unwritable external portfolio storage does not block truthful project closure; reconciliation is reported as pending.
5. `programstart-what-next.prompt.md` now distinguishes repository scope from portfolio scope. Portfolio questions reuse retained state, refresh only evidence that can change the decision, and return at most one operator gate, one primary build, and one fallback before handing execution back to project Mode C.
6. `config/registry/systems/programbuild.json` now propagates `PROGRAMBUILD_PORTFOLIO_CONTROL.md` as a PROGRAMBUILD control file.
7. Focused static contract coverage protects the startup/checkpoint, portfolio-what-next, bounded-WIP, and propagation behavior.

## Anti-bloat result

This correction deliberately does **not** add:

- background polling;
- a cron/scheduled portfolio scan;
- automatic audits of every repository;
- another PROGRAMSTART CLI state machine;
- a filled portfolio inside PROGRAMSTART;
- cross-project mutation authority;
- automatic priority from staleness or commit activity.

Automation is event/checkpoint-shaped rather than continuous: normal project work remains local, and the portfolio is touched only when current evidence can materially change operator attention.

## Storage boundary still truthful

The live portfolio still needs an external durable writable surface. The previously attempted Google Sheets import remains unavailable because the current Drive connection lacks create/import scope. PROGRAMSTART therefore defines and recognizes the automatic reconciliation responsibility, but it must not falsely claim persistence when the external workspace cannot be written.

If a future portfolio workspace is another GitHub repository, existing explicit repository-boundary consent rules still apply. This change does not weaken them.

## Retest

`PSL-018` remains **implemented**, not validated.

The next natural retest should occur after a real project reaches one of the declared portfolio checkpoints or when the operator next asks a portfolio-level "what should we work on?" question after project state has materially changed.

Validation should show that PROGRAMSTART:

- does not perform routine portfolio-wide scans;
- notices the checkpoint without requiring the operator to remember an administrative update command;
- reconciles only the relevant project row when the external workspace is writable/authorized;
- otherwise reports pending persistence without blocking project closure;
- refreshes only decision-relevant evidence for portfolio prioritization;
- preserves one primary build and existing project authority.
