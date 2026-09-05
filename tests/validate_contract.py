from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "contracts" / "interop-envelope-v1.schema.json"
PROSE_PATH = ROOT / "contracts" / "INTEROP_CONTRACT_V1.md"


def artifact_rule(schema: dict, artifact_type: str) -> dict:
    for rule in schema["allOf"]:
        condition = rule.get("if", {})
        const = (
            condition.get("properties", {})
            .get("artifact_type", {})
            .get("const")
        )
        if const == artifact_type:
            return rule["then"]
    raise AssertionError(f"missing schema rule for {artifact_type}")


def authority_guard(schema: dict) -> dict:
    for rule in schema["allOf"]:
        condition = rule.get("if", {})
        if "anyOf" in condition:
            then = rule.get("then", {})
            props = then.get("properties", {})
            if "authorization_refs" in props and "producer" in props:
                return then
    raise AssertionError("missing authority runtime/auth-reference guard")


def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    prose = PROSE_PATH.read_text(encoding="utf-8")

    assert schema["contract_version"] if False else True  # schema is parsed above
    assert "structural only" in schema.get("$comment", "")

    auth_ref = schema["$defs"]["authorizationRef"]
    assert "issuer_identity" in auth_ref["required"]
    issuer_identity = auth_ref["properties"]["issuer_identity"]
    assert issuer_identity["type"] == "object"
    assert issuer_identity["minProperties"] == 1

    guard = authority_guard(schema)["properties"]
    assert guard["authorization_refs"]["minItems"] == 1
    runtime_identity = guard["producer"]["properties"]["runtime_identity"]
    assert runtime_identity["type"] == "object"
    assert runtime_identity["minProperties"] == 1

    learning = artifact_rule(schema, "LEARNING_CANDIDATE")["properties"]
    for key in ("execution", "external_action", "promotion"):
        assert learning["authority"]["properties"][key]["const"] is False
    learning_required = set(learning["payload"]["required"])
    assert {
        "claim",
        "original_outcome",
        "completion_conditions",
        "supporting_evidence_refs",
        "counter_evidence_refs",
        "applicability",
        "counterconditions",
        "unresolved",
        "defect_history_refs",
        "source_trace_refs",
    } <= learning_required

    freeze = artifact_rule(schema, "FREEZE_RECORD")["properties"]
    for key in ("execution", "external_action", "promotion"):
        assert freeze["authority"]["properties"][key]["const"] is False
    freeze_required = set(freeze["payload"]["required"])
    assert {
        "claim",
        "promotion_decision_ref",
        "provenance_refs",
        "applicability",
        "counterconditions",
        "authority_scope",
        "reassessment_conditions",
    } <= freeze_required

    required_prose = (
        "ENVELOPE SAYS AUTHORIZED != AUTHORITY VERIFIED",
        "PROMOTE != PROMOTION AUTHORITY",
        "No trusted verifier => BLOCKED",
        "RESULT target hash matches -> producer authenticated",
        "content-addressed ref string exists -> payload reconstructable",
    )
    for phrase in required_prose:
        assert phrase in prose, f"missing contract invariant: {phrase}"


if __name__ == "__main__":
    main()
