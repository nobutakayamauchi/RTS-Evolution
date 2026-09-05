# Inter-Repository Contract v1 — DA / Counter-DA — 2026-09-05

## Candidate attacked

Initial `rts-interop/v1` draft on `integration/ecosystem-reassembly-v1`.

## Raison d'être attack

### Attack
Why create a shared contract at all? Every repository already has its own schemas and could simply call the next component directly.

### Death condition
If the contract requires repos to replace local domain models, introduces a central controller/database, or duplicates product-local governance, remove it.

### Finding
A minimal edge contract still survives because the current failure mode is cross-repository ambiguity: result vs evidence vs approval vs promotion are represented differently or not bound together at all. However, the contract is justified only at repository boundaries.

### Survivor
`BOUNDARY INTEROP CONTRACT`, not `GLOBAL INTERNAL MODEL`.

---

## Attack 1 — lifecycle and judgment conflation

### Initial defect
The first JSON schema used one generic `status` enum containing both:

- lifecycle-like values;
- gate outcomes (`PASS`, `FAIL`);
- promotion-like outcomes (`REJECTED`, `DEFERRED`, `QUARANTINED`).

This could recreate the exact class of ambiguity the contract was meant to remove.

### Verdict
`FAIL`

### Repair
Split into three orthogonal axes:

- `state` — artifact lifecycle/availability only;
- `verdict` — required only on `GATE_RESULT`;
- `disposition` — required only on `PROMOTION_DECISION`.

### Counter-DA
Could three fields be needless complexity?

No. They answer materially different questions:

1. what state is this artifact in?
2. what did the gate conclude?
3. what did promotion governance decide?

Removing the distinction allows a green test to become an accepted lesson by vocabulary accident.

### Survivor
Keep the split.

---

## Attack 2 — free-floating human approval

### Initial defect
The draft described exact candidate binding as desirable but did not require the envelope to identify what the approval authorizes.

### Failure mode
An old approval could be replayed against a changed candidate, a broader action, or a different runtime identity.

### Verdict
`FAIL`

### Repair
Every `APPROVAL` must bind to at least one of:

- exact `target_artifact_id`; or
- concrete `target_identity`.

The approval remains separate from promotion authority.

### Counter-DA
Can some human approvals legitimately be broad policy?

Yes, but a broad policy is not the same artifact as a one-shot consequence approval. The interop APPROVAL record is intentionally bounded. Broader policy belongs in a policy/config source and should itself be referenced when relevant.

### Survivor
Keep target binding.

---

## Attack 3 — disguised central event bus

### Attack
A common envelope plus many producers/consumers can quietly become a mandatory global broker/controller.

### Verdict
`SURVIVES WITH RESTRICTION`

### Repair
- contract applies only at cross-repository edges;
- product-local/internal schemas remain authoritative internally;
- `intended_consumers` can name the next expected owner without requiring a broker;
- transport remains replaceable: direct API, file, Git/GitHub artifact, local adapter, or another bounded mechanism;
- RTS Evolution owns contract semantics, not runtime dispatch.

### Counter-DA
Could `intended_consumers` itself create tight coupling?

It is optional and descriptive. It prevents ambient broadcast semantics when the next owner is known but does not establish delivery authority.

### Survivor
`EDGE CONTRACT != CENTRAL BUS`.

---

## Attack 4 — FREEZER resurrection

### Attack
Naming `FREEZE_RECORD` could accidentally recreate old RTS FREEZER implementation as a mandatory dependency.

### Verdict
`SURVIVES AS RESPONSIBILITY ONLY`

### Repair
Define `FREEZE_RECORD` as a stable promoted knowledge/invariant record. The physical implementation is replaceable and may be Git/GitHub, an Obsidian-linked governed store, or another reconstructable holder.

Old RTS FREEZER code is historical source material, not automatic current runtime authority.

### Counter-DA
Why retain a freeze concept at all?

Because the surviving requirement is real: accepted learning must be distinguishable from raw capture and learning candidates, retain provenance/counterconditions, and be reusable without re-deriving every prior decision.

### Survivor
Keep `FREEZE_RECORD`; reject old-runtime dependency.

---

## Attack 5 — Obsidian capture becoming Canon

### Attack
The stranded old Knowledge Bridge already contains an Obsidian adapter and FREEZER export path. Porting it naively could make capture equivalent to canonicalization.

### Verdict
`FAIL WHOLESALE PORT`

### Repair
Required target path:

```text
RAW NOTE
-> PROPOSAL_ONLY
-> sensitivity/privacy gate
-> normalization
-> evidence/candidate
-> challenge/counter-evidence
-> learning candidate
-> promotion decision
-> freeze record
```

The old branch may supply implementation/test fragments only after responsibility-level review.

### Survivor
Salvage adapter/normalization/sensitivity/routing/deployment-identity semantics and still-valid tests. Do not merge the old branch wholesale.

---

## Attack 6 — authority leakage from PASS/PROMOTE

### Attack
Even with separate verdict/disposition, callers may assume `PASS` or `PROMOTE` authorizes execution, sending, payment, deployment, or publication.

### Verdict
`SURVIVES WITH EXPLICIT AUTHORITY VECTOR`

### Repair
Every envelope carries explicit booleans for:

- `execution`;
- `external_action`;
- `promotion`.

No verdict/disposition has an implicit authority mapping.

### Counter-DA
Why not infer safe defaults by artifact type?

Because the same artifact type can exist in advisory, dry-run, production, or human-authorized contexts. Explicit false is safer and reconstructable.

### Survivor
Keep explicit authority vector.

---

## Attack 7 — premature owner assignment

### Attack
The first mapping could accidentally canonize current convenience repos as permanent architecture: e.g. Connector Hub as all ingress, Talent Registry as permanent promotion authority.

### Verdict
`PARTIAL FAIL`

### Repair
Treat these as initial candidate owners where necessity has not yet been destructively proven. The contract owns semantics; repository ownership remains replaceable.

### Survivor
- `right-arm`: current personal operating-layer owner is explicit in its own repository.
- `Ultimate-Loop`: canonical method owner is explicit in its own repository.
- `RTS-Evolution`: canonical reconstruction owner is explicit in its own repository.
- other owner assignments remain bounded/candidate unless independently established.

---

## Counter-DA summary

The smallest survivor is:

```text
Independent repos
+ local schemas
+ one tiny boundary envelope
+ separated evidence / verdict / promotion / authority
+ exact identity where material
+ optional direct routing
+ no central runtime
+ no automatic Canon
```

Rejected:

```text
one giant RTS repo
old FREEZER wholesale revival
Obsidian -> Canon shortcut
ambient event bus
PASS -> authority
PR/branch existence -> current implementation authority
```

## Current verdict

`SURVIVOR / DRAFT / READY FOR FIRST VERTICAL-SLICE DOGFOOD`

This is not merge approval. The next test is to adapt one real path and see whether the contract reduces ambiguity without adding ceremony.

Recommended first slice:

```text
right-arm
-> connector/worker
-> result/evidence
-> gate
-> trace
-> bounded approval
```

If this vertical slice needs large glue or duplicates local models, shrink or abolish the contract before wider rollout.
