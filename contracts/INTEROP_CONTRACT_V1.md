# RTS Evolution Inter-Repository Contract v1

Status: DRAFT / DOGFOOD / POST-DA REPAIR

## Purpose

This contract is the smallest common language for connecting independent RTS ecosystem repositories without rebuilding them into one monolith.

**Edges are canonical; internals remain replaceable.**

A repository keeps its own models, storage, runtime and workflow. The common envelope applies only when responsibility crosses a repository boundary.

This contract is not an event bus, global controller, governance kernel, database, or replacement for product-local schemas.

## Artifact vocabulary

- `UNIT` — bounded requested work;
- `RESULT` — bounded worker/tool output;
- `EVIDENCE` — observable support for a claim;
- `GATE_RESULT` — falsifiable/governed evaluation;
- `RETRY_REQUEST` — bounded correction/re-plan request;
- `APPROVAL` — exact-target approval **decision record**; it may remain non-authorizing until trusted verification;
- `TRACE` — reconstructable observation record/candidate;
- `LEARNING_CANDIDATE` — proposed reusable lesson, not Canon;
- `PROMOTION_DECISION` — exact-target promotion **decision record**; disposition is not authority;
- `FREEZE_RECORD` — promoted reusable knowledge/state with provenance.

## Independent axes

Do not collapse lifecycle, evaluation, promotion, and authority into one status.

### Lifecycle `state`

`PROPOSED | READY | FINAL | BLOCKED | UNKNOWN | CONFLICT`

### Gate `verdict`

Only `GATE_RESULT` carries:

`PASS | FAIL | BLOCKED | UNKNOWN | CONFLICT | HUMAN_REQUIRED`

### Promotion `disposition`

Only `PROMOTION_DECISION` carries:

`PROMOTE | REJECT | DEFER | QUARANTINE | NEEDS_MORE_EVIDENCE | UNKNOWN | CONFLICT`

### Authority vector

Every envelope carries:

```json
{
  "execution": false,
  "external_action": false,
  "promotion": false
}
```

The vector is a **producer assertion**, not cross-repository proof.

Even when an authority bit is true, a consumer must independently establish all applicable identity and authority facts before acting:

1. authenticate the producer/repository through the transport or equivalent trusted boundary;
2. authenticate the producer runtime/deployment identity;
3. recompute/verify the exact target identity or digest when applicable;
4. resolve and verify the referenced policy/human/promotion authority source;
5. verify required scope and consumer binding.

`ENVELOPE SAYS AUTHORIZED != AUTHORITY VERIFIED`

A consumer that cannot perform the required verification must fail closed or preserve `UNKNOWN`.

## Immutable target identity

Authority-bearing work and consequential decisions bind to immutable content identity, not only a local name or ID.

```json
{
  "repository": "owner/repo",
  "artifact_id": "candidate-123",
  "sha256": "<64 lowercase hex>",
  "commit": null
}
```

If content changes, the digest changes and old evidence/approval/authorization does not transfer.

`SAME ID != SAME CANDIDATE`

## Authorization references

An `authorization_refs` entry is a structured pointer/assertion:

```json
{
  "kind": "POLICY_AUTHORIZATION",
  "ref": "right-arm:policy:read-only-v1",
  "issuer": "nobutakayamauchi/right-arm",
  "scope": ["execution:bounded"],
  "target_sha256": "<exact target digest>",
  "issuer_identity": {"runtime": "..."}
}
```

Kinds:

- `POLICY_AUTHORIZATION`
- `HUMAN_APPROVAL`
- `PROMOTION_AUTHORIZATION`

Structural presence is not proof. The consumer must resolve/authenticate the reference and issuer identity before honoring it.

Whenever any authority bit is true, the envelope must contain at least one authorization reference and a non-empty producer runtime identity. The consumer still must verify both independently.

## UNIT

A UNIT defines bounded work:

- requested outcome;
- scope;
- completion conditions;
- consequence class;
- source identity;
- exact task payload;
- intended consumer(s).

`UNIT EXISTS != EXECUTION AUTHORITY`

A UNIT is non-authorizing by default, including reversible/read-only work.

