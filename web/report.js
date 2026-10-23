/* Browser-only report viewer. Render all untrusted report text via textContent. */
const $ = id => document.getElementById(id);
let report = null;
const columns = {
  findings: ["category","context","start_ms","end_ms","confidence","channel","commercial_signal","verified","evidence"],
  transcript: ["start_ms","end_ms","text"],
  observations: ["category","channel","timing_basis","start","end","confidence","confidence_calibrated","verified","method","evidence"]
};
function table(rows, target) {
  const node = $(target); node.replaceChildren();
  const element = document.createElement("table");
  const head = document.createElement("thead"), body = document.createElement("tbody");
  for (const [i,row] of rows.entries()) {
    const tr = document.createElement("tr");
    row.forEach(value => {
      const cell = document.createElement(i === 0 ? "th" : "td");
      cell.textContent = String(value ?? "");
      tr.appendChild(cell);
    });
    (i === 0 ? head : body).appendChild(tr);
  }
  element.append(head,body); node.appendChild(element);
}
function rowsFor(name) {
  if (name === "findings" && report.schema_version === "evidence-1.0") {
    return [columns.observations,...(Array.isArray(report.observations) ? report.observations : []).map(item => columns.observations.map(key => item?.[key] ?? ""))];
  }
  if (name === "findings") {
    return [columns.findings,...(Array.isArray(report.findings) ? report.findings : []).map(
      item => columns.findings.map(key => item?.[key] ?? ""))];
  }
  if (name === "transcript") {
    return [columns.transcript,...(Array.isArray(report.transcript?.segments) ? report.transcript.segments : []).map(
      item => columns.transcript.map(key => item?.[key] ?? ""))];
  }
  if(report.schema_version === "evidence-1.0") {
    return [["Field","Value"],["Schema",report.schema_version],["Source",report.source],["Coverage",report.coverage],["Observations",report.observation_count],["Content safe","not_assessed"],["Promotion","not_assessed"]];
  }
  const assessment = report.assessment || {};
  return [["Field","Value"],...Object.entries({
    "Schema":report.schema_version,"Source":report.source,
    "Frames examined":report.frames_examined,"Frames available":report.frames_available,
    "Timing basis":report.timing_basis,"Monetization":assessment.monetization || "not_assessed",
    "Publication":assessment.publication || "not_assessed",
    "Explanation":assessment.explanation || "Not evaluated"
  })];
}
function show() {
  table(rowsFor("summary"),"summary");
  table(rowsFor("findings"),"findings");
  table(rowsFor("transcript"),"transcript");
  const node = $("limitations"); node.replaceChildren();
  const ul = document.createElement("ul");
  for (const item of Array.isArray(report.limitations) ? report.limitations : []) {
    const li = document.createElement("li"); li.textContent = String(item); ul.appendChild(li);
  }
  node.appendChild(ul);
  for (const id of ["csv","html","json"]) $(id).disabled = false;
  $("message").textContent = "Отчёт загружен. Результаты требуют проверки человеком.";
}
function save(content, name, type) {
  const url = URL.createObjectURL(new Blob([content],{type}));
  const a = document.createElement("a"); a.href = url; a.download = name; a.click();
  setTimeout(() => URL.revokeObjectURL(url), 30000);
}
function csvEscape(value) {
  let s = String(value ?? "");
  // Guard against formula injection in Excel and Google Sheets.
  if (/^[\s]*[=+\-@]/.test(s)) s = "'" + s;
  return '"' + s.replaceAll('"','""') + '"';
}
$("file").addEventListener("change",async event => {
  report = null;
  for (const id of ["csv","html","json"]) $(id).disabled = true;
  try {
    const file = event.target.files?.[0];
    if (!file || file.size > 20_000_000) throw new Error("Файл отсутствует или больше 20 МБ");
    const parsed = JSON.parse(await file.text());
    if (!parsed || typeof parsed !== "object" || !["scan-1.0","evidence-1.0"].includes(parsed.schema_version)) {
      throw new Error("Ожидается отчёт scan-1.0 или evidence-1.0");
    }
    if(parsed.schema_version==="evidence-1.0" && (!Array.isArray(parsed.observations) || parsed.observations.length>10000)) throw new Error("Недопустимый список наблюдений");
    report = parsed; show();
  } catch (error) { $("message").textContent = "Ошибка: " + error.message; }
});
$("csv").addEventListener("click",() => {
  if (!report) return;
  for (const name of ["summary","findings","transcript"]) {
    const csv = "\uFEFF" + rowsFor(name).map(row => row.map(csvEscape).join(",")).join("\r\n");
    save(csv,name+".csv","text/csv;charset=utf-8");
  }
});
$("html").addEventListener("click",() => {
  if (!report) return;
  // Reuse the already safe DOM tables and lists; all report data came through textContent.
  const parts = ["summary","findings","transcript","limitations"].map(id => {
    const title = {summary:"Сводка",findings:"Обнаруженные признаки",transcript:"Речь",limitations:"Ограничения"}[id];
    return "<h2>"+title+"</h2>"+$(id).innerHTML;
  });
  save('<!doctype html><html lang="ru"><meta charset="utf-8"><title>Cinema Catharsis</title><h1>Cinema Catharsis — отчёт</h1><p>Автоматические результаты не подтверждены.</p>'+parts.join("")+"</html>",
       "cinema_report.html","text/html;charset=utf-8");
});
$("json").addEventListener("click",() => {
  if (report) save(JSON.stringify(report,null,2),"cinema_report.json","application/json");
});
