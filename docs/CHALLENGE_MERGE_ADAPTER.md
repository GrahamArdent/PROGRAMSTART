# Bounded Challenge merge adapter

`scripts/programstart_challenge_merge.py` is an opt-in GitHub CLI consumer for
the existing Challenge Gate. It is not a reviewer, release registry, runtime
service, source of new permission, or replacement for Compute's cycle evaluator.
Issue113 remains the owner of stronger merge/activation enforcement.

Run the script from the accepted methodology checkout. Do not run a changed PR's
copy as its own acceptance authority. It uses existing `gh` authentication,
explicitly addresses github.com and never reads or exports credentials.
Read-only admission is the default:

The consumer compares its local script bytes with the named accepted source,
and every admission snapshot revalidates the current PROGRAMSTART main SHA.
This helps detect a wrong checkout; it does not make hostile code capable of
authenticating itself. The caller still owns trusted-code execution/admission.

```bash
python scripts/programstart_challenge_merge.py OWNER/REPO 123 \
  --expected-head EXACT_HEAD_SHA --methodology-sha ACCEPTED_METHOD_SHA
```

An already-authorized caller may add `--merge` to request a squash merge. This is
an explicit consequence request, not permission supplied by the script. It reads
all PR reviews and issue comments, validates twice immediately before an
expected-head-guarded merge, then checks the actual merged state/evidence.
The caller must retain the JSON receipt with its existing owner evidence.

## Accepted disposition

Only the repository owner's provider-authenticated numeric user ID and login
can supply a disposition. An org-owned repository needs a separately accepted
delegation adapter; this implementation does not infer one. Author labels,
`author_association`, body text, URLs and arbitrary reviewer names are not
authentication. A bare CLEAR, native approval, green tests or an unrecognized
issuer cannot supply the required exact-head disposition.

After the actual applicable Challenge review and verification, the authorized
owner may append one PR conversation comment whose complete body is the marker
line below followed by one JSON object (without a Markdown fence):

```text
PROGRAMSTART_CHALLENGE_DISPOSITION_V1
{"repository":"OWNER/REPO","pr":123,"head_sha":"EXACT_HEAD_SHA","methodology_sha":"ACCEPTED_METHOD_SHA","scope":"repository_merge","result":"clear","findings":[],"resolutions":[],"evidence_refs":["ACTUAL_REVIEW_REFERENCE","ACTUAL_VERIFICATION_REFERENCE"]}
```

SHA placeholders must be replaced by full lowercase Git SHAs. An owner
attestation authenticates the owner's decision; it does not prove that a model
ran, make a same-context review independent, or turn arbitrary evidence URLs
into executed checks. The issuer remains responsible for truthful applicable
review, exact verification and owner acceptance under the canonical gate.
There is no automatic delegate, inferred model authority or credential grant.

To block, use `result: blocked` with nonempty stable `findings` IDs. A later
clear does not erase those IDs. Its `resolutions` must explicitly name each
retained `finding_id` and nonempty actual `evidence_refs`. Resolution proof must
be re-attested on the current candidate and methodology; historical resolutions
remain historical. Native CHANGES_REQUESTED submissions also block until
explicitly dismissed through GitHub's existing authorized review process.
The adapter never dismisses a review or publishes its own clearance.

Append dispositions rather than editing them. Edited or malformed recognized
owner records fail closed. To revoke a structured positive assertion, or recover
from its invalid positive metadata, append an authenticated owner withdrawal:

```text
PROGRAMSTART_CHALLENGE_CLEAR_WITHDRAWAL_V1
{"repository":"OWNER/REPO","pr":123,"comment_id":456,"body_sha256":"SHA256_OF_EXACT_ORIGINAL_COMMENT_BODY_UTF8","reason":"ACTUAL_WITHDRAWAL_REASON","evidence_refs":["ACTUAL_CORRECTION_OR_REVOCATION_EVIDENCE"]}
```

The original record must remain present and unedited, match both provider owner
identity and work item, and have the V1 fields with `result: clear`, empty
findings, merge scope and valid head/methodology SHAs. Invalid resolutions in
that positive record need not be interpreted before withdrawal. Unknown/edited
targets, wrong hashes, forward references, arbitrary malformed bodies, blocked
records and legacy prose blockers cannot be withdrawn this way. The withdrawal
itself must remain unedited with nonempty reason and proof references.

Withdrawal removes the named positive assertion and its resolutions, so the
original blockers survive/reappear. It also invalidates earlier same-head CLEARs
at that point in history: an older positive record cannot silently revive after
revocation. A new later exact-head/current-methodology CLEAR must explicitly
resolve every retained blocker. Withdrawals confer no acceptance or permission,
and never withdraw negative evidence. They participate in the existing evidence
digest/re-read/postmerge checks; a late observed withdrawal prohibits acceptance
or activation just as an observed new blocker does.

GitHub comments are mutable by privileged actors:
this is not a cryptographically append-only ledger, and deletion before a
first read cannot be detected by this adapter. Existing trusted owner evidence
must retain required history. Do not use this path when stronger immutable
disposition retention is required. Legacy owner comments containing
`CHANGES REQUIRED` are retained as `github-comment:COMMENT_ID` blockers. This
conservative recognition can also hold historical quotations; the owner must
explicitly reconcile them with proof rather than relying on ambiguous prose.
Do not migrate an unresolved legacy PR by merely adding a clear record.
The adapter does not discover cross-PR or cross-repository
release obligations and cannot accept a composed release.

## Exact coverage and remaining race

Missing, edited, malformed, stale, conflicting or unresolved required evidence
denies admission. A blocker observed on the second read prevents the merge.
The evidence digest binds repository/owner, PR, head, base, reviews and comments.
An altered evidence snapshot requires reorientation instead of a blind retry.
Post-effect reconciliation verifies that the squash merge's sole parent is the
admitted base. Only that exact merge's expected base advancement, and its own
PROGRAMSTART methodology advancement when applicable, are normalized. This
preserves the incumbent review binding without blessing an unrelated advance.

GitHub's merge endpoint accepts a head guard, but no comment/review-version
compare-and-merge. A new same-head blocker arriving after the last GET can race
the PUT. The post-effect read reports `MERGED_BUT_UNACCEPTED` if it observes that
change or cannot establish the merged poststate. It cannot undo the merge or
prove that no later contradiction will appear. This is degraded enforcement,
not the atomic disposition fencing required by the execution plan.

An unavailable merge response is `UNKNOWN`; the script does not retry the PUT.
Read the existing PR/effect result under the original identity before resuming.
Even an unchanged successful poststate is
`MERGED_REQUIRES_OWNER_RECONCILIATION`, never release acceptance. All receipts
set `activation_permitted: false` and `retry_merge: false`. Effect-mode exit
status remains nonzero to require receipt-aware reconciliation; do not configure
blind command retries on that exit status.

No installed runtime consumer, restart target, branch-protection rule, connector
merge tool or manual GitHub path is intercepted by this script. Do not claim
global enforcement or close113 from its tests. The remaining implementation must
compose trusted disposition production/revocation with the actual serialized
merge/release consumers and prove the natural acceptance case.
