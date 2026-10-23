"""Explicit user review of acoustic candidate identities.

A review decision is stored separately from similarity rankings.
"""
from datetime import datetime, timezone

SCHEMA="acoustic-reviews-1.0"
DECISIONS=frozenset({"confirmed","rejected","uncertain"})

def new_reviews():
    return {"schema_version":SCHEMA,"decisions":[]}

def review_candidate(store, *, work_id, report_ref, decision, reviewer="local_user", note=""):
    if not isinstance(store,dict) or store.get("schema_version")!=SCHEMA or not isinstance(store.get("decisions"),list):
        raise ValueError("Invalid review store")
    if decision not in DECISIONS:
        raise ValueError("Invalid decision")
    for value in (work_id,report_ref,reviewer,note):
        if not isinstance(value,str) or len(value)>1024:
            raise ValueError("Invalid review field")
    if not work_id.strip() or not report_ref.strip() or not reviewer.strip():
        raise ValueError("Missing review identifier")
    item={"work_id":work_id,"report_ref":report_ref,"decision":decision,
          "reviewer":reviewer,"note":note,
          "reviewed_at":datetime.now(timezone.utc).isoformat(),
          "source":"human_review_not_automatic_detection"}
    store["decisions"].append(item)
    return item

def latest_review(store,work_id,report_ref):
    if not isinstance(store,dict) or store.get("schema_version")!=SCHEMA or not isinstance(store.get("decisions"),list):
        raise ValueError("Invalid review store")
    for item in reversed(store["decisions"]):
        if item.get("work_id")==work_id and item.get("report_ref")==report_ref:
            return item
    return None
