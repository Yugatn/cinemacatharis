/* Browser-side evidence-1.0 conversion. Pure local data transformation. */
export function lexicalToEvidence(report,source="provided_text") {
  if(!report || report.schema_version!=="lexical-composition-1.1") throw new Error("Unsupported lexical report");
  const observations=[];
  for(const [category,data] of Object.entries(report.categories||{})) {
    for(const hit of data.examples||[]) {
      if(!Number.isSafeInteger(hit.start)||!Number.isSafeInteger(hit.end)||hit.start<0||hit.end<=hit.start) continue;
      observations.push({
        category,channel:"text",timing_basis:"text_offsets",
        start:hit.start,end:hit.end,confidence:null,confidence_calibrated:false,
        verified:false,method:"lexical_dictionary",
        evidence:String(hit.excerpt||hit.term||"").slice(0,500),
        interpretation:"observed_candidate_not_intent_or_harm"
      });
    }
  }
  return {
    schema_version:"evidence-1.0",source,coverage:"partial",
    observations,observation_count:observations.length,
    content_safe:null,promotion_detected:null,
    limitations:[
      "Detected presence does not establish endorsement, promotion or harm",
      "No observations is not proof of absence",
      "Confidence scores are not probabilities unless calibrated",
      "Only the first ten lexical matches per category are included"
    ]
  };
}
