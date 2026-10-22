import {analyzeText} from "./composition-core.js";
const $=id=>document.getElementById(id);
let last=null;
$("analyze").addEventListener("click",()=>{
  try {
    last=analyzeText($("content").value);
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
    if (!Object.keys(last.categories).length) {
      const p=document.createElement("p");p.textContent="Словарных совпадений не найдено. Это не означает отсутствие какого-либо содержания.";target.append(p);
    }
  } catch(error) { $("result").textContent="Ошибка: "+error.message; }
});
$("export").addEventListener("click",()=>{
  if(!last) { $("result").textContent="Сначала запустите анализ.";return;}
  const url=URL.createObjectURL(new Blob([JSON.stringify(last,null,2)],{type:"application/json"}));
  const a=document.createElement("a");a.href=url;a.download="composition.json";a.click();
  setTimeout(()=>URL.revokeObjectURL(url),30000);
});
