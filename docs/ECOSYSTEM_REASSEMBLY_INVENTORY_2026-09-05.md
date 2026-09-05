# Ecosystem Reassembly Inventory — 2026-09-05

## Purpose

This inventory is the current migration/reassembly map for the 45 repositories owned by `nobutakayamauchi`.

The goal is not to merge everything into one repository. The goal is to identify:

- which responsibility is still justified;
- where the current canonical implementation actually lives;
- whether useful work is on `main`, an open PR, or a floating branch;
- what must be connected through a common inter-repository contract;
- what should remain historical, experimental, or isolated.

`CODE EXISTS != CURRENT AUTHORITY`

`BRANCH EXISTS != INTEGRATED`

`PR GREEN != PROMOTED`

`HISTORICAL RTS != DEFAULT CURRENT ARCHITECTURE`

## Current canonical split

There is no single repository that should absorb the entire system.

- `RTS-Evolution` — canonical reconstruction of surviving RTS responsibilities.
- `Ultimate-Loop` — canonical development method and destructive evaluation sequence.
- `right-arm` — personal operating/decision layer.
- product/runtime repositories — own their bounded product or execution responsibility.
- old `RTS` — historical implementation/evidence by default; use only when explicitly required, except material that is still explicitly canonical there.

The integration target is therefore a **shared edge contract**, not a monolith.

## Status vocabulary

- `CANONICAL` — current source of truth for its responsibility.
- `ACTIVE` — current implementation/product surface worth connecting.
- `SPECIALIST` — bounded capability that should remain replaceable.
- `PR_HEAVY` — meaningful implementation exists mainly outside `main`; resolve before rebuilding.
- `EXPERIMENT` — evidence-generating or destructive-test surface; do not wire as production authority.
- `HISTORICAL` — preserve for lineage/evidence; do not treat as default architecture.
- `SHELL` — little or no implementation on `main`; decide merge/archive/rebuild from survivor evidence.

## Repository inventory

