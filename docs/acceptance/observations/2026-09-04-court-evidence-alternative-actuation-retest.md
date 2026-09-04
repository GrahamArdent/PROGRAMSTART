# Learning Observation — Court Evidence Alternative-Actuation Retest

**Date:** 2026-09-04
**System:** PROGRAMSTART Effective Autonomy / GrahamArdent/whats Court Case Evidence Bell pipeline
**Classification:** systemic methodology confirmation + strengthening
**Lesson:** `PSL-021`
**Maturity result:** validated

## Trigger

The Court Case Evidence Bell work reached an apparent final operator relay: the Windows machine had an already-installed typed Bell endpoint whose allow-list exposed only the older read-only/status actions, while the newly accepted repository implementation added `bell_pipeline_v1`.

The first conclusion was that the operator would need to run one local PowerShell command to refresh the endpoint before autonomous acquisition could continue.

The operator challenged that conclusion and asked PROGRAMSTART to look for alternatives using the tools and execution surfaces already available.

## What happened in the real project

The project authority already permitted the Bell evidence acquisition consequence after live Bell authentication had passed. The remaining issue was therefore mechanical actuation, not human judgment or new authorization.

A wider capability search found that the old installed Bell endpoint already performed an important bounded sequence for `bell_readonly_probe_v1`:

1. accept a short-lived typed request containing an exact accepted commit;
2. clone the Court Evidence repository;
3. verify that the requested commit equals current accepted `v2.0`;
4. require a clean detached runtime;
5. execute the Bell launcher from that exact accepted runtime.

That existing bridge was sufficient to remove the manual refresh relay without introducing SSH, WinRM, arbitrary shell execution, broader credentials, or a new control plane.

The accepted Bell launcher was extended so that, when the fixed Bell endpoint is already installed, it may refresh only that fixed agent file from its own exact accepted runtime. The refresh candidate must parse, pass the Windows PowerShell 5.1 endpoint self-test, match staged/final SHA-256 checks, preserve the protected install-root boundary, and retain rollback evidence. It does not accept a caller-selected command, repository, target path, task definition, privilege level, or secret.

The Court Evidence implementation and Challenge were carried in `GrahamArdent/whats` PR #42. Candidate CI proved an old running agent could replace its own fixed installed file and continue, then the next invocation executed the new three-action endpoint. The refresh was also tested for idempotence and rollback/fail-closed behavior. PR #42 merged to `v2.0` and post-merge Court Evidence and Bell endpoint refresh checks passed.

No Bell account address, password, mailbox content, subject/body, or raw evidence is retained in this PROGRAMSTART observation.

## PROGRAMSTART help / hinder / failure analysis

### What helped

The existing Effective Autonomy protocol already contained the core rule:

- distinguish `genuine_human_gate` from `temporary_automation_gap`;
- current-environment inability alone is not proof of a genuine human gate;
- prefer an existing trusted temporary bridge when authority permits it;
- new capability may automate existing permission but may not create permission.

Those rules made the eventual self-refresh mechanism easy to evaluate without changing project authority.

### What hindered

The methodology did not make the **search behavior** explicit enough. The first pass examined the obvious installed endpoint allow-list and stopped at “this agent cannot execute the new action.” It did not immediately inspect what that older action could already cause an exact accepted runtime to do.

The missing operational behavior was not another controller or universal shell. It was a deliberate requirement to search across and compose the current capability graph before escalating already-authorized mechanical work to the operator.

## Learning disposition

This evidence strengthens existing `PSL-021`; it does not earn a new lesson ID.

The reusable formulation is:

> **Tool creativity is mandatory before human transport. Be creative in mechanism and conservative in authority.**

For a `temporary_automation_gap`, PROGRAMSTART should search available connected APIs/connectors, provider APIs, CLI tools, repository automation, accepted runtimes, local agents/tasks, machine identities, control queues, custom/bounded APIs, and safe compositions of those surfaces before requesting an operator relay.

That search must remain consequence-scoped and must Challenge candidate compositions for permission widening, secret/identity expansion, arbitrary command execution, destructive/external effects, spend, privacy, persistence and recovery risk.

This is an extension of Effective Autonomy behavior, not a new lifecycle or execution platform.

## Why this validates PSL-021

The original PSL-021 retest required a real existing project to consume newly available execution capability without rewriting project authority, preserve verification/Challenge boundaries, avoid routine `proceed`/transport work, and retain stronger consequence gates.

The Bell case does that materially:

- existing Court Evidence authority remained authoritative;
- a temporary automation gap was identified after live provider/credential acceptance;
- the obvious manual relay was challenged rather than normalized;
- existing bounded execution capabilities were composed into a safer autonomous bridge;
- exact accepted commit, clean-runtime, typed action and Challenge rules remained intact;
- no broader Windows shell, secret scope or Bell source-mutation authority was created;
- operator transport was removed while genuine future factual/legal gates remain human.

Therefore `PSL-021` advances from **implemented / real retest pending** to **validated**.

## Counterevidence / future retest conditions

Keep this rule narrow or revise it if later use shows that alternative-actuation search:

- repeatedly creates more ceremony than operator burden avoided;
- encourages brittle multi-tool chains where a simple relay is safer for a one-off low-cost action;
- disguises authority expansion as tool composition;
- broadens credentials or arbitrary execution merely to preserve autonomy;
- delays a genuine human gate by searching indefinitely for a nonexistent workaround;
- cannot explain why the selected composition is safer than the rejected operator path.

Future projects should continue to provide natural counterevidence. The required behavior is a bounded search proportional to consequence, recurrence and operator burden—not an assumption that every external limitation can or should be bypassed.

## Methodology change earned

Strengthen `docs/PROGRAMSTART_EFFECTIVE_AUTONOMY.md` and the existing PROGRAMBUILD checklist so that:

1. operator transport for an already-authorized mechanical action requires an alternative-actuation search first;
2. the search explicitly considers composition across available tools rather than only one obvious surface;
3. creativity applies to mechanism, while authority/gates remain conservative;
4. the search may end quickly when no safe alternative exists;
5. genuine human judgment/authorization/physical/legal/security gates remain unchanged.

No new controller, roadmap, capability registry, lifecycle, or universal actuator is earned by this observation.
