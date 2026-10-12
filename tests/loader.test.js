import test from 'node:test';
import assert from 'node:assert/strict';
import {createBookLoader} from '../web/loader.js';
import {configureLanguage, translateTree} from '../web/i18n.js';

const makeBook = () => ({
  domains: [{id: 'a', zh: '甲篇', en: 'Part A'}, {id: 'b', zh: '乙篇', en: 'Part B'}], principles: [],
  entries: [{id: 'x', domain: 'a', zh: '甲', en: 'Alpha', definition: '甲的定义。'}, {id: 'y', domain: 'b', zh: '乙', en: 'Beta', definition: '乙的定义。'}],
});
const FILES = {
  './bodies/a.json': {x: {'原理': '甲的原理。'}}, './bodies/b.json': {y: {'原理': '乙的原理。'}},
  './en.json': {'甲的定义。': 'Definition of alpha.', '乙的定义。': 'Definition of beta.', '甲': 'Alpha', '乙': 'Beta'},
  './en/bodies/a.json': {'甲的原理。': 'Principle of alpha.'}, './en/bodies/b.json': {'乙的原理。': 'Principle of beta.'},
};
// Every request stays pending until the test releases it, so any arrival order can be replayed.
function harness() {
  const pending = new Map(), requested = [];
  const fetchJSON = path => { requested.push(path); return new Promise((resolve, reject) => pending.set(path, {resolve, reject})); };
  const settle = () => new Promise(resolve => setImmediate(resolve));
  const release = async path => { assert.ok(pending.has(path), 'not requested: ' + path); pending.get(path).resolve(structuredClone(FILES[path])); pending.delete(path); await settle(); };
  const fail = async path => { pending.get(path).reject(new Error('offline')); pending.delete(path); await settle(); };
  const book = makeBook();
  const loader = createBookLoader({book, fetchJSON, configureLanguage, translateTree, language: () => 'en'});
  return {loader, book, requested, pending, release, fail, settle};
}
const withTimeout = promise => Promise.race([promise, new Promise((_, reject) => setTimeout(() => reject(new Error('loader did not settle: chapter and catalogue loads are waiting on each other')), 500))]);
const englishEntry = (loader, id) => loader.englishBook.entries.find(e => e.id === id);

test('a Chinese reader downloads one chapter and no English at all', async () => {
  const {loader, book, requested, release} = harness();
  assert.equal(loader.hasBodies('a'), false); assert.deepEqual(book.entries[0].fields, {});
  assert.ok(loader.searchText('x').includes('甲的定义')); assert.ok(!loader.searchText('x').includes('原理'));
  const done = loader.ensureBodies(['a']); const again = loader.ensureBodies(['a']);
  await release('./bodies/a.json'); await withTimeout(Promise.all([done, again]));
  assert.deepEqual(requested, ['./bodies/a.json'], 'one request, shared by both callers, and nothing in English');
  assert.equal(book.entries[0].fields['原理'], '甲的原理。'); assert.ok(loader.searchText('x').includes('甲的原理'));
  assert.equal(loader.hasBodies('a'), true); assert.equal(loader.hasBodies('b'), false); assert.equal(loader.complete, false); assert.equal(loader.catalog, null);
  await loader.ensureBodies(['a']); assert.equal(requested.length, 1);
});

test('switching to English later fetches English only for the chapters already read', async () => {
  const {loader, requested, release} = harness();
  const bodies = loader.ensureBodies(['a']); await release('./bodies/a.json'); await bodies;
  const english = loader.ensureTranslations(); await release('./en.json'); await release('./en/bodies/a.json'); await withTimeout(english);
  assert.deepEqual(requested, ['./bodies/a.json', './en.json', './en/bodies/a.json']);
  assert.equal(englishEntry(loader, 'x').fields['原理'], 'Principle of alpha.'); assert.equal(englishEntry(loader, 'x').zh, 'Alpha'); assert.equal(englishEntry(loader, 'x').originalZh, '甲');
  assert.ok(loader.searchText('x').includes('principle of alpha'));
  const next = loader.ensureBodies(['b']); await release('./bodies/b.json'); await release('./en/bodies/b.json'); await withTimeout(next);
  assert.equal(englishEntry(loader, 'y').fields['原理'], 'Principle of beta.'); assert.equal(loader.complete, true);
  await loader.ensureTranslations(); assert.equal(requested.length, 5);
});

test('a chapter requested while the catalogue is still downloading cannot deadlock, in either arrival order', async () => {
  for (const order of [['./bodies/a.json', './en.json'], ['./en.json', './bodies/a.json']]) {
    const {loader, release, pending} = harness();
    const english = loader.ensureTranslations();
    const bodies = loader.ensureBodies(['a']);
    for (const path of order) await release(path);
    await release('./en/bodies/a.json');
    await withTimeout(Promise.all([english, bodies]));
    assert.equal(pending.size, 0, order.join(' then '));
    assert.equal(englishEntry(loader, 'x').fields['原理'], 'Principle of alpha.', order.join(' then '));
  }
});

test('a chapter that finishes while English chapter files download is still translated', async () => {
  const {loader, release} = harness();
  const first = loader.ensureBodies(['a']); await release('./bodies/a.json'); await first;
  const english = loader.ensureTranslations(); await release('./en.json');
  const second = loader.ensureBodies(['b']); await release('./bodies/b.json');   // arrives before the catalogue is in place
  await release('./en/bodies/a.json'); await release('./en/bodies/b.json');
  await withTimeout(Promise.all([english, second]));
  assert.equal(englishEntry(loader, 'x').fields['原理'], 'Principle of alpha.'); assert.equal(englishEntry(loader, 'y').fields['原理'], 'Principle of beta.');
});

test('a failed download can be retried and leaves earlier data intact', async () => {
  const {loader, book, requested, release, fail} = harness();
  const broken = assert.rejects(loader.ensureBodies(['a']), /offline/); await fail('./bodies/a.json'); await broken;
  assert.equal(loader.hasBodies('a'), false);
  const retry = loader.ensureBodies(['a']); await release('./bodies/a.json'); await retry; assert.equal(book.entries[0].fields['原理'], '甲的原理。');
  const english = assert.rejects(loader.ensureTranslations(), /offline/); await fail('./en.json'); await english; assert.equal(loader.catalog, null);
  const again = loader.ensureTranslations(); await release('./en.json'); await release('./en/bodies/a.json'); await withTimeout(again);
  assert.equal(englishEntry(loader, 'x').fields['原理'], 'Principle of alpha.');
  assert.equal(requested.filter(path => path === './en.json').length, 2);
  configureLanguage({}, 'zh');
});
