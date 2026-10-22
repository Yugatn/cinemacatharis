import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import test from "node:test";
const load=async(path)=>{
 const src=await readFile(new URL(path,import.meta.url),"utf8");
 return import("data:text/javascript;base64,"+Buffer.from(src).toString("base64"));
};
const {analyzeText}=await load("../../web/composition-core.js");
const {lexicalToEvidence}=await load("../../web/evidence-core.js");
test("end-to-end browser lexical evidence",()=>{
 const input="Пиво — предмет исследования, а не реклама.";
 const result=lexicalToEvidence(analyzeText(input));
 assert.equal(result.schema_version,"evidence-1.0");
 assert.equal(result.content_safe,null);
 const item=result.observations.find(x=>x.category==="alcohol");
 assert.ok(item);
 assert.equal(input.slice(item.start,item.end),"Пиво");
 assert.equal(item.verified,false);
 assert.equal(item.timing_basis,"text_offsets");
});
test("reject unsupported format",()=>assert.throws(()=>lexicalToEvidence({schema_version:"scan-1.0"})));
test("no detections is not safe",()=>{
 const r=lexicalToEvidence(analyzeText("Обычная статья о погоде."));
 assert.equal(r.observation_count,0);
 assert.equal(r.content_safe,null);
});
