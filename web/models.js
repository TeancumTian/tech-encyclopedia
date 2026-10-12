// Pure models: units and simplifications are also shown in the interface.
export function gateOutput(gate, a, b) {
  if (gate === 'AND') return Number(Boolean(a && b));
  if (gate === 'OR') return Number(Boolean(a || b));
  if (gate === 'XOR') return Number(Boolean(a) !== Boolean(b));
  throw new Error('Unknown gate');
}
export const binaryValue = bits => bits.reduce((sum, bit) => sum * 2 + Number(bit), 0);
export const circuitCurrent = (volts, ohms) => volts / ohms;
export const transmissionLoss = (kv, powerKW = 1000, resistance = 10) => {
  const amps = powerKW / kv;
  return { amps, lossKW: amps * amps * resistance / 1000 };
};
export const gradientStep = (x, rate) => x - rate * 2 * x;
// Delta-v to reach low Earth orbit in km/s: the manuscript's estimate, drag and gravity losses included.
export const LEO_DELTA_V = 9.4;
// Tsiolkovsky equation for a single stage. propellantFraction = propellant mass / liftoff mass.
export function rocketDeltaV(exhaustKmS, propellantFraction) {
  if (!(exhaustKmS > 0) || !(propellantFraction >= 0) || !(propellantFraction < 1)) return 0;
  return exhaustKmS * Math.log(1 / (1 - propellantFraction));
}
// Upper limit for an ideal reversible heat engine; inputs in degrees Celsius, computed in kelvin.
export function carnotEfficiency(hotC, coldC) {
  const hot = hotC + 273.15, cold = coldC + 273.15;
  return hot > cold && cold > 0 ? 1 - cold / hot : 0;
}
// Ideal amplification: every cycle copies a fraction `efficiency` of the molecules present.
export const pcrCopies = (cycles, efficiency = 1, start = 1) => start * (1 + Math.max(0, Math.min(1, efficiency))) ** Math.max(0, cycles);
// Shift cipher over the 26 Latin letters; every other character is returned unchanged.
export function caesarShift(text, shift) {
  const k = ((Math.trunc(shift) % 26) + 26) % 26;
  return String(text).replace(/[A-Za-z]/g, ch => { const base = ch <= 'Z' ? 65 : 97; return String.fromCharCode((ch.charCodeAt(0) - base + k) % 26 + base); });
}
// Geometric similarity: lengths x k, areas x k^2, volume and weight x k^3, so load per unit of base area x k.
export const scaleLaw = k => ({ area: k * k, volume: k ** 3, pressure: k });
// Language-neutral count: grouped digits below a million, otherwise mantissa x 10^n.
export function formatCount(n) {
  if (!Number.isFinite(n)) return '∞';
  if (n < 1e6) return Math.round(n).toLocaleString('en-US');
  let exponent = Math.floor(Math.log10(n)), mantissa = Number((n / 10 ** exponent).toFixed(2));
  if (mantissa >= 10) { mantissa /= 10; exponent++; }
  return `${mantissa.toFixed(2)} × 10${String(exponent).replace(/\d/g, d => '⁰¹²³⁴⁵⁶⁷⁸⁹'[d])}`;
}
export function normalizeProgress(raw, validIds, readingIds = []) {
  const allowed = new Set(validIds), sections = new Set(readingIds);
  const ids = value => Array.isArray(value) ? [...new Set(value.filter(id => allowed.has(id)))] : [];
  const object = value => value && typeof value === 'object' && !Array.isArray(value) ? value : {};
  const fraction = value => Number.isFinite(value) ? Math.max(0, Math.min(1, value)) : 0;
  const stamp = value => Number.isFinite(value) && value >= 0 && value <= 1e15 ? Math.floor(value) : 0;
  return {
    learned: ids(raw?.learned), saved: ids(raw?.saved), passed: ids(raw?.passed), mistakes: ids(raw?.mistakes),
    last: allowed.has(raw?.last) ? raw.last : null,
    lastRead: sections.has(raw?.lastRead) ? raw.lastRead : null,
    notes: Object.fromEntries(Object.entries(object(raw?.notes))
      .filter(([id, note]) => allowed.has(id) && typeof note === 'string')
      .map(([id, note]) => [id, note.slice(0, 5000)])),
    reading: Object.fromEntries(Object.entries(object(raw?.reading)).filter(([id, value]) => sections.has(id) && value && typeof value === 'object')
      .map(([id, v]) => [id, {fraction:fraction(v.fraction), maxFraction:fraction(v.maxFraction), anchor:String(v.anchor || '').slice(0,100), offset:fraction(v.offset), finished:v.finished === true, updatedAt:stamp(v.updatedAt)}])),
    review: Object.fromEntries(Object.entries(object(raw?.review)).filter(([id, v]) => allowed.has(id) && v && typeof v === 'object')
      .map(([id, v]) => [id, {due:stamp(v.due), interval:Math.min(30,stamp(v.interval)), count:Math.min(10000,stamp(v.count)), rating:v.rating === 'know' ? 'know' : 'again'}])),
    prefs: {fontSize:raw?.prefs?.fontSize === 'large' ? 'large' : 'normal', focus:raw?.prefs?.focus === true, language:['zh','en','bi'].includes(raw?.prefs?.language)?raw.prefs.language:'zh',theme:['auto','dark','light'].includes(raw?.prefs?.theme)?raw.prefs.theme:'auto'},
  };
}

export function nextReview(previous, rating, now = Date.now()) {
  const count = Math.min(10000, (previous?.count || 0) + 1);
  const interval = rating === 'know' ? Math.min(30, previous?.rating === 'know' ? Math.max(1,previous.interval) * 2 + 1 : 1) : 0;
  return {due:now + (rating === 'know' ? interval * 86400000 : 600000), interval, count, rating};
}

export function mergeProgress(incoming, current) {
  const result = {...incoming, ...current};
  for (const field of ['learned', 'saved', 'passed', 'mistakes']) result[field] = [...new Set([...(incoming[field] || []), ...(current[field] || [])])];
  for (const field of ['notes', 'reading', 'review']) result[field] = {...incoming[field], ...current[field]};
  result.last ||= incoming.last;
  result.lastRead ||= incoming.lastRead;
  return result;
}