The current first dogfood slice permits one bounded read-only exception: RIGHT ARM may issue execution authority only for a locally recognized read policy, exact canonical UNIT digest, exact Connector Hub consumer, and established RIGHT ARM runtime identity. Connector Hub must independently authenticate the RIGHT ARM repository/runtime and verify the authorization binding before dispatch.

Consequential work must not reuse this read-only policy.

## Consequential two-stage flow

Do not perform an irreversible/external action merely because preparation succeeded.

```text
UNIT: PREPARE / INSPECT / PROPOSE
 -> RESULT / EVIDENCE / GATE_RESULT
 -> exact ACTION CANDIDATE identity
 -> APPROVAL decision record bound to candidate digest
 -> trusted authority verifier resolves/authenticates the approval
 -> second bounded EXECUTION invocation carrying verified authority
 -> observable RESULT / external OUTCOME
 -> TRACE
```

Approval after execution is not a Human Gate.

The first Connector Hub dogfood slice is intentionally read-only and does not implement the consequential second invocation.

## RESULT and evidence

A RESULT is not automatically accepted truth or completion.

```text
RESULT EXISTS != COMPLETION
RESULT FINAL != EXTERNAL OUTCOME
```

Before a RESULT becomes supported local evidence, the consumer must bind it to the exact outstanding target and authenticate its producer/runtime identity. A correct target digest alone does not prove who produced the result.

If a full payload is omitted from an observer/archive, `SUPPORTED` reconstructability requires a resolver to retrieve the referenced content and hash-verify the actual bytes/value against the captured payload digest. A producer-supplied `ref` or `digest` alone is not enough.

No resolvable verified source => `UNKNOWN / reconstruction_gap`.

## GATE_RESULT

Prefer the smallest falsifiable gate owned by the component able to check the completion condition.

`PASS != AUTHORITY`

A failed gate returns to the smallest producer capable of correcting the failed unit. Whole-batch restart is not the default. Repeated bounded failure should re-plan/escalate rather than spin indefinitely.

## APPROVAL

An APPROVAL artifact records a decision bound to exact target identity.

It may legitimately carry all authority bits as `false` when the current producer can record the decision but cannot authenticate the human/authority source itself. A downstream trusted verifier may validate the referenced decision and create/use a separately authenticated execution boundary.

Therefore:

```text
APPROVE disposition/decision != execution authority
approved_by string != authenticated human
APPROVAL artifact != PROMOTION authority
```

A pure JSON builder must not become an authority mint merely because the caller supplied a non-empty identity dictionary.

## TRACE

TRACE observes and preserves evidence; it does not govern.

```text
RESULT OBSERVED != COMPLETION PROVED
PASS OBSERVED != AUTHORITY GRANTED
PROMOTION DECISION OBSERVED != FREEZE RECORD EXISTS
```

A pre-archive TRACE conversion is only `PROPOSED`. It publishes no final evidence ref until the archive owner actually appends/reseals it.

Observer runtime/deployment identity is required for material TRACE output.

A claimed human actor becomes `HUMAN_DECISION` only when a trusted verifier establishes the human identity evidence. `verified: true` inside a producer-controlled dictionary is not enough.

A sealed candidate record must be re-hashed before deriving provenance so mutation after sealing cannot silently alter what the hash is said to represent.

## LEARNING_CANDIDATE

A learning candidate must preserve at minimum:

- the original requested outcome;
- original completion conditions;
- supporting evidence;
- counter-evidence;
- applicability conditions;
- counterconditions;
- unresolved uncertainty;
- defect-history references;
- source TRACE references.

It carries no execution/external/promotion authority.

These requirements preserve the surviving WITNESS semantics without reviving WITNESS as software.

## PROMOTION_DECISION

Promotion is a decision about an exact candidate digest.

A `PROMOTE` disposition may be recorded while `authority.promotion=false`. This is correct when the producer can record the decision but cannot itself authenticate promotion authority.

A consumer may honor promotion only after trusted verification of the exact target, decision source, evidence classifications, and authority boundary.

`PROMOTE != PROMOTION AUTHORITY`

Unresolved judgment remains explicit as `UNKNOWN` or `CONFLICT`.

There is no mandatory central Promotion Engine. `RTS-Talent-Registry` remains COLD/FROZEN historical governance material, not the default promotion runtime.