| # | Repository | Current role | State | Reassembly action |
|---|---|---|---|---|
| 1 | RTS | original RTS / historical evidence / selected legacy canonical material | HISTORICAL | Do not use as default hub. Salvage only surviving responsibilities or targeted canonical material with provenance. |
| 2 | nobutakayamauchi | public ecosystem/profile index | ACTIVE | Keep as outward map; consume canonical status, never define runtime truth. |
| 3 | rts01-offer | offer/legal/intake surface | ACTIVE | Connect to product/payment evidence only through bounded public-safe contracts. |
| 4 | rts-video-flow | video generation/render workflow | SPECIALIST | Adopt shared UNIT/RESULT/EVIDENCE/GATE edge contract. |
| 5 | rts-dev-protocol | development kernel/protocol candidate | PR_HEAVY | Resolve current kernel PRs against Ultimate Loop + RTS Evolution before promotion. |
| 6 | codex-connector-test | disposable connector/kernel harness | EXPERIMENT | Keep isolated; export evidence only, never production authority. |
| 7 | ryoushuushotesutoyou | narrow receipt-test surface | SHELL | Review for archival/merge; do not wire by default. |
| 8 | seminar-compass | seminar/research application | ACTIVE | Keep product-local logic; adopt shared evidence/result envelope only where useful. |
| 9 | RTS-Skills- | public reusable skill definitions | SPECIALIST | Keep skills replaceable; emit execution/verification evidence, not promotion authority. |
| 10 | RTS-MCP-Packs | declarative capability packs | SPECIALIST | Define pack inputs/outputs using common artifact types. |
| 11 | RTS-Hermes-Drive | multi-skill workflow manifests | SPECIALIST | Use as graph/workflow description; do not duplicate runtime authority. |
| 12 | AIX | research/legacy domain experiments | EXPERIMENT | Preserve research; connect only explicit surviving outputs. |
| 13 | RTS-AGE | replaceable execution/runtime engine | ACTIVE | Adopt Security→Cost→Approval + common execution/result/trace contracts. |
| 14 | RTS-Talent-Registry | promotion/registry boundary | SPECIALIST | Candidate owner for PROMOTION_DECISION records; no self-promotion. |
| 15 | RTS-Signal-Feeds | evidence/source intake | SPECIALIST | Produce bounded EVIDENCE with provenance and UNKNOWN/CONFLICT preservation. |
| 16 | RTS-Design-Research | design/provenance decision research | SPECIALIST | Provide evidence/provenance contracts; no runtime authority. |
| 17 | rts-lite | minimal shell | SHELL | Compare against current restart/minimal-runtime responsibilities; merge/archive if redundant. |
| 18 | RTS-Minimal-Runtime | reconstructable minimal execution proof | SPECIALIST | Keep as minimal reference implementation for RESULT/TRACE identity. |
| 19 | RTS-minicompany | dogfood mini-company/runtime | ACTIVE | Keep product-local; adopt interop envelope at external responsibility boundaries. |
| 20 | RS-AI-limit-development | debug/dogfood/episode laboratory | ACTIVE | Export validated episode evidence; do not promote experiments automatically. |
| 21 | WITNESS | destructive semantic necessity experiments | EXPERIMENT | Preserve surviving principles; do not require standalone WITNESS runtime as a dependency. |
| 22 | TRACE | observation/execution trace specialist | SPECIALIST | Candidate producer of TRACE artifacts; must remain evidence, not governance. |
| 23 | limit-development | public foundry/site/product dogfood | ACTIVE | Connect request/research/product evidence through public-safe contracts. |
| 24 | RTS-Evolution | current RTS responsibility reconstruction | CANONICAL | Own responsibility map + inter-repo contract + survivor migration decisions. |
| 25 | Ultimate-Loop | canonical development method | CANONICAL | Apply destructive evaluation to material integrations; no extra permanent loop. |
| 26 | WebAI-Bridge | public/runtime WebAI product | ACTIVE | Adopt common identity/evidence/approval/result edges at external integrations. |
| 27 | NAGI | experimental planner/learning runtime | EXPERIMENT | Keep isolated until necessity/overlap against current components survives review. |
| 28 | WebAI-Bridge-Core | private canonical WebAI core | ACTIVE | Preserve public/private boundary; use shared contract without leaking private payloads. |
| 29 | RTS-Skills-Core | private skill overlay | SPECIALIST | Preserve export boundary/upstream lock; consume/produce only public-safe envelopes across repos. |
| 30 | FGE | former foundry/growth shell | SHELL | Current implementation appears elsewhere; compare with `limit-development` and retire duplicate shell if no survivor remains. |
| 31 | Sales-Distribution-Network | sales/affiliate distribution runtime | PR_HEAVY | Resolve V1 Reality Gate PR before treating branch implementation as canonical. |
| 32 | sales-catalog | public sales/catalog surface | ACTIVE | Consume product/promotion/payment state; never invent runtime success. |
| 33 | Developer-Card | public developer diagnosis/card product | PR_HEAVY | Resolve iPhone Reality Gate before promotion; then adopt shared evidence/result contract. |
| 34 | Developer-Card-Core | private evaluator/core boundary | PR_HEAVY | Resolve private-core foundation; preserve double-gate/evidence boundary. |
| 35 | Audience-Miner | audience discovery/ranking worker | ACTIVE | Treat as specialist worker; produce evidence-backed ranked RESULT, not outreach authority. |
| 36 | LLM-Cost-Router | public product/evidence surface | PR_HEAVY | Resolve public release/evidence contract before promotion. |
| 37 | LLM-Cost-Router-Core | private routing core/research | PR_HEAVY | Resolve foundation + Evidence Stop Rule branches; do not rebuild from shell main. |
| 38 | x-ads-bridge | ad/bridge execution surface | ACTIVE | Keep consequence/human gates; adopt common execution/result/evidence edges. |
| 39 | rakuten-sidehustle-operator | Rakuten ROOM operator product | PR_HEAVY | Complete real-phone/API Reality Gate on existing PR; do not duplicate implementation. |
| 40 | render-worker | rendering/graph worker | ACTIVE | Strong worker candidate; adopt UNIT/RESULT/GATE/TRACE contract. |
| 41 | right-arm | personal operating/decision layer | CANONICAL | Primary intent/unit orchestration consumer/producer; keep Human Gate boundaries explicit. |
| 42 | invoice-payment-ops | invoice/payment operations product | PR_HEAVY | Existing PR contains runnable implementation; finish provider/reality boundaries before promotion. |
| 43 | connector-hub | connector/permission/credential adapter hub | ACTIVE | Use as replaceable connector boundary; strong candidate for Obsidian/manual-ingress adapter plumbing. |
| 44 | proof-ops | evidence/proof packaging specialist | SPECIALIST | Produce bounded EVIDENCE/GATE inputs; do not become a second orchestrator. |
| 45 | ai-domain-baken-private | private domain/research product lab | ACTIVE | Keep domain logic local; adopt shared contract only at evidence/result/promotion edges. |

