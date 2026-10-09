import test from 'node:test';
import assert from 'node:assert/strict';
import {ProjectProgress} from '../web/storage.js';
import {normalizeProgress} from '../web/models.js';
const normalize=raw=>normalizeProgress(raw,['logic-gate','bit-byte'],['entry/logic-gate','document/howto']);
function memory(){const values=new Map();return {getItem:k=>values.get(k)||null,setItem:(k,v)=>values.set(k,v),values};}
function api(){let remote={exists:false,revision:0,progress:normalize({})};return {get data(){return remote;},set data(v){remote=v;},fetcher:async(_url,options)=>{if(options.method==='GET')return Response.json(remote);const payload=JSON.parse(options.body);if(payload.revision!==remote.revision)return Response.json({error:'conflict'},{status:409});remote={exists:true,revision:remote.revision+1,progress:payload.progress};return Response.json(remote);}};}

test('first run migrates existing v1 notes to project; later run reads project',async()=>{
  const server=api(),cache=memory();const first=new ProjectProgress({normalize,storage:cache,fetcher:server.fetcher});
  const p=await first.init({notes:{'logic-gate':'old note'},saved:['logic-gate']});await first.flush();assert.equal(server.data.progress.notes['logic-gate'],'old note');assert.equal(first.state,'saved');
  const second=new ProjectProgress({normalize,storage:memory(),fetcher:server.fetcher});const loaded=await second.init({});assert.equal(loaded.notes['logic-gate'],'old note');assert.equal(second.pending,false);
});
test('failed network preserves pending local draft and retries against same revision',async()=>{
  const server=api(),cache=memory();let offline=false;const client=new ProjectProgress({normalize,storage:cache,fetcher:(...args)=>offline?Promise.reject(new Error('offline')):server.fetcher(...args)});
  const p=await client.init({});await client.flush();offline=true;p.notes['logic-gate']='draft';client.schedule(p);await client.flush();assert.equal(client.state,'offline');assert.equal(JSON.parse(cache.getItem(client.cacheKey)).pending,true);assert.equal(server.data.progress.notes['logic-gate'],undefined);
  offline=false;await client.retry();assert.equal(client.state,'saved');assert.equal(server.data.progress.notes['logic-gate'],'draft');
});
test('a stale client stops on conflict without replacing server or discarding draft',async()=>{
  const server=api();server.data={exists:true,revision:1,progress:normalize({notes:{'logic-gate':'original'}})};
  const a=new ProjectProgress({normalize,storage:memory(),fetcher:server.fetcher}),b=new ProjectProgress({normalize,storage:memory(),fetcher:server.fetcher});
  const pa=await a.init({}),pb=await b.init({});pa.notes['logic-gate']='first edit';a.schedule(pa);await a.flush();pb.notes['logic-gate']='second draft';b.schedule(pb);await b.flush();
  assert.equal(b.state,'conflict');assert.equal(server.data.progress.notes['logic-gate'],'first edit');assert.equal(b.current.notes['logic-gate'],'second draft');
  const loaded=await b.useProject();assert.equal(loaded.notes['logic-gate'],'first edit');assert.equal(JSON.parse(b.storage.getItem(b.cacheKey+'-recovery')).notes['logic-gate'],'second draft');
});
test('pending draft from a closed tab is retried, not replaced by older disk state',async()=>{
  const server=api(),cache=memory();server.data={exists:true,revision:5,progress:normalize({})};cache.setItem('tech-encyclopedia-project-v2',JSON.stringify({revision:5,pending:true,progress:normalize({notes:{'bit-byte':'not lost'}})}));
  const client=new ProjectProgress({normalize,storage:cache,fetcher:server.fetcher});await client.init({});await client.flush();assert.equal(server.data.progress.notes['bit-byte'],'not lost');
});
test('full browser cache does not prevent successful disk saving',async()=>{
  const server=api();const client=new ProjectProgress({normalize,storage:{getItem:()=>null,setItem:()=>{throw new Error('quota');}},fetcher:server.fetcher});await client.init({});await client.flush();assert.equal(client.state,'saved');assert.equal(client.cacheOK,false);
});

test('edits made during an in-flight save are sent after the first revision completes',async()=>{
  const server=api();server.data={exists:true,revision:1,progress:normalize({})};
  let release,started;
  const begun=new Promise(resolve=>{started=resolve;});
  const gate=new Promise(resolve=>{release=resolve;});
  let held=false;
  const client=new ProjectProgress({normalize,storage:memory(),fetcher:async(url,options)=>{
    if(options.method==='PUT'&&!held){held=true;started();await gate;}
    return server.fetcher(url,options);
  }});
  const p=await client.init({});p.notes['logic-gate']='first';client.schedule(p);
  const first=client.flush();await begun;
  p.notes['logic-gate']='latest';p.reading['entry/logic-gate']={fraction:.6,finished:true};client.schedule(p);
  release();await first;assert.equal(client.pending,true);await client.flush();
  assert.equal(server.data.revision,3);assert.equal(server.data.progress.notes['logic-gate'],'latest');
  assert.equal(server.data.progress.reading['entry/logic-gate'].fraction,.6);assert.equal(client.pending,false);
});
