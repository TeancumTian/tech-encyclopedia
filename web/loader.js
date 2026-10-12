// On-demand book data. The first request brings the book without entry bodies; chapter bodies and
// English text are fetched when a page needs them and merged into the same in-memory book.
export function createBookLoader({book, fetchJSON, configureLanguage, translateTree, language = () => 'zh'}) {
  const loaded = new Set(), loads = new Map(), englishBodies = new Set(), search = new Map();
  let catalog = null, catalogLoading = null, englishBook = null, englishById = new Map();
  function index(entry) {
    const translated = englishById.get(entry.id);
    search.set(entry.id, [entry.zh, entry.en, entry.definition, ...Object.values(entry.fields || {}),
      ...(translated ? [translated.definition, ...Object.values(translated.fields || {})] : [])].join(' ').toLowerCase());
  }
  function attach(domain, bodies) {
    for (const entry of book.entries) {
      if (entry.domain !== domain) continue;
      entry.fields = bodies[entry.id] || {};
      const translated = englishById.get(entry.id);
      if (translated) translated.fields = translateTree(entry.fields);
      index(entry);
    }
    loaded.add(domain);
  }
  for (const entry of book.entries) { entry.fields = {}; index(entry); }

  function ensureBodies(domains = book.domains.map(d => d.id)) {
    return Promise.all(domains.filter(domain => !loaded.has(domain)).map(domain => {
      // A chapter load never waits for the catalogue, and the catalogue load waits for chapters,
      // so the two cannot block each other whatever order the responses arrive in.
      if (!loads.has(domain)) loads.set(domain, (async () => {
        const bodies = await fetchJSON(`./bodies/${domain}.json`);
        if (catalog && !englishBodies.has(domain)) {
          Object.assign(catalog, await fetchJSON(`./en/bodies/${domain}.json`));
          englishBodies.add(domain);
          configureLanguage(catalog, language());
        }
        attach(domain, bodies);
      })().catch(error => { loads.delete(domain); throw error; }));
      return loads.get(domain);
    }));
  }
  function ensureTranslations() {
    if (catalog) return Promise.resolve();
    if (!catalogLoading) catalogLoading = (async () => {
      const merged = await fetchJSON('./en.json'), fetched = new Set();
      for (;;) {
        // Include every chapter that is attached, also those that finish while English files download.
        await Promise.allSettled([...loads.values()]);
        const missing = [...loaded].filter(domain => !fetched.has(domain));
        if (!missing.length) break;
        Object.assign(merged, ...await Promise.all(missing.map(domain => fetchJSON(`./en/bodies/${domain}.json`))));
        missing.forEach(domain => fetched.add(domain));
      }
      // No await from here on: a chapter that arrives later sees the catalogue and fetches its own English.
      configureLanguage(merged, language());
      catalog = merged; fetched.forEach(domain => englishBodies.add(domain));
      englishBook = translateTree(book);
      for (const key of ['entries', 'principles', 'domains']) englishBook[key].forEach((item, i) => { item.originalZh = book[key][i].zh; item.zh = book[key][i].en; });
      englishById = new Map(englishBook.entries.map(e => [e.id, e]));
      book.entries.forEach(index);
    })().catch(error => { catalogLoading = null; throw error; });
    return catalogLoading;
  }
  return {
    ensureBodies, ensureTranslations,
    hasBodies: domain => loaded.has(domain),
    searchText: id => search.get(id) || '',
    get complete() { return loaded.size === book.domains.length; },
    get catalog() { return catalog; },
    get englishBook() { return englishBook; },
  };
}
