// Read-aloud for the current reading section, using the speech voices built into the browser or system.
// Only book text is spoken. Personal notes, quizzes and experiments are never sent to a speech voice.
const CLOSERS = /["”’」』）)\s]/;
function sentences(text) {
  const out = []; let start = 0;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i], next = text[i + 1];
    // A full stop inside a number (7.9) or an abbreviation is not a sentence end.
    const ends = '。！？；'.includes(ch) || ('.!?;'.includes(ch) && (next === undefined || CLOSERS.test(next)));
    if (!ends) continue;
    let end = i + 1;
    while (end < text.length && CLOSERS.test(text[end])) end++;
    out.push(text.slice(start, end)); start = end; i = end - 1;
  }
  if (start < text.length) out.push(text.slice(start));
  return out;
}
// Short utterances avoid the cut-off some browsers apply to long ones, and make pause and resume precise.
export function speechChunks(text, limit = 160) {
  const clean = String(text ?? '').replace(/[↗→←↓↑✓★✳·]/g, ' ').replace(/\s+/g, ' ').trim();
  if (!clean) return [];
  const chunks = []; let current = '';
  for (const part of sentences(clean)) {
    if (current && (current + part).length > limit) { chunks.push(current.trim()); current = ''; }
    current += part;
    while (current.length > limit * 2) { chunks.push(current.slice(0, limit).trim()); current = current.slice(limit); }
  }
  if (current.trim()) chunks.push(current.trim());
  return chunks;
}
// Parallel mode reads the Chinese source; the English lines are a reading aid beside it.
export const speechLanguage = language => language === 'en' ? 'en-US' : 'zh-CN';
export function pickVoice(voices, lang) {
  const tag = voice => String(voice.lang || '').replace('_', '-').toLowerCase();
  const matching = (voices || []).filter(voice => tag(voice).startsWith(lang.slice(0, 2).toLowerCase()));
  const exact = matching.filter(voice => tag(voice) === lang.toLowerCase());
  const pool = exact.length ? exact : matching;
  // Prefer a voice that runs on the device over one that sends text to a remote service.
  return pool.find(voice => voice.localService && voice.default) || pool.find(voice => voice.localService) || pool.find(voice => voice.default) || pool[0] || null;
}
const SKIP = '[data-lab],#quiz,#experiment,.quiz,#reflection,.lesson-complete,.source-note,.reader-toolbar,.reader-end,.book-pagination,.principle-tags,.resume-position,table,details:not([open]),.article-aside,.entry-grid,.chapter-directory,.parallel-figure,nav,button,textarea';
function collectFromPage() {
  const root = document.querySelector('main .reading-unit') || document.querySelector('main');
  const items = [];
  for (const element of root?.querySelectorAll('h1,h2,h3,h4,p,li,summary') || []) {
    if (element.closest(SKIP)) continue;
    const copy = element.cloneNode(true);
    copy.querySelectorAll('.translation-en,.sr-only,svg,button,[aria-hidden="true"]').forEach(node => node.remove());
    // Section counters such as "01" are visual only.
    const counter = copy.firstElementChild;
    if (counter && !counter.classList.contains('parallel-text') && /^[\d✓]+$/.test(counter.textContent.trim())) counter.remove();
    for (const text of speechChunks(copy.textContent)) items.push({element, text});
  }
  return items;
}
export function createSpeechReader({getLanguage, notify = () => {}, collect = collectFromPage, synth = globalThis.speechSynthesis, Utterance = globalThis.SpeechSynthesisUtterance}) {
  const supported = Boolean(synth && Utterance);
  let queue = [], index = 0, state = 'idle', rate = 1, run = 0, marked = null, controls = null;
  const labels = {idle: '朗读本节', speaking: '暂停朗读', paused: '继续朗读'};
  function mark(element) {
    marked?.classList?.remove('speaking'); marked = element || null;
    if (!marked?.classList) return;
    marked.classList.add('speaking');
    const reduced = globalThis.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
    marked.scrollIntoView?.({block: 'center', behavior: reduced ? 'instant' : 'smooth'});
  }
  function refresh() {
    if (!controls) return;
    controls.play.textContent = labels[state]; controls.play.setAttribute('aria-pressed', String(state === 'speaking'));
    controls.stop.hidden = state === 'idle'; controls.rate.hidden = state === 'idle';
  }
  function setState(next) { state = next; refresh(); }
  function speakNext() {
    if (index >= queue.length) { mark(null); setState('idle'); return; }
    const token = ++run, item = queue[index], lang = speechLanguage(getLanguage());
    const utterance = new Utterance(item.text);
    utterance.lang = lang; utterance.rate = rate;
    const voice = pickVoice(synth.getVoices?.() || [], lang); if (voice) utterance.voice = voice;
    utterance.onend = () => { if (token !== run) return; index++; speakNext(); };
    utterance.onerror = event => {
      if (token !== run || ['canceled', 'interrupted'].includes(event?.error)) return;
      run++; mark(null); setState('idle'); notify('朗读中断了，请再试一次。');
    };
    mark(item.element); setState('speaking'); synth.speak(utterance);
  }
  function start() {
    if (!supported) return;
    run++; synth.cancel();
    queue = collect(); index = 0;
    if (!queue.length) { setState('idle'); notify('本节没有可朗读的正文。'); return; }
    const lang = speechLanguage(getLanguage()), voices = synth.getVoices?.() || [];
    if (voices.length && !pickVoice(voices, lang)) notify(lang === 'en-US' ? '这台设备没有找到英文语音，朗读可能无法开始。' : '这台设备没有找到中文语音，朗读可能无法开始。');
    speakNext();
  }
  // Pause by cancelling and resume from the start of the same sentence group; this works on every browser.
  function pause() { if (state !== 'speaking') return; run++; synth.cancel(); setState('paused'); }
  function resume() { if (state === 'paused') speakNext(); }
  function stop() { if (!supported) return; run++; synth.cancel(); queue = []; index = 0; mark(null); setState('idle'); }
  function toggle() { state === 'idle' ? start() : state === 'speaking' ? pause() : resume(); }
  function setRate(value) {
    rate = [0.8, 1, 1.25, 1.5].includes(Number(value)) ? Number(value) : 1;
    if (state === 'speaking') { run++; synth.cancel(); speakNext(); }
  }
  function mount(toolbar) {
    controls = null;
    if (!supported || !toolbar) return;
    toolbar.insertAdjacentHTML('beforeend', `<span class="reader-speech"><button type="button" class="reader-focus-button" id="reader-speak" aria-pressed="false">朗读本节</button><button type="button" class="reader-focus-button" id="reader-speak-stop" hidden>停止朗读</button><select id="reader-rate" aria-label="朗读速度" hidden>${[0.8, 1, 1.25, 1.5].map(value => `<option value="${value}" ${value === rate ? 'selected' : ''}>${value}×</option>`).join('')}</select></span>`);
    controls = {play: toolbar.querySelector('#reader-speak'), stop: toolbar.querySelector('#reader-speak-stop'), rate: toolbar.querySelector('#reader-rate')};
    controls.play.onclick = toggle; controls.stop.onclick = stop; controls.rate.onchange = event => setRate(event.target.value);
    refresh();
  }
  globalThis.addEventListener?.('pagehide', () => { if (supported) synth.cancel(); });
  return {supported, mount, start, pause, resume, stop, toggle, setRate, get state() { return state; }, get position() { return index; }};
}
