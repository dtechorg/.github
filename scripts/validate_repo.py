from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
required = ["README.md", "LICENSE", "CODEOWNERS", "SECURITY.md", "CONTRIBUTING.md", "dte-subsystem.yaml"]
missing = [name for name in required if not (ROOT / name).is_file()]
for manifest in ROOT.glob("sources/*/*/SourceManifest.json"):
    value = json.loads(manifest.read_text(encoding="utf-8"))
    if value.get("schema") != "https://schemas.deep-tree-echo.org/dte.source-manifest/v1":
        raise SystemExit(f"Invalid source manifest schema: {manifest}")
if missing:
    raise SystemExit("Missing required files: " + ", ".join(missing))
print(f"validated {ROOT.name}")
