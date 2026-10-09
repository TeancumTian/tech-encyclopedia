import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {configureLanguage,english,translateTree,paired,currentLanguage} from '../web/i18n.js';
import {normalizeProgress,mergeProgress} from '../web/models.js';
import {lessons} from '../web/learning.js';

test('dynamic translations preserve values and translate nested labels',()=>{
  configureLanguage({'第 {0} 篇 · {1}':'Chapter {0} · {1}','能源与动力':'Energy & Power','找到 {0} 个词条':'{0} entries found'},'en');
  assert.equal(english('第 1 篇 · 能源与动力'),'Chapter 1 · Energy & Power');
  assert.equal(english('找到 997 个词条'),'997 entries found');
  assert.equal(english('  能源与动力  '),'  Energy & Power  ');
});

test('parallel text retains both paragraphs and explicit language tags',()=>{
  configureLanguage({'原理':'Principle'},'bi');
  assert.equal(currentLanguage(),'bi');
  const html=paired('原理',text=>text);
  assert.match(html,/lang="zh-CN">原理/);assert.match(html,/lang="en">Principle/);
  configureLanguage({},'invalid');assert.equal(currentLanguage(),'zh');
});

test('book localization keeps identifiers, reference keys and index sorting stable',()=>{
  configureLanguage({'蒸汽机':'Steam engine','能量不会消失。':'Energy does not disappear.'},'en');
  const book={id:'steam-engine',zh:'蒸汽机',fields:{'原理':'能量不会消失。'},index:{key:'zheng qi ji',letter:'Z'},readingOrder:['entry/steam-engine']};
  const en=translateTree(book);
  assert.equal(en.zh,'Steam engine');assert.equal(en.fields['原理'],'Energy does not disappear.');
  assert.equal(en.id,book.id);assert.deepEqual(en.index,book.index);assert.deepEqual(en.readingOrder,book.readingOrder);
  assert.equal(book.zh,'蒸汽机');
});

test('language selection uses the existing progress format without changing notes or reading IDs',()=>{
  const raw={prefs:{language:'bi',fontSize:'large'},notes:{battery:'我的中文笔记 <script> test'},reading:{'entry/battery':{finished:true,anchor:'how',fraction:.6}},saved:['battery']};
  const p=normalizeProgress(raw,['battery'],['entry/battery']);
  assert.equal(p.prefs.language,'bi');assert.equal(p.notes.battery,raw.notes.battery);assert.equal(p.reading['entry/battery'].anchor,'how');
  const imported=normalizeProgress(JSON.parse(JSON.stringify({version:2,...p})),['battery'],['entry/battery']);
  assert.deepEqual(imported,p);
  assert.equal(normalizeProgress({prefs:{language:'fr'}},[],[]).prefs.language,'zh');
  assert.equal(mergeProgress({...p,prefs:{language:'en'}},p).prefs.language,'bi');
});

test('all quiz and review feedback translates complete multi-sentence explanations',()=>{
  const catalog=Object.assign({},...['en.auto.json','ui.en.json','en.json'].map(name=>
    JSON.parse(readFileSync(new URL('../translations/'+name,import.meta.url)))));
  configureLanguage(catalog,'bi');
  for(const lesson of Object.values(lessons)) {
    const explanation=english(lesson.explanation);
    assert.doesNotMatch(explanation,/[\u3400-\u9fff]/);
    for(const prefix of ['✓ 对，就是这样。','再想想。','✓ 这次理解对了。','再想一想。']) {
      const result=english(prefix+lesson.explanation);
      assert.doesNotMatch(result,/[\u3400-\u9fff]/);
      assert.ok(result.endsWith(explanation));
    }
  }
  configureLanguage({},'zh');
});

test('published translations cover the entire book and retain all wiki reference IDs',()=>{
  const book=JSON.parse(readFileSync(new URL('../build/web/book.json',import.meta.url)));
  const catalog=JSON.parse(readFileSync(new URL('../build/web/en.json',import.meta.url)));
  const refs=text=>[...text.matchAll(/\[\[([^\]|]+)(?:\|[^\]]+)?\]\]/g)].map(m=>m[1]).sort();
  const check=text=>{
    for(const line of text.split('\n'))if(/[\u3400-\u9fff]/.test(line)) {
      assert.ok(catalog[line],`Missing translation: ${line.slice(0,55)}`);
      assert.doesNotMatch(catalog[line],/[\u3400-\u9fff]/);
      assert.deepEqual(refs(catalog[line]),refs(line));
    }
  };
  for(const e of book.entries){check(e.definition);Object.values(e.fields).forEach(check);}
  for(const p of book.principles)check(p.statement);
  function walk(value){if(typeof value==='string')check(value);else if(Array.isArray(value))value.forEach(walk);else if(value&&typeof value==='object')Object.values(value).forEach(walk);}
  for(const d of book.domains){walk(d.intro);walk(d.outro);}
  for(const d of book.documents)walk(d.blocks);
});
