"""Analyze exported screen-capture frames and optional audio locally."""
import argparse
import json
from pathlib import Path
from .detectors import inspect_frames, transcribe_audio
from .policy import analyze_document

def scan_capture(manifest_path: str, *, vision: bool = False, audio_path: str | None = None,
                 threshold: float = 0.55) -> dict:
    path = Path(manifest_path).resolve(strict=True)
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != "capture-1.0":
        raise ValueError("Unsupported capture manifest version")
    frames = manifest.get("frames")
    if not isinstance(frames, list) or len(frames) > 2000:
        raise ValueError("Invalid capture frame list")
    images, times = [], []
    for item in frames:
        if not isinstance(item, dict) or not isinstance(item.get("file"), str):
            raise ValueError("Invalid frame")
        name = item["file"]
        # Manifest is untrusted: restrict to JPEG files in the manifest directory.
        if Path(name).name != name or not name.lower().endswith((".jpg", ".jpeg")):
            raise ValueError("Unsafe frame filename")
        timestamp = item.get("wall_ms")
        if type(timestamp) is not int or timestamp < 0:
            raise ValueError("Invalid wall clock timestamp")
        images.append(str(path.parent / name))
        times.append(timestamp)
    findings = inspect_frames(images, threshold=threshold) if vision and images else []
    for finding in findings:
        # Detector indexes correspond to capture sample indexes, not source media time.
        i = finding["start_ms"] // 1000
        finding["start_ms"] = times[i]
        finding["end_ms"] = times[i] + 1
    transcript = transcribe_audio(audio_path) if audio_path else None
    assessment = analyze_document({"schema_version": "1.0", "findings": findings})
    # Unverified detector output must never be treated as approval.
    assessment["monetization"] = "pending_review" if findings else "not_assessed"
    assessment["explanation"] = "Automated sample detections are unverified; full video coverage and commercial intent are not established."
    return {"schema_version": "scan-1.0", "source": "screen_capture",
            "timing_basis": "capture_wall_clock", "frames_examined": len(images) if vision else 0,
            "frames_available": len(images), "vision_enabled": vision,
            "transcript": transcript, "findings": findings, "assessment": assessment,
            "limitations": ["Sampled frames may miss brief scenes",
                            "No original media timeline or playback speed mapping",
                            "ASR may fail on accelerated or missing audio",
                            "No automated finding can establish promotional intent"]}

def main():
    parser = argparse.ArgumentParser(description="Local capture analysis with optional AI models")
    parser.add_argument("manifest")
    parser.add_argument("--vision", action="store_true", help="Enable local CLIP image analysis")
    parser.add_argument("--audio", help="Captured audio file for optional Whisper transcription")
    parser.add_argument("--threshold", type=float, default=0.55)
    parser.add_argument("--output", help="Save JSON report")
    parser.add_argument("--exports-dir", help="Also export XLSX, CSV and HTML reports")
    args = parser.parse_args()
    result = scan_capture(args.manifest, vision=args.vision,
                          audio_path=args.audio, threshold=args.threshold)
    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    if args.exports_dir:
        from .export import export_csv, export_html, export_xlsx
        directory = Path(args.exports_dir)
        export_xlsx(result, directory / "cinema_catharsis.xlsx")
        export_csv(result, directory)
        export_html(result, directory / "cinema_catharsis.html")

if __name__ == "__main__":
    main()
