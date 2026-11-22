"""Collect documents exported with ArtifactData (out_dir) into data/<collection>.json.
Usage: python3 export_db.py EXPORT_DIR [DATA_DIR]   (EXPORT_DIR holds games/, insights/, parts/ with <doc_id>.json)"""
import json, os, sys
src = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
os.makedirs(out, exist_ok=True)
for col in ("games", "insights", "parts"):
    d = os.path.join(src, col)
    docs = {}
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.endswith(".json"):
                docs[f[:-5]] = json.load(open(os.path.join(d, f), encoding="utf-8"))
    json.dump(docs, open(os.path.join(out, col + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(col, len(docs))
