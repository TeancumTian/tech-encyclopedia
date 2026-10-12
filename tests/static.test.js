import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
const out = new URL('../build/web/', import.meta.url).pathname;
const book = JSON.parse(fs.readFileSync(out + 'book.json'));
const read = file => fs.readFileSync(out + file, 'utf8');
const escapeHtml = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#x27;');

test('every entry and principle has a plain page in both languages with its own address', () => {
  for (const e of book.entries) {
    const zh = read(`e/${e.id}.html`), en = read(`en/e/${e.id}.html`);
    assert.ok(zh.includes(`<h1>${escapeHtml(e.zh)}</h1>`), e.id);
    assert.ok(en.includes(`<h1>${escapeHtml(e.en)}</h1>`), e.id);
    assert.match(zh, new RegExp(`<link rel="canonical" href="https://[^"]+/e/${e.id}\\.html">`));
    assert.match(en, new RegExp(`<link rel="canonical" href="https://[^"]+/en/e/${e.id}\\.html">`));
    assert.ok(zh.includes(`href="../#/entry/${e.id}"`)); assert.ok(en.includes(`href="../../#/entry/${e.id}"`));
    assert.ok(zh.includes('<html lang="zh-CN">')); assert.ok(en.includes('<html lang="en">'));
    assert.ok(!/<script(?! type="application\/ld\+json")/.test(zh + en), 'plain pages run no scripts');
  }
  for (const p of book.principles) { assert.ok(read(`p/${p.id}.html`).includes(escapeHtml(p.zh))); assert.ok(read(`en/p/${p.id}.html`).includes(escapeHtml(p.en))); }
});

test('plain pages keep the manuscript text and link only to files that exist', () => {
  const sample = book.entries.find(e => e.id === 'turing-machine');
  const zh = read('e/turing-machine.html');
  for (const line of sample.fields['原理'].split('\n')) assert.ok(zh.includes(escapeHtml(line.replace(/\[\[[^\]]+\]\]|\*\*/g, '')).slice(0, 30)));
  assert.ok(zh.includes('src="../figs/computing/turing-machine.svg"'));
  let checked = 0;
  for (const dir of ['e', 'p', 'en/e', 'en/p']) for (const file of fs.readdirSync(out + dir)) {
    const text = read(`${dir}/${file}`);
    for (const [, href] of text.matchAll(/(?:href|src)="([^"#]+)/g)) {
      if (/^(https?:|data:)/.test(href)) continue;
      assert.ok(fs.existsSync(path.resolve(out + dir, href)), `${dir}/${file} -> ${href}`); checked++;
    }
  }
  assert.ok(checked > 10000);
});

test('the sitemap lists every plain page once and the home page declares its address', () => {
  const sitemap = read('sitemap.xml');
  const locations = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1]);
  assert.equal(locations.length, 1 + 2 * (book.entries.length + book.principles.length + 1));
  assert.equal(new Set(locations).size, locations.length);
  const base = locations[0];
  assert.match(base, /^https:\/\/.+\/$/);
  for (const url of locations.slice(1)) assert.ok(fs.existsSync(out + url.slice(base.length)), url);
  const home = read('index.html');
  assert.ok(home.includes(`<link rel="canonical" href="${base}">`)); assert.ok(!home.includes('__SITE_URL__'));
  assert.ok(home.includes('href="./e/index.html"')); assert.ok(home.includes('property="og:title"'));
});
