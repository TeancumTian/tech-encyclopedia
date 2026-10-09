import { pathways, lessons, labs, labSources } from './learning.js';
import { gateOutput, binaryValue, circuitCurrent, transmissionLoss, gradientStep, normalizeProgress } from './models.js';

const $ = (s, root = document) => root.querySelector(s);
const $$ = (s, root = document) => [...root.querySelectorAll(s)];
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const icons = {
  home: '<path d="m3 11 9-8 9 8M5 10v11h5v-7h4v7h5V10"/>',
  compass: '<circle cx="12" cy="12" r="9"/><path d="m16 8-2 6-6 2 2-6Z"/>',
  route: '<circle cx="6" cy="5" r="2"/><circle cx="18" cy="19" r="2"/><path d="M8 5h9a4 4 0 0 1 0 8H7a3 3 0 0 0 0 6h9"/>',
  lab: '<path d="M9 3h6M10 3v7L4 20q0 1 2 1h12q2 0 2-1l-6-10V3M7 15h10"/>',
  book: '<path d="M12 5v16M12 5Q6 1 2 4v15q5-3 10 2 5-5 10-2V4q-4-3-10 1Z"/>',
  search: '<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6"/>',
  arrow: '<path d="M4 12h16m-6-6 6 6-6 6"/>',
  bolt: '<path d="m14 2-9 12h6l-1 8 9-12h-6Z"/>',
  chip: '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 6V2m6 4V2M9 22v-4m6 4v-4M6 9H2m4 6H2m20-6h-4m4 6h-4"/>',
  globe: '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>',
  spark: '<path d="m12 2 3 7 7 3-7 3-3 7-3-7-7-3 7-3Z"/>',
  grid: '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
  check: '<path d="m5 12 4 4L20 5"/>',
  bookmark: '<path d="M6 3h12v19l-6-4-6 4Z"/>',
  clock: '<circle cx="12" cy="12" r="9"/><path d="M12 6v6l4 2"/>',
  github: '<path d="M8 21v-4q-4 1-5-3m14 7v-5q5-3 3-9l-1-4-4 2a15 15 0 0 0-6 0L5 3 4 7q-2 6 3 9v5"/>',
  leaf: '<path d="M5 19C-2 7 10 2 21 3c1 12-5 19-14 15M5 21 16 8"/>',
};
const icon = (name, cls = '') => `<svg class="icon ${cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${icons[name] || icons.compass}</svg>`;
const repo = 'https://github.com/TeancumTian/tech-encyclopedia';
const key = 'tech-encyclopedia-learning-v1';
let book, entries, principles, domains, progress, filter = { query: '', domain: '', tier: '', page: 1 };
let storageOK = true;

