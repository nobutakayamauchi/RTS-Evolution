from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "contracts" / "interop-envelope-v1.schema.json").read_text(encoding="utf-8"))
PROSE = (ROOT / "contracts" / "INTEROP_CONTRACT_V1.md").read_text(encoding="utf-8")


def rule_for(artifact_type: str) -> dict:
    for rule in SCHEMA["allOf"]:
        const = rule.get("if", {}).get("properties", {}).get("artifact_type", {}).get("const")
        if const == artifact_type:
            return rule["then"]
    raise AssertionError(f"missing rule for {artifact_type}")


def main() -> None:
    assert SCHEMA["properties"]["contract_version"]["const"] == "rts-interop/v1"
    assert "non-authorizing" in SCHEMA["$comment"]

    authority = SCHEMA["properties"]["authority"]["properties"]
    assert all(authority[key]["const"] is False for key in ("execution", "external_action", "promotion"))
    assert SCHEMA["properties"]["authorization_refs"]["maxItems"] == 0

    unit = rule_for("UNIT")["properties"]
    assert unit["intended_consumers"]["minItems"] == 1
    assert {"unit_id", "target_identity"} <= set(unit["subject"]["required"])
    assert {
        "issuance_id", "outcome", "completion_conditions", "scope", "consequence_class",
        "source_identity", "task", "target_sha256",
    } <= set(unit["payload"]["required"])

    approval = rule_for("APPROVAL")["properties"]
    assert approval["evidence_refs"]["minItems"] == 1
    assert {"decision", "approved_by_asserted", "approval_ref"} <= set(approval["payload"]["required"])

    promotion = rule_for("PROMOTION_DECISION")["properties"]
    assert promotion["evidence_refs"]["minItems"] == 1
    assert {"decided_by_asserted", "decision_ref"} <= set(promotion["payload"]["required"])

    learning = rule_for("LEARNING_CANDIDATE")["properties"]["payload"]["required"]
    assert {
        "claim", "original_outcome", "completion_conditions", "supporting_evidence_refs",
        "counter_evidence_refs", "applicability", "counterconditions", "unresolved",
        "defect_history_refs", "source_trace_refs",
    } <= set(learning)

    freeze = rule_for("FREEZE_RECORD")["properties"]["payload"]["required"]
    assert {
        "claim", "promotion_decision_ref", "provenance_refs", "applicability",
        "counterconditions", "authority_scope", "reassessment_conditions",
    } <= set(freeze)

    for phrase in (
        "RTS-INTEROP/V1 DOES NOT CARRY AUTHORITY",
        "UNIT EXISTS != EXECUTION AUTHORITY",
        "RESULT FINAL != SUPPORTED EVIDENCE",
        "No trusted runtime boundary => BLOCKED",
        "APPROVE != EXECUTION AUTHORITY",
        "PROMOTE != PROMOTION AUTHORITY",
        "content-addressed ref string exists -> payload reconstructable",
    ):
        assert phrase in PROSE, f"missing invariant: {phrase}"


if __name__ == "__main__":
    main()
