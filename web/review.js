import {nextReview} from './models.js';
export function createReview({book, entries, domains, lessons, getProgress, save, esc, icon, pageTitle}) {
  let queue=[], position=0, revealed=false, completed=0;
  function page(params) {
    const domain=params.get('domain')||'',mode=params.get('mode')||'all';
    return `${pageTitle('ACTIVE RECALL','把「看过」，变成能自己说出来。','先回想，再翻卡核对原文。你可以复习任意词条，也可以专练收藏、错题或到期内容。')}<div class="filter-bar review-filters"><select id="review-domain" aria-label="复习领域"><option value="">全部领域</option>${book.domains.map(d=>`<option value="${d.id}" ${d.id===domain?'selected':''}>${d.zh}</option>`).join('')}</select><select id="review-mode" aria-label="复习范围"><option value="all" ${mode==='all'?'selected':''}>全部词条</option><option value="read" ${mode==='read'?'selected':''}>已经读过</option><option value="saved" ${mode==='saved'?'selected':''}>我的收藏</option><option value="due" ${mode==='due'?'selected':''}>到期复习</option><option value="mistakes" ${mode==='mistakes'?'selected':''}>小测错题</option></select><button class="btn secondary" id="shuffle-review">换一组词条 ↻</button></div><section id="review-session" class="review-session"></section><p class="model-note">翻卡采用自评，不会替你标记「学会」。想起来的词条安排在 1、3、7、15、30 天后再看；需要巩固的词条 10 分钟后再看。这是固定复习规则，不是记忆能力诊断。</p>`;
  }
  function buildQueue() {
    const p=getProgress(), domain=document.querySelector('#review-domain').value, mode=document.querySelector('#review-mode').value;
    queue=book.entries.filter(e=>(!domain||e.domain===domain)&&(mode==='all'||mode==='read'&&p.reading['entry/'+e.id]?.finished||mode==='saved'&&p.saved.includes(e.id)||mode==='due'&&p.review[e.id]?.due<=Date.now()||mode==='mistakes'&&p.mistakes.includes(e.id)&&lessons[e.id]));
    // Fisher–Yates: sample without duplicates; each session stays short enough to finish.
    for(let i=queue.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[queue[i],queue[j]]=[queue[j],queue[i]];}
    queue=queue.slice(0,10);position=0;completed=0;revealed=false;renderCard();
    const params=new URLSearchParams();if(domain)params.set('domain',domain);if(mode!=='all')params.set('mode',mode);
    history.replaceState(null,'','#/review'+(params.size?'?'+params:''));
  }
  function renderCard() {
    const root=document.querySelector('#review-session');const mode=document.querySelector('#review-mode').value;
    if(!queue.length){root.innerHTML='<div class="empty-state"><h3>这一组暂时没有词条</h3><p>可以换成「全部词条」，或先阅读、收藏几个感兴趣的知识。</p><a class="btn primary" href="#/book">去读一小节 →</a></div>';return;}
    if(position>=queue.length){root.innerHTML=`<div class="review-finish"><span class="eyebrow">A LITTLE BETTER THAN BEFORE</span><h2>这一轮，完成了 ${completed} 次回想。</h2><p>慢慢来。下次回来，待复习清单会记得它们。</p><button class="btn primary" id="another-review">再来一组 ${icon('arrow')}</button><a class="text-link" href="#/notebook">查看我的学习 →</a></div>`;document.querySelector('#another-review').onclick=buildQueue;return;}
    const e=queue[position],lesson=lessons[e.id];revealed=false;
    root.innerHTML=`<div class="review-counter"><span>${domains.get(e.domain).zh}</span><span>${position+1} / ${queue.length}</span></div><article class="recall-card"><span class="eyebrow">${mode==='mistakes'?'再试一次，不急着看答案':'先不用查，试着说给自己听'}</span><h2>${e.zh}</h2><span class="article-en">${esc(e.en)}</span>${mode==='mistakes'?`<h3>${lesson.question}</h3><div class="quiz-options">${lesson.options.map((o,i)=>`<button data-review-answer="${i}">${String.fromCharCode(65+i)} · ${o}</button>`).join('')}</div><div class="review-feedback" role="status"></div>`:`<p>它解决了什么问题？<br>你能用一个生活例子解释它的原理吗？</p><button class="btn primary" id="reveal-card">翻开原文，核对理解 ${icon('arrow')}</button><div id="recall-answer" hidden><h3>是什么</h3><p>${esc(e.definition)}</p><h3>为什么行得通</h3><p>${esc(e.fields['原理'].replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(_,id,label)=>label||entries.get(id)?.zh||book.principles.find(p=>p.id===id.slice(2))?.zh||id))}</p></div><div class="rating-buttons" hidden><button class="btn secondary" data-rating="again">还需巩固 · 10 分钟后</button><button class="btn primary" data-rating="know">我能解释 · 稍后复习 ✓</button></div>`}<a class="text-link recall-source" href="#/entry/${e.id}">回到完整词条 ${icon('arrow')}</a></article>`;
    document.querySelector('#reveal-card')?.addEventListener('click',event=>{revealed=true;event.currentTarget.hidden=true;document.querySelector('#recall-answer').hidden=false;document.querySelector('.rating-buttons').hidden=false;});
    root.querySelectorAll('[data-rating]').forEach(button=>button.onclick=()=>{if(!revealed)return;getProgress().review[e.id]=nextReview(getProgress().review[e.id],button.dataset.rating);save();completed++;position++;renderCard();});
    root.querySelectorAll('[data-review-answer]').forEach(button=>button.onclick=()=>{
      const correct=Number(button.dataset.reviewAnswer)===lesson.answer;
      root.querySelectorAll('[data-review-answer]').forEach(b=>b.classList.remove('correct','incorrect'));
      button.classList.add(correct?'correct':'incorrect');
      document.querySelector('.review-feedback').textContent=(correct?'✓ 这次理解对了。':'再想一想。')+lesson.explanation;
      if(correct){const p=getProgress();p.mistakes=p.mistakes.filter(id=>id!==e.id);if(!p.passed.includes(e.id))p.passed.push(e.id);save();root.querySelectorAll('[data-review-answer]').forEach(b=>b.disabled=true);document.querySelector('.review-feedback').insertAdjacentHTML('afterend','<button class="btn primary" id="next-mistake">下一题 →</button>');document.querySelector('#next-mistake').onclick=()=>{completed++;position++;renderCard();};}
    });
  }
  function bind() {
    if(!document.querySelector('#review-session'))return;
    document.querySelector('#review-domain').onchange=buildQueue;
    document.querySelector('#review-mode').onchange=buildQueue;
    document.querySelector('#shuffle-review').onclick=buildQueue;
    buildQueue();
  }
  return {page,bind};
}
