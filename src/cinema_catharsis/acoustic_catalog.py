"""Local acoustic candidate retrieval with explicit human-review status."""
from .acoustic_compare import compare_raw

SCHEMA="acoustic-catalog-1.0"

def new_catalog():
    return {"schema_version":SCHEMA,"items":[]}

def add_record(catalog, *, work_id, report_ref, fingerprint):
    if not isinstance(catalog,dict) or catalog.get("schema_version")!=SCHEMA or not isinstance(catalog.get("items"),list):
        raise ValueError("Invalid catalog")
    if any(not isinstance(v,str) or not v.strip() or len(v)>1024 for v in (work_id,report_ref)):
        raise ValueError("Invalid work identifier or report reference")
    compare_raw(fingerprint,fingerprint,min_overlap=1,max_shift=0)
    if any(x["work_id"]==work_id for x in catalog["items"]):
        raise ValueError("Duplicate work identifier")
    catalog["items"].append({"work_id":work_id,"report_ref":report_ref,"fingerprint":fingerprint})
    return catalog

def find_candidates(query,catalog, *, limit=5,min_overlap=16,max_shift=500):
    if not isinstance(catalog,dict) or catalog.get("schema_version")!=SCHEMA or not isinstance(catalog.get("items"),list):
        raise ValueError("Invalid catalog")
    if type(limit) is not int or not 1<=limit<=100:
        raise ValueError("Invalid limit")
    results=[]
    for entry in catalog["items"]:
        result=compare_raw(query,entry["fingerprint"],min_overlap=min_overlap,max_shift=max_shift)
        if result["shift_frames"] is None:
            continue
        results.append({
            "work_id":entry["work_id"],"report_ref":entry["report_ref"],
            "score":result["score"],"shift_frames":result["shift_frames"],
            "overlap_frames":result["overlap_frames"],"verified":False,
            "status":"candidate_requires_review",
        })
    results.sort(key=lambda item:(-item["score"],-item["overlap_frames"],item["work_id"]))
    return {"schema_version":"acoustic-candidates-1.0","candidates":results[:limit],
            "limitations":["Ranking is uncalibrated and may include false matches",
                           "A report reference is not a content safety verdict",
                           "No audio is uploaded by this function"]}