## FREEZE_RECORD

FREEZER survives as a responsibility, not as an obligation to restore the old RTS runtime.

A FREEZE_RECORD is valid only after trusted governed promotion and must include:

- promoted claim/invariant;
- exact promotion decision reference;
- supporting provenance/evidence;
- applicability;
- counterconditions;
- authority scope of the frozen knowledge;
- reassessment/supersession conditions.

A FREEZE_RECORD itself always carries all authority bits `false`.

`FREEZE_RECORD EXISTS != EXECUTION/PROMOTION AUTHORITY`

## Obsidian private/public split

### Private RIGHT ARM lane

```text
explicitly selected local note
 -> credential/sensitivity gate
 -> local PROPOSAL_ONLY candidate
 -> canonical candidate digest
 -> evidence / challenge / promotion decision record
 -> trusted promotion verifier
 -> local FREEZE_RECORD
```

Personal/internal knowledge may remain and freeze locally. Credentials/secrets are not duplicated into durable knowledge candidates.

Candidate and source hashes are revalidated at promotion time. Editing the candidate invalidates the decision target.

A caller-controlled PROMOTION_DECISION dictionary never authorizes FREEZE by itself. No trusted verifier => BLOCKED.

### Public-safe RTS-AGE lane

```text
human-authored public-safe proposal
 -> proposal-only ingress
 -> public-safety validation
 -> reviewable implementation/record proposal
```

Do not send private Vault bodies through a public GitHub Issue path.

Forbidden shortcut:

`OBSIDIAN NOTE -> FREEZE_RECORD`

## Current initial owners

### right-arm

Personal operating layer. Produces bounded UNIT/TRACE and non-authorizing APPROVAL/PROMOTION decision records. The current executable interop exception is the exact runtime-bound read-only UNIT policy described above.

### connector-hub

Connectivity specialist. The current dogfood path accepts only exact read-only RIGHT ARM UNITs after transport-authenticated repository/runtime verification, exact content digest recomputation, authorization issuer-identity matching, and fixed allowlist validation. RESULT carries Connector Hub runtime identity back to RIGHT ARM.

### TRACE

Passive evidence observer/reconstruction substrate. No governance or archive mutation is implied by observing an envelope.

### Ultimate-Loop

Canonical development/challenge method, not an event bus.

### proof-ops

Sales/outreach-domain public-evidence preparation, not a universal system Gate.

### RTS Evolution

Owns current responsibility mapping and edge-contract semantics. It must not become a duplicate runtime controller.

## Migration / archaeology rule

When a current gap is found, do not immediately create a new subsystem.

```text
problem found
 -> search current main + open PR + floating branches + historical predecessor
 -> identify newer/surviving responsibility
 -> salvage smallest useful implementation/test
 -> connect to current owner
 -> DA / Counter-DA
 -> verify
 -> freeze old implementation as history when superseded
```

**Copy the survivor, preserve the graveyard.**

Do not finish an obsolete 80% implementation when a newer implementation already contains the surviving responsibility. Port the useful 20% forward instead.

## Forbidden implications

```text
UNIT exists -> execution authority
REVERSIBLE label -> execution authority
producer field -> authenticated producer
runtime_identity field -> authenticated runtime
authorization_ref exists -> authority verified
PASS -> execution/external/promotion authority
APPROVE -> execution/external authority
approved_by string -> human identity
PROMOTE -> promotion authority
approval id matches -> approval still valid
RESULT exists -> accepted result
RESULT target hash matches -> producer authenticated
TRACE candidate exists -> archived TRACE evidence exists
content-addressed ref string exists -> payload reconstructable
LEARNING_CANDIDATE exists -> FREEZE_RECORD
FREEZE_RECORD exists -> build/execution authority
credential exists -> permission/spend authority
code exists -> runtime/deployment evidence
```

## Machine source of truth

The normative structural machine shape is `contracts/interop-envelope-v1.schema.json`.

JSON Schema can validate structure but cannot prove transport identity, runtime identity, human identity, referenced content reachability, or authority-source authenticity. Those are consumer/runtime verification responsibilities.

When prose and schema conflict, classify the conflict and repair them together before widening runtime use. Do not silently pick the more permissive interpretation.
