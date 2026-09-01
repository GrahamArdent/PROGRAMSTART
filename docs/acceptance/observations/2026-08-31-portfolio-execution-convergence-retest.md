# Portfolio execution-convergence retest — 2026-08-31

## Learning Gate classification

- **Real project:** `GrahamArdent/execution-node-control`
- **Portfolio workspace:** `GrahamArdent/portfolio-operations`
- **Existing lesson:** `PSL-018`
- **Classification:** counterevidence that strengthens an existing validated lesson; no new lesson ID earned
- **Methodology surface:** `PROGRAMBUILD/PROGRAMBUILD_PORTFOLIO_CONTROL.md`

## Observation

The live Portfolio Operations sweep correctly selected Execution Node EN-03 V2.1 Stage 5 as `PRIMARY_BUILD` and correctly recognized that repository-only work was available. However, the retained portfolio status described the immediate next action as creating the Stage-5 repository candidate even though Execution Node PR #42 already existed and had advanced beyond that point.

The four-hour auto-progress loop therefore demonstrated a specific failure mode: **portfolio selection and status refresh can be correct at the attention layer while still failing to converge into the owning project's actual executable frontier.** A recommendation/status refresh is not sufficient progression when current project authority already permits unattended-safe work.

## Live correction and retest

The auto-progress behavior was strengthened so that selection is the start of execution rather than a terminal portfolio result. The corrected flow then resumed the owning repository from its actual current work:

1. loaded the Execution Node Stage-5 authority;
2. discovered existing PR #42 rather than creating a duplicate lane;
3. inspected its exact current head and CI evidence;
4. found that the prior green CI run validated GitHub's synthetic PR merge ref rather than the candidate head;
5. corrected CI to bind checkout and verification to the exact pull-request head;
6. continued into the required post-implementation Challenge Gate rather than stopping at green CI;
7. found a material Docker CLI plugin-discovery shadow path in which inventory could select a later trusted system plugin while normal Docker CLI discovery could encounter an earlier `/usr/local/.../cli-plugins` candidate;
8. remediated that condition with fail-closed reviewed acceptance and positive/negative regressions;
9. reran exact-head CI on candidate `d22b812001e561a9172a9f61586660668876235d`;
10. exact-head CI passed 164 tests, Ansible syntax validation, and dangerous-execution-primitive guards after explicitly proving the checkout SHA;
11. re-challenged the candidate and recorded CLEAR only for the next project-authorized boundary;
12. stopped before exact reviewed-release human/admin installation and physical Stage-5 acceptance, preserving the real manual/privileged gate.

The corrected behavior therefore changed execution materially: it moved from stale portfolio recommendation → current owning-project candidate → trustworthy exact-head verification → adversarial correction → real human boundary without inventing a second portfolio authority or crossing the project's physical-install gate.

## Reusable methodology delta

Strengthen `PSL-018` with **execution convergence after portfolio selection**:

- before recommending or creating the next action, inspect existing current branches/PRs, candidate heads, current-head checks, unresolved Challenge/review evidence, and recently returned evidence that can invalidate the retained portfolio row;
- if owning-project work is already farther ahead than the portfolio row, resume the actual frontier instead of repeating planning or creating a duplicate lane;
- when the selected step is unattended-safe under current project authority, selection should hand into Mode C and attempt that work in the same execution cycle;
- continue consecutive unattended-safe convergence steps through targeted verification, applicable Challenge Gate, bounded remediation/rechallenge, project reconciliation, and portfolio refresh until a genuine gate, unavailable tool boundary, contradictory evidence, or packet completion is reached;
- a portfolio/status refresh alone is not successful progression while executable owning-project work remains;
- green CI is evidence, not convergence, when exact-candidate proof, Challenge Gate, reconciliation, or another already-required project gate remains;
- reconcile the owning project first, then refresh the derived portfolio view.

## Boundary preserved

This does **not** authorize Portfolio Operations to mutate project scope or become cross-repository execution authority. It also does not earn a global autonomous multi-repository transaction scheduler. The owning project's Mode-C authority continues to decide whether each immediate step is safe, PR-only, human-gated, or blocked.

## Maturity result

`PSL-018` remains **validated**, with a strengthened lesson summary and acceptance semantics. The same real Execution Node packet supplied the correction and an immediate natural retest that demonstrated the intended behavior through the genuine physical-install boundary.

## Future counterevidence to watch

Revisit if execution-convergence semantics cause any of the following:

- duplicate or competing project lanes;
- unsafe continuation across provider/device/security/cost/product gates;
- excessive repository scanning when retained evidence remains valid;
- WIP leakage into multiple consequential builds;
- repeated failure to discover an already-existing candidate;
- repeated stopping at status/CI evidence while a required unattended-safe convergence step remains.
