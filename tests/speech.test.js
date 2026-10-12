import test from 'node:test';
import assert from 'node:assert/strict';
import {speechChunks, speechLanguage, pickVoice, createSpeechReader} from '../web/speech.js';

test('text is split at sentence ends, never inside a number, and stays within the limit', () => {
  assert.deepEqual(speechChunks(''), []); assert.deepEqual(speechChunks(null), []);
  assert.deepEqual(speechChunks('速度约 7.9 公里/秒。它就一直绕着地球转。', 12), ['速度约 7.9 公里/秒。', '它就一直绕着地球转。']);
  assert.deepEqual(speechChunks('It costs $1.5 million. See Fig. 2 (left). Done!', 22), ['It costs $1.5 million.', 'See Fig. 2 (left).', 'Done!']);
  assert.deepEqual(speechChunks('It costs $1.5 million. Done!', 160), ['It costs $1.5 million. Done!']);
  const long = '这是一个没有任何标点的很长的句子'.repeat(40);
  for (const chunk of speechChunks(long, 100)) assert.ok(chunk.length <= 200);
  assert.equal(speechChunks(long, 100).join(''), long);
  assert.deepEqual(speechChunks('下一节 → 轨道 ↗ ✓ 已读'), ['下一节 轨道 已读']);
  const paragraph = '第一句。第二句！第三句？第四句；第五句。';
  assert.equal(speechChunks(paragraph, 8).join(''), paragraph);
});
test('parallel mode reads the Chinese source and English mode reads English', () => {
  assert.equal(speechLanguage('zh'), 'zh-CN'); assert.equal(speechLanguage('bi'), 'zh-CN'); assert.equal(speechLanguage('en'), 'en-US');
});
test('an on-device voice in the right language is preferred', () => {
  const voices = [{name: 'remote zh', lang: 'zh-CN', localService: false, default: true}, {name: 'local zh', lang: 'zh_CN', localService: true}, {name: 'tw', lang: 'zh-TW', localService: true}, {name: 'en', lang: 'en-US', localService: true}];
  assert.equal(pickVoice(voices, 'zh-CN').name, 'local zh');
  assert.equal(pickVoice(voices, 'en-US').name, 'en');
  assert.equal(pickVoice([{name: 'gb', lang: 'en-GB'}], 'en-US').name, 'gb');
  assert.equal(pickVoice(voices, 'fr-FR'), null); assert.equal(pickVoice([], 'zh-CN'), null);
});
function fakeSpeech() {
  const spoken = []; let active = null;
  class Utterance { constructor(text) { this.text = text; } }
  const synth = {speak(u) { spoken.push(u); active = u; }, cancel() { active = null; }, getVoices: () => [{lang: 'zh-CN', localService: true}],
    finish() { const u = active; active = null; u?.onend?.(); }, fail(error) { const u = active; active = null; u?.onerror?.({error}); }};
  return {spoken, synth, Utterance};
}
test('sections are spoken in order; pause resumes the same sentence and stop clears the queue', () => {
  const {spoken, synth, Utterance} = fakeSpeech(); const notes = [];
  const items = ['第一段。', '第二段。', '第三段。'].map(text => ({element: null, text}));
  const reader = createSpeechReader({getLanguage: () => 'bi', notify: m => notes.push(m), collect: () => items, synth, Utterance});
  assert.equal(reader.supported, true); assert.equal(reader.state, 'idle');
  reader.toggle(); assert.equal(reader.state, 'speaking'); assert.equal(spoken.at(-1).text, '第一段。'); assert.equal(spoken.at(-1).lang, 'zh-CN');
  synth.finish(); assert.equal(spoken.at(-1).text, '第二段。');
  reader.toggle(); assert.equal(reader.state, 'paused');
  synth.finish(); assert.equal(spoken.length, 2, 'a cancelled utterance must not advance the queue');
  reader.toggle(); assert.equal(reader.state, 'speaking'); assert.equal(spoken.at(-1).text, '第二段。');
  reader.setRate(1.5); assert.equal(spoken.at(-1).rate, 1.5); assert.equal(spoken.at(-1).text, '第二段。');
  reader.setRate(99); assert.equal(spoken.at(-1).rate, 1);
  synth.finish(); synth.finish(); assert.equal(reader.state, 'idle'); assert.equal(spoken.at(-1).text, '第三段。');
  reader.start(); reader.stop(); assert.equal(reader.state, 'idle'); synth.finish(); assert.equal(reader.state, 'idle');
  assert.deepEqual(notes, []);
});
test('empty sections, real errors and missing speech support are reported without throwing', () => {
  const {synth, Utterance} = fakeSpeech(); const notes = [];
  const empty = createSpeechReader({getLanguage: () => 'zh', notify: m => notes.push(m), collect: () => [], synth, Utterance});
  empty.start(); assert.equal(empty.state, 'idle'); assert.equal(notes.length, 1);
  const reader = createSpeechReader({getLanguage: () => 'en', notify: m => notes.push(m), collect: () => [{element: null, text: 'Hello.'}], synth, Utterance});
  reader.start(); assert.equal(notes.length, 2, 'no English voice in the fake list is announced');
  synth.fail('canceled'); assert.equal(reader.state, 'speaking');
  reader.start(); synth.fail('synthesis-failed'); assert.equal(reader.state, 'idle'); assert.equal(notes.length, 4);
  const none = createSpeechReader({getLanguage: () => 'zh', synth: undefined, Utterance: undefined});
  assert.equal(none.supported, false); none.start(); none.stop(); none.mount(null); assert.equal(none.state, 'idle');
});
