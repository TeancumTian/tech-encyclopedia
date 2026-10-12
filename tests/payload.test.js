import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
const read=path=>JSON.parse(fs.readFileSync(new URL('../build/web/'+path,import.meta.url)));
const han=/[\u3400-\u9fff]/;

test('the core book plus per-chapter bodies reassemble the complete book exactly',()=>{
  const book=read('book.json'),core=read('book.core.json');
  assert.equal(core.entries.length,book.entries.length);
  assert.deepEqual(core.readingOrder,book.readingOrder);assert.deepEqual(core.coverage,book.coverage);
  for(const entry of core.entries)assert.equal(entry.fields,undefined);
  let total=0;
  for(const domain of book.domains){
    const bodies=read(`bodies/${domain.id}.json`);total+=Object.keys(bodies).length;
    for(const entry of book.entries.filter(e=>e.domain===domain.id))assert.deepEqual(bodies[entry.id],entry.fields,entry.id);
  }
  assert.equal(total,book.entries.length);
});

test('English chapter files cover every body line while the core catalog covers names, definitions, front matter and interface',()=>{
  const book=read('book.json'),core=read('en.json'),ui=JSON.parse(fs.readFileSync(new URL('../translations/ui.source.json',import.meta.url))).strings;
  for(const domain of book.domains){
    const part=read(`en/bodies/${domain.id}.json`);
    for(const entry of book.entries.filter(e=>e.domain===domain.id))for(const text of Object.values(entry.fields))for(const line of text.split('\n'))if(han.test(line)){assert.ok(part[line],line.slice(0,50));assert.doesNotMatch(part[line],han);}
  }
  for(const entry of book.entries){assert.ok(core[entry.zh],entry.zh);for(const line of entry.definition.split('\n'))if(han.test(line))assert.ok(core[line],line.slice(0,50));}
  for(const principle of book.principles)assert.ok(core[principle.statement]);
  for(const document of book.documents)for(const block of document.blocks)if(block.type==='paragraph')for(const line of block.text.split('\n'))if(han.test(line))assert.ok(core[line],line.slice(0,50));
  const signature=text=>text.trim().replace(/\{\d+\}/g,'{}');const keys=new Set(Object.keys(core).map(signature));
  for(const text of ui)assert.ok(keys.has(signature(text)),text.slice(0,50));
});

test('runtime fetches of chapter files carry the same release version as the modules',()=>{
  const app=fs.readFileSync(new URL('../build/web/app.js',import.meta.url),'utf8');
  const versions=[...app.matchAll(/\?v=([a-f0-9]{16})/g)].map(m=>m[1]);
  const placeholder=app.match(/const ASSET_VERSION='([a-f0-9]{16})'/);
  assert.ok(placeholder,'build must replace __ASSET_VERSION__');
  assert.ok(!app.includes('__ASSET_VERSION__'));
  assert.equal(new Set([...versions,placeholder[1]]).size,1);
});
