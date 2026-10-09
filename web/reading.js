export function createReadingController({book, getProgress, save, title, esc, icon, changeLanguage}) {
  let active = null, dirty = false, ready = false, generation = 0, timer;
  const readingTop=()=>Math.max(145,(document.querySelector('.reader-toolbar')?.getBoundingClientRect().height||0)+16);
  function measure() {
    const fraction = Math.min(1, Math.max(0, scrollY / Math.max(1,document.documentElement.scrollHeight-innerHeight)));
    const candidates = [...document.querySelectorAll('.reading-unit [id], .article section[id], .timeline-year[id], .index-letter[id]')];
    let anchor = '', offset = 0; const top=readingTop();
    for (const element of candidates) {
      const r = element.getBoundingClientRect();
      if (r.height && r.top <= top) { anchor = element.id; offset = Math.max(0,Math.min(1,(top-r.top)/r.height)); }
    }
    return {fraction,anchor,offset};
  }
  function capture() {
    clearTimeout(timer);
    if (!active || !ready || !dirty) return;
    const p=getProgress(), previous=p.reading[active]||{}, position=measure();
    p.reading[active]={...previous,...position,maxFraction:Math.max(previous.maxFraction||0,position.fraction),finished:previous.finished||false,updatedAt:Date.now()};
    p.lastRead=active; dirty=false; save();
    const out=document.querySelector('[data-reading-percent]'); if(out)out.textContent=Math.round(position.fraction*100)+'%';
  }
  window.addEventListener('scroll',()=>{if(active&&ready){dirty=true;clearTimeout(timer);timer=setTimeout(capture,250);}},{passive:true});
  window.addEventListener('pagehide',capture);
  document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='hidden')capture();});
  async function restore(record, run) {
    ready=false;
    // Images have intrinsic sizes; waiting for them keeps anchors reliable across browsers.
    await Promise.all([...document.querySelectorAll('.reading-unit img,.article img')].filter(img=>!img.closest('details:not([open])')).map(img=>img.complete?Promise.resolve():new Promise(resolve=>{img.addEventListener('load',resolve,{once:true});img.addEventListener('error',resolve,{once:true});setTimeout(resolve,1600);})));
    if(run!==generation)return;
    const node=record.anchor&&document.getElementById(record.anchor);
    const y=node?scrollY+node.getBoundingClientRect().top+(record.offset||0)*node.getBoundingClientRect().height-readingTop():(record.fraction||0)*Math.max(0,document.documentElement.scrollHeight-innerHeight);
    window.scrollTo({top:Math.max(0,y),behavior:'instant'});
    requestAnimationFrame(()=>{if(run===generation){ready=true;dirty=false;}});
  }
  function mount(key, params, keepScroll=false) {
    active=null;ready=false;dirty=false; const run=++generation;
    document.body.classList.toggle('reader-large',getProgress().prefs.fontSize==='large');
    document.body.classList.toggle('reader-focus',getProgress().prefs.focus&&book.readingOrder.includes(key));
    if(!book.readingOrder.includes(key))return;
    active=key;
    const p=getProgress(), saved=p.reading[key];
    const index=book.readingOrder.indexOf(key), prev=book.readingOrder[index-1], next=book.readingOrder[index+1];
    const done=saved?.finished===true;
    const html=`<div class="reader-toolbar"><a class="reader-directory" href="#/book">${icon('book')} 全书目录</a><span class="reader-position">${index+1} / ${book.readingOrder.length}</span><span class="reader-save" data-sync-status></span><label class="reader-font">字号<select id="reader-font" aria-label="阅读字号"><option value="normal" ${p.prefs.fontSize==='normal'?'selected':''}>标准</option><option value="large" ${p.prefs.fontSize==='large'?'selected':''}>大字</option></select></label><button class="reader-focus-button" id="reader-focus" aria-pressed="${p.prefs.focus}">${p.prefs.focus?'退出专注':'专注阅读'}</button></div>${saved?.fraction>.03&&!keepScroll?`<div class="resume-position"><span>上次读到本节 <b data-reading-percent>${Math.round(saved.fraction*100)}%</b></span><button id="restore-position">回到上次位置 ↓</button></div>`:''}`;
    document.querySelector('main').insertAdjacentHTML('afterbegin',html);
    document.querySelector('.reader-toolbar').insertAdjacentHTML('beforeend',`<label class="reader-language language-picker" data-no-translate><span class="sr-only">语言 / Language</span><select id="reader-language" aria-label="语言 / Language">${[['zh','中文'],['en','English'],['bi','中英对照']].map(([value,label])=>`<option value="${value}" ${p.prefs.language===value?'selected':''}>${label}</option>`).join('')}</select></label>`);
    document.querySelector('#reader-language').onchange=event=>changeLanguage?.(event.target.value);
    document.querySelector('main').insertAdjacentHTML('beforeend',`<div class="reader-end"><div><span class="eyebrow">读完这一节，给自己一个小记号</span><button class="btn ${done?'secondary':'primary'}" id="mark-read" aria-pressed="${done}">${done?'✓ 已读 · 点击撤销':'标记本节已读'} ${icon('check')}</button></div><p>「已读」记录阅读进度；「学会」和复习自测单独记录。</p></div><nav class="book-pagination" aria-label="全书前后节导航">${prev?`<a href="#/${prev}"><small>← 上一节</small><strong>${esc(title(prev))}</strong></a>`:'<span></span>'}${next?`<a href="#/${next}"><small>下一节 →</small><strong>${esc(title(next))}</strong></a>`:'<a href="#/book"><small>全书目录</small><strong>回看你的阅读足迹 →</strong></a>'}</nav>`);
    document.querySelector('#reader-font').onchange=event=>{p.prefs.fontSize=event.target.value;document.body.classList.toggle('reader-large',p.prefs.fontSize==='large');save();};
    document.querySelector('#reader-focus').onclick=event=>{p.prefs.focus=!p.prefs.focus;document.body.classList.toggle('reader-focus',p.prefs.focus);event.currentTarget.textContent=p.prefs.focus?'退出专注':'专注阅读';event.currentTarget.setAttribute('aria-pressed',String(p.prefs.focus));save();};
    document.querySelector('#restore-position')?.addEventListener('click',()=>restore(saved,run));
    document.querySelector('#mark-read').onclick=event=>{
      const record=p.reading[key]||{}; record.finished=!record.finished; record.updatedAt=Date.now();
      p.reading[key]={fraction:0,maxFraction:0,anchor:'',offset:0,...record}; p.lastRead=key;save();
      event.currentTarget.innerHTML=(record.finished?'✓ 已读 · 点击撤销':'标记本节已读')+' '+icon('check');
      event.currentTarget.setAttribute('aria-pressed',String(record.finished));
    };
    p.lastRead=key;
    if(!saved)p.reading[key]={fraction:0,maxFraction:0,anchor:'',offset:0,finished:false,updatedAt:Date.now()};
    save();
    if(params.get('resume')==='1'&&saved&&!keepScroll)restore(saved,run);
    else requestAnimationFrame(()=>{if(run===generation)ready=true;});
  }
  return {capture,mount};
}
