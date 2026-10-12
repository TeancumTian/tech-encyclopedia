import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { gateOutput, binaryValue, circuitCurrent, transmissionLoss, gradientStep, normalizeProgress, LEO_DELTA_V, rocketDeltaV, carnotEfficiency, pcrCopies, caesarShift, scaleLaw, formatCount } from '../web/models.js';
import { pathways, lessons, labs, labSources } from '../web/learning.js';

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
  assert.equal(normalizeProgress({prefs:{theme:'dark'}},ids).prefs.theme,'dark');
  assert.equal(normalizeProgress({prefs:{theme:'neon'}},ids).prefs.theme,'auto');
  assert.equal(normalizeProgress(null,ids).prefs.theme,'auto');
});
test('all guided lessons, routes, lab destinations, answers and assets resolve', () => {
  assert.equal(ids.size,book.meta.total_entries);
  assert.equal(book.principles.length,book.meta.total_principles);
  for(const p of pathways){assert.equal(new Set(p.ids).size,p.ids.length);for(const id of p.ids){assert.ok(ids.has(id));assert.ok(lessons[id]);}}
  for(const [id,lesson] of Object.entries(lessons)){assert.ok(ids.has(id));assert.ok(lesson.answer>=0&&lesson.answer<lesson.options.length);assert.ok(lesson.explanation.length>10);}
  for(const lab of labs)assert.ok(ids.has(lab.entry));
  for(const e of book.entries){assert.ok(e.fields['原理']);for(const image of e.figures)assert.ok(fs.existsSync(new URL('../build/web/'+image,import.meta.url)),image);}
});
test('rocket equation: velocity grows with the logarithm of the mass ratio', () => {
  const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-9,`${a} vs ${b}`);
  close(rocketDeltaV(3,.5),3*Math.log(2));
  close(rocketDeltaV(6,.5),2*rocketDeltaV(3,.5));
  // Each halving of the dry mass adds the same step, so equal gains need ever more propellant.
  close(rocketDeltaV(3,.75)-rocketDeltaV(3,.5),rocketDeltaV(3,.875)-rocketDeltaV(3,.75));
  // The manuscript's example: hydrogen-oxygen at 4.4 km/s needs about 89% propellant for 9.4 km/s.
  assert.equal(LEO_DELTA_V,9.4);
  assert.ok(rocketDeltaV(4.4,.89)>=LEO_DELTA_V);assert.ok(rocketDeltaV(4.4,.88)<LEO_DELTA_V);
  assert.equal(rocketDeltaV(3,0),0);
  for(const bad of [[0,.8],[-1,.8],[3,1],[3,1.2],[3,-.1],[NaN,.5],[3,NaN]])assert.equal(rocketDeltaV(...bad),0);
});
test('Carnot limit uses kelvin, rises with the temperature gap and never reaches 100%', () => {
  assert.ok(Math.abs(carnotEfficiency(600,30)-(1-303.15/873.15))<1e-12);
  assert.ok(carnotEfficiency(1500,0)<1);
  assert.ok(carnotEfficiency(700,30)>carnotEfficiency(600,30));assert.ok(carnotEfficiency(600,10)>carnotEfficiency(600,30));
  // Doubling the Celsius reading of the hot side does not double the limit.
  assert.ok(carnotEfficiency(600,30)<2*carnotEfficiency(300,30));
  assert.equal(carnotEfficiency(30,30),0);assert.equal(carnotEfficiency(20,80),0);assert.equal(carnotEfficiency(100,-300),0);
});
test('PCR doubling passes a billion copies at cycle 30 and slows with lower efficiency', () => {
  assert.equal(pcrCopies(0),1);assert.equal(pcrCopies(10),1024);
  assert.ok(pcrCopies(29)<1e9);assert.ok(pcrCopies(30)>=1e9);
  assert.equal(pcrCopies(2,.5),2.25);assert.ok(pcrCopies(30,.8)<pcrCopies(30,1));
  assert.equal(pcrCopies(5,2),pcrCopies(5,1));assert.equal(pcrCopies(5,-1),1);assert.equal(pcrCopies(-3),1);
  assert.equal(pcrCopies(3,1,10),80);
});
test('shift cipher wraps past Z, leaves other characters alone and reverses exactly', () => {
  assert.equal(caesarShift('HELLO WORLD',3),'KHOOR ZRUOG');
  assert.equal(caesarShift('xyz, XYZ!',3),'abc, ABC!');
  assert.equal(caesarShift('密码 2026',5),'密码 2026');
  for(const k of [0,1,11,25,26,-3,52])assert.equal(caesarShift(caesarShift('Knowledge is Power',k),-k),'Knowledge is Power');
  assert.equal(caesarShift('ABC',26),'ABC');assert.equal(caesarShift('ABC',27),'BCD');assert.equal(caesarShift('ABC',-1),'ZAB');
  // Only 25 shifts change the text, so trying them all always recovers the message.
  const secret=caesarShift('KNOWLEDGE',11);
  assert.deepEqual(Array.from({length:26},(_,k)=>caesarShift(secret,-k)).filter(text=>text==='KNOWLEDGE').length,1);
  assert.equal(caesarShift(secret,-11),'KNOWLEDGE');
});
test('square-cube law: weight outgrows the supporting area by the scale factor', () => {
  assert.deepEqual(scaleLaw(1),{area:1,volume:1,pressure:1});
  assert.deepEqual(scaleLaw(2),{area:4,volume:8,pressure:2});
  for(const k of [1.5,3,5,10]){const law=scaleLaw(k);assert.ok(Math.abs(law.volume/law.area-law.pressure)<1e-9);}
  assert.equal(scaleLaw(5).pressure,5);
});
test('large counts stay readable in every language', () => {
  assert.equal(formatCount(1),'1');assert.equal(formatCount(1024),'1,024');assert.equal(formatCount(2.25),'2');
  assert.equal(formatCount(2**30),'1.07 × 10⁹');assert.equal(formatCount(2**40),'1.10 × 10¹²');
  assert.equal(formatCount(9999999),'1.00 × 10⁷');assert.equal(formatCount(Infinity),'∞');
});
test('every experiment has a destination entry and new experiments cite a reference', () => {
  assert.equal(new Set(labs.map(l=>l.id)).size,labs.length);
  for(const id of ['rocket','carnot','pcr','caesar','scale']){assert.ok(labs.some(l=>l.id===id),id);assert.match(labSources[id][1],/^https:\/\//);}
  assert.equal(pathways.length,7);assert.equal(Object.keys(lessons).length,35);
  for(const p of pathways)assert.equal(p.ids.length,5);
});

