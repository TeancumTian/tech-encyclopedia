import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {BrowserProgress,browserStorageKey} from '../web/browser-storage.js';
import {normalizeProgress} from '../web/models.js';
const normalize=p=>normalizeProgress(p,['battery','cpu'],['entry/battery','document/howto']);
const key=browserStorageKey('https://teancumtian.github.io/tech-encyclopedia/#/book');
function memory(){const values=new Map();return {values,getItem:k=>values.get(k)??null,setItem:(k,v)=>values.set(k,v)};}
const client=storage=>new BrowserProgress({normalize,storage,cacheKey:key});

test('browser record restores notes, anchors, learning and review without a server',async()=>{
  const storage=memory(),a=client(storage),p=await a.init({saved:['battery'],notes:{battery:'legacy'}});
  p.reading['entry/battery']={fraction:.42,anchor:'how',offset:.3,finished:true};p.lastRead='entry/battery';
  p.review.battery={due:10000,count:1,interval:1,rating:'know'};p.passed=['battery'];a.schedule(p);
  const b=client(storage),restored=await b.init({});
  assert.equal(restored.notes.battery,'legacy');assert.equal(restored.reading['entry/battery'].anchor,'how');
  assert.equal(restored.reading['entry/battery'].fraction,.42);assert.equal(restored.review.battery.due,10000);
  assert.deepEqual(restored.passed,['battery']);assert.equal(b.state,'saved');assert.equal(b.pending,false);
});
test('browser storage is scoped to the deployed path rather than a shared github.io key',()=>{
  assert.equal(key,browserStorageKey('https://teancumtian.github.io/tech-encyclopedia/index.html#/notebook'));
  assert.notEqual(key,browserStorageKey('https://teancumtian.github.io/another-book/'));
});
test('quota failure retains unsaved work for export and retry',async()=>{
  const storage=memory(),set=storage.setItem;const a=client(storage),p=await a.init({});
  storage.setItem=()=>{throw new Error('quota');};p.notes.battery='do not lose';a.schedule(p);
  assert.equal(a.state,'error');assert.equal(a.pending,true);assert.equal(a.current.notes.battery,'do not lose');
  storage.setItem=set;a.retry();assert.equal(a.state,'saved');assert.equal(a.pending,false);
  assert.equal((await client(storage).init({})).notes.battery,'do not lose');
});
test('stale browser tabs cannot quietly replace newer notes',async()=>{
  const storage=memory(),a=client(storage),b=client(storage),pa=await a.init({}),pb=await b.init({});
  pa.notes.battery='first';a.schedule(pa);pb.notes.battery='second';b.schedule(pb);
  assert.equal(b.state,'conflict');assert.equal(b.current.notes.battery,'second');
  assert.equal((await client(storage).init({})).notes.battery,'first');
  assert.equal((await b.useProject()).notes.battery,'first');assert.equal(JSON.parse(storage.getItem(key+'-recovery')).notes.battery,'second');
});
test('malformed records survive automatic saves and only explicit reset replaces them',async()=>{
  const storage=memory();storage.setItem(key,'{broken');const a=client(storage),p=await a.init({});
  p.last='battery';a.schedule(p);a.retry();assert.equal(storage.getItem(key),'{broken');assert.equal(a.state,'error');
  a.reset({});assert.equal(a.state,'saved');assert.equal((await client(storage).init({})).last,null);
});
test('a different project storage event is ignored while same-site changes prompt recovery',async()=>{
  const a=client(memory());await a.init({});a.observe({key:'another-site',newValue:'x'});assert.equal(a.state,'saved');
  a.observe({key,newValue:'changed'});assert.equal(a.state,'conflict');
});
test('public build uses browser mode and includes no personal progress or server source',()=>{
  assert.equal(JSON.parse(fs.readFileSync('build/web/runtime-config.json')).progressMode,'browser');
  const paths=fs.readdirSync('build/web',{recursive:true});
  for(const path of paths)assert.ok(!/(?:learning-data|progress(?:\.previous)?\.json|serve_web\.py|^\.git)/.test(path),path);
  assert.ok(paths.includes('browser-storage.js'));
});
