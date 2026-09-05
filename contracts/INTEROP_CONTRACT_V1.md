# RTS Evolution Inter-Repository Contract v1

Status: CANDIDATE / DOGFOOD / NON-AUTHORIZING V1

## Purpose

This contract is the smallest common language for connecting independent RTS ecosystem repositories without rebuilding them into one monolith.

**Edges are canonical; internals remain replaceable.**

A repository keeps its own models, storage, runtime and workflow. The common envelope applies only when responsibility crosses a repository boundary.

This contract is not an event bus, global controller, governance kernel, database, credential system, transport authenticator, or authority service.

## Core invariant

**RTS-INTEROP/V1 DOES NOT CARRY AUTHORITY.**

Every v1 envelope carries:

```json
{
  "execution": false,
  "external_action": false,
  "promotion": false
}
```

and `authorization_refs` is empty.

No JSON field, producer string, runtime-identity dictionary, policy name, approval string, gate result, or promotion disposition can grant authority in v1.

Actual execution, external action, human authentication, or promotion authorization must occur in a separate trusted runtime/transport boundary that can establish identity and authority independently. If that boundary does not exist, the action remains blocked.

`No trusted runtime boundary => BLOCKED`

## Artifact vocabulary

- `UNIT` — bounded work proposal;
- `RESULT` — bounded reported output or blocked result;
- `EVIDENCE` — observable support/counter-evidence;
- `GATE_RESULT` — falsifiable evaluation;
- `RETRY_REQUEST` — bounded correction/re-plan request;
- `APPROVAL` — exact-target approval decision record;
- `TRACE` — reconstructable observation record/candidate;
- `LEARNING_CANDIDATE` — proposed reusable lesson, not Canon;
- `PROMOTION_DECISION` — exact-target promotion decision record;
- `FREEZE_RECORD` — promoted reusable knowledge/state with provenance.

## Independent axes

Do not collapse lifecycle, evaluation, promotion, and authority into one status.

Lifecycle state:

`PROPOSED | READY | FINAL | BLOCKED | UNKNOWN | CONFLICT`

Gate verdict:

`PASS | FAIL | BLOCKED | UNKNOWN | CONFLICT | HUMAN_REQUIRED`

Promotion disposition:

`PROMOTE | REJECT | DEFER | QUARANTINE | NEEDS_MORE_EVIDENCE | UNKNOWN | CONFLICT`

Authority is not an axis v1 can activate. It remains false.

## Immutable target identity and issuance

Bounded work and decisions use immutable target identity:

```json
{
  "repository": "owner/repo",
  "artifact_id": "candidate-123",
  "sha256": "<64 lowercase hex>",
  "commit": null
}
```

For UNITs, the canonical digest also includes a unique `issuance_id`. Reissuing identical work therefore produces a different target digest.

`SAME WORK != SAME ISSUANCE`

`SAME ID != SAME TARGET`

This prevents a prior RESULT or decision from silently transferring to a later issuance.

## UNIT

A UNIT defines at minimum:

- unique issuance ID;
- requested outcome;
- completion conditions;
- scope;
- consequence class;
- source identity;
- exact task payload;
- intended consumer(s);
- canonical target digest.

`UNIT EXISTS != EXECUTION AUTHORITY`

A UNIT may name a requested policy or expected runtime only as proposal metadata. Those claims never authorize dispatch.

### Current Connector Hub v1 behavior

The current RIGHT ARM → Connector Hub slice is validation-only:

```text
RIGHT ARM UNIT proposal
 -> exact structure + issuance + digest validation
 -> pinned github/pull_requests.read proposal validation
 -> BLOCKED: TRUSTED_RUNTIME_REQUIRED
```

Connector Hub v1 does **not** invoke `ConnectorRuntime` from the interop envelope path. Dynamic registry contents therefore cannot widen the authority of this edge.

Execution can be added only when a real authenticated runtime boundary exists outside the v1 JSON contract.

## RESULT and evidence

A RESULT is not automatically truth, completion, or supported evidence.

```text
RESULT EXISTS != COMPLETION
RESULT FINAL != EXTERNAL OUTCOME
RESULT FINAL != SUPPORTED EVIDENCE
```

RIGHT ARM may bind a RESULT to the exact outstanding target digest, but producer/runtime identity written inside the envelope remains an assertion. Without independent trusted verification, the local evidence classification remains `UNKNOWN` rather than `SUPPORTED`.

A `CONFLICT` RESULT may still become counter-evidence without pretending producer identity is established.

## GATE_RESULT

Prefer the smallest falsifiable gate owned by the component that can actually check the completion condition.

`PASS != AUTHORITY`

A failed gate returns to the smallest producer capable of correcting the failed unit. Whole-batch restart is not the default. Repeated bounded failure should re-plan/escalate rather than spin indefinitely.

## APPROVAL

An APPROVAL is a decision record, not an authority token.

