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
  const tokens = Array.from(input.toLocaleLowerCase().matchAll(WORD), m => m[0]);
  const evidence = {};
  for (const [category,terms] of Object.entries(LEXICON)) {
    const hits = [];
    for (const term of terms) {
      const parts = term.toLocaleLowerCase().match(WORD) || [];
      for (let i=0; i<=tokens.length-parts.length; i++) {
        if (parts.every((part,j)=>tokens[i+j]===part)) hits.push({token_index:i,term});
      }
    }
    if (hits.length) evidence[category] = {matches:hits.length,examples:hits.slice(0,10)};
  }
  return {schema_version:"lexical-composition-1.0",method:"dictionary_matches_only",
    token_count:tokens.length, categories:evidence, coverage:"provided_text_only",
    not_assessed:["images","audio","video","meaning","speaker_intent","effects_on_viewer"],
    disclaimer:"Keyword occurrence is not evidence of endorsement, advertising, harm or intent."};
}
