# PROGRAMSTART Learning Observation

Status: **subordinate / non-canonical evidence**.

This record does not own product scope, execution order, release state, secret values, provider configuration, or PROGRAMSTART priority.

## Observation identity

- **Date:** 2026-08-28
- **Project / repository:** Real cross-project Secrets & Credential Architecture Audit; methodology owner `GrahamArdent/PROGRAMSTART`
- **PROGRAMSTART lesson ID:** `PSL-014` primary; `PSL-013` secondary Learning Gate retest
- **Checkpoint / acceptance surface:** First normal post-PR-62 decision where a new paid/free external service (central secrets manager / credential broker) could materially change architecture, security, and recurring cost
- **Classification:** confirmation

## What happened

A read-only audit evaluated whether the current project portfolio should adopt a central secrets-management product, remain entirely provider-native, or use a hybrid architecture. The decision naturally activated PROGRAMSTART's Cost Gate because the candidate products have free tiers, paid identity/RBAC/rotation tiers, and materially different operational/security behavior.

The Cost Envelope changed the recommendation in a useful way. The audit did **not** recommend replacing existing provider-native secret stores or immediately purchasing a paid vault. Instead it separated two concerns:

1. provider-native runtime secret delivery is already the correct destination-of-use for several current systems; and
2. a central broker can fill the cross-provider/operator/local-development/AI-agent gap without becoming the runtime authority for every secret.

The strongest current pilot candidate is a $0 Infisical Free deployment focused on agent/local credential brokering, especially for Repo Watchtower's high-blast-radius GitHub control-plane credentials. The current official Infisical Free plan includes five identities, unlimited projects, three environments per project, and static-secret Agent Proxy; paid Pro currently adds unlimited identities, access controls, rotation, SAML SSO, audit retention, versioning, and recovery. The audit deliberately did not depend on a permanent copied price catalogue: current pricing evidence was used only for this decision and is subject to invalidation.

Doppler Developer remains a credible $0 alternative, particularly for local development and configuration syncs/service tokens. Its official MCP surface can read secret values when authorized, so it is a weaker match for the specific requirement that an AI agent be able to use credentials without receiving the plaintext secret. Infisical Agent Proxy explicitly brokers credentials at the proxy so the agent sees placeholders rather than the underlying value.

## Evidence

- repository / provider / runtime evidence:
  - `GrahamArdent/Dedication` main exposes only public Supabase/VAPID values in `.env.example`; privileged Edge Functions read server credentials from runtime environment variables.
  - Hosted `dedication-tick` currently consumes `SUPABASE_SERVICE_ROLE_KEY`, cron, Firebase, and VAPID server secrets through `Deno.env`; no legacy database fallback was present in the inspected active function.
  - Hosted `dedication-calendar-integration` uses a bridge-scoped bearer token and keeps `SUPABASE_SERVICE_ROLE_KEY` inside Dedication's server-side boundary.
  - Dedication's Supabase `vault.secrets` currently contains one metadata-visible secret entry for the database-local cron authentication secret; no secret value was queried or exposed.
  - Dedication's GitHub backup workflow consumes named GitHub Actions secrets for the database backup connection and backup encryption key and explicitly keeps production Vault/cron/Auth runtime configuration separate from portable restore state.
  - `GrahamArdent/GCRM` `.env.example` identifies Supabase service role/database credentials, OpenAI, internal agent, observability, enrichment, OAuth, webhook, cron, and development credential surfaces; its Render blueprint keeps agent runtime secrets `sync: false` and out of repository values.
  - GCRM's Supabase `vault.secrets` currently has zero rows, so there is no existing GCRM database-vault authority to preserve.
  - `GrahamArdent/Dedication-Calendar-Bridge` explicitly forbids receiving the Supabase service-role key and expects only a bridge-scoped token plus Google OAuth credentials/refresh token at the real provider gate.
  - `GrahamArdent/Dedication-Email-Bridge` architecture defers real Gmail OAuth until credentials are the actual blocker and requires server-side token storage with no client exposure.
  - `GrahamArdent/resume-creator-v6` and `GrahamArdent/LinkedInGenV2` use placeholder `.env.example` files for OpenAI/provider credentials and ignore local `.env` files; LinkedInGenV2 also contains an older provider free-tier statement that reinforces price-evidence invalidation.
  - `GrahamArdent/repo-watchtower` identifies GitHub App webhook/private-key/token and Slack/database credentials in `.env.example`, making it the highest-blast-radius candidate for a central broker pilot.
  - PROGRAMSTART maintains a `detect-secrets` baseline including GitHub token, OpenAI, private-key, Slack, and other detectors.
  - Connected Supabase organization is currently on the Free plan with GCRM and Dedication active/healthy.
  - Connected Vercel team is currently Hobby and returns no visible projects; repository deployment URLs are separate historical/current evidence, so this visibility discrepancy was not interpreted as proof the deployments do not exist.
  - Current official Infisical and Doppler pricing/documentation were checked on 2026-08-28 for decision-relevant free/paid limits and agent-access behavior.
