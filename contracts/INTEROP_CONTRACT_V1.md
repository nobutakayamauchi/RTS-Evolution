# RTS Evolution Inter-Repository Contract v1

## Purpose

This contract defines the smallest common language for connecting independent RTS ecosystem repositories without turning them into one monolith.

A repository may keep its own implementation, storage, workflow, and domain model. Interoperability applies only at a cross-repository boundary, where a repository declares:

```text
PRODUCES: <artifact types>
CONSUMES: <artifact types>
```

and exchanges a bounded envelope that preserves identity, evidence, lifecycle state, decision semantics, and authority.

## Core rule

**Edges are canonical; internals remain replaceable.**

The contract is not an event bus, global controller, mandatory internal domain model, or second runtime. A component is not required to copy another repository's classes, prompts, database, or control loop merely to interoperate.

## Three independent axes

The initial draft incorrectly allowed one generic `status` field to mix lifecycle, gate judgment, and promotion judgment. These are now explicitly separate.

### Lifecycle `state`

Common artifact state only:

- `PROPOSED`
- `READY`
- `FINAL`
- `BLOCKED`
- `UNKNOWN`
- `CONFLICT`

### Gate `verdict`

Only `GATE_RESULT` may carry:

- `PASS`
- `FAIL`
- `BLOCKED`
- `UNKNOWN`
- `CONFLICT`
- `HUMAN_REQUIRED`

### Promotion `disposition`

Only `PROMOTION_DECISION` may carry:

- `PROMOTE`
- `REJECT`
- `DEFER`
- `QUARANTINE`
- `NEEDS_MORE_EVIDENCE`

None of these fields implies authority.

## Artifact types

### 1. UNIT
A bounded piece of requested work.

Minimum meaning:
- requested outcome;
- scope/boundaries;
- completion conditions;
- known consequence class;
- source identity.

A UNIT is not execution authority by itself.

### 2. RESULT
The bounded output of a worker/tool/product step.

A RESULT must not erase UNKNOWN/CONFLICT or claim success without evidence.

### 3. EVIDENCE
Observable support for a claim.

Examples:
- repository identity;
- diff/commit;
- test/CI result;
- source excerpt/reference;
- runtime/deployment identity;
- external outcome;
- explicit human decision.

`INTERPRETATION != EVIDENCE`

### 4. GATE_RESULT
A deterministic or governed evaluation of a candidate/result.

A `GATE_RESULT` requires a `verdict`.

`PASS != AUTHORITY`

### 5. RETRY_REQUEST
A request to redo only the failed/bounded unit or to re-plan when the failure invalidates the current unit shape.

Must identify:
- failed unit;
- failed gate;
- reason;
- retained evidence;
- allowed retry scope.

Whole-batch restart is not the default.

### 6. APPROVAL
An explicit human authorization record for a bounded consequence.

Every APPROVAL must bind to an exact `target_artifact_id` or a concrete `target_identity`. A free-floating approval is invalid.

`HUMAN APPROVAL != PROMOTION AUTHORITY` unless a separate promotion decision grants that authority.

### 7. TRACE
A reconstructable record of what actually happened.

TRACE is evidence/observation, not governance.

Minimum useful trace separates:
- intended action;
- executor/runtime identity;
- observable execution;
- result;
- gate/verdict;
- external outcome when applicable.

### 8. LEARNING_CANDIDATE
A proposed reusable lesson/invariant derived from one or more traces/evidence sets.

It is not reusable Canon yet.

It must retain:
- supporting evidence;
- counter-evidence;
- applicability conditions;
- counterconditions;
- unresolved uncertainty.

### 9. PROMOTION_DECISION
A governed decision over a learning candidate or component state.

A `PROMOTION_DECISION` requires a `disposition`.

### 10. FREEZE_RECORD
A stable reusable decision/invariant/state accepted after promotion.

FREEZE_RECORD is the surviving semantic responsibility of FREEZER in the reconstructed architecture. It does not require importing the old RTS FREEZER runtime or storage layout.

A freeze record should contain:
- immutable identifier/version;
- promoted claim/invariant;
- applicability and counterconditions;
- provenance/evidence references;
- authority scope;
- supersession/reassessment conditions.

## Common envelope

Every cross-repository artifact should be representable as:

```json
{
  "contract_version": "rts-interop/v1",
  "artifact_type": "RESULT",
  "artifact_id": "...",
  "created_at": "2026-09-05T15:00:00+09:00",
  "producer": {
    "repository": "owner/repo",
    "component": "...",
    "commit": "..."
  },
  "subject": {
    "unit_id": "...",
    "target_artifact_id": null,
    "target_identity": null,
    "parent_artifact_ids": []
  },
  "intended_consumers": ["owner/consumer-repo"],
  "state": "READY",
  "evidence_refs": [],
  "authority": {
    "execution": false,
    "external_action": false,
    "promotion": false
  },
  "payload": {}
}
```

`GATE_RESULT` adds `verdict`. `PROMOTION_DECISION` adds `disposition`.

The machine contract is `interop-envelope-v1.schema.json`.

## Routing boundary

`intended_consumers` identifies the expected next owner(s) when known. It is not delivery authority and does not require a central broker.

The contract supports direct file/API/message handoff, Git/GitHub records, a product-local adapter, or another replaceable transport.

`ENVELOPE != EVENT BUS`

## Identity rules

### Repository identity
Material artifacts should bind to a commit/ref when the claim depends on code state.

