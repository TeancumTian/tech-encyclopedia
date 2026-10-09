// Static hosting uses a path-scoped localStorage record, with no progress API calls.
export const browserStorageKey = url => 'tech-encyclopedia-browser-v2:' + new URL('.', url).pathname;

export class BrowserProgress {
  constructor({normalize, onStatus, cacheKey, storage = localStorage}) {
    this.normalize = normalize; this.onStatus = onStatus; this.cacheKey = cacheKey;
    this.storage = storage; this.current = null; this.snapshot = null;
    this.pending = false; this.blocked = false; this.corrupt = false;
    this.status('loading');
  }
  status(state, message = '') { this.state = state; this.message = message; this.onStatus?.(state, message); }
  decode(raw) {
    if (raw === null) return this.normalize({});
    const record = JSON.parse(raw);
    if (record?.format !== 2 || !record.progress || typeof record.progress !== 'object' || Array.isArray(record.progress)) throw new Error('Invalid browser record');
    return this.normalize(record.progress);
  }
  async init(legacy) {
    this.current = this.normalize(legacy);
    try {
      this.snapshot = this.storage.getItem(this.cacheKey);
      if (this.snapshot !== null) {
        try { this.current = this.decode(this.snapshot); }
        catch { this.corrupt = true; throw new Error('浏览器存档无法读取，原记录已保留。请先导出当前记录备份，再使用下方清空功能重新开始。'); }
        this.status('saved');
      } else this.schedule(this.current);
    } catch (error) {
      this.blocked = true; this.status('error', this.corrupt ? error.message : '浏览器存储不可用。请允许本站存储数据，或用导出功能保存本次记录。');
    }
    return this.current;
  }
  schedule(progress) {
    this.current = this.normalize(progress); this.pending = true; this.flush();
  }
  flush() {
    if (!this.pending || this.blocked) return;
    try {
      if (this.storage.getItem(this.cacheKey) !== this.snapshot) {
        this.blocked = true; this.status('conflict'); return;
      }
      const raw = JSON.stringify({format:2, updatedAt:Date.now(), progress:this.current});
      this.storage.setItem(this.cacheKey, raw);
      this.snapshot = raw; this.pending = false; this.status('saved');
    } catch {
      this.status('error', '浏览器存储空间不足或已被禁用。当前改动仍在页面中，请立即导出备份；恢复存储后可以重试。');
    }
  }
  observe(event) {
    if ((event.key === this.cacheKey || event.key === null) && event.newValue !== this.snapshot) {
      this.blocked = true; this.status('conflict');
    }
  }
  retry() {
    if (this.corrupt) return;
    this.blocked = false; this.pending = true; this.flush();
  }
  async useProject() {
    // Same adapter method as ProjectProgress: load the current persistent version.
    const raw = this.storage.getItem(this.cacheKey);
    let loaded;
    try { loaded = this.decode(raw); } catch { throw new Error('浏览器存档已损坏，未替换当前记录。请先导出备份。'); }
    try { this.storage.setItem(this.cacheKey + '-recovery', JSON.stringify(this.current)); } catch { /* Export remains available. */ }
    this.current = loaded; this.snapshot = raw; this.pending = false; this.blocked = false; this.corrupt = false;
    this.status('saved'); return this.current;
  }
  reset(progress) {
    // Called only by the explicit reset control, also permits recovery from malformed storage.
    this.current = this.normalize(progress); this.pending = true;
    try { this.snapshot = this.storage.getItem(this.cacheKey); }
    catch { this.status('error', '浏览器存储不可用，清空操作未保存。'); return; }
    this.blocked = false; this.corrupt = false; this.flush();
  }
}
