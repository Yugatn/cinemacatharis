"""Optional local ML adapters; all outputs remain unverified."""
from pathlib import Path

LABELS = {
    "alcohol": "alcoholic beverage bottle or drinking",
    "tobacco": "tobacco cigarette or smoking",
    "nicotine": "electronic cigarette or vaping",
}

def inspect_frames(paths, model="openai/clip-vit-base-patch32", threshold=0.55):
    """Candidate visual observations; similarity is not proof of an object."""
    if not 0 <= threshold <= 1:
        raise ValueError("threshold outside [0,1]")
    try:
        from PIL import Image
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError("Install optional vision dependencies") from exc
    classifier = pipeline("zero-shot-image-classification", model=model)
    labels = list(LABELS.values()) + ["ordinary scene"]
    findings = []
    for index, filename in enumerate(paths):
        with Image.open(filename) as image:
            scores = classifier(image.convert("RGB"), candidate_labels=labels)
        for category, label in LABELS.items():
            score = next((float(p["score"]) for p in scores if p["label"] == label), 0)
            if score >= threshold:
                findings.append({
                    "category": category, "context": "unknown",
                    "start_ms": index * 1000, "end_ms": (index + 1) * 1000,
                    "confidence": score,
                    "evidence": "Unverified image similarity: " + label + " in " + Path(filename).name,
                    "channel": "visual", "commercial_signal": False, "verified": False
                })
    return findings

def transcribe_audio(path, model_size="small"):
    """Transcribe audio without inferring commercial or social intent."""
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError("Install optional speech dependencies") from exc
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(path, vad_filter=True)
    return {"language": info.language,
            "segments": [{"start_ms": round(s.start * 1000),
                          "end_ms": round(s.end * 1000), "text": s.text.strip()}
                         for s in segments],
            "note": "Unverified transcription, not an advertising assessment."}
