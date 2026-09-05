# RTS Evolution Inter-Repository Contract v1

## Purpose

This contract defines the smallest common language for connecting independent RTS ecosystem repositories without turning them into one monolith.

A repository may keep its own implementation, storage, workflow, and domain model. It becomes interoperable by declaring:

```text
PRODUCES: <artifact types>
CONSUMES: <artifact types>
```

and by exchanging bounded envelopes that preserve identity, evidence, status, and authority.

## Core rule

**Edges are canonical; internals remain replaceable.**

A component is not required to copy another repository's internal classes, prompts, database, or control loop merely to interoperate.

## Artifact types

### 1. UNIT
A bounded piece of requested work.

Minimum meaning:
- what outcome is requested;
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

Expected verdict vocabulary:

- `PASS`
- `FAIL`
- `BLOCKED`
- `UNKNOWN`
- `CONFLICT`
- `HUMAN_REQUIRED`

A PASS has no implicit promotion or external-action authority.

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

Approval should bind to the exact candidate/identity whenever practical.

`HUMAN APPROVAL != PROMOTION AUTHORITY` unless the promotion decision explicitly says so.

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
A governed decision to accept, reject, defer, or quarantine a learning candidate or component state.

Expected disposition vocabulary:

- `PROMOTE`
- `REJECT`
- `DEFER`
- `QUARANTINE`
- `NEEDS_MORE_EVIDENCE`

### 10. FREEZE_RECORD
A stable reusable decision/invariant/state accepted after promotion.

FREEZE_RECORD is the surviving role of FREEZER in the reconstructed architecture.

It does not require importing the old RTS FREEZER runtime.

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
  "created_at": "...",
  "producer": {
    "repository": "owner/repo",
    "component": "...",
    "commit": "..."
  },
  "subject": {
    "unit_id": "...",
    "parent_artifact_ids": []
  },
  "status": "UNKNOWN",
  "evidence_refs": [],
  "authority": {
    "execution": false,
    "external_action": false,
    "promotion": false
  },
  "payload": {}
}
```

The JSON Schema is stored separately as `interop-envelope-v1.schema.json`.

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

Authority is explicit and orthogonal to status.

The following are forbidden implications:

```text
PASS -> execution authority
PASS -> external-action authority
PASS -> promotion authority
RESULT exists -> accepted result
TRACE exists -> governed truth
LEARNING_CANDIDATE exists -> FREEZE_RECORD
API key exists -> spend authority
credential exists -> permission expansion
```

Missing authority defaults to `false`.

## Evidence rules

- Preserve UNKNOWN/CONFLICT.
- Never convert missing evidence to a green verdict.
- A verifier must not silently repair the candidate it verifies.
- A material final judgment should use separated review when evaluator fallibility matters.
- Evidence generated against an old candidate identity does not automatically transfer to a new candidate.

## Repository declaration

Every repository connected to this contract should eventually contain a small declaration similar to:

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

This declaration describes edges only. It does not create runtime dependency on RTS Evolution.

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

### Ultimate-Loop

Ultimate Loop is a method, not a permanent event bus. When applied to a material integration it may produce evaluation evidence and learning candidates, but the method repository itself need not receive every runtime artifact.

```text
LOGICAL OUTPUTS: GATE_RESULT, LEARNING_CANDIDATE
INPUTS: UNIT, RESULT, EVIDENCE, TRACE
```

### RTS-Talent-Registry

```text
PRODUCES: PROMOTION_DECISION
CONSUMES: LEARNING_CANDIDATE, EVIDENCE, GATE_RESULT
```

### RTS Evolution

RTS Evolution owns the current responsibility map, contract semantics, and canonical survivor decisions. It should not become a duplicate runtime controller.

### FREEZER role

```text
PRODUCES: FREEZE_RECORD
CONSUMES: PROMOTION_DECISION, LEARNING_CANDIDATE, EVIDENCE
```

The physical store may be Git/GitHub, Obsidian-linked governed storage, or another replaceable implementation as long as the semantics remain reconstructable.

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
- bypass Human Gates;
- grant automatic promotion.