- verification actually performed:
  - live repository/default-branch inspection of secret placeholders, `.gitignore` boundaries, workflows, architecture, and provider blueprints;
  - live Supabase project/organization, Edge Function, Vault metadata, and cron metadata inspection without reading secret values;
  - live Vercel team/project visibility check;
  - current official provider pricing and agent-access documentation review;
  - targeted GitHub search for obvious private-key material returned no result across the audited repositories; this is not claimed as a complete historical secret scan.
- checks not performed / unavailable:
  - GitHub repository/environment secret values were not and cannot be read through the available connector;
  - Render secret values and its current account/billing state were not available through connected tooling;
  - local developer machines and plaintext `.env` contents were not accessible;
  - connected Vercel visibility did not expose the historically referenced Dedication/Resume Creator projects, so their current Vercel environment-variable state remains unresolved;
  - no credential was copied, revealed, rotated, migrated, or mutated.

## PROGRAMSTART behavior

- **What PROGRAMSTART did:** Mode-C evidence reuse preserved each product's existing authority and secret boundary. The Cost Gate activated because a central secrets manager could change recurring spend and architecture, then forced explicit consideration of included capacity, the paid upgrade trigger, existing provider-native reuse, alternatives, and the evidence that would earn payment.
- **What helped:** The anti-registry rule prevented volatile Infisical/Doppler prices from becoming permanent PROGRAMSTART authority. `EXISTING_INFRA_REUSE` prevented a superficial `centralize everything` recommendation. `PAY_WHEN` produced a concrete condition for future paid RBAC/rotation/identity spend instead of buying ahead of need.
- **What created friction or uncertainty:** No material methodology gap was exposed. The main unresolved facts are product/provider-local (actual future machine-identity count, unavailable Render/Vercel secret inventory, and whether automatic cross-provider secret sync becomes valuable enough to justify payment).
- **Was existing methodology sufficient?** yes

## Cost Envelope outcome

```text
COST_GATE: active
COST_SURFACE: central secrets manager / AI credential broker pilot
EXPOSURE_TYPE: fixed (currently $0 candidate; future per-identity/per-user paid tiers)
CURRENT_COST_EVIDENCE: current official Infisical and Doppler pricing/docs checked 2026-08-28
INCLUDED_OR_FREE_CAPACITY: Infisical Free — 5 identities, unlimited projects, 3 environments/project, Agent Proxy; Doppler Developer — free for 3 users, service tokens, CLI, 5 config syncs and documented Developer limits
CHARGE_TRIGGER: Infisical >5 identities or need paid access-control/rotation/SSO/versioning/recovery capabilities; Doppler Team features such as RBAC/automatic rotation/service accounts or user growth beyond the free allowance
HARD_CAP_OR_BUDGET: $0 pilot; no paid upgrade without operator approval
CAP_BEHAVIOR: remain within free feature/identity limits or stop and re-evaluate; no automatic paid upgrade
EXISTING_INFRA_REUSE: keep Supabase, GitHub Actions, Render/Vercel, and other provider-native runtime stores as destination-of-use; do not migrate database-local/runtime-local secrets solely for centralization
LOWER_COST_ALTERNATIVES: provider-native only at $0; Doppler Developer at $0; self-hosted/open-source options only if their operational burden is justified
PAY_WHEN: least-privilege identity count exceeds free capacity, production multi-user RBAC/audit requirements become real, automatic rotation materially reduces risk/toil, or measured operational value justifies the recurring fee
APPROVAL_OWNER: operator/project owner
COST_INVALIDATION: pricing/feature changes, identity count changes, production/compliance requirements, resolved provider visibility, or a native provider/broker capability that materially changes the tradeoff
COST_DECISION: stay_free (pilot), with provider-native runtime stores retained
```

## Learning decision

- **Existing lesson match:** `PSL-014` exactly matched the decision. `PSL-013` also reached its open real-checkpoint retest because the normal product/security work triggered the Learning Gate and produced a maturity update rather than methodology invention.
- **Maturity before:** `PSL-014` implemented; `PSL-013` implemented
- **Maturity after:** `PSL-014` validated; `PSL-013` validated
- **Why the evidence changes maturity:** The Cost Gate materially altered the architecture recommendation: it selected a bounded $0 pilot and preserved provider-native secret stores instead of either paying early or centralizing indiscriminately. It also stopped at decision sufficiency and retained volatile price evidence as local/current evidence rather than a central registry. The Learning Gate then recognized this as confirmation of existing methodology with no new feature request.
- **PROGRAMSTART change required now:** none; only acceptance evidence and maturity rollup reconciliation

## Retest

- **Next real condition that could strengthen/challenge this lesson:** a future metered API or paid infrastructure decision with a different cost shape, or a central-vault rollout that actually exceeds free identity limits and tests `PAY_WHEN` against measured need.
- **What evidence would be sufficient:** the Cost Gate should again change or confirm the decision proportionally without forcing price-registry maintenance or cost ceremony for ordinary included-capacity work.

## Safety / authority check

- [x] Product/project authority remains unchanged.
- [x] No new project backlog or portfolio execution spine was created.
- [x] No secret value/private credential was copied into this observation.
- [x] Evidence claims match checks that actually ran.
- [x] No unnecessary PROGRAMSTART methodology change was manufactured.
