// Whole-book navigation. Content comes from the same manuscript as the PDF.
export function createBookReader({book, entries, principles, domains, progress: getProgress, esc, icon, entryCard, pageTitle}) {
  const documents = new Map(book.documents.map(d => [d.id, d]));
  const title = key => {
    const [kind, id] = key.split('/');
    return kind === 'entry' ? entries.get(id)?.zh : kind === 'principle' ? principles.get(id)?.zh : kind === 'chapter' ? `第 ${domains.get(id)?.num} 篇 · ${domains.get(id)?.zh}` : kind === 'document' ? documents.get(id)?.title : ({book:'整本书',review:'复习自测',timeline:'大事年表',sources:'资料来源与核实记录','index/zh':'中文拼音索引','index/en':'English Index',master:'全书词条总表'})[key];
  };
  const href = key => '#/' + key;
  function safeLink(url) {
    return /^(?:https?:\/\/|#\/(?:entry|principle|chapter|document|book|sources|timeline|index|master)(?:\/|$))/.test(url) ? esc(url) : '#/book';
  }
  function inline(text) {
    const pattern = /\[\[([^\]|]+)(?:\|([^\]]+))?\]\]|\*\*(.+?)\*\*|`([^`]+)`|\[([^\]]+)\]\(([^\s)]+)\)|(https?:\/\/[^\s<>；，。)]+)|\b((?:[a-z0-9-]+\.)+(?:com|org|net|edu|gov|eu|ai|io|co|cn)\/[a-zA-Z0-9_./?=%&+#-]*)/g;
    let result = '', start = 0;
    for (const m of String(text).matchAll(pattern)) {
      result += esc(String(text).slice(start,m.index));
      if (m[1]) {
        const p = m[1].startsWith('p:'); const item = p ? principles.get(m[1].slice(2)) : entries.get(m[1]);
        result += item ? `<a href="#/${p ? 'principle/' + m[1].slice(2) : 'entry/' + m[1]}">${esc(m[2] || item.zh)}</a>` : esc(m[2] || m[1]);
      } else if (m[3]) result += '<strong>' + inline(m[3]) + '</strong>';
      else if (m[4]) result += '<code>' + esc(m[4]) + '</code>';
      else {
        const url = m[6] || m[7] || 'https://' + m[8];
        result += `<a href="${safeLink(url)}" ${url.startsWith('http') ? 'target="_blank" rel="noopener"' : ''}>${esc(m[5] || m[7] || m[8])}</a>`;
      }
      start = m.index + m[0].length;
    }
    return result + esc(String(text).slice(start));
  }
  function blocks(items, {skipTitle = false, prefix = 'block'} = {}) {
    return items.map((b,i) => {
      const id = `${prefix}-${i}`;
      if (b.type === 'heading') return b.level === 1 && skipTitle ? '' : `<h${Math.min(4, Math.max(2,b.level))} id="${id}">${inline(b.text)}</h${Math.min(4, Math.max(2,b.level))}>`;
      if (b.type === 'figure') return `<figure id="${id}" class="book-figure"><a href="./${b.src}" target="_blank" rel="noopener"><img src="./${b.src}" alt="${esc(b.src.split('/').slice(-2).join(' / '))} 知识图解"></a><figcaption>原书图解 · 点击打开大图</figcaption></figure>`;
      if (b.type === 'list') { const tag = b.ordered ? 'ol' : 'ul'; return `<${tag} id="${id}">${b.items.map(item=>`<li>${inline(item)}</li>`).join('')}</${tag}>`; }
      if (b.type === 'table') return `<div class="book-table-wrap" id="${id}" tabindex="0" role="region" aria-label="书稿表格，可以左右滚动"><table class="book-table"><thead><tr>${b.rows[0].map(c=>`<th scope="col">${inline(c)}</th>`).join('')}</tr></thead><tbody>${b.rows.slice(1).map(row=>`<tr>${row.map(c=>`<td>${inline(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
      if (b.type === 'code') return `<pre id="${id}"><code>${esc(b.text)}</code></pre>`;
      return `<p id="${id}">${inline(b.text)}</p>`;
    }).join('');
  }
  function bookshelf() {
    const p = getProgress(); const count = Object.values(p.reading).filter(r=>r.finished).length;
    return `<section class="book-cover"><div><span class="eyebrow">THE COMPLETE EDITION · 1700–2026</span><h1>一整本科技史，<br>随时翻到你这一页。</h1><p>全部 17 篇正文、导读与知识地图，连同年表、来源和中英文索引，完整收在这里。</p><div class="hero-actions"><a class="btn primary" href="${p.lastRead ? href(p.lastRead) + '?resume=1' : '#/document/howto'}">${p.lastRead ? '继续阅读：' + esc(title(p.lastRead)) : '从阅读指南开始'} ${icon('arrow')}</a></div><span class="small muted">${count} / ${book.readingOrder.length} 个阅读小节已读 · ${book.coverage.figures.length} 张原书图解</span></div><img src="./cover.svg" alt="近现代科技百科全书封面"></section>
      <div class="book-quick-links">${[['document/howto','怎么读这本书','先找到适合自己的读法'],['document/map','全书地图','看见 17 个领域之间的联系'],['document/principles-intro','第一性原理','59 条反复出现的规律'],['timeline','大事年表','沿着时间理解技术的变化'],['index/zh','中文拼音索引','从名字找到一个知识'],['index/en','English Index','中英文术语对照'],['sources','资料来源','核实记录与延伸阅读'],['master','词条总表','按领域和子类查阅']].map(([key,name,desc])=>`<a href="${href(key)}"><strong>${name} ${icon('arrow')}</strong><span>${desc}</span></a>`).join('')}</div>
      <div class="section-head"><div><span class="eyebrow">SEVENTEEN CONNECTED CHAPTERS</span><h2>按篇，慢慢读完整本书。</h2></div></div><div class="chapter-grid">${book.domains.map(d=>{const read=book.entries.filter(e=>e.domain===d.id&&p.reading['entry/'+e.id]?.finished).length;return `<a class="chapter-card" href="#/chapter/${d.id}"><span class="chapter-number">${String(d.num).padStart(2,'0')}</span><div><h3>${d.zh}</h3><p>${d.tagline}</p><div class="chapter-card-progress"><progress max="${d.count}" value="${read}" aria-label="${d.zh}阅读进度"></progress><span>${read} / ${d.count} 已读</span></div></div>${icon('arrow')}</a>`;}).join('')}</div><p class="source-note">© 2026 Teancum Tian · 保留所有权利。网页沿用原书稿及其核实时间；阅读小节不是 PDF 页码。</p>`;
  }
  function chapter(id) {
    const d = domains.get(id); if (!d) return null;
    const p = getProgress(); const list = book.entries.filter(e=>e.domain===id);
    const next = list.find(e=>!p.reading['entry/'+e.id]?.finished) || list[0];
    return `<a class="back-link" href="#/book">← 整本书目录</a>${pageTitle('CHAPTER '+String(d.num).padStart(2,'0')+' / '+d.en, d.zh,d.tagline)}<div class="chapter-actions"><a class="btn primary" href="#/entry/${next.id}?resume=1">${next===list[0]?'开始阅读':'继续本篇'} ${icon('arrow')}</a><a class="btn secondary" href="#/review?domain=${id}">本篇翻卡自测</a><a class="text-link" href="#/document/sources-${id}">资料来源 →</a></div><article class="book-prose reading-unit">${blocks(d.intro,{prefix:'intro'})}${blocks(d.outro,{prefix:'outro'})}</article><section class="chapter-directory"><h2>本篇 ${d.count} 个词条</h2>${d.subcategories.map((sub,i)=>`<details class="chapter-category" ${i===0?'open':''}><summary>${sub}<small>${list.filter(e=>e.subcategory===sub).length} 个词条</small></summary><div class="chapter-entry-list">${list.filter(e=>e.subcategory===sub).map(e=>`<a href="#/entry/${e.id}"><span class="read-dot ${p.reading['entry/'+e.id]?.finished?'done':''}">${p.reading['entry/'+e.id]?.finished?'✓':e.tier==='A'?'★':'·'}</span><span>${e.zh}<small>${esc(e.en)}</small></span>${icon('arrow')}</a>`).join('')}</div></details>`).join('')}</section>`;
  }
  function documentPage(id) {
    const doc = documents.get(id); if (!doc) return null;
    return `<a class="back-link" href="${id.startsWith('sources-')?'#/sources':'#/book'}">← ${id.startsWith('sources-')?'全部资料来源':'整本书目录'}</a>${pageTitle(id.startsWith('sources-')?'SOURCES & VERIFICATION':'FROM THE MANUSCRIPT',doc.title,'原书内容完整呈现；提到的页码与版式指纸书 / PDF，网页使用链接跳转。')}<article class="book-prose reading-unit ${id.startsWith('sources-')?'source-document':''}">${blocks(doc.blocks,{skipTitle:true})}</article>${id==='principles-intro'?`<div class="principle-grid">${book.principles.map(p=>`<a class="principle-card" href="#/principle/${p.id}"><h3>${p.zh} ${icon('arrow')}</h3><p>${esc(p.statement)}</p></a>`).join('')}</div>`:''}`;
  }
  function sourcesPage() {
    return `${pageTitle('APPENDIX II','资料来源与核实记录','保留每篇的原始来源、批量核对方法、未通过项处理、收词范围与延伸阅读。内容在本机即可阅读，外部参考链接联网后访问。')}<article class="reading-unit"><div class="callout"><p>2025–2026 年的数据沿用原书注明的访问时间。这里记录的是书稿已有核实过程，本次网页化未重新核实全部历史与数字。</p></div><div class="chapter-grid">${book.domains.map(d=>`<a class="chapter-card" href="#/document/sources-${d.id}"><span class="chapter-number">${String(d.num).padStart(2,'0')}</span><div><h3>${d.zh}</h3><p>原始来源 · 核实与更正 · 延伸阅读</p></div>${icon('arrow')}</a>`).join('')}</div></article>`;
  }
  const dated = book.entries.filter(e=>Number.isInteger(e.year)).sort((a,b)=>a.year-b.year || domains.get(a.domain).num-domains.get(b.domain).num || a.order-b.order);
  function timelinePage() {
    return `${pageTitle('APPENDIX I','一条时间线，许多次世界的改变。',`共 ${dated.length} 个具有关键起点年份的词条。年份表示发明、首次演示或首次商用之一，完整背景请进入词条阅读。`)}<div class="filter-bar"><label class="catalog-search">${icon('search')}<input type="search" id="timeline-query" aria-label="搜索年表" placeholder="搜索技术名称…"></label><select id="timeline-domain" aria-label="年表领域"><option value="">全部领域</option>${book.domains.map(d=>`<option value="${d.id}">${d.zh}</option>`).join('')}</select><select id="timeline-era" aria-label="年表年代"><option value="">全部年代</option><option value="0,1799">1799 年及以前</option><option value="1800,1869">1800–1869</option><option value="1870,1913">1870–1913</option><option value="1914,1945">1914–1945</option><option value="1946,1969">1946–1969</option><option value="1970,1999">1970–1999</option><option value="2000,2100">2000–2026</option></select></div><article class="reading-unit" id="timeline-results"></article>`;
  }
  function timelineResults(query='',domain='',era='') {
    const [min,max] = era ? era.split(',').map(Number) : [-Infinity,Infinity];
    const found = dated.filter(e=>(!domain||e.domain===domain)&&e.year>=min&&e.year<=max&&`${e.zh} ${e.en}`.toLowerCase().includes(query.toLowerCase()));
    const years = [...new Set(found.map(e=>e.year))];
    return `<p class="results-label" role="status">${found.length} 项技术 · ${years.length} 个年份</p>${years.map(year=>`<section class="timeline-year" id="year-${year}"><h2>${year}</h2><div>${found.filter(e=>e.year===year).map(e=>`<a class="timeline-event" href="#/entry/${e.id}"><span class="small muted">${domains.get(e.domain).zh}${e.tier==='A'?' · ★ 核心':''}</span><h3>${e.zh}</h3><p>${esc(e.definition)}</p></a>`).join('')}</div></section>`).join('') || '<div class="empty-state">这个范围里没有匹配的词条，试试清空搜索或切换年代。</div>'}`;
  }
  function indexPage(language) {
    const en=language==='en';
    return `${pageTitle(en?'APPENDIX IV':'APPENDIX III',en?'English Index':'中文关键词索引',en?'按英文 A–Z 排序，忽略词首 The / A / An。每条附中文名，直接进入全文。':'使用原书的拼音排序键，支持输入中文、拼音或英文。每条附英文名。')}<div class="index-mode"><a class="chip ${en?'':'active'}" href="#/index/zh">中文拼音</a><a class="chip ${en?'active':''}" href="#/index/en">English A–Z</a></div><label class="catalog-search index-search">${icon('search')}<input type="search" id="index-query" aria-label="搜索中英文索引" placeholder="${en?'Search a term…':'输入名称或拼音，例如 dian chi'}"></label><article class="reading-unit" id="index-results" data-language="${en?'en':'zh'}"></article>`;
  }
  function indexResults(language,query='') {
    const en=language==='en';
    const englishKey=e=>e.en.trim().replace(/^(the|a|an)\s+/i,'').toLowerCase();
    const letter=e=>en?(/^[a-z]/.test(englishKey(e))?englishKey(e)[0].toUpperCase():'#'):e.index.letter;
    const order=e=>en?englishKey(e):e.index.key;
    const q=query.toLowerCase().trim();
    const found=book.entries.filter(e=>`${e.zh} ${e.en} ${e.index.key} ${e.index.key.replaceAll(' ','')}`.toLowerCase().includes(q)).sort((a,b)=>letter(a).localeCompare(letter(b),'en') || order(a).localeCompare(order(b),'en'));
    const groups=[...new Set(found.map(letter))];
    return `<p class="results-label" role="status">${found.length} 个词条</p><nav class="alphabet-nav" aria-label="字母导航">${groups.map(l=>`<a href="#letter-${l}" data-jump="letter-${l}">${l==='#'?'0–9':l}</a>`).join('')}</nav>${groups.map(l=>`<section class="index-letter" id="letter-${l}"><h2>${l==='#'?'0–9':l}</h2><div class="index-entries">${found.filter(e=>letter(e)===l).map(e=>`<a href="#/entry/${e.id}"><strong>${esc(en?e.en:e.zh)}</strong><span>${esc(en?e.zh:e.en)}</span></a>`).join('')}</div></section>`).join('') || '<div class="empty-state">没有找到匹配的名称，请换一个关键词。</div>'}`;
  }
  function masterPage() {
    return `${pageTitle('COMPLETE CATALOG','全书词条总表','按领域和子类查阅全部词条。A / B / C 表示原书篇幅等级；关键年份和中英文定义均来自原书数据。')}<article class="reading-unit">${book.domains.map(d=>`<section class="master-domain" id="master-${d.id}"><h2><a href="#/chapter/${d.id}">${String(d.num).padStart(2,'0')} ${d.zh} ↗</a></h2>${d.subcategories.map((sub,i)=>`<details class="chapter-category" ${i===0?'open':''}><summary>${sub}</summary><div class="book-table-wrap" tabindex="0" role="region" aria-label="${sub}词条表"><table class="book-table"><thead><tr><th>名称 / Name</th><th>年份 · 等级</th><th>是什么</th></tr></thead><tbody>${book.entries.filter(e=>e.domain===d.id&&e.subcategory===sub).map(e=>`<tr><td><a href="#/entry/${e.id}">${e.zh}<small>${esc(e.en)}</small></a></td><td>${e.year??'—'} · ${e.tier}</td><td>${esc(e.definition)}</td></tr>`).join('')}</tbody></table></div></details>`).join('')}</section>`).join('')}</article>`;
  }
  return {bookshelf,chapter,documentPage,sourcesPage,timelinePage,timelineResults,indexPage,indexResults,masterPage,blocks,inline,title};
}
