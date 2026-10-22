"""Decode a local source video at known media timestamps using ffmpeg.

This is sample extraction, not continuous coverage or content recognition.
"""
import json
import subprocess
from pathlib import Path

def sample_source_video(source, output_dir, *, every_seconds=5, max_frames=1000, timeout=180):
    if isinstance(every_seconds,bool) or not isinstance(every_seconds,(int,float)) or not 0.1 <= every_seconds <= 3600:
        raise ValueError("Invalid sampling interval")
    if type(max_frames) is not int or not 1 <= max_frames <= 10000:
        raise ValueError("Invalid frame limit")
    source=Path(source).resolve(strict=True)
    if not source.is_file():
        raise ValueError("Expected video file")
    directory=Path(output_dir)
    directory.mkdir(parents=True,exist_ok=True)
    # FFmpeg seeks each frame by source-media timestamp, never by accelerated playback clock.
    from .media import probe_video
    metadata=probe_video(str(source))
    duration=metadata.get("duration_seconds")
    if not isinstance(duration,(int,float)) or duration <= 0:
        raise ValueError("Video duration unavailable")
    frames=[]
    index=0
    while index < max_frames:
        timestamp=index*every_seconds
        if timestamp >= duration:
            break
        name=f"frame_{index:05d}.jpg"
        output=directory/name
        result=subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-nostdin",
                               "-ss",str(timestamp),"-i",str(source),"-frames:v","1",
                               "-y",str(output)],capture_output=True,text=True,timeout=timeout,
                              check=False)
        if result.returncode != 0 or not output.is_file() or not output.stat().st_size:
            raise RuntimeError(f"ffmpeg failed at {timestamp}s: {result.stderr[:300]}")
        frames.append({"file":name,"source_ms":round(timestamp*1000)})
        index+=1
    manifest={"schema_version":"source-samples-1.0","source":source.name,
              "duration_ms":round(duration*1000),"sampling_interval_ms":round(every_seconds*1000),
              "frames":frames,"coverage_kind":"discrete_samples_not_continuous",
              "content_classification":"not_assessed"}
    path=directory/"source_manifest.json"
    path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding="utf-8")
    return manifest
