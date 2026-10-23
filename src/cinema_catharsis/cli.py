"""Run: python -m cinema_catharsis.cli input.json [output.json]"""
import argparse
import json
from pathlib import Path
from .policy import analyze_document

def main():
    parser = argparse.ArgumentParser(description="Cinema Catharsis pre-upload annotation policy")
    parser.add_argument("input", help="JSON annotations")
    parser.add_argument("output", nargs="?", help="JSON result; stdout if omitted")
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = json.dumps(analyze_document(data), ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(result + "\n", encoding="utf-8")
    else:
        print(result)

if __name__ == "__main__":
    main()
