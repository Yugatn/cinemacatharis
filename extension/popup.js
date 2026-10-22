import {analyzeText} from "./composition-core.js";
document.getElementById("run").addEventListener("click",async()=>{
  const output=document.getElementById("result");
  try {
    const [tab]=await chrome.tabs.query({active:true,currentWindow:true});
    if(!tab?.id) throw new Error("Нет активной вкладки");
    const response=await chrome.scripting.executeScript({
      target:{tabId:tab.id},
      func:()=> (document.body?.innerText || "").slice(0,200000)
    });
    const text=response?.[0]?.result;
    if(typeof text!=="string") throw new Error("Текст страницы недоступен");
    const result=analyzeText(text);
    output.textContent="Слов: "+result.token_count+"\n"+Object.entries(result.categories)
      .map(([k,v])=>k+": "+v.matches+" словарных совпадений").join("\n")+
      "\n\nСовпадения не устанавливают намерение, рекламу или вред.";
  }catch(error){output.textContent="Не удалось проанализировать страницу: "+error.message;}
});