## Cross-cutting incomplete work already confirmed

### 1. Old RTS Knowledge Bridge is implemented but stranded

`feature/obsidian-freezer-knowledge-bridge-v1` and `v1.2` contain substantial implementation and tests but diverged heavily from current old-RTS `main`.

Do **not** merge those branches wholesale.

Salvage by responsibility:

- capture / normalize / sensitivity / routing semantics;
- Obsidian/manual note adapter behavior;
- challenge/candidate-compare logic where it still survives current principles;
- FREEZER export semantics;
- deployment-identity fix from v1.2;
- tests that encode still-valid failure conditions.

Port only surviving pieces into current owners.

### 2. Many products are PR-heavy

Several repositories have only AGENTS/README on `main` while substantial implementation lives in Draft/Open PRs. These are not empty products and must not be rebuilt from scratch.

Priority examples:

- `invoice-payment-ops` PR #1;
- `rakuten-sidehustle-operator` PR #1;
- `Sales-Distribution-Network` PR #1;
- `Developer-Card` PR #2;
- `Developer-Card-Core` PR #2;
- `LLM-Cost-Router` PR #1;
- `LLM-Cost-Router-Core` PR #1/#2;
- `right-arm` PR #8 and older pack PR #1.

Each must be classified as one of:

- promote after required evidence;
- rebase/repair;
- superseded by `main`;
- preserve as experiment;
- close as stale.

### 3. Old RTS has a large open-PR tail

Old RTS still has many open stacked/experimental PRs even though the repository is moving to COLD/FROZEN historical status.

They must not be interpreted as current architecture simply because they are open or green.

### 4. WITNESS has many intentionally unmerged experiments

WITNESS PRs are evidence-generating ablations/necessity tests. Their open state is not a backlog to merge into production.

The survivor is primarily semantic responsibility, not a requirement for a permanent WITNESS software service.

## First integration spine

Use this as the first end-to-end reassembly path:

```text
Human Intent / Capture
        ↓
RIGHT ARM
        ↓
UNIT
        ↓
Connector / Specialist / Product Worker
        ↓
RESULT + EVIDENCE
        ↓
Deterministic/Product Gate
        ↓
TRACE
        ↓
Ultimate Loop destructive evaluation when material
        ↓
Human Gate when consequence requires it
        ↓
External action / bounded completion
        ↓
LEARNING_CANDIDATE
        ↓
separated review / counter-evidence
        ↓
PROMOTION_DECISION
        ↓
FREEZE_RECORD / reusable invariant
```

## Obsidian / FREEZER reassembly target

FREEZER should survive as a **governed knowledge state**, not as a dependency on the old RTS implementation.

Target flow:

```text
Obsidian / manual capture
  -> PROPOSAL_ONLY
  -> normalize + sensitivity gate
  -> EVIDENCE / candidate
  -> separated challenge / counter-evidence
  -> LEARNING_CANDIDATE
  -> PROMOTION_DECISION
  -> FREEZE_RECORD
```

Raw notes must never become canonical merely because they were captured.

## Immediate execution order

1. Freeze this inventory as the review baseline.
2. Define the shared interop envelope and artifact types.
3. Reconstruct the Obsidian/FREEZER bridge by salvaging only surviving old-branch pieces.
4. Wire the first live path: `right-arm -> connector-hub/worker -> proof/trace -> approval`.
5. Wire learning/promotion/freeze after the execution path is observable.
6. Resolve PR-heavy products one by one without rebuilding existing work.
7. Review SHELL/HISTORICAL repositories for archive/merge only after successor ownership is explicit.

## Promotion boundary

This inventory authorizes no merge, deployment, publication, payment, external message, repository deletion, or destructive migration.

It is a reassembly map for review and implementation sequencing.
