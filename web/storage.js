// Project file is authoritative. A browser draft survives a failed request or interrupted tab.
export class ProjectProgress {
  constructor({normalize, onStatus, cacheKey = 'tech-encyclopedia-project-v2', fetcher = (...args) => globalThis.fetch(...args), storage = localStorage}) {
    this.normalize = normalize; this.onStatus = onStatus; this.cacheKey = cacheKey;
    this.fetcher = fetcher; this.storage = storage; this.revision = null;
    this.current = null; this.pending = false; this.connected = false; this.blocked = false;
    this.inflight = null; this.timer = null; this.cacheOK = true;
    this.status('loading');
  }
  status(state, message = '') { this.state = state; this.message = message; this.onStatus?.(state, message); }
  cache() {
    try { this.storage.setItem(this.cacheKey, JSON.stringify({revision:this.revision, pending:this.pending, progress:this.current})); }
    catch { this.cacheOK = false; }
  }
  async request(method, body, keepalive = false) {
    const controller = new AbortController(); const timeout = setTimeout(() => controller.abort(), 5000);
    try {
      return await this.fetcher('./api/progress', {method, cache:'no-store', signal:controller.signal,
        headers: method === 'GET' ? {} : {'Content-Type':'application/json','X-Local-Progress':'1'},
        ...(body ? {body:JSON.stringify(body)} : {}), keepalive});
    } finally { clearTimeout(timeout); }
  }
  async init(legacy) {
    let cached;
    try { cached = JSON.parse(this.storage.getItem(this.cacheKey) || 'null'); } catch { /* Legacy data remains untouched. */ }
    this.current = this.normalize(cached?.progress || legacy);
    try {
      const response = await this.request('GET');
      if (!response.ok) throw new Error('本机项目服务暂时不可用');
      const remote = await response.json();
      this.connected = true; this.revision = remote.revision;
      if (cached?.pending && remote.exists && cached.revision !== remote.revision) {
        this.pending = true; this.blocked = true; this.status('conflict'); return this.current;
      }
      if (!remote.exists || cached?.pending) {
        this.pending = true; this.cache(); this.schedule(this.current, 0);
      } else {
        this.current = this.normalize(remote.progress); this.pending = false; this.cache(); this.status('saved');
      }
    } catch {
      this.pending = true; this.status('offline', '请用 make web-serve 启动支持项目保存的本机服务。'); this.cache();
    }
    return this.current;
  }
  schedule(progress, delay = 400) {
    this.current = this.normalize(progress); this.pending = true; this.cache();
    if (this.blocked) { this.status('conflict'); return; }
    if (!this.connected) { this.status('offline'); return; }
    this.status('saving'); clearTimeout(this.timer);
    this.timer = setTimeout(() => this.flush(), delay);
  }
  async flush(keepalive = false) {
    clearTimeout(this.timer);
    if (this.inflight) return this.inflight;
    if (!this.pending || !this.connected || this.blocked) return;
    const snapshot = JSON.stringify(this.current);
    this.inflight = (async () => {
      try {
        const response = await this.request('PUT', {revision:this.revision, progress:JSON.parse(snapshot)}, keepalive);
        if (response.status === 409) { this.blocked = true; this.status('conflict'); return; }
        if (!response.ok) { const error = await response.json(); throw new Error(error.error || '写入失败'); }
        const result = await response.json(); this.revision = result.revision;
        this.pending = snapshot !== JSON.stringify(this.current);
        this.cache(); this.status(this.pending ? 'saving' : 'saved');
      } catch (error) {
        this.connected = false; this.status('offline', error.message); this.cache();
      } finally {
        this.inflight = null;
        if (this.pending && this.connected && !this.blocked) this.timer = setTimeout(() => this.flush(), 100);
      }
    })();
    return this.inflight;
  }
  async retry() {
    try {
      const response = await this.request('GET'); if (!response.ok) throw new Error('服务无法读取项目记录');
      const remote = await response.json();
      if (remote.exists && this.revision !== remote.revision) { this.blocked = true; this.status('conflict'); return; }
      this.revision = remote.revision; this.connected = true; this.blocked = false; await this.flush();
    } catch (error) { this.status('offline', error.message); }
  }
  async useProject() {
    if (this.inflight) await this.inflight;
    const response = await this.request('GET'); if (!response.ok) throw new Error('项目记录暂时无法读取');
    const remote = await response.json();
    // Retain one recovery copy even when the user explicitly chooses the project version.
    try { this.storage.setItem(this.cacheKey + '-recovery', JSON.stringify(this.current)); } catch { /* Export is also available. */ }
    this.current = this.normalize(remote.progress); this.revision = remote.revision;
    this.connected = true; this.blocked = false; this.pending = false; clearTimeout(this.timer);
    this.cache(); this.status('saved'); return this.current;
  }
}
