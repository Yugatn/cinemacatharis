"""Experimental offset-aware comparison of raw Chromaprint integer sequences.

The score is a bit-agreement heuristic, NOT calibrated match probability.
"""
import json
import subprocess
from pathlib import Path

def raw_fingerprint(path, *, executable="fpcalc", timeout=60):
    source=Path(path).resolve(strict=True)
    result=subprocess.run([executable,"-raw","-json",str(source)],
                          capture_output=True,text=True,timeout=timeout,check=False)
    if result.returncode:
        raise RuntimeError("fpcalc raw fingerprint failed")
    try:
        payload=json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid fpcalc JSON") from exc
    values=payload.get("fingerprint")
    if not isinstance(values,list) or not 1<=len(values)<=100000 or any(
        type(v) is not int or not -(2**31)<=v<2**32 for v in values
    ):
        raise ValueError("Invalid raw Chromaprint sequence")
    return {"schema_version":"acoustic-raw-1.0","algorithm":"chromaprint-raw",
            "values":[v & 0xffffffff for v in values],
            "duration_seconds":payload.get("duration"),
            "match_verified":False}

def compare_raw(a,b, *, min_overlap=16, max_shift=500):
    """Search integer-frame offsets and return best normalized bit agreement.

    Complexity O(max_shift * shorter_length); input length and shift capped.
    """
    if not 1<=min_overlap<=100000 or not 0<=max_shift<=5000:
        raise ValueError("Invalid comparison parameters")
    def sequence(obj):
        if not isinstance(obj,dict) or obj.get("schema_version")!="acoustic-raw-1.0":
            raise ValueError("Expected acoustic-raw-1.0")
        vals=obj.get("values")
        if not isinstance(vals,list) or len(vals)>100000 or any(
            type(v) is not int or not 0<=v<2**32 for v in vals
        ):
            raise ValueError("Invalid fingerprint sequence")
        return vals
    left,right=sequence(a),sequence(b)
    best={"score":0.0,"shift_frames":None,"overlap_frames":0,
          "verified":False,"interpretation":"uncalibrated_bit_agreement_not_identity"}
    for shift in range(-min(max_shift,len(right)),min(max_shift,len(left))+1):
        first=max(0,shift)
        second=max(0,-shift)
        overlap=min(len(left)-first,len(right)-second)
        if overlap<min_overlap:
            continue
        same=sum(32-(left[first+i]^right[second+i]).bit_count() for i in range(overlap))
        score=same/(32*overlap)
        if score>best["score"] or (score==best["score"] and overlap>best["overlap_frames"]):
            best.update(score=score,shift_frames=shift,overlap_frames=overlap)
    return best
