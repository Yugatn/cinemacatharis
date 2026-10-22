"""Read local video metadata with ffprobe; never execute shell commands."""
import json
import shutil
import subprocess
from pathlib import Path

def probe_video(path: str, timeout: int = 20) -> dict:
    file = Path(path).expanduser().resolve(strict=True)
    if not file.is_file():
        raise ValueError("Not a file")
    if not shutil.which("ffprobe"):
        raise RuntimeError("FFmpeg ffprobe is required for media metadata")
    process = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration,size,format_name:stream=index,codec_type,codec_name,width,height,r_frame_rate",
         "-of", "json", str(file)],
        capture_output=True, text=True, timeout=timeout, check=False)
    if process.returncode:
        raise ValueError("Cannot probe media: " + process.stderr[:300])
    payload = json.loads(process.stdout)
    streams = payload.get("streams", [])
    if not any(s.get("codec_type") == "video" for s in streams):
        raise ValueError("File contains no video stream")
    fmt = payload.get("format", {})
    return {"filename": file.name, "duration_seconds": float(fmt.get("duration", 0)),
            "size_bytes": int(fmt.get("size", file.stat().st_size)),
            "streams": streams,
            "note": "Metadata only; no automatic semantic classification."}
