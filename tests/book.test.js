import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {createBookReader} from '../web/book-reader.js';
import {nextReview,normalizeProgress,mergeProgress} from '../web/models.js';
const book=JSON.parse(fs.readFileSync(new URL('../build/web/book.json',import.meta.url)));
const entries=new Map(book.entries.map(e=>[e.id,e])),principles=new Map(book.principles.map(p=>[p.id,p])),domains=new Map(book.domains.map(d=>[d.id,d]));
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const blank=()=>normalizeProgress({},entries.keys(),book.readingOrder);
const reader=createBookReader({book,entries,principles,domains,progress:blank,esc,icon:()=>'',pageTitle:()=>'',entryCard:()=>''});
test('every manuscript, introduction, index key and figure is included',()=>{
  const files=[...fs.readdirSync('front').filter(f=>f.endsWith('.md')).map(f=>'front/'+f),...fs.readdirSync('domains').filter(f=>f.endsWith('.md')).map(f=>'domains/'+f)];
  assert.deepEqual(book.coverage.sources.map(s=>s.path).sort(),files.sort());
  for(const source of book.coverage.sources)assert.equal(source.sha256,crypto.createHash('sha256').update(fs.readFileSync(source.path)).digest('hex'));
  assert.equal(book.coverage.figures.length,183);
  assert.equal(book.documents.length,20);
  for(const domain of book.domains){assert.ok(domain.intro.length);assert.ok(domain.intro.some(b=>b.type==='figure'));assert.ok(reader.chapter(domain.id).includes(`sources-${domain.id}`));}
  for(const e of book.entries)assert.ok(e.index.key);
  assert.equal(book.readingOrder.length,new Set(book.readingOrder).size);
  for(const key of book.readingOrder)assert.ok(reader.title(key),key);
});
test('all source tables, lists, maps and paragraph blocks render with no raw placeholders',()=>{
  for(const d of book.documents){const html=reader.documentPage(d.id);assert.ok(!html.includes('@@'));for(const block of d.blocks){if(block.type==='table')assert.ok(html.includes('<table'));if(block.type==='figure')assert.ok(html.includes(block.src));}}
  assert.ok(reader.documentPage('sources-ai').includes('核对'));
  assert.ok(reader.documentPage('map').includes('#/chapter/energy'));
});
test('both indexes and the unfiltered timeline cover every eligible entry',()=>{
  for(const language of ['zh','en']){const html=reader.indexResults(language);for(const e of book.entries)assert.ok(html.includes(`href="#/entry/${e.id}"`),e.id);}
  assert.ok(reader.indexResults('zh','dian chi').includes('电池'));
  const timeline=reader.timelineResults();assert.equal((timeline.match(/class="timeline-event"/g)||[]).length,book.entries.filter(e=>Number.isInteger(e.year)).length);
  assert.ok(reader.timelineResults('不存在内容').includes('没有匹配'));
});
test('Markdown text and unsafe URLs never execute as HTML',()=>{
  const html=reader.inline('<img src=x onerror=alert(1)> **bold** [bad](javascript:alert) [[p:energy]] https://example.com');
  assert.ok(!html.includes('<img'));assert.ok(!html.includes('href="javascript:'));assert.ok(html.includes('#/principle/energy'));
  assert.ok(html.includes('<strong>bold</strong>'));assert.ok(html.includes('rel="noopener"'));
});
test('v1 records migrate while v2 read anchors, notes and review ratings survive',()=>{
  const old=normalizeProgress({saved:['bit-byte'],notes:{'bit-byte':'my note'}},entries.keys(),book.readingOrder);assert.equal(old.notes['bit-byte'],'my note');assert.deepEqual(old.reading,{});
  const newer=normalizeProgress({...old,reading:{'entry/bit-byte':{fraction:.7,anchor:'how',offset:.4,finished:true}},lastRead:'entry/bit-byte'},entries.keys(),book.readingOrder);
  assert.equal(newer.reading['entry/bit-byte'].anchor,'how');assert.equal(newer.lastRead,'entry/bit-byte');
  const merged=mergeProgress({...old,notes:{'bit-byte':'imported','cpu':'new'}},newer);assert.equal(merged.notes['bit-byte'],'my note');assert.equal(merged.notes.cpu,'new');
});
test('review scheduling has a deterministic due date and caps intervals',()=>{
  const now=1000000;const again=nextReview(null,'again',now);assert.equal(again.due,now+600000);
  let review=nextReview(again,'know',now);assert.equal(review.interval,1);review=nextReview(review,'know',now);assert.equal(review.interval,3);
  for(let i=0;i<20;i++)review=nextReview(review,'know',now);assert.equal(review.interval,30);
});
