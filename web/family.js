/* Local allowlist launcher; not a web-content filter or protected browser. */
const $ = id => document.getElementById(id);
const KEY = "cinema-catharsis-family-sites-v1";
let sites = [];
function safeUrl(raw) {
  try {
    const u = new URL(raw);
    if (u.protocol !== "https:" || !u.hostname || u.username || u.password) return null;
    if (u.hostname === "localhost" || u.hostname.endsWith(".localhost")) return null;
    return u.href;
  } catch { return null; }
}
function load() {
  try {
    const parsed = JSON.parse(localStorage.getItem(KEY) || "[]");
    if (Array.isArray(parsed)) sites = parsed.filter(s =>
      s && typeof s.label === "string" && s.label.length <= 80 && safeUrl(s.url)).slice(0,100);
  } catch { sites = []; }
}
function persist() {
  try { localStorage.setItem(KEY,JSON.stringify(sites)); return true; }
  catch { $("feedback").textContent = "Не удалось сохранить настройки на устройстве."; return false; }
}
function render() {
  const list = $("sites"); list.replaceChildren();
  $("count").textContent = "Разрешённых ссылок: " + sites.length;
  $("empty").hidden = !!sites.length;
  for (const [index,site] of sites.entries()) {
    const li = document.createElement("li");
    const link = document.createElement("a");
    link.href = site.url; link.target = "_blank"; link.rel = "noopener noreferrer";
    link.textContent = site.label + " — " + new URL(site.url).hostname;
    li.append(link);
    if ($("parent").classList.contains("open")) {
      const remove = document.createElement("button");
      remove.className = "secondary"; remove.style.marginLeft = "10px";
      remove.textContent = "Удалить"; remove.setAttribute("aria-label","Удалить "+site.label);
      remove.addEventListener("click",() => { sites.splice(index,1); persist(); render(); });
      li.append(remove);
    }
    list.append(li);
  }
}
$("toggle").addEventListener("click",() => {
  const open = $("parent").classList.toggle("open");
  $("toggle").setAttribute("aria-expanded",String(open));
  $("toggle").textContent = open ? "Скрыть настройки" : "Показать настройки";
  render();
});
$("add").addEventListener("click",() => {
  const label = $("label").value.trim(), url = safeUrl($("url").value.trim());
  if (!label || label.length > 80 || !url) {
    $("feedback").textContent = "Укажите название и корректный HTTPS-адрес без логина и пароля."; return;
  }
  if (sites.length >= 100 || sites.some(s => s.url === url)) {
    $("feedback").textContent = "Ссылка уже добавлена или достигнут лимит 100."; return;
  }
  sites.push({label,url}); persist(); render();
  $("feedback").textContent = "Ссылка добавлена."; $("label").value = ""; $("url").value = "";
});
$("reset").addEventListener("click",() => {
  if (!confirm("Удалить все ссылки из подборки на этом устройстве?")) return;
  sites = []; persist(); render(); $("feedback").textContent = "Список очищен.";
});
load(); render();