### Runtime/deployment identity
When a claim concerns deployed behavior, repository identity alone is insufficient.

At minimum record the strongest available observable identity such as:
- service/unit;
- working directory;
- executable/module;
- route/endpoint;
- deployed commit/revision;
- provider/model identity where relevant and observable.

`CODE EXISTENCE != RUNTIME EVIDENCE`

### External outcome identity
For payments, publications, sends, deployments, or other consequential actions, trace the actual external outcome separately from the attempted execution.

`EXECUTION ATTEMPT != OUTCOME`

## Authority rules

Authority is explicit and orthogonal to lifecycle state, gate verdict, and promotion disposition.

Forbidden implications:

```text
PASS -> execution authority
PASS -> external-action authority
PASS -> promotion authority
PROMOTE -> external-action authority
RESULT exists -> accepted result
TRACE exists -> governed truth
LEARNING_CANDIDATE exists -> FREEZE_RECORD
API key exists -> spend authority
credential exists -> permission expansion
```

Missing authority is invalid at the interop boundary; each envelope must state it explicitly. The default safe value is `false`.

## Evidence rules

- Preserve UNKNOWN/CONFLICT.
- Never convert missing evidence to a green verdict.
- A material evidence reference should identify both its kind and location/reference when structured form is used.
- A verifier must not silently repair the candidate it verifies.
- A material final judgment should use separated review when evaluator fallibility matters.
- Evidence generated against an old candidate identity does not automatically transfer to a new candidate.

## Repository declaration

A connected repository may contain a small edge declaration such as:

```yaml
contract_version: rts-interop/v1
repository: nobutakayamauchi/right-arm
role: personal_operating_layer
produces:
  - UNIT
  - APPROVAL
consumes:
  - EVIDENCE
  - GATE_RESULT
  - RESULT
```

This declaration describes cross-repository edges only. It does not make RTS Evolution a runtime dependency and does not require replacing product-local schemas.

## Initial ecosystem mapping

### right-arm

```text
PRODUCES: UNIT, APPROVAL
CONSUMES: EVIDENCE, RESULT, GATE_RESULT, TRACE
```

### connector-hub

```text
PRODUCES: EVIDENCE, RESULT
CONSUMES: UNIT, APPROVAL
```

Connector Hub is an initial connectivity candidate, not a governance authority.

### product/worker repositories

```text
PRODUCES: RESULT, EVIDENCE
CONSUMES: UNIT, APPROVAL (when consequence requires it)
```

### proof-ops

```text
PRODUCES: EVIDENCE, GATE_RESULT
CONSUMES: RESULT, EVIDENCE
```

### TRACE

```text
PRODUCES: TRACE
CONSUMES: UNIT, RESULT, EVIDENCE, GATE_RESULT, APPROVAL
```

TRACE remains an observation/evidence specialist, not governance.

### Ultimate-Loop

Ultimate Loop is a method, not a permanent event bus. When applied to a material integration it can logically produce evaluation evidence and learning candidates, but the method repository itself need not receive every runtime artifact.

```text
LOGICAL OUTPUTS: GATE_RESULT, LEARNING_CANDIDATE
INPUTS: UNIT, RESULT, EVIDENCE, TRACE
```

### RTS-Talent-Registry

The current registry is an initial candidate owner for promotion records; this assignment itself remains subject to survivor review.

```text
CANDIDATE PRODUCES: PROMOTION_DECISION
CONSUMES: LEARNING_CANDIDATE, EVIDENCE, GATE_RESULT
```

### RTS Evolution

RTS Evolution owns the current responsibility map, contract semantics, and survivor/canonicalization decisions. It must not become a duplicate runtime controller merely because it owns this contract.

### FREEZER role

```text
PRODUCES: FREEZE_RECORD
CONSUMES: PROMOTION_DECISION, LEARNING_CANDIDATE, EVIDENCE
```

The physical store may be Git/GitHub, an Obsidian-linked governed store, or another replaceable implementation as long as provenance and reconstruction semantics survive.

## Obsidian ingress contract

Obsidian is capture/staging, not automatic Canon.

```text
RAW NOTE
  -> PROPOSAL_ONLY
  -> sensitivity/privacy gate
  -> normalization
  -> bounded EVIDENCE/CANDIDATE
  -> challenge/counter-evidence
  -> LEARNING_CANDIDATE
  -> PROMOTION_DECISION
  -> FREEZE_RECORD
```

Forbidden shortcut:

```text
OBSIDIAN NOTE -> FREEZE_RECORD
```

## Retry / loop rule

Use loop inside a bounded unit and graph between units.

A failed gate should return to the smallest producer capable of correcting the failure.

After bounded repeated failure, re-plan or escalate rather than spinning indefinitely.

The exact retry count is implementation-specific; it is not a universal architectural constant.

## Migration rule

When salvaging old RTS or floating-branch implementation:

1. identify the responsibility;
2. prove the responsibility still survives;
3. identify the current owner;
4. port the smallest implementation/test surface that carries that responsibility;
5. preserve provenance to the old source;
6. run destructive DA / Counter-DA for material semantics;
7. verify the current owner rather than merging old architecture wholesale.

**Copy the survivor, preserve the graveyard.**

## Non-goals

This contract does not:
- merge repositories;
- dictate language/framework;
- create a global database;
- create a permanent central controller;
- make RTS Evolution a runtime dependency;
- replace product-local schemas;
- require every internal object to use the interop envelope;
- bypass Human Gates;
- grant automatic promotion.
