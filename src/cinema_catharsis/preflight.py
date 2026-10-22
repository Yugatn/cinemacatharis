"""Local creator workflow: inspect video metadata and evaluate supplied annotations."""
import argparse
import json
from pathlib import Path
from .media import probe_video
from .policy import analyze_document

def main():
    parser = argparse.ArgumentParser(description="Local media preflight with explainable policy")
    parser.add_argument("video")
    parser.add_argument("--annotations", help="Optional JSON annotations from a reviewer/detector")
    args = parser.parse_args()
    media = probe_video(args.video)
    if args.annotations:
        document = json.loads(Path(args.annotations).read_text(encoding="utf-8"))
        result = analyze_document(document)
    else:
        result = {"monetization": "not_assessed", "publication": "not_assessed",
                  "explanation": "No annotations supplied; no content classification was performed."}
    print(json.dumps({"media": media, "assessment": result}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
