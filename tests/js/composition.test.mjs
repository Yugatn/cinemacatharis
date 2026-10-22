import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import test from "node:test";
const src=await readFile(new URL("../../web/composition-core.js",import.meta.url),"utf8");
const {analyzeText}=await import("data:text/javascript;base64,"+Buffer.from(src).toString("base64"));
test("finds exact words without matching substrings",()=>{
  const r=analyzeText("Вино и виновник. Пиво и пивовар.");
  assert.equal(r.categories.alcohol.matches,2);
});
test("finds multiword expressions",()=>{
  const r=analyzeText("Это азартные игры. Купи сейчас!");
  assert.equal(r.categories.gambling.matches,1);
  assert.equal(r.categories.advertising.matches,1);
});
test("does not infer intent or harm",()=>{
  const r=analyzeText("Исследователь критикует рекламу алкоголя.");
  assert.equal(r.method,"dictionary_matches_only");
  assert.ok(r.not_assessed.includes("speaker_intent"));
});
test("rejects oversized input",()=>assert.throws(()=>analyzeText("x".repeat(200001))));
test("same engine in web and extension",async()=>{
  const ext=await readFile(new URL("../../extension/composition-core.js",import.meta.url),"utf8");
  assert.equal(src,ext);
});
