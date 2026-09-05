# First Interop Vertical Slice Evidence — 2026-09-05

## Goal

Test whether `rts-interop/v1` can connect two existing repositories with thin adapters instead of creating a new controller or replacing local models.

Target slice:

```text
RIGHT ARM
  -> authorized UNIT
Connector Hub
  -> existing ConnectorRuntime
  -> RESULT
RIGHT ARM
  -> existing EvidenceRef
```

## Implemented candidates

### RIGHT ARM

Draft PR: `nobutakayamauchi/right-arm#10`

Candidate changes:
- emits bounded `UNIT` artifacts;
- derives `authority.execution=true` only for work already classified by the existing RIGHT ARM policy as reversible;
- consequential work remains non-authorized until a target-bound approval exists;
- exports existing `DecisionTrace` as `TRACE` without changing its internal schema;
- accepts a returned `RESULT` as an existing `EvidenceRef` rather than inventing a second evidence model;
- does not copy provider item bodies into the evidence metadata summary;
- preserves blocked results as `UNKNOWN` evidence rather than converting them to success/failure.

Current verification state:

```text
CODE: PRESENT ON DRAFT BRANCH
TESTS: ADDED
CI/ACTIONS: NOT PRESENT FOR THIS REPO
EXECUTED TEST EVIDENCE: UNKNOWN
PROMOTION: NOT AUTHORIZED
```

### Connector Hub

Draft PR: `nobutakayamauchi/connector-hub#2`

Candidate changes:
- consumes `UNIT` only when contract/version/type/state/consumer checks pass;
- requires explicit `authority.execution=true`;
- rejects `external_action=true` at the v0.1 read/fetch boundary;
- reuses the existing `ConnectorRuntime.execute()` path;
- converts `NormalizedResponse` to bounded `RESULT`;
- converts known Connector Hub failures such as missing credentials to `BLOCKED` RESULT rather than false success;
- does not add a new orchestrator/runtime.

Verification evidence:

```text
HEAD: 67a8164e0fbc34ad730fce51c42c91b7f7aa4711
GITHUB ACTIONS RUN: 33950217672
JOB: test
SETUP: success
INSTALL: success
PYTEST: success
RUN CONCLUSION: success
```

This proves repository-local test success for the Connector Hub candidate head. It does not prove live provider correctness or production deployment.

## DA finding discovered during dogfood

The initial contract wording could have forced every UNIT to remain `execution=false`, which would make harmless read/check work wait for Human Approval and contradict the system goal of escalating only consequential decisions.

Repair:

```text
UNIT EXISTS != EXECUTION AUTHORITY
```

but:

```text
CURRENT POLICY/GATE MAY EXPLICITLY ESTABLISH BOUNDED EXECUTION AUTHORITY
```

Therefore:
- reversible/read-only bounded work may carry `execution=true` when the producer has already established that authority;
- consequential work remains false until its applicable approval boundary is satisfied;
- `external_action=true` is narrower than `execution=true` and is never inferred from it.

The canonical contract draft was updated accordingly.

## Current evidence verdict

```text
CONTRACT SHAPE: SURVIVES FIRST DOGFOOD
CONNECTOR SIDE: TEST PASS
RIGHT ARM SIDE: TEST EXECUTION UNKNOWN
LIVE API: NOT RUN
PRODUCTION RUNTIME: NOT RUN
EXTERNAL ACTION: NOT RUN / NOT AUTHORIZED
MERGE: NOT AUTHORIZED
```

## Next edge

The next meaningful connection is not another worker. It is the knowledge path:

```text
private Obsidian note
-> local candidate
-> separated promotion decision
-> local FREEZE_RECORD
```

A stacked RIGHT ARM draft implements this private path without Vault scanning, secret duplication, automatic promotion, or public GitHub upload of private note bodies.

The public-safe Obsidian proposal path remains separately represented by RTS-AGE draft PR #73 and must not be conflated with the private knowledge route.
