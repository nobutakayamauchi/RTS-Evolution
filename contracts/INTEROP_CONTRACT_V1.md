# RTS Evolution Inter-Repository Contract v1

Status: DRAFT / DOGFOOD / POST-DA REPAIR

## Purpose

This contract is the smallest common language for connecting independent RTS ecosystem repositories without rebuilding them into one monolith.

**Edges are canonical; internals remain replaceable.**

A repository keeps its own models, storage, runtime and workflow. The common envelope is required only when responsibility crosses a repository boundary.

This contract is not an event bus, global controller, governance kernel, database, or replacement for product-local schemas.

## Artifact vocabulary

Cross-repository work may use these artifact types:

- `UNIT` — bounded requested work;
- `RESULT` — bounded worker/tool output;
- `EVIDENCE` — observable support for a claim;
- `GATE_RESULT` — falsifiable/governed evaluation;
- `RETRY_REQUEST` — bounded correction/re-plan request;
- `APPROVAL` — explicit authorization for an exact consequence;
- `TRACE` — reconstructable observation record/candidate;
- `LEARNING_CANDIDATE` — proposed reusable lesson, not Canon;
- `PROMOTION_DECISION` — governed disposition of an exact candidate;
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

### Authority

Every envelope carries explicit booleans:

```json
{
  "execution": false,
  "external_action": false,
  "promotion": false
}
```

A true authority bit is never sufficient by itself. It must be backed by a matching `authorization_refs` entry.

## Immutable target identity

Authority-bearing decisions must bind to immutable content identity, not only a local name or ID.

Required target shape:

```json
{
  "repository": "owner/repo",
  "artifact_id": "candidate-123",
  "sha256": "<64 lowercase hex>",
  "commit": null
}
```

The digest represents the exact bounded material being authorized or promoted.

If content changes, the digest changes and the old authorization does not transfer.

`SAME ID != SAME CANDIDATE`

## Authorization references

When any authority bit is true, at least one explicit authorization reference is required.

```json
{
  "kind": "POLICY_AUTHORIZATION",
  "ref": "right-arm:policy:read-only-v1",
  "issuer": "nobutakayamauchi/right-arm",
  "scope": ["execution:bounded"],
  "target_sha256": "<exact target digest>",
  "issuer_identity": {}
}
```

Kinds:

- `POLICY_AUTHORIZATION`
- `HUMAN_APPROVAL`
- `PROMOTION_AUTHORIZATION`

The authorization must match the exact target digest and contain the required scope.

For `external_action=true` or `promotion=true`, the producing boundary must also expose a non-empty runtime/deployment identity. A free-floating string such as `approved_by: human` is not sufficient evidence of who authorized a consequential action.

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

Safe bounded execution may proceed without asking the human every time only when the current operating layer has already issued a matching policy authorization for the exact UNIT digest.

Consequential work must not reuse a read-only policy authorization.

## Consequential two-stage flow

Do not perform an irreversible/external action merely because preparation succeeded.

Required logical shape:

```text
UNIT: PREPARE / INSPECT / PROPOSE
  -> RESULT / EVIDENCE / GATE_RESULT
  -> exact ACTION CANDIDATE identity
  -> HUMAN APPROVAL bound to candidate digest
  -> second bounded EXECUTION invocation
  -> observable RESULT / external OUTCOME
  -> TRACE
```

The approval must flow back to the executor. Approval after execution is not a Human Gate.

The first Connector Hub dogfood slice is intentionally read-only and does not implement the consequential second invocation yet.

## RESULT and evidence

A RESULT is not automatically accepted truth or completion.

```text
RESULT EXISTS != COMPLETION
RESULT FINAL != EXTERNAL OUTCOME
```

A consumer may transform a RESULT into local evidence, but it must preserve producer identity, target identity, uncertainty, and durable source references when available.

If the full source payload is omitted from an observer/archive, preserve a content-addressed retrievable reference. If no durable reference exists, reconstructability is degraded and must remain `UNKNOWN` rather than `SUPPORTED`.

## GATE_RESULT

Prefer the smallest falsifiable gate owned by the component that can actually check the completion condition.

Do not create a universal gate service merely for architectural symmetry.

`PASS != AUTHORITY`

A failed gate should return to the smallest producer capable of correcting the failed bounded unit. Whole-batch restart is not the default.

Repeated bounded failure should re-plan/escalate rather than spin indefinitely.

## APPROVAL

An APPROVAL must:

