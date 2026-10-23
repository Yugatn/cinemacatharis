/* Deterministic local lexical evidence only, not semantic inference. */
export const LEXICON = Object.freeze({
  alcohol: ["алкоголь","спиртное","водка","пиво","вино","alcohol","beer","vodka","wine"],
  tobacco_nicotine: ["табак","курение","сигарета","вейп","никотин","tobacco","cigarette","vaping","nicotine"],
  violence: ["насилие","убийство","избиение","violence","murder","assault"],
  gambling: ["азартные игры","ставки","казино","gambling","casino","betting"],
  advertising: ["реклама","спонсор","купи сейчас","скидка","advertisement","sponsored","buy now"],
  cooperation: ["взаимопомощь","сотрудничество","поддержка","cooperation","mutual aid"]
});
const WORD = /[\p{L}\p{N}]+/gu;
export function analyzeText(input) {
  if (typeof input !== "string" || input.length > 200000) throw new Error("Text limit is 200,000 characters");
  const tokens = Array.from(input.matchAll(WORD), m => ({word:m[0].toLocaleLowerCase(),start:m.index,end:m.index+m[0].length}));
  const evidence = {};
  for (const [category,terms] of Object.entries(LEXICON)) {
    const hits = [];
    for (const term of terms) {
      const parts = term.toLocaleLowerCase().match(WORD) || [];
      for (let i=0; i<=tokens.length-parts.length; i++) {
        if (parts.every((part,j)=>tokens[i+j].word===part)) hits.push({token_index:i,term,start:tokens[i].start,end:tokens[i+parts.length-1].end,excerpt:input.slice(Math.max(0,tokens[i].start-40),Math.min(input.length,tokens[i+parts.length-1].end+40))});
      }
    }
    if (hits.length) evidence[category] = {matches:hits.length,examples:hits.slice(0,10)};
  }
  return {schema_version:"lexical-composition-1.1",method:"dictionary_matches_only",
    token_count:tokens.length, categories:evidence, coverage:"provided_text_only",
    not_assessed:["images","audio","video","meaning","speaker_intent","effects_on_viewer"],
    disclaimer:"Keyword occurrence is not evidence of endorsement, advertising, harm or intent."};
}
