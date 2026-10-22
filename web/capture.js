/* Local browser capture. No network requests and no automated semantic claims. */
const $ = id => document.getElementById(id);
let stream, recorder, timer, started, frames = [], chunks = [], audioBlob = null;
let lastCaptureAt = 0, stopRequested = false, capturing = false;
const status = message => { $("status").textContent = message; };
const download = (blob, name) => {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a"); a.href = url; a.download = name; a.click();
  setTimeout(() => URL.revokeObjectURL(url), 30000);
};
const waitMetadata = video => new Promise(resolve => {
  if (video.videoWidth) return resolve();
  video.addEventListener("loadedmetadata", resolve, {once:true});
});
function stop() {
  if (stopRequested) return;
  stopRequested = true;
  clearInterval(timer);
  if (recorder && recorder.state !== "inactive") recorder.stop();
  if (stream) stream.getTracks().forEach(t => t.stop());
  $("start").disabled = false; $("stop").disabled = true;
  $("export").disabled = !frames.length;
  status(`Остановлено. Снимков: ${frames.length}. Звук: ${audioBlob ? "готов" : "если запись завершится, появится при экспорте"}. Семантическая оценка не выполнялась.`);
}
async function start() {
  const interval = Number($("interval").value), limit = Number($("limit").value);
  if (!Number.isInteger(interval) || interval < 200 || interval > 60000 ||
      !Number.isInteger(limit) || limit < 1 || limit > 2000) {
    status("Неверные настройки интервала или лимита."); return;
  }
  frames = []; chunks = []; audioBlob = null; stopRequested = false; capturing = false;
  try {
    stream = await navigator.mediaDevices.getDisplayMedia({video:{frameRate:15},audio:true});
    const video = $("preview"); video.srcObject = stream;
    await waitMetadata(video); await video.play();
    started = performance.now(); lastCaptureAt = started;
    const canvas = document.createElement("canvas");
    const maxWidth = 960;
    canvas.width = Math.min(video.videoWidth, maxWidth);
    canvas.height = Math.max(1, Math.round(video.videoHeight * canvas.width / video.videoWidth));
    const ctx = canvas.getContext("2d");
    const audioTracks = stream.getAudioTracks();
    if (audioTracks.length && window.MediaRecorder) {
      try {
        const audioStream = new MediaStream(audioTracks);
        recorder = new MediaRecorder(audioStream);
        recorder.ondataavailable = e => { if (e.data.size) chunks.push(e.data); };
        recorder.onstop = () => { if (chunks.length) audioBlob = new Blob(chunks,{type:recorder.mimeType || "audio/webm"}); };
        recorder.start(1000);
      } catch (e) { status("Захват звука не поддерживается: " + e.message); }
    }
    stream.getVideoTracks()[0].addEventListener("ended", stop, {once:true});
    $("start").disabled = true; $("stop").disabled = false; $("export").disabled = true;
    timer = setInterval(async () => {
      if (stopRequested || capturing || !video.videoWidth) return;
      capturing = true;
      const now = performance.now();
      // Prevent concurrent asynchronous snapshots and preserve wall-clock timing.
      if (frames.length >= limit) { stop(); return; }
      const wallMs = Math.round(now - started);
      const gapMs = Math.round(now - lastCaptureAt);
      lastCaptureAt = now;
      ctx.drawImage(video,0,0,canvas.width,canvas.height);
      const blob = await new Promise(resolve => canvas.toBlob(resolve,"image/jpeg",0.72));
      if (!blob || stopRequested) { capturing = false; return; }
      frames.push({wall_ms:wallMs,gap_ms:gapMs,blob});
      status(`Снимков: ${frames.length}/${limit}. Время захвата: ${(wallMs/1000).toFixed(1)} с. Аудиодорожек: ${audioTracks.length}. Исходное время фильма неизвестно.`);
      capturing = false;
      if (frames.length >= limit) stop();
    }, interval);
  } catch (e) {
    if (stream) stream.getTracks().forEach(t => t.stop());
    status("Захват не запущен: " + e.message);
  }
}
function exportCapture() {
  if (!frames.length) return;
  const manifest = {
    schema_version:"capture-1.0", capture_type:"screen", captured_at:new Date().toISOString(),
    timing_basis:"wall_clock_not_media_time", content_classification:"not_assessed",
    frame_count:frames.length, audio_recorded:!!audioBlob,
    limitations:["Sampling may miss brief scenes","Playback speed and original media time not observable",
      "Audio may be absent or time-compressed","DRM may block capture"],
    frames:frames.map((f,i)=>({file:`frame_${String(i).padStart(5,"0")}.jpg`,
      wall_ms:f.wall_ms,gap_ms:f.gap_ms}))
  };
  download(new Blob([JSON.stringify(manifest,null,2)],{type:"application/json"}),"capture_manifest.json");
  frames.forEach((f,i)=>download(f.blob,`frame_${String(i).padStart(5,"0")}.jpg`));
  if (audioBlob) download(audioBlob,"captured_audio.webm");
}
$("start").addEventListener("click",start);
$("stop").addEventListener("click",stop);
$("export").addEventListener("click",exportCapture);
