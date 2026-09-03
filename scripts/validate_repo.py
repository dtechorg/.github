from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / ".dte-validation"
REPORT_DIR.mkdir(exist_ok=True)
failures: list[str] = []
checks: list[dict[str, object]] = []


def check(name: str, condition: bool, detail: str) -> None:
    checks.append({"name": name, "passed": bool(condition), "detail": detail})
    if not condition:
        failures.append(f"{name}: {detail}")


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as error:
        failures.append(f"json:{path.relative_to(ROOT)}: {error}")
        return None


required = ["README.md", "LICENSE", "CODEOWNERS", "SECURITY.md", "CONTRIBUTING.md", "dte-subsystem.yaml"]
missing = [name for name in required if not (ROOT / name).is_file()]
check("repository-foundation", not missing, "missing: " + ", ".join(missing) if missing else "all required foundation files present")

subsystem_text = (ROOT / "dte-subsystem.yaml").read_text(encoding="utf-8") if (ROOT / "dte-subsystem.yaml").is_file() else ""
for key in ("schema:", "organization:", "repository:", "purpose:", "future_enterprise_org:", "contract_source:", "artifact_policy:", "source_import_policy:", "license_policy:"):
    check(f"subsystem-{key[:-1]}", key in subsystem_text, f"{key} must be declared")

manifest_paths = sorted(ROOT.glob("sources/*/*/SOURCE_MANIFEST.json"))
manifest_sources: set[str] = set()
for path in manifest_paths:
    value = load_json(path)
    if not isinstance(value, dict):
        continue
    rel_parent = path.parent.relative_to(ROOT).as_posix()
    required_manifest = {"schema", "source_repo", "source_url", "source_head", "import_mode", "destination_prefix", "license_status"}
    allowed_manifest = required_manifest | {"imported_head", "canonical_status", "license_gate", "source_digest", "provenance_notes"}
    check(f"manifest-required:{rel_parent}", required_manifest <= set(value), f"required keys: {sorted(required_manifest)}")
    check(f"manifest-extra:{rel_parent}", set(value) <= allowed_manifest, f"unexpected keys: {sorted(set(value) - allowed_manifest)}")
    check(f"manifest-schema:{rel_parent}", value.get("schema") == "https://schemas.deep-tree-echo.org/dte.source-manifest/v1", "schema URI must match v1")
    source_repo = value.get("source_repo")
    check(f"manifest-source:{rel_parent}", isinstance(source_repo, str) and re.fullmatch(r"[^/]+/[^/]+", source_repo) is not None, "source_repo must be owner/repo")
    if isinstance(source_repo, str):
        check(f"manifest-unique:{rel_parent}", source_repo not in manifest_sources, "source_repo must be unique within the destination repository")
        manifest_sources.add(source_repo)
    check(f"manifest-placement:{rel_parent}", value.get("destination_prefix") == rel_parent, "destination_prefix must equal manifest directory")
    source_head = value.get("source_head")
    check(f"manifest-head:{rel_parent}", source_head is None or (isinstance(source_head, str) and re.fullmatch(r"[0-9a-f]{40}", source_head) is not None), "source_head must be null or a 40-character SHA")
    source_digest = value.get("source_digest")
    check(f"manifest-digest:{rel_parent}", source_digest is None or (isinstance(source_digest, str) and re.fullmatch(r"sha256:[0-9a-f]{64}", source_digest) is not None), "source_digest must be null or sha256:<64 hex>")
    check(f"manifest-license:{rel_parent}", value.get("license_gate") in {"review_required", "preserve_and_verify", "cleared"}, "license_gate must use the registered enum")
    provenance_path = path.parent / "SOURCE_PROVENANCE.json"
    check(f"provenance-present:{rel_parent}", provenance_path.is_file(), "SOURCE_PROVENANCE.json must accompany every manifest")
    if provenance_path.is_file():
        provenance = load_json(provenance_path)
        if isinstance(provenance, dict):
            check(f"provenance-source:{rel_parent}", provenance.get("source", {}).get("repository") == source_repo, "provenance source must match flat manifest")
            check(f"provenance-destination:{rel_parent}", provenance.get("placement", {}).get("destination_prefix") == rel_parent, "provenance destination must match directory")

identity_graphs = sorted(list(ROOT.glob("identity/*identity-graph*.json")) + list(ROOT.glob("contracts/examples/*identity-graph*.json")))
for path in identity_graphs:
    value = load_json(path)
    if not isinstance(value, dict):
        continue
    nodes = value.get("nodes", [])
    relations = value.get("relations", [])
    node_ids = {node.get("id") for node in nodes if isinstance(node, dict)}
    relation_ids: set[str] = set()
    check(f"identity-version:{path.name}", value.get("version") == "1.0.0", "version must remain 1.0.0")
    check(f"identity-nodes:{path.name}", bool(nodes) and len(node_ids) == len(nodes), "node IDs must be present and unique")
    for relation in relations:
        rid = relation.get("id")
        check(f"identity-relation-id:{rid}", isinstance(rid, str) and rid not in relation_ids, "relation IDs must be unique")
        if isinstance(rid, str):
            relation_ids.add(rid)
        endpoints = [relation.get("source"), relation.get("target")]
        check(f"identity-relation-refs:{rid}", all(isinstance(item, str) and item in node_ids for item in endpoints), "source and target must resolve to identity nodes")
        check(f"identity-relation-evidence:{rid}", bool(relation.get("evidence_ids")) or relation.get("status") == "hypothesis", "non-hypothesis relations require evidence")

experiment_paths = sorted(ROOT.glob("experiments/exp-001-relation-balanced-curriculum.json"))
for path in experiment_paths:
    value = load_json(path)
    if not isinstance(value, dict):
        continue
    check("exp001-id", value.get("id") == "exp-001-relation-balanced-curriculum", "registered experiment ID must match")
    check("exp001-seeds", value.get("seeds") == [42, 31415], "matched seeds must remain [42, 31415]")
    fixed_variables = value.get("fixed_variables", [])
    check("exp001-fixed-steps", isinstance(fixed_variables, list) and "max-steps:60" in fixed_variables, "fixed variables must include max-steps:60")
    check("exp001-runtime", value.get("budget", {}).get("max_steps") == 60, "registered smoke-scale budget must remain 60 steps")

matrix_paths = sorted(ROOT.glob("experiments/exp-001/unsloth/exp001_unsloth_matrix.json"))
for path in matrix_paths:
    value = load_json(path)
    if isinstance(value, dict):
        runs = value.get("runs", [])
        signatures = {(run.get("arm"), run.get("seed")) for run in runs if isinstance(run, dict)}
        check("exp001-matrix", signatures == {("baseline", 42), ("baseline", 31415), ("relation_balanced", 42), ("relation_balanced", 31415)}, "four matched arm/seed runs are required")

report = {
    "schema": "https://schemas.deep-tree-echo.org/dte.repository-validation-report/v1",
    "repository": ROOT.name,
    "checks_total": len(checks),
    "checks_passed": sum(1 for item in checks if item["passed"]),
    "source_manifests": len(manifest_paths),
    "identity_graphs": len(identity_graphs),
    "failures": failures,
    "passed": not failures,
    "checks": checks,
}
(REPORT_DIR / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: report[key] for key in ("repository", "checks_total", "checks_passed", "source_manifests", "identity_graphs", "passed")}, indent=2))
if failures:
    raise SystemExit("\n".join(failures))
