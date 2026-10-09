// Published, versioned translations only. Reading never contacts a translation API.
export const LANGUAGES = ['zh', 'en', 'bi'];
let language = 'zh', catalog = {}, patterns = [];
const han = /[\u3400-\u9fff]/;
const escapePattern = text => text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
export function configureLanguage(values, selected = 'zh') {
  catalog = Object.fromEntries(Object.entries(values).map(([key,value])=>[key.trim(),value.trim()]));
  language = LANGUAGES.includes(selected) ? selected : 'zh';
  patterns = Object.entries(catalog).filter(([source]) => /\{\d+\}/.test(source))
    .sort((a,b) => b[0].replace(/\{\d+\}/g,'').length-a[0].replace(/\{\d+\}/g,'').length)
    .map(([source,target]) => {
      const ids = [...source.matchAll(/\{(\d+)\}/g)].map(m=>m[1]);
      const chunks=source.split(/\{\d+\}/);
      const re = new RegExp('^'+chunks.map(part=>escapePattern(part).replace(/\s+/g,'\\s*')).join('(.*?)')+'$','s');
      return {re, ids, target, literals:chunks.map(s=>s.trim()).filter(Boolean)};
    });
}
export const currentLanguage = () => language;
export const isBilingual = () => language === 'bi';
export function english(text, depth = 0) {
  const value=String(text ?? '');
  if(!han.test(value)) return value.replace(/[。！？]/g,mark=>({'。':'. ','！':'!','？':'?'}[mark]));
  const trimmed=value.trim();
  if(Object.hasOwn(catalog,trimmed)) return value.replace(trimmed,catalog[trimmed]);
  if(value.includes('\n')) return value.split('\n').map(line=>english(line,depth)).join('\n');
  if(depth<4) for(const {re,ids,target,literals} of patterns) {
    if(literals.some(part=>!trimmed.includes(part)))continue;
    const match=trimmed.match(re); if(!match)continue;
    const replacements=Object.fromEntries(ids.map((id,i)=>[id,english(match[i+1],depth+1)]));
    return value.replace(trimmed,target.replace(/\{(\d+)\}/g,(_,id)=>replacements[id] ?? ''));
  }
  if(depth<4 && /[。！？]/.test(value)) {
    const parts=value.match(/[^。！？]*[。！？]|[^。！？]+$/g)||[];
    if(parts.length>1) return parts.map(part=>english(part,depth+1)).join(' ');
    const mark=value.slice(-1), body=value.slice(0,-1);
    if(!han.test(body))return body+({'。':'.','！':'!','？':'?'}[mark]||mark);
  }
  if(depth<4) {
    const decorated=trimmed.match(/^([←↗✓★·\s]*)(.*?)([\s→↗↓↑]*)$/s);
    if(decorated && (decorated[1]||decorated[3]) && decorated[2]!==trimmed) {
      const translated=english(decorated[2],depth+1);
      if(translated!==decorated[2])return value.replace(trimmed,decorated[1]+translated+decorated[3]);
    }
    for(const separator of [' · ',' / ']) {
      const pieces=value.split(separator);
      if(pieces.length>1)return pieces.map(part=>english(part,depth+1)).join(separator);
    }
  }
  return value;
}
export function translateTree(value) {
  if(typeof value==='string')return english(value);
  if(Array.isArray(value))return value.map(translateTree);
  if(value && typeof value==='object')return Object.fromEntries(Object.entries(value).map(([key,item])=>[key,
    ['id','src','source','file','index','coverage','readingOrder'].includes(key)?item:translateTree(item)]));
  return value;
}
export function paired(text, formatter) {
  if(!isBilingual() || !han.test(String(text))) return formatter(text,language==='en');
  const translated=english(text);
  if(translated===text || han.test(translated))return formatter(text,false);
  return `<span class="parallel-text" data-no-translate><span lang="zh-CN">${formatter(text,false)}</span><span class="translation-en" lang="en">${formatter(translated,true)}</span></span>`;
}
export function parallelFigure(src, alt = 'English diagram') {
  if(!isBilingual())return '';
  // src comes exclusively from the validated figure inventory in book.json.
  const safe=String(src).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  return `<details class="parallel-figure" data-no-translate><summary lang="en">English diagram ↗</summary><a href="./en/${safe}" target="_blank" rel="noopener"><img src="./en/${safe}" alt="English diagram" loading="lazy"></a></details>`;
}

let observer;
const localizedOptions = new WeakMap();
const localizedAttributes = new WeakMap();
const excluded = 'script,style,textarea,[data-no-translate],.translation-en';
function localizeRoot(root) {
  if(language==='zh')return;
  const doc=root.ownerDocument || root;
  const walker=doc.createTreeWalker(root,NodeFilter.SHOW_TEXT);
  const nodes=[];
  while(walker.nextNode())nodes.push(walker.currentNode);
  for(const node of nodes) {
    const parent=node.parentElement;
    if(!parent || parent.closest(excluded) || !(language==='en'?/[\u3400-\u9fff。！？]/:han).test(node.nodeValue))continue;
    const source=node.nodeValue;
    if(localizedOptions.get(node)===source)continue;
    const target=english(source);
    if(source===target || han.test(target))continue;
    if(language==='en' || parent.closest('svg'))node.nodeValue=target;
    else if(parent.closest('option')) {
      node.nodeValue=source+' / '+target;
      localizedOptions.set(node,node.nodeValue);
    }
    else {
      const wrapper=doc.createElement('span');wrapper.className='parallel-text';wrapper.setAttribute('data-no-translate','');
      const zh=doc.createElement('span');zh.lang='zh-CN';zh.textContent=source;
      const en=doc.createElement('span');en.lang='en';en.className='translation-en';en.textContent=target;
      wrapper.append(zh,en);node.replaceWith(wrapper);
    }
  }
  for(const element of root.querySelectorAll?.('[placeholder],[aria-label],[alt],[title]') || []) {
    if(element.closest('script,style,[data-no-translate]'))continue;
    const previous=localizedAttributes.get(element)||{};
    for(const name of ['placeholder','aria-label','alt','title']) {
      const source=element.getAttribute(name);if(!source)continue;
      if(previous[name]===source)continue;
      const target=english(source);
      if(source!==target) {
        const translated=language==='en'?target:source+' / '+target;
        element.setAttribute(name,translated);previous[name]=translated;
      }
    }
    localizedAttributes.set(element,previous);
  }
}
export function localizePage() {
  observer?.disconnect();
  document.documentElement.lang=language==='en'?'en':'zh-CN';
  document.documentElement.dataset.language=language;
  localizeRoot(document.body);
  if(language==='en')document.title=english(document.title);
  observer?.observe(document.body,{childList:true,characterData:true,subtree:true});
}
export function observeTranslations() {
  observer = new MutationObserver(()=>localizePage());
  localizePage();
}
