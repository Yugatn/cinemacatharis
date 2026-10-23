"""Local media fingerprint indexing; exact digest is not a Shazam-like robust match."""
import hashlib
import json
from pathlib import Path

SCHEMA = "fingerprint-index-1.0"

def file_digest(path, chunk_size=1024 * 1024):
    """Exact-byte SHA-256 identifier, streamed to avoid large memory use."""
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while chunk := stream.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()

def identify_exact(path, index):
    """Return indexed report references only for identical bytes."""
    if not isinstance(index, dict) or index.get("schema_version") != SCHEMA:
        raise ValueError("Invalid fingerprint index")
    matches = index.get("entries", {})
    if not isinstance(matches, dict):
        raise ValueError("Invalid entries")
    return matches.get(file_digest(path), [])

def add_exact(path, report_ref, index=None):
    """Build an index without loading media or uploading any bytes."""
    if not isinstance(report_ref, str) or not report_ref.strip() or len(report_ref) > 1024:
        raise ValueError("Invalid report reference")
    if index is None:
        index = {"schema_version": SCHEMA, "entries": {}}
    if not isinstance(index, dict) or index.get("schema_version") != SCHEMA or not isinstance(index.get("entries"), dict):
        raise ValueError("Invalid fingerprint index")
    key = file_digest(path)
    existing = index["entries"].setdefault(key, [])
    if report_ref not in existing:
        existing.append(report_ref)
    return index

def save_index(index, path):
    target = Path(path)
    target.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
