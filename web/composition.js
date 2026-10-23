import {analyzeText} from "./composition-core.js";
import {lexicalToEvidence} from "./evidence-core.js";
const $=id=>document.getElementById(id);
let last=null;
let unified=null;
$("analyze").addEventListener("click",()=>{
  try {
    last=analyzeText($("content").value);
    unified=lexicalToEvidence(last);
    const target=$("result");target.replaceChildren();
    const summary=document.createElement("p");
    summary.textContent="Слов: "+last.token_count+". Найденные словарные признаки (не оценка вреда):";
    target.append(summary);
    const table=document.createElement("table");
    const header=document.createElement("tr");
    for (const text of ["Категория","Совпадений","Примеры"]) {const th=document.createElement("th");th.textContent=text;header.append(th);}
    table.append(header);
    for (const [category,data] of Object.entries(last.categories)) {
      const tr=document.createElement("tr");
      for (const value of [category,data.matches,data.examples.map(x=>x.term).join(", ")]) {
        const td=document.createElement("td");td.textContent=String(value);tr.append(td);
      }
      table.append(tr);
    }
    target.append(table);
    const evidenceTitle=document.createElement("h3"); evidenceTitle.textContent="Подтверждающие фрагменты"; target.append(evidenceTitle);
    const evidenceList=document.createElement("ul");
    for(const [category,data] of Object.entries(last.categories)) {
      for(const hit of data.examples) {
        const item=document.createElement("li");
        item.textContent=category+" · символы "+hit.start+"–"+hit.end+": «"+hit.excerpt+"»";
        evidenceList.append(item);
      }
    }
    target.append(evidenceList);
    const status=document.createElement("p");
    status.textContent="Единый отчёт evidence-1.0: "+unified.observation_count+" наблюдений; покрытие частичное; оценка безопасности не выполнялась.";
    target.append(status);
    const warning=document.createElement("p");
    warning.textContent="Это словарные совпадения, а не подтверждение намерения, рекламы или вреда. Примеры ограничены десятью на категорию.";
    target.append(warning);
    if (!Object.keys(last.categories).length) {
      const p=document.createElement("p");p.textContent="Словарных совпадений не найдено. Это не означает отсутствие какого-либо содержания.";target.append(p);
    }
  } catch(error) { $("result").textContent="Ошибка: "+error.message; }
});
$("exportEvidence").addEventListener("click",()=>{
  if(!unified){$("result").textContent="Сначала запустите анализ.";return;}
  const url=URL.createObjectURL(new Blob([JSON.stringify(unified,null,2)],{type:"application/json"}));
  const a=document.createElement("a");a.href=url;a.download="evidence.json";a.click();
  setTimeout(()=>URL.revokeObjectURL(url),30000);
});
$("export").addEventListener("click",()=>{
  if(!last) { $("result").textContent="Сначала запустите анализ.";return;}
  const url=URL.createObjectURL(new Blob([JSON.stringify(last,null,2)],{type:"application/json"}));
  const a=document.createElement("a");a.href=url;a.download="composition.json";a.click();
  setTimeout(()=>URL.revokeObjectURL(url),30000);
});