function save() {
  try { localStorage.setItem(key, JSON.stringify(progress)); }
  catch { storageOK = false; toast('浏览器未能保存进度，请导出学习记录备份。'); }
}
let toastTimer;
function toast(message) {
  $('#toast').textContent = message; $('#toast').classList.add('visible');
  clearTimeout(toastTimer); toastTimer = setTimeout(() => $('#toast').classList.remove('visible'), 3000);
}
function inline(text) {
  return esc(text).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g, (_, id, label) => {
    const p = id.startsWith('p:'); const item = p ? principles.get(id.slice(2)) : entries.get(id);
    return item ? `<a href="#/${p ? 'principle/' + id.slice(2) : 'entry/' + id}">${label || esc(item.zh)}</a>` : (label || id);
  }).replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/`(.*?)`/g, '<code>$1</code>');
}
const prose = text => String(text || '').split('\n').filter(Boolean).map(line => `<p>${inline(line.replace(/^[-*] /, ''))}</p>`).join('');
const entryLink = (id, path = '') => `#/entry/${id}${path ? '?path=' + path : ''}`;
const learned = id => progress.learned.includes(id);
const progressCount = path => path.ids.filter(learned).length;
function route() {
  const [path, search = ''] = (location.hash.slice(1) || '/').split('?');
  return { parts: path.split('/').filter(Boolean), params: new URLSearchParams(search) };
}
function shell(content, active) {
  const links = [['home', '', '探索首页'], ['route', 'paths', '学习路线'], ['compass', 'explore', '知识图谱'], ['lab', 'labs', '互动实验室'], ['book', 'notebook', '我的学习']];
  $('#app').innerHTML = `
  <aside class="sidebar">
    <a href="#/" class="brand"><span class="brand-symbol">✳</span><span>原来如此<small>THE TECHNOLOGY ATLAS</small></span></a>
    <span class="sidebar-label">给好奇心一个去处</span>
    <nav aria-label="主导航">${links.map(([i, href, label]) => `<a href="#/${href}" ${active === href ? 'aria-current="page"' : ''}>${icon(i)}<span>${label}</span>${href === 'labs' ? '<span class="nav-pill">6</span>' : ''}</a>`).join('')}</nav>
    <div class="sidebar-bottom"><div class="small-quote">世界很复杂，<br>理解可以简单一点。</div><div class="side-progress"><span>你的探索足迹</span><b>${progress.learned.length} <small>/ ${book.entries.length}</small></b><progress value="${progress.learned.length}" max="${book.entries.length}"></progress></div><a class="repo-link" href="${repo}" target="_blank" rel="noopener">${icon('github')} 项目与书稿 ↗</a></div>
  </aside>
  <div class="workspace"><header class="topbar"><div class="top-caption">近现代科技百科 <span>/</span> 互动学习版</div><form class="global-search" role="search"><label class="sr-only" for="global-search">搜索科技知识</label>${icon('search')}<input id="global-search" type="search" placeholder="搜索一个好奇的问题…" autocomplete="off"><kbd>/</kbd></form><a class="profile" href="#/notebook" aria-label="打开我的学习">好奇</a></header>
  <main id="main" tabindex="-1">${content}</main><footer>保持好奇，慢慢弄懂。<span>© 2026 Teancum Tian · 基于《近现代科技百科全书》</span></footer></div>`;
  $('.global-search').onsubmit = event => { event.preventDefault(); location.hash = '#/explore?q=' + encodeURIComponent($('#global-search').value); };
}
function render({ keepScroll = false } = {}) {
  const { parts, params } = route();
  const type = parts[0] || ''; const id = parts[1];
  if (type === 'explore') filter = { query: params.get('q') || '', domain: params.get('domain') || '', tier: params.get('tier') || '', page: 1 };
  const views = { '': home, paths: () => pathPage(id), explore: explorePage, labs: () => labPage(id), entry: () => entryPage(id, params.get('path')), principle: () => principlePage(id), notebook: notebookPage };
  const content = views[type] ? views[type]() : notFound();
  shell(content, type === 'entry' || type === 'principle' ? 'explore' : type);
  document.title = `${(entries.get(id)?.zh || principles.get(id)?.zh || ({paths:'学习路线',explore:'知识图谱',labs:'互动实验室',notebook:'我的学习'})[type] || '把科技变成常识')} · 原来如此`;
  bindPage();
  if (!keepScroll) { window.scrollTo(0, 0); $('#main').focus({ preventScroll: true }); }
}
function sectionHead(kicker, title, link = '', label = '') {
  return `<div class="section-head"><div><span class="eyebrow">${kicker}</span><h2>${title}</h2></div>${link ? `<a class="text-link" href="${link}">${label} ${icon('arrow')}</a>` : ''}</div>`;
}
function home() {
  const next = progress.last ? entries.get(progress.last) : null;
  return `<section class="hero"><div class="hero-copy"><span class="eyebrow"><span class="tiny-sun">✳</span> 写给每一个好奇的人</span><h1>把科技，<br>变成你的<span class="underline-word">常识</span>。</h1><p>芯片为什么会计算？AI 到底怎么学？<br>从一个小问题开始，动手试一试，复杂的世界就清楚了一点。</p><div class="hero-actions"><a class="btn primary" href="${next ? entryLink(next.id) : '#/paths/computer'}">${next ? '继续上次的探索' : '开启第一段探索'} ${icon('arrow')}</a><a class="text-link" href="#/explore">随便逛逛 ↗</a></div><div class="hero-note"><span class="mini-avatars"><i>?</i><i>!</i><i>✳</i></span>不用专业背景，带上好奇心就好。</div></div>
    <div class="hero-lab"><div class="lab-label"><span class="live-dot"></span> 此刻，就能试试 <span>EXPERIMENT 01</span></div><div class="hero-lab-title">电脑的思考，<br>从两个小开关开始。</div><div data-lab="logic" data-compact="true"></div><a class="hero-lab-link" href="#/labs/logic">这是怎么回事？探索逻辑门 ${icon('arrow')}</a></div></section>
    <div class="stats-strip"><div><strong>${book.entries.length}</strong><span>个科技知识，慢慢解锁</span></div><div><strong>${book.domains.length}</strong><span>个领域，看见彼此的联系</span></div><div><strong>${book.principles.length}</strong><span>条底层规律，举一反三</span></div><div><strong>∞</strong><span>个「原来如此」的瞬间</span></div></div>
    <section class="home-section">${sectionHead('FOLLOW YOUR CURIOSITY', '不知道从哪开始？跟着问题走。', '#/paths', '全部学习路线')}<div class="path-grid">${pathways.map(pathCard).join('')}</div></section>
    <section class="home-section">${sectionHead('LESS READING, MORE DISCOVERING', '动手之后，理解就不一样了。', '#/labs', '进入实验室')}<div class="lab-preview-grid">${labs.filter(l => ['binary', 'gradient', 'grid'].includes(l.id)).map(labCard).join('')}</div></section>
    <section class="domain-band"><div><span class="eyebrow">A CONNECTED WORLD</span><h2>知识没有围墙。<br>你想从哪里推开一扇门？</h2><a class="text-link" href="#/explore">探索完整知识图谱 ${icon('arrow')}</a></div><div class="domain-cloud">${book.domains.map((d, i) => `<a href="#/explore?domain=${d.id}"><span>${String(i+1).padStart(2,'0')}</span>${d.zh}<small>${d.count}</small></a>`).join('')}</div></section>`;
}
function pathCard(p) {
  const count = progressCount(p);
  return `<a class="path-card ${p.color}" href="#/paths/${p.id}"><div class="path-card-top"><span class="tile-icon">${icon(p.icon)}</span><span class="path-number">0${pathways.indexOf(p)+1}</span></div><span class="muted small">${p.subtitle}</span><h3>${p.name}</h3><div class="card-bottom"><span>${p.ids.length} 小节 · 约 ${p.time} 分钟</span>${icon('arrow')}</div>${count ? `<progress value="${count}" max="${p.ids.length}" aria-label="${p.name}学习进度"></progress>` : ''}</a>`;
}
function labCard(l) {
  const artwork = l.id === 'binary' ? '<span class="binary-art">0<span>1</span>0<span>1</span></span>' : l.id === 'gradient' ? '<span class="curve-art"><i></i></span>' : `<span class="large-icon">${icon(l.icon)}</span>`;
  return `<a class="lab-card" href="#/labs/${l.id}"><div class="lab-art ${l.color}">${artwork}<span class="art-label">可交互 · ${l.time}</span></div><div class="lab-card-body"><span class="eyebrow">${l.tag}</span><h3>${l.title}</h3><p>${l.desc}</p><span class="text-link">动手试试 ${icon('arrow')}</span></div></a>`;
}
function pageTitle(kicker, title, description) { return `<div class="page-title"><span class="eyebrow">${kicker}</span><h1>${title}</h1><p>${description}</p></div>`; }
function pathPage(id) {
  if (!id) return `${pageTitle('LEARNING JOURNEYS', '给好奇心，一条小路。', '每条路线从生活中的问题出发。每次学一小节，慢慢把知识连起来。')}<div class="path-grid full">${pathways.map(pathCard).join('')}</div><div class="callout">${icon('leaf')}<p>建议这样学：先看生活例子 → 动手做实验 → 回答小问题 → 用自己的话记下来。路线没有解锁限制，随时可以跳到感兴趣的一节。</p></div>`;
  const p = pathways.find(p => p.id === id); if (!p) return notFound();
  return `<a class="back-link" href="#/paths">← 所有学习路线</a>${pageTitle('JOURNEY 0' + (pathways.indexOf(p)+1), p.name, p.intro)}<div class="journey-layout"><div class="journey-steps">${p.ids.map((eid, i) => `<a class="journey-step" href="${entryLink(eid, p.id)}"><span class="step-number ${learned(eid) ? 'done' : ''}">${learned(eid) ? icon('check') : String(i+1).padStart(2,'0')}</span><div><span class="small muted">第 ${i+1} 小节 ${labs.some(l => l.entry === eid) ? '· 含互动实验' : ''}</span><h3>${entries.get(eid).zh}</h3><p>${lessons[eid].analogy}</p></div>${icon('arrow')}</a>`).join('')}</div><aside class="journey-note ${p.color}">${icon(p.icon)}<h3>不用一口气学完。</h3><p>每次 5 分钟，让一个问号变小一点。</p><strong>${progressCount(p)} / ${p.ids.length}</strong><progress max="${p.ids.length}" value="${progressCount(p)}" aria-label="路线完成进度"></progress><p class="small">进度保存在当前浏览器。完成小测后，记得点击「学会了」。</p><a class="btn primary" href="${entryLink(p.ids.find(id => !learned(id)) || p.ids[0], p.id)}">${progressCount(p) ? '继续学习' : '开始第一节'} ${icon('arrow')}</a></aside></div>`;
}
function explorePage() {
  return `${pageTitle('THE KNOWLEDGE ATLAS', '从一个词，走进一个世界。', '搜索中英文名称、生活关键词或正文。点击相关原理，还能发现跨领域的联系。')}<div class="explore-tabs"><button class="chip active" data-explore-tab="entries">${book.entries.length} 个科技词条</button><button class="chip" data-explore-tab="principles">${book.principles.length} 条底层原理</button></div><div id="entry-browser"><div class="filter-bar"><label class="catalog-search">${icon('search')}<input type="search" id="catalog-query" aria-label="搜索词条和正文" placeholder="试试「电池」「AI」「能量」" value="${esc(filter.query)}"></label><select id="domain-filter" aria-label="筛选领域"><option value="">全部领域</option>${book.domains.map(d => `<option value="${d.id}" ${filter.domain === d.id ? 'selected' : ''}>${d.zh}</option>`).join('')}</select><select id="tier-filter" aria-label="筛选词条"><option value="">所有词条</option><option value="A" ${filter.tier === 'A' ? 'selected' : ''}>核心图解</option><option value="lesson" ${filter.tier === 'lesson' ? 'selected' : ''}>入门导学</option></select></div><div id="catalog-results"></div></div><div id="principle-browser" hidden>${book.principle_groups.map(group => `<h2 class="group-heading">${group}</h2><div class="principle-grid">${book.principles.filter(p => p.group === group).map(p => `<a class="principle-card" href="#/principle/${p.id}"><h3>${p.zh} ${icon('arrow')}</h3><p>${esc(p.statement)}</p><span class="small muted">${p.entry_count} 个相关词条</span></a>`).join('')}</div>`).join('')}</div>`;
}
function entryCard(e) { return `<a class="entry-card" href="${entryLink(e.id)}"><div class="entry-meta"><span>${domains.get(e.domain).zh}</span>${learned(e.id) ? '<span class="learned-label">✓ 已学</span>' : `<span>${lessons[e.id] ? '入门导学' : e.tier === 'A' ? '核心图解' : '百科词条'}</span>`}</div><h3>${e.zh}</h3><span class="english-name">${esc(e.en)}</span><p>${esc(e.definition)}</p><div class="entry-card-foot"><span>${e.year ?? '—'} <small>· ${e.subcategory}</small></span>${icon('arrow')}</div></a>`; }
function updateCatalog() {
  const q = filter.query.trim().toLowerCase();
  const found = book.entries.filter(e => (!filter.domain || e.domain === filter.domain) && (!filter.tier || (filter.tier === 'lesson' ? !!lessons[e.id] : e.tier === filter.tier)) && (!q || `${e.zh} ${e.en} ${e.definition} ${Object.values(e.fields).join(' ')} ${e.principles.map(id => principles.get(id).zh).join(' ')}`.toLowerCase().includes(q)));
  const count = Math.ceil(found.length / 24); filter.page = Math.min(filter.page, count || 1);
  $('#catalog-results').innerHTML = `<div class="results-label" aria-live="polite">找到 ${found.length} 个词条${filter.domain && domains.has(filter.domain) ? ' · ' + domains.get(filter.domain).tagline : ''}</div>${found.length ? `<div class="entry-grid">${found.slice((filter.page-1)*24, filter.page*24).map(entryCard).join('')}</div><div class="pagination"><button class="btn secondary" data-page="-1" ${filter.page <= 1 ? 'disabled' : ''}>← 上一页</button><span>${filter.page} / ${count}</span><button class="btn secondary" data-page="1" ${filter.page >= count ? 'disabled' : ''}>下一页 →</button></div>` : '<div class="empty-state"><h3>这个问题还没有匹配的词条</h3><p>换一个短一点的词，或清除领域筛选再试试。</p><button class="btn secondary" id="clear-filters">清除筛选</button></div>'}`;
  $$('[data-page]').forEach(button => button.onclick = () => { filter.page += Number(button.dataset.page); updateCatalog(); $('#entry-browser').scrollIntoView({ block: 'start' }); });
  $('#clear-filters')?.addEventListener('click', () => { filter = { query: '', domain: '', tier: '', page: 1 }; $('#catalog-query').value = ''; $('#domain-filter').value = ''; $('#tier-filter').value = ''; updateCatalog(); });
}
function principlePage(id) {
  const p = principles.get(id); if (!p) return notFound();
  const related = book.entries.filter(e => e.principles.includes(id));
  return `<a class="back-link" href="#/explore">← 回到知识图谱</a>${pageTitle(p.en, p.zh, p.statement)}<div class="callout">${icon('spark')}<p>${p.group === '经济与系统' ? '这是一种理解技术与社会的分析框架，并非没有例外的自然定律。' : '抓住共同的原理，许多看似无关的技术就连接起来了。'}下面 ${related.length} 个词条用到了它。</p></div><div class="entry-grid">${related.map(entryCard).join('')}</div>`;
}
function entryPage(id, pathId) {
  const e = entries.get(id); if (!e) return notFound();
  const lesson = lessons[id]; const lab = labs.find(l => l.entry === id);
  const path = pathways.find(p => p.id === pathId && p.ids.includes(id));
  const next = path?.ids[path.ids.indexOf(id)+1];
  progress.last = id; save();
  return `<a class="back-link" href="${path ? '#/paths/' + path.id : '#/explore?domain=' + e.domain}">← ${path ? path.name : domains.get(e.domain).zh}</a><div class="article-layout"><article class="article"><div class="article-heading"><span class="eyebrow">${path ? `第 ${path.ids.indexOf(id)+1} / ${path.ids.length} 小节` : domains.get(e.domain).zh} · ${lesson ? '零基础导学' : '百科探索'}</span><h1>${e.zh}</h1><div class="article-en">${esc(e.en)}</div><p class="article-definition">${esc(e.definition)}</p></div>${lesson ? `<section class="analogy"><span class="eyebrow">先从生活里理解</span><p>${lesson.analogy}</p></section>` : ''}<section id="why"><h2><span>01</span> 为什么行得通</h2>${prose(e.fields['原理'])}<div class="principle-tags">${e.principles.map(id => `<a href="#/principle/${id}">${icon('spark')}${principles.get(id).zh} ↗</a>`).join('')}</div></section>${lab ? `<section id="experiment"><h2><span>02</span> 自己动手，试一次</h2><p class="muted">${lab.desc}</p><div class="inline-lab" data-lab="${lab.id}"></div></section>` : ''}<section id="how"><h2><span>${lab ? '03' : '02'}</span> 它是怎么工作的</h2>${prose(e.fields['怎么工作'] || e.fields['是什么'] || e.definition)}${e.figures.map(src => `<figure><a href="./${src}" target="_blank" rel="noopener"><img src="./${src}" alt="${e.zh}原理图" loading="lazy"></a><figcaption>${inline(e.fields['图注'] || e.zh + '图解')} · 点击放大</figcaption></figure>`).join('')}</section>${e.fields['注意'] ? `<section class="misconception"><span class="eyebrow">等等，别理解错了</span>${prose(e.fields['注意'])}</section>` : ''}${lesson ? `<section id="quiz"><h2><span>✓</span> 用一个问题，检验理解</h2><div class="quiz" data-quiz="${id}"><h3>${lesson.question}</h3><div class="quiz-options">${lesson.options.map((o,i) => `<button data-answer="${i}"><span>${String.fromCharCode(65+i)}</span>${o}</button>`).join('')}</div><div class="quiz-feedback" role="status">${progress.passed.includes(id) ? '之前已答对。你也可以再练一次。' : '选一个答案，看看你的理解。'}</div></div></section>` : ''}<details class="deep-read"><summary>再了解一点：历史与影响</summary><h3>关键年份与人物</h3>${prose(e.fields['年份人物'] || '本词条暂无补充说明。')}<h3>改变了什么</h3>${prose(e.fields['改变了'] || '本词条暂无补充说明。')}</details><section id="reflection"><h2>用自己的话，记下一点</h2><label for="entry-note" class="muted">试着回答：它解决了什么问题？生活中哪里会用到它？</label><textarea id="entry-note" data-note="${id}" maxlength="5000" rows="4" placeholder="比如：高压输电是为了减小电流，减少路上的发热损耗…">${esc(progress.notes[id] || '')}</textarea><span class="small muted" id="note-status">${storageOK ? '输入后自动保存在当前浏览器' : '当前无法持久保存，请导出备份'}</span></section><div class="lesson-complete"><button class="btn primary" data-complete="${id}">${learned(id) ? '✓ 已学会 · 点击撤销' : '我理解了，标记学会'} ${icon('check')}</button>${next ? `<a class="text-link" href="${entryLink(next,path.id)}">下一节：${entries.get(next).zh} ${icon('arrow')}</a>` : path ? `<a class="text-link" href="#/paths/${path.id}">查看路线进度 ${icon('arrow')}</a>` : ''}</div><p class="source-note">书稿来源：<a href="${repo}/blob/main/${domains.get(e.domain).source}" target="_blank" rel="noopener">${domains.get(e.domain).zh} ↗</a> · <a href="${repo}/blob/main/front/sources-${e.domain}.md" target="_blank" rel="noopener">核实记录 ↗</a>。原书的历史与数字沿用书稿核实时间；互动数值为教学模型。</p></article><aside class="article-aside"><div class="reading-guide"><span class="eyebrow">这一小节</span><a href="#why" data-scroll="why">为什么行得通</a>${lab ? '<a href="#experiment" data-scroll="experiment">动手试一试</a>' : ''}<a href="#how" data-scroll="how">怎么工作</a>${lesson ? '<a href="#quiz" data-scroll="quiz">检验理解</a>' : ''}<a href="#reflection" data-scroll="reflection">我的笔记</a><button class="btn secondary" data-save="${id}">${icon('bookmark')}${progress.saved.includes(id) ? '已收藏 · 取消' : '留着慢慢看'}</button></div><div class="related-box"><span class="eyebrow">顺着好奇心，继续走</span>${e.related.map(id => `<a href="${entryLink(id)}">${entries.get(id).zh} ${icon('arrow')}</a>`).join('')}</div></aside></div>`;
}
function labPage(id) {
  if (!id) return `${pageTitle('THE PLAYGROUND', '让知识，在你手里发生。', '拨一个开关，调一个参数，观察结果怎么改变。这里的实验不需要任何器材。')}<div class="lab-preview-grid">${labs.map(labCard).join('')}</div><div class="callout">${icon('lab')}<p>每个实验都是为了说明一个核心概念而简化的模型。先预测结果，再动手验证，最后试着说出为什么。</p></div>`;
  const l = labs.find(l => l.id === id); if (!l) return notFound();
  return `<a class="back-link" href="#/labs">← 所有互动实验</a>${pageTitle(l.tag + ' / INTERACTIVE LAB', l.title, l.desc)}<div class="standalone-lab" data-lab="${id}"></div><div class="lab-next"><p>看见变化之后，再把原理串起来。</p><a class="btn primary" href="${entryLink(l.entry)}">学习「${entries.get(l.entry).zh}」 ${icon('arrow')}</a></div>`;
}
function notebookPage() {
  const noted = Object.keys(progress.notes).filter(id => progress.notes[id].trim());
  return `${pageTitle('YOUR FIELD NOTES', '每一个懂了，都算数。', '学习进度、收藏和笔记保存在这个浏览器中。导出一份记录，就能备份或带到另一台设备。')}<div class="notebook-stats"><div><strong>${progress.learned.length}</strong>已学会的知识</div><div><strong>${progress.passed.length}</strong>答对的小测</div><div><strong>${progress.saved.length}</strong>收藏的好奇</div><div><strong>${noted.length}</strong>自己的想法</div></div><div class="backup-actions"><button class="btn secondary" id="export-progress">导出学习记录 ↓</button><label class="btn secondary import-button">导入记录 ↑<input id="import-progress" type="file" accept="application/json,.json"></label><span class="small muted">导入会合并记录；同一词条的笔记优先保留本机版本。</span></div>${!storageOK ? '<p class="storage-warning" role="alert">浏览器存储不可用。当前进度可能在关闭页面后丢失，请导出记录。</p>' : ''}${sectionHead('YOUR JOURNEYS', '正在走的路')}<div class="path-grid">${pathways.map(pathCard).join('')}</div><section class="home-section">${sectionHead('SAVED FOR LATER', '留着慢慢看')}<div class="entry-grid">${progress.saved.length ? progress.saved.map(id => entryCard(entries.get(id))).join('') : '<div class="empty-state compact"><p>在词条里点击「留着慢慢看」，就能在这里找到它。</p><a class="text-link" href="#/explore">去发现一个新问题 →</a></div>'}</div></section><section class="home-section">${sectionHead('IN YOUR OWN WORDS', '我的理解')}<div class="note-list">${noted.length ? noted.map(id => `<a class="note-card" href="${entryLink(id)}"><h3>${entries.get(id).zh} ↗</h3><p>${esc(progress.notes[id])}</p></a>`).join('') : '<p class="muted">读完一节，用自己的话写下理解。笔记会汇集在这里。</p>'}</div></section>${progress.learned.length ? `<section>${sectionHead('WHAT YOU KNOW', '已学会的知识')}<div class="entry-grid">${progress.learned.map(id => entryCard(entries.get(id))).join('')}</div></section>` : ''}<details class="reset-records"><summary>清空本机学习记录</summary><p>这会移除当前浏览器的进度、收藏和笔记。建议先导出备份。</p><button class="btn secondary" id="reset-progress">确认清空本机记录</button></details>`;
}
function notFound() { return `${pageTitle('A LITTLE DETOUR', '这条小路还没有通向知识。', '链接可能有误，回到首页换一个方向继续探索吧。')}<a class="btn primary" href="#/">返回探索首页 ${icon('arrow')}</a>`; }
function bindPage() {
  $$('[data-lab]').forEach(mountLab);
  if ($('#catalog-results')) {
    updateCatalog();
    for (const [selector, field] of [['#catalog-query', 'query'], ['#domain-filter', 'domain'], ['#tier-filter', 'tier']]) {
      $(selector).addEventListener(field === 'query' ? 'input' : 'change', event => {
        filter[field] = event.target.value; filter.page = 1; updateCatalog();
        const params = new URLSearchParams(); if (filter.query) params.set('q', filter.query); if (filter.domain) params.set('domain', filter.domain); if (filter.tier) params.set('tier', filter.tier);
        history.replaceState(null, '', '#/explore' + (params.size ? '?' + params : ''));
      });
    }
    $$('[data-explore-tab]').forEach(button => button.onclick = () => { $$('[data-explore-tab]').forEach(b => b.classList.toggle('active', b === button)); $('#entry-browser').hidden = button.dataset.exploreTab !== 'entries'; $('#principle-browser').hidden = button.dataset.exploreTab === 'entries'; });
  }
  $$('[data-scroll]').forEach(link => link.onclick = event => { event.preventDefault(); document.getElementById(link.dataset.scroll).scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' }); });
  $$('[data-save]').forEach(button => button.onclick = () => {
    const id = button.dataset.save; const exists = progress.saved.includes(id);
    progress.saved = exists ? progress.saved.filter(x => x !== id) : [...progress.saved, id]; save();
    button.innerHTML = `${icon('bookmark')}${exists ? '留着慢慢看' : '已收藏 · 取消'}`;
    toast(exists ? '已取消收藏' : '已放进「我的学习」');
  });
  $$('[data-complete]').forEach(button => button.onclick = () => {
    const id = button.dataset.complete;
    if (!learned(id) && lessons[id] && !progress.passed.includes(id)) { toast('先完成上面的小测，再标记学会吧。'); $('#quiz').scrollIntoView({ block: 'center' }); return; }
    progress.learned = learned(id) ? progress.learned.filter(x => x !== id) : [...progress.learned, id]; save(); render({keepScroll:true}); toast(learned(id) ? '又弄懂了一个小问题。进度已记录。' : '已撤销，可以再学一遍。');
  });
  $$('[data-quiz]').forEach(quiz => {
    const lesson = lessons[quiz.dataset.quiz];
    $$('[data-answer]', quiz).forEach(button => button.onclick = () => {
      const correct = Number(button.dataset.answer) === lesson.answer;
      $$('[data-answer]', quiz).forEach(b => { b.classList.remove('correct', 'incorrect'); b.setAttribute('aria-pressed', String(b === button)); });
      button.classList.add(correct ? 'correct' : 'incorrect');
      $('.quiz-feedback', quiz).className = `quiz-feedback ${correct ? 'correct' : 'incorrect'}`;
      $('.quiz-feedback', quiz).textContent = (correct ? '✓ 对，就是这样。' : '再想想。') + lesson.explanation;
      if (correct && !progress.passed.includes(quiz.dataset.quiz)) { progress.passed.push(quiz.dataset.quiz); save(); }
    });
  });
  $('#entry-note')?.addEventListener('input', event => { progress.notes[event.target.dataset.note] = event.target.value; save(); $('#note-status').textContent = storageOK ? '已自动保存' : '未能保存到浏览器，请导出记录'; });
  $('#reset-progress')?.addEventListener('click', () => { progress = normalizeProgress(null, entries.keys()); save(); render(); toast('本机记录已清空'); });
  $('#export-progress')?.addEventListener('click', () => {
    const blob = new Blob([JSON.stringify({version:1, exportedAt: new Date().toISOString(), ...progress}, null, 2)], {type:'application/json'});
    const url = URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = '原来如此-学习记录.json'; a.click(); setTimeout(() => URL.revokeObjectURL(url),1000); toast('学习记录已导出');
  });
  $('#import-progress')?.addEventListener('change', async event => {
    try {
      const file = event.target.files[0]; if (!file) return;
      if (file.size > 5_000_000) throw new Error('记录文件过大，请选择 5 MB 以内的文件');
      const raw = JSON.parse(await file.text());
      if (raw.version !== 1 || !Array.isArray(raw.learned) || !Array.isArray(raw.saved)) throw new Error('这不是有效的学习记录文件');
      const incoming = normalizeProgress(raw, entries.keys());
      for (const field of ['learned','saved','passed']) progress[field] = [...new Set([...progress[field], ...incoming[field]])];
      progress.notes = {...incoming.notes, ...progress.notes}; progress.last ||= incoming.last;
      save(); render({keepScroll:true}); toast('记录已合并');
    } catch (error) { toast(error instanceof SyntaxError ? '文件不是有效的 JSON，未导入记录。' : error.message); }
  });
}
function mountLab(root) {
  const id = root.dataset.lab; const compact = root.dataset.compact === 'true';
  if (id === 'logic') {
    let gate = 'AND', a = 0, b = 1;
    root.innerHTML = `${compact ? '' : '<p class="lab-instruction">先猜一猜：两个条件里只有一个成立，灯会亮吗？点击 A、B，再切换判断规则。</p>'}<div class="gate-tabs" role="group" aria-label="逻辑门规则">${['AND','OR','XOR'].map((g,i) => `<button data-gate="${g}" aria-pressed="${i === 0}" class="${i===0?'active':''}">${g} <span>${['与','或','异或'][i]}</span></button>`).join('')}</div><div class="logic-machine"><div class="logic-inputs"><div><span>A</span><button data-bit="a" aria-label="输入 A" aria-pressed="false" class="bit-switch"><span>0</span><i></i></button></div><div><span>B</span><button data-bit="b" aria-label="输入 B" aria-pressed="true" class="bit-switch on"><span>1</span><i></i></button></div></div><div class="logic-wires"><i></i><i></i></div><div class="gate-body"><span class="gate-name">AND</span><small>两个都要</small></div><div class="output-wire"></div><div class="bulb-output"><div class="bulb">${icon('bolt')}</div><span class="output-value">输出 0</span></div></div><div class="lab-observation" aria-live="polite"></div>${compact ? '<p class="try-hint">↑ 点一下开关，看看会发生什么</p>' : '<details class="truth-details"><summary>展开真值表，检查所有组合</summary><table><thead><tr><th>A</th><th>B</th><th>输出</th></tr></thead><tbody></tbody></table></details>'}`;
    function update() {
      const out = gateOutput(gate,a,b);
      for (const [key,v] of [['a',a],['b',b]]) { const button = $(`[data-bit="${key}"]`,root); button.classList.toggle('on',Boolean(v)); button.setAttribute('aria-pressed',String(Boolean(v))); $('span',button).textContent=v; }
      $('.gate-name',root).textContent=gate; $('.gate-body small',root).textContent={AND:'两个都要',OR:'至少一个',XOR:'恰好一个'}[gate];
      $('.bulb',root).classList.toggle('lit',Boolean(out)); $('.output-wire',root).classList.toggle('lit',Boolean(out));
      $('.output-value',root).textContent='输出 '+out;
      $('.lab-observation',root).textContent=`${a} ${gate} ${b} = ${out}。${{AND:'两个输入都是 1，灯才会亮。',OR:'至少一个输入是 1，灯就会亮。',XOR:'两个输入不同时，灯才会亮。'}[gate]}`;
      if ($('tbody',root)) $('tbody',root).innerHTML=[[0,0],[0,1],[1,0],[1,1]].map(([x,y])=>`<tr class="${x===a&&y===b?'current':''}"><td>${x}</td><td>${y}</td><td>${gateOutput(gate,x,y)}</td></tr>`).join('');
    }
    $$('[data-bit]',root).forEach(btn=>btn.onclick=()=>{if(btn.dataset.bit==='a')a=1-a;else b=1-b;update();});
    $$('[data-gate]',root).forEach(btn=>btn.onclick=()=>{gate=btn.dataset.gate;$$('[data-gate]',root).forEach(b=>{b.classList.toggle('active',b===btn);b.setAttribute('aria-pressed',String(b===btn));});update();});
    update();
  } else if (id === 'binary') {
    let bits = [0,0,0,0,0,1,0,1];
    root.innerHTML = `<p class="lab-instruction">把每个开关当成一盏灯。亮的灯贡献上方的数值，灭的灯贡献 0。</p><div class="binary-switches">${bits.map((bit,i)=>`<div><small>${2**(7-i)}</small><button data-binary="${i}" aria-label="数位 ${2**(7-i)}" aria-pressed="${!!bit}">${bit}</button></div>`).join('')}</div><div class="binary-result"><span>十进制数值</span><strong></strong><p></p></div><div class="lab-challenge">小挑战：拨出数字 <b>42</b>。<span role="status"></span></div><button class="btn secondary" data-reset>全部归零</button><p class="model-note">这里演示一个字节的无符号整数：从 0 到 255。</p>`;
    const update = () => {const n=binaryValue(bits);$$('[data-binary]',root).forEach((btn,i)=>{btn.textContent=bits[i];btn.classList.toggle('on',!!bits[i]);btn.setAttribute('aria-pressed',String(!!bits[i]));});$('.binary-result strong',root).textContent=n;$('.binary-result p',root).textContent=(bits.map((b,i)=>b?2**(7-i):0).filter(Boolean).join(' + ')||'0')+' = '+n;$('.lab-challenge span',root).textContent=n===42?'✓ 做到了！32 + 8 + 2 = 42。':'试着组合上面的数位。';};
    $$('[data-binary]',root).forEach(btn=>btn.onclick=()=>{bits[btn.dataset.binary]=1-bits[btn.dataset.binary];update();});$('[data-reset]',root).onclick=()=>{bits.fill(0);update();};update();
  } else if (id === 'circuit' || id === 'grid') {
    const circuit=id==='circuit';
    root.innerHTML=`<p class="lab-instruction">${circuit?'电压好比推动水流的压力差，电阻好比通道的阻碍。保持一个不变，试着改变另一个。':'保持输送功率 1000 kW、线路电阻 10 Ω 不变。把电压翻倍，预测损耗会变为多少。'}</p><div class="energy-display"><div class="energy-node">${icon('bolt')}<span>${circuit?'电源':'发电端'}</span></div><div class="energy-line"><i></i><span class="energy-flow"></span></div><div class="energy-node receiver">${icon('home')}<span>${circuit?'电阻负载':'用电端'}</span></div></div><div class="slider-control"><label>电压 <output class="voltage-output"></output><input type="range" data-voltage min="${circuit?1:10}" max="${circuit?24:100}" value="${circuit?12:10}" step="1" aria-label="电压"></label>${circuit?'<label>电阻 <output class="resistance-output"></output><input type="range" data-resistance min="1" max="100" value="10" aria-label="电阻"></label>':''}</div><div class="model-metrics"><div><span>电流</span><strong class="current-value"></strong></div><div><span>${circuit?'电阻消耗功率':'线路发热损耗'}</span><strong class="power-value"></strong></div></div><div class="lab-observation" aria-live="polite"></div><p class="model-note">${circuit?'理想直流电路，电阻恒定且忽略温度变化。I = U / R；P = U × I。真实灯泡的电阻可能随温度改变。':'简化教学模型：用 I = P / U 估算电流，线路损耗 = I²R；不模拟完整交流电网、变压器损耗和电压降。'}</p>`;
    function update(){const v=Number($('[data-voltage]',root).value);const r=circuit?Number($('[data-resistance]',root).value):10;const amps=circuit?circuitCurrent(v,r):transmissionLoss(v).amps;const power=circuit?v*amps:transmissionLoss(v).lossKW;$('.voltage-output',root).textContent=v+(circuit?' V':' kV');if(circuit)$('.resistance-output',root).textContent=r+' Ω';$('.current-value',root).textContent=amps.toFixed(2)+' A';$('.power-value',root).textContent=power.toFixed(2)+(circuit?' W':' kW');$('.energy-flow',root).textContent=amps.toFixed(2)+' A →';$('.energy-line',root).style.setProperty('--flow-speed',Math.max(.3,3/(amps+1))+'s');$('.lab-observation',root).textContent=circuit?`当前电流是 ${v} ÷ ${r} = ${amps.toFixed(2)} A。电阻不变时，提高电压会增大电流。`:`与 10 kV 时的 100 kW 损耗相比，现在的损耗是 ${(power/100*100).toFixed(1)}%。电压变为 ${v/10} 倍，损耗变为原来的 1 / ${(v/10)**2}。`;}
    $$('input',root).forEach(input=>input.oninput=update);update();
  } else if (id === 'gradient') {
    let x=4, steps=0, history=[4];
    root.innerHTML=`<p class="lab-instruction">把小球横向位置当成模型的一个参数，把高度当成误差。点击「走一步」，观察误差是变小还是变大。</p><div class="gradient-chart"><svg viewBox="0 0 600 280" role="img" aria-label="损失函数 L=x² 的曲线与参数位置"><defs><pattern id="chart-grid" width="50" height="40" patternUnits="userSpaceOnUse"><path d="M 50 0 L 0 0 0 40" fill="none" stroke="#dbe0d5" stroke-width="1"/></pattern></defs><rect x="30" y="20" width="540" height="225" fill="url(#chart-grid)"/><path d="M50 25Q300 465 550 25" fill="none" stroke="#5c7360" stroke-width="3"/><path d="M30 245h540M300 20v230" stroke="#bac4b7"/><text x="35" y="15">误差 L</text><text x="559" y="264">x</text><text x="306" y="262">0</text><polyline class="gradient-trail" fill="none" stroke="#ed825c" stroke-width="2" stroke-dasharray="5 5"/><circle class="gradient-ball" r="10" fill="#e87850" stroke="#fff" stroke-width="3"/></svg></div><label class="rate-control">学习率（步长） <output></output><input type="range" data-rate min="0.05" max="1.2" step="0.05" value="0.15" aria-label="学习率"></label><div class="lab-buttons"><button class="btn primary" data-step>走一步 ${icon('arrow')}</button><button class="btn secondary" data-reset>重新开始</button></div><div class="model-metrics"><div><span>已走步数</span><strong class="step-count"></strong></div><div><span>当前误差 x²</span><strong class="loss-value"></strong></div><div><span>参数 x</span><strong class="x-value"></strong></div></div><div class="lab-observation" aria-live="polite"></div><p class="model-note">一维教学模型：L(x) = x²，梯度是 2x；下一步 x = x − 学习率 × 2x。真实模型通常有很多参数，损失曲面也更复杂。曲线之外的位置会在边缘显示。</p>`;
    const update=()=>{const rate=Number($('[data-rate]',root).value);$('output',root).textContent=rate.toFixed(2);const plotted=Math.max(-5,Math.min(5,x));$('.gradient-ball',root).setAttribute('cx',300+plotted*50);$('.gradient-ball',root).setAttribute('cy',245-plotted*plotted*8.8);$('.gradient-trail',root).setAttribute('points',history.map(v=>Math.max(-5,Math.min(5,v))).map(v=>`${300+v*50},${245-v*v*8.8}`).join(' '));$('.step-count',root).textContent=steps;$('.loss-value',root).textContent=(x*x).toFixed(4);$('.x-value',root).textContent=x.toFixed(4);$('.lab-observation',root).textContent=Math.abs(x)<.01?'✓ 误差已经很小了。试试重置后把学习率调到 1.1，对比结果。':Math.abs(x)>1000?'参数已经发散，暂停计算。请重新开始，试试更小的学习率。':rate>=1?'当前步长会让参数在两侧振荡；大于 1 时，误差还会增大。':'当前步长能让误差逐渐下降。多走几步，看看会靠近哪里。';$('[data-step]',root).disabled=Math.abs(x)>1000||steps>=100;};
    $('[data-rate]',root).oninput=update;$('[data-step]',root).onclick=()=>{x=gradientStep(x,Number($('[data-rate]',root).value));steps++;history.push(x);update();};$('[data-reset]',root).onclick=()=>{x=4;steps=0;history=[4];update();};update();
  } else if (id === 'packets') {
    let received=[], step=0;const words=['科技','让','世界','相连'];const order=[2,0,3];
    root.innerHTML=`<p class="lab-instruction">我们发送「科技让世界相连」。先把它拆成四个编号包，模拟第 2 包丢失，其余包乱序到达。</p><div class="packet-sender"><span class="eyebrow">发送端 · 原消息</span><div class="packet-row">${words.map((w,i)=>`<span class="packet"><small>#${i+1}</small>${w}</span>`).join('')}</div></div><div class="network-track"><span>发送端</span><i></i><span>网络转发</span><i></i><span>接收端</span></div><div class="packet-receiver"><span class="eyebrow">接收端 · 到达顺序</span><div class="packet-row received-packets"></div></div><div class="lab-buttons"><button class="btn primary" data-send>接收下一个包</button><button class="btn secondary" data-retry disabled>请求重传缺失包</button><button class="btn secondary" data-reset>重置</button></div><div class="lab-observation" aria-live="polite"></div><p class="model-note">示意分组交换和 TCP 式的编号、重传、重排。IP 本身不保证有序可靠；这里每包用一个词块来帮助理解，真实网络按字节划分数据。</p>`;
    const update=()=>{$('.received-packets',root).innerHTML=received.length?received.map(i=>`<span class="packet"><small>#${i+1}</small>${words[i]}</span>`).join(''):'<span class="muted">还没有数据包到达</span>';$('[data-send]',root).disabled=step>=3;$('[data-retry]',root).disabled=step<3||received.includes(1);$('.lab-observation',root).textContent=received.length===4?'✓ 按编号重排后：'+[...received].sort().map(i=>words[i]).join('')+'。到达顺序不同，仍能还原消息。':step===3?'第 2 包没有到达，消息还不完整。请求重传后，再按编号拼起来。':`已接收 ${received.length} / 4 个包。顺序可能改变，编号帮助接收端识别位置。`;};
    $('[data-send]',root).onclick=()=>{received.push(order[step++]);update();};$('[data-retry]',root).onclick=()=>{received.push(1);update();};$('[data-reset]',root).onclick=()=>{received=[];step=0;update();};update();
  }
  if (!compact && labSources[id]) root.insertAdjacentHTML('beforeend',`<p class="lab-source">原理参考：<a href="${labSources[id][1]}" target="_blank" rel="noopener">${labSources[id][0]} ↗</a></p>`);
}

try {
  const response = await fetch('./book.json');
  if (!response.ok) throw new Error('资料加载失败');
  book = await response.json();
  entries = new Map(book.entries.map(e => [e.id, e]));
  principles = new Map(book.principles.map(p => [p.id, p]));
  domains = new Map(book.domains.map(d => [d.id, d]));
  let raw;
  try { raw = JSON.parse(localStorage.getItem(key) || '{}'); } catch { storageOK = false; }
  progress = normalizeProgress(raw, entries.keys());
  render();
  $('.skip-link').onclick = event => { event.preventDefault(); $('#main').focus(); };
  window.addEventListener('hashchange', () => render());
  document.addEventListener('keydown', event => {
    if (event.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) {
      event.preventDefault(); $('#global-search')?.focus();
    }
  });
} catch (error) {
  $('#app').innerHTML = '<div class="error-page"><h1>资料暂时没有打开</h1><p>请确认已运行 make web，并通过 make web-serve 打开网页。</p><button class="btn primary" id="reload">重新加载</button></div>';
  $('#reload').onclick = () => location.reload();
  console.error(error);
}