- bind to immutable target identity;
- preserve the exact decision;
- identify its authority source;
- contain a matching `HUMAN_APPROVAL` authorization reference when it grants authority;
- preserve runtime/issuer identity when consequential authority is granted.

An approval for one digest is invalid after the target changes.

`APPROVAL != PROMOTION`

## TRACE

TRACE observes and preserves evidence; it does not govern.

```text
RESULT OBSERVED != COMPLETION PROVED
PASS OBSERVED != AUTHORITY GRANTED
PROMOTION DECISION OBSERVED != FREEZE RECORD EXISTS
```

A pre-archive TRACE conversion is only a `PROPOSED` record candidate.

It must not publish a candidate record hash as final archived evidence until the owning TRACE archive actually appends it and updates/reseals its integrity metadata.

A claimed human decision is recorded as `HUMAN_DECISION` only when human actor identity is established by evidence. Otherwise it remains `APPROVAL_ARTIFACT_OBSERVED`.

Observer runtime/deployment identity is required for material TRACE output.

## LEARNING_CANDIDATE

A learning candidate must preserve:

- supporting evidence;
- counter-evidence;
- applicability conditions;
- counterconditions;
- unresolved uncertainty.

It is not reusable Canon merely because a model derived it.

## PROMOTION_DECISION

Promotion is a decision about an exact candidate digest.

It may preserve unresolved judgment explicitly as `UNKNOWN` or `CONFLICT`; do not hide those states inside `DEFER` or lifecycle state.

`PROMOTE` requires evidence and a matching `PROMOTION_AUTHORIZATION` bound to the target digest.

Current repository ownership of promotion is contextual. There is no mandatory central Promotion Engine.

`RTS-Talent-Registry` is currently COLD/FROZEN historical governance material and is not the default current promotion authority. Its surviving useful ideas—separating confirmed facts, assumptions, unverified facts, and risks—may be reused without reviving the repository as a central service.

## FREEZE_RECORD

FREEZER survives as a responsibility, not as an obligation to restore the old RTS runtime.

A FREEZE_RECORD is valid only after governed promotion and must include:

- promoted claim/invariant;
- exact promotion decision reference;
- supporting provenance/evidence;
- applicability;
- counterconditions;
- authority scope;
- reassessment/supersession conditions.

Empty/raw `FREEZE_RECORD` envelopes are invalid.

A FREEZE_RECORD grants no new execution/external/promotion authority by existing.

## Obsidian private/public split

### Private RIGHT ARM lane

```text
explicitly selected local note
 -> credential/sensitivity gate
 -> local PROPOSAL_ONLY candidate
 -> canonical candidate digest
 -> evidence / challenge / human promotion decision as required
 -> local FREEZE_RECORD
```

Personal/internal knowledge may freeze locally. Credentials/secrets are not duplicated into durable knowledge candidates.

The candidate is re-hashed at promotion time. Editing the candidate after the promotion target was established invalidates the decision.

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

Personal operating layer. Produces bounded UNIT/TRACE/APPROVAL/PROMOTION_DECISION artifacts and consumes result/evidence/gate/trace artifacts as needed.

### connector-hub

Connectivity specialist. The current interop dogfood path accepts only exact, authorized, read-only RIGHT ARM UNITs. The v1 allowlist is intentionally narrower than Connector Hub's whole internal registry so future write capabilities cannot silently inherit read authority.

### TRACE

Passive evidence observer/reconstruction substrate. No governance or archive mutation is implied by observing an envelope.

### Ultimate-Loop

Canonical development/challenge method, not an event bus. It may logically produce evaluation evidence and learning candidates while leaving runtime transport to bounded owners.

### proof-ops

Sales/outreach-domain public-evidence proof preparation. It is not the universal system Gate.

### RTS Evolution

Owns current reconstruction, responsibility mapping, and interop contract semantics. It must not become a duplicate runtime controller.

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
PASS -> execution/external/promotion authority
approval id matches -> approval still valid
PROMOTE -> external-action authority
RESULT exists -> accepted result
TRACE candidate exists -> archived TRACE evidence exists
LEARNING_CANDIDATE exists -> FREEZE_RECORD
FREEZE_RECORD exists -> build/execution authority
credential exists -> permission/spend authority
code exists -> runtime/deployment evidence
```

## Machine source of truth

The normative machine shape is `contracts/interop-envelope-v1.schema.json`.

When prose and schema conflict, classify the conflict and repair them together before widening runtime use. Do not silently pick the more permissive interpretation.
