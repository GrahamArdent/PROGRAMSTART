# Backbone audit — ten-step continuation

This is the exact ten-step recommendation supplied by Graham in the conversation, preserved as the audit's execution reference. It is a derived audit plan under PROGRAMSTART; component authority, acceptance and existing hosted holds still control execution. It does not replace the owning projects' execution spines.

## Progress and resumption

- Steps **1–3: completed for the documented local scope** in PROGRAMSTART PR257, commit `c98d9d21f8d5c5d16b546474c2bd2db13b56f9d6`. See [validation evidence](VALIDATION_NEXT_THREE.md): 3,127 passing tests, zero skips, zero raw coverage gaps across 67 configured production modules; ten-track knowledge review; qualified browser environment.
- Steps **4–6: executed to the recorded boundaries**; see [source, native and audit results](STEPS_04_06.md). Step4 has review and automatic audit enforcement, with hosted/owner acceptance still held. Step5 has fresh native status and a failed fixed probe; installed guard journey remains unproven. Step6 has the scoped EN/Compute obligation map and a reproduced Compute repair in draft PR215. Steps4/5 remain open; a draft PR or local gate is not acceptance.
- Steps **7–10: pending**.
- Resume from this file and [implementation status](IMPLEMENTATION.md). Preserve the numbering below when reporting progress. Update this progress section with evidence as work completes; preserve the original recommendation.
- The earlier `N01`–`N04` identifiers in the register are pilot/action IDs, not this ten-step numbering.

## Original recommendation

The next milestone should be a trustworthy test baseline and one verified backbone journey. We have useful source fixes and an organized audit, but both PRs remain drafts and the installed system is still unproven.

Here are the next ten steps I recommend, in priority order:

1. Fix PROGRAMSTART’s seven test-collection errors.
   Correct the import/package problems, then run the full suite and coverage checks. Finish line: tests actually execute, with remaining failures individually explained—not merely counted as discovered.

2. Resolve the knowledge-base freshness failures properly.
   Review the ten overdue tracks and update their evidence. Separately assess whether a blanket seven-day blocking policy is proportionate. Finish line: genuine current evidence and a justified policy; no date changes just to turn checks green.

3. Establish a reproducible validation environment.
   Resolve the Chromium installation failure and run the browser smoke test using the declared dependencies. Finish line: a repeatable command, known environment and observed result that another session can reproduce.

4. Finish the two existing PRs through their required checks.
   Take Paths PR81 and PROGRAMSTART PR257 through review and acceptance. Give the audit’s currently manual checks an appropriate place in existing validation. Finish line: accepted source changes, clear maintenance ownership and explicit remaining installation obligations. Preserve hosted holds until their owner resolves them.

5. Prove the actual installed Paths lookup journey.
   Verify which consumer uses the guard, observe the first call and actual target result, then test failure recovery and resumption without duplicating the original effect. Finish line: evidence from the real chain, beyond local fixtures.

6. Apply the same outcome-first audit to Execution Node and Compute.
   Write down what each boundary must guarantee before inspecting its tests: admission, correct target, bounded execution, completion evidence and recovery. Finish line: explicit obligations, independent expected observations and identified gaps for both components.

7. Map and challenge test execution across the backbone.
   Connect each obligation to its tests, discovery commands, CI selectors, required checks and actual results. Include skipped, quarantined, flaky and never-selected tests. Deliberately break representative behavior and selection rules. Finish line: evidence that relevant failures are detected and relevant changes select the checks.

8. Reconcile implemented work with what actually runs.
   Compare repository changes with installed versions, consumers, services, schedules and configuration. Identify unadopted fixes, disconnected components and legacy processes still active. Finish line: every finding has an owner and a disposition: adopt, retain, repair, retire or investigate.

9. Build the first risk-selected E2E tranche.
   Select journeys covering useful completion, denial, recovery, cancellation, concurrency and rollback where applicable. Use cheaper contract tests for cases that do not need full E2E execution. Finish line: meaningful cross-component proof with independent observations, bounded costs and cleanup. The 18 families and 84 scenarios remain a coverage map—not a mandatory suite size.

10. Remove measured waste and establish ongoing upkeep.
    Baseline test/runtime costs, retire one justified duplicate or legacy candidate at a time, and verify that fault detection and recovery remain intact. Update the four views as changes land. Finish line: demonstrated savings without lost protection; revisit a separate repository only when maintenance or ownership needs justify it.

I would tackle steps 1–3 next, while preparing the installed Paths trial. Independent mapping can continue wherever an acceptance hold blocks execution.