It must contain:

- immutable target identity;
- explicit `APPROVE` or `REJECT` decision;
- asserted actor;
- resolvable approval record/reference;
- at least one evidence/reference entry.

`APPROVE != EXECUTION AUTHORITY`

`approved_by string != authenticated human`

A downstream trusted verifier may authenticate an approval, but that trusted verification exists outside v1.

## TRACE

TRACE observes and preserves evidence; it does not govern.

```text
RESULT OBSERVED != COMPLETION PROVED
PASS OBSERVED != AUTHORITY GRANTED
PROMOTION DECISION OBSERVED != FREEZE RECORD EXISTS
```

A pre-archive TRACE conversion is only `PROPOSED`. It publishes no final archive evidence reference until the archive owner appends/reseals it.

Observer runtime/deployment identity is required for material TRACE output, and TRACE derivation must use the same observer identity sealed into the candidate record.

A claimed human actor becomes `HUMAN_DECISION` only when a trusted verifier attests the exact approval envelope digest together with the asserted actor and evidence reference. Reusing a valid human-session reference on another approval does not transfer verification.

### Reconstructability

A payload omitted from TRACE is `SUPPORTED` as reconstructable only when:

1. the reference is exactly `sha256:<captured payload digest>`;
2. its declared digest matches;
3. a resolver retrieves the referenced content;
4. the retrieved content hashes to that digest.

Forbidden implication:

`content-addressed ref string exists -> payload reconstructable`

Otherwise TRACE preserves `UNKNOWN / reconstruction_gap`.

## LEARNING_CANDIDATE

A learning candidate preserves at minimum:

- original requested outcome;
- original completion conditions;
- supporting evidence;
- counter-evidence;
- applicability conditions;
- counterconditions;
- unresolved uncertainty;
- defect-history references;
- source TRACE references.

It carries no authority.

These requirements preserve the surviving WITNESS semantics without reviving WITNESS as software.

## PROMOTION_DECISION

Promotion is a decision about an exact candidate digest.

A `PROMOTE` disposition remains a non-authorizing record.

`PROMOTE != PROMOTION AUTHORITY`

A trusted promotion verifier outside v1 must authenticate the exact decision/target/evidence before FREEZE can occur.

Unresolved judgment remains explicit as `UNKNOWN` or `CONFLICT`.

There is no mandatory central Promotion Engine. `RTS-Talent-Registry` remains historical governance material rather than a required promotion runtime.

## FREEZE_RECORD

FREEZER survives as a responsibility, not as an obligation to restore the old RTS runtime.

A FREEZE_RECORD is valid only after trusted governed promotion and includes:

- promoted claim/invariant;
- exact promotion decision reference;
- supporting provenance/evidence;
- applicability;
- counterconditions;
- authority scope of the frozen knowledge;
- reassessment/supersession conditions.

A FREEZE_RECORD itself carries no execution/external/promotion authority.

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

A caller-controlled PROMOTION_DECISION dictionary never authorizes FREEZE by itself.

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

## Current owners

### right-arm

Produces bounded UNIT/TRACE and non-authorizing APPROVAL/PROMOTION decision records. UNIT issuance is uniquely hashed. Unverified RESULT claims remain UNKNOWN.

### connector-hub

Connectivity specialist. The v1 interop edge validates one pinned read proposal and returns BLOCKED until a real trusted execution boundary exists. It does not dispatch ConnectorRuntime from v1 envelopes.

### TRACE

Passive evidence observer/reconstruction substrate. No governance or archive mutation is implied by observing an envelope.

### Ultimate-Loop

Canonical development/challenge method, not an event bus.

### RTS Evolution

Owns current responsibility mapping and edge-contract semantics. It must not become a duplicate runtime controller.

## Migration / archaeology rule

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

## Forbidden implications

```text
UNIT exists -> execution authority
REVERSIBLE label -> execution authority
producer field -> authenticated producer
runtime_identity field -> authenticated runtime
requested policy ref -> execution authority
PASS -> execution/external/promotion authority
APPROVE -> execution/external authority
approved_by string -> human identity
PROMOTE -> promotion authority
RESULT exists -> accepted result
RESULT target hash matches -> producer authenticated
RESULT FINAL -> supported evidence
TRACE candidate exists -> archived TRACE evidence exists
content-addressed ref string exists -> payload reconstructable
LEARNING_CANDIDATE exists -> FREEZE_RECORD
FREEZE_RECORD exists -> build/execution authority
credential exists -> permission/spend authority
code exists -> runtime/deployment evidence
```

## Machine source of truth

The normative structural machine shape is `contracts/interop-envelope-v1.schema.json`.

JSON Schema validates structure only. It cannot authenticate transport, runtime, people, referenced content, or authority. v1 intentionally refuses to encode authority as true.

A future execution-capable edge must introduce an independently authenticated runtime boundary rather than silently widening v1.
