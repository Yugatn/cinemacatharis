"""Optional local Chromaprint fingerprint extraction via installed fpcalc executable.

This provides acoustic fingerprints, NOT validated robust matching.
No audio is sent to any external service.
"""
import json
import shutil
import subprocess
from pathlib import Path

def acoustic_fingerprint(path, *, executable="fpcalc", timeout=60):
    source=Path(path).resolve(strict=True)
    if not source.is_file():
        raise ValueError("Audio source must be a file")
    if not shutil.which(executable):
        raise RuntimeError("fpcalc (Chromaprint) is not installed")
    try:
        process=subprocess.run(
            [executable,"-json",str(source)],capture_output=True,text=True,
            timeout=timeout,check=False
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("Acoustic fingerprint timed out") from exc
    if process.returncode:
        raise RuntimeError("fpcalc failed: verify supported media format")
    try:
        data=json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid fpcalc output") from exc
    fingerprint=data.get("fingerprint")
    duration=data.get("duration")
    if not isinstance(fingerprint,str) or not fingerprint or len(fingerprint)>1000000:
        raise ValueError("Invalid Chromaprint fingerprint")
    if type(duration) not in (int,float) or not 0<=duration<=86400:
        raise ValueError("Invalid audio duration")
    return {"schema_version":"acoustic-fingerprint-1.0",
            "algorithm":"chromaprint-fpcalc",
            "fingerprint":fingerprint,"duration_seconds":duration,
            "match_verified":False,
            "limitations":["No robust similarity threshold or offset matching has been validated",
                           "Fingerprint identifies signal similarity, not content safety"]}

def exact_acoustic_match(left,right):
    """Strict equality baseline; not tolerant of offsets or transcoding."""
    if any(not isinstance(x,dict) or x.get("algorithm")!="chromaprint-fpcalc" for x in (left,right)):
        raise ValueError("Expected Chromaprint records")
    return (left.get("fingerprint")==right.get("fingerprint") and
            bool(left.get("fingerprint")) and
            left.get("duration_seconds")==right.get("duration_seconds"))
