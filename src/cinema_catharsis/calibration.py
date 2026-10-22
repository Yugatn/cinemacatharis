"""Evaluate detector confidence against independently verified ground truth."""
from math import isfinite, sqrt

def calibration_report(observations, bins=10, threshold=0.5):
    """Binary calibration diagnostics; scores must be calibrated on held-out data."""
    if type(bins) is not int or bins < 2 or bins > 100:
        raise ValueError("bins must be integer in [2,100]")
    if isinstance(threshold, bool) or not isinstance(threshold,(int,float)) or not isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("Invalid threshold")
    rows = []
    for item in observations:
        if not isinstance(item,dict) or type(item.get("truth")) is not bool:
            raise ValueError("Each observation needs verified boolean truth")
        score = item.get("score")
        if isinstance(score,bool) or not isinstance(score,(int,float)) or not isfinite(score) or not 0 <= score <= 1:
            raise ValueError("Score must be finite within [0,1]")
        rows.append((float(score),item["truth"]))
    if not rows:
        return {"count":0,"status":"insufficient_data","precision":None,"recall":None,"f1":None,
                "brier":None,"ece":None,"bins":[]}
    tp=sum(score>=threshold and truth for score,truth in rows)
    fp=sum(score>=threshold and not truth for score,truth in rows)
    fn=sum(score<threshold and truth for score,truth in rows)
    precision=tp/(tp+fp) if tp+fp else None
    recall=tp/(tp+fn) if tp+fn else None
    f1=2*precision*recall/(precision+recall) if precision is not None and recall is not None and precision+recall else None
    brier=sum((score-int(truth))**2 for score,truth in rows)/len(rows)
    buckets=[[] for _ in range(bins)]
    for score,truth in rows:
        buckets[min(int(score*bins),bins-1)].append((score,truth))
    details=[]
    ece=0.0
    for i,group in enumerate(buckets):
        if not group:
            continue
        confidence=sum(s for s,_ in group)/len(group)
        accuracy=sum(t for _,t in group)/len(group)
        ece+=len(group)/len(rows)*abs(confidence-accuracy)
        details.append({"range":[i/bins,(i+1)/bins],"count":len(group),
                        "mean_score":confidence,"empirical_frequency":accuracy})
    return {"count":len(rows),"status":"descriptive_not_validated","threshold":threshold,
            "tp":tp,"fp":fp,"fn":fn,"precision":precision,"recall":recall,"f1":f1,
            "brier":brier,"ece":ece,"bins":details,
            "note":"Use an independent representative labeled dataset; frames from the same film are correlated."}
