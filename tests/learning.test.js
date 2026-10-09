import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { gateOutput, binaryValue, circuitCurrent, transmissionLoss, gradientStep, normalizeProgress } from '../web/models.js';
import { pathways, lessons, labs } from '../web/learning.js';

const book = JSON.parse(fs.readFileSync(new URL('../build/web/book.json', import.meta.url)));
const ids = new Set(book.entries.map(e => e.id));

test('all gate truth tables cover every input combination', () => {
  for (const [name, expected] of [['AND',[0,0,0,1]],['OR',[0,1,1,1]],['XOR',[0,1,1,0]]]) {
    assert.deepEqual([[0,0],[0,1],[1,0],[1,1]].map(([a,b])=>gateOutput(name,a,b)),expected);
  }
});
test('one byte covers all 256 unsigned values including the challenge', () => {
  for(let n=0;n<256;n++) assert.equal(binaryValue(n.toString(2).padStart(8,'0').split('').map(Number)),n);
  assert.equal(binaryValue([0,0,1,0,1,0,1,0]),42);
});
test('ohmic current scales with voltage and inverse resistance', () => {
  assert.equal(circuitCurrent(12,10),1.2);
  assert.equal(circuitCurrent(24,10),2*circuitCurrent(12,10));
  assert.equal(circuitCurrent(12,20),circuitCurrent(12,10)/2);
});
test('doubling transmission voltage quarters loss at fixed power', () => {
  assert.deepEqual(transmissionLoss(10),{amps:100,lossKW:100});
  assert.equal(transmissionLoss(20).lossKW,25);
  assert.equal(transmissionLoss(100).lossKW,1);
});
test('gradient steps converge, oscillate, or diverge according to learning rate', () => {
  let small=4, large=4;
  for(let i=0;i<20;i++){small=gradientStep(small,.15);large=gradientStep(large,1.1);}
  assert.ok(Math.abs(small)<.01);
  assert.equal(gradientStep(4,.5),0);
  assert.equal(gradientStep(4,1),-4);
  assert.ok(Math.abs(large)>4);
});
test('import handles corrupt and stale progress without unknown IDs or non-text notes', () => {
  assert.equal(normalizeProgress(null,ids).last,null);
  assert.deepEqual(normalizeProgress(null,ids).notes,{});
  const result=normalizeProgress({learned:['bit-byte','bit-byte','bad-id'],saved:42,last:'bad-id',notes:{'bit-byte':'hello','logic-gate':23,'bad-id':'secret'}},ids);
  assert.deepEqual(result.learned,['bit-byte']);assert.deepEqual(result.saved,[]);assert.equal(result.last,null);assert.deepEqual(result.notes,{'bit-byte':'hello'});
  assert.equal(normalizeProgress({notes:{'bit-byte':'a'.repeat(8000)}},ids).notes['bit-byte'].length,5000);
});
test('all guided lessons, routes, lab destinations, answers and assets resolve', () => {
  assert.equal(ids.size,book.meta.total_entries);
  assert.equal(book.principles.length,book.meta.total_principles);
  for(const p of pathways){assert.equal(new Set(p.ids).size,p.ids.length);for(const id of p.ids){assert.ok(ids.has(id));assert.ok(lessons[id]);}}
  for(const [id,lesson] of Object.entries(lessons)){assert.ok(ids.has(id));assert.ok(lesson.answer>=0&&lesson.answer<lesson.options.length);assert.ok(lesson.explanation.length>10);}
  for(const lab of labs)assert.ok(ids.has(lab.entry));
  for(const e of book.entries){assert.ok(e.fields['原理']);for(const image of e.figures)assert.ok(fs.existsSync(new URL('../build/web/'+image,import.meta.url)),image);}
});
