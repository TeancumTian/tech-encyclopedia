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
export function normalizeProgress(raw, validIds) {
  const allowed = new Set(validIds);
  const ids = value => Array.isArray(value) ? [...new Set(value.filter(id => allowed.has(id)))] : [];
  return {
    learned: ids(raw?.learned), saved: ids(raw?.saved), passed: ids(raw?.passed),
    last: allowed.has(raw?.last) ? raw.last : null,
    notes: Object.fromEntries(Object.entries(raw?.notes && typeof raw.notes === 'object' ? raw.notes : {})
      .filter(([id, note]) => allowed.has(id) && typeof note === 'string')
      .map(([id, note]) => [id, note.slice(0, 5000)])),
  };
}
