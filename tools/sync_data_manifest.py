#!/usr/bin/env python3
"""Refresh data-manifest.json from the Data-Sources release (for static hosting; the Node server also
refreshes it automatically every 6 hours). Standard library only.

    python3 tools/sync_data_manifest.py
"""
import json, urllib.request
from pathlib import Path

URL = "https://github.com/Open-Medical-Affairs/Data-Sources/releases/latest/download/manifest.json"
OUT = Path(__file__).resolve().parents[1] / "data-manifest.json"
req = urllib.request.Request(URL, headers={"User-Agent": "ai-in-action-website"})
m = json.loads(urllib.request.urlopen(req, timeout=60).read())
assert m.get("datasets"), "manifest has no datasets"
OUT.write_text(json.dumps(m, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"data-manifest.json: {len(m['datasets'])} datasets", json.dumps(m.get("counts", {})))
