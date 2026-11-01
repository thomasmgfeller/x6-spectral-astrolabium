import {analyze, makeModel} from './engine.mjs';

export const ARCHIVE_URL = 'https://raw.githubusercontent.com/thomasmgfeller/x6-spectral-astrolabium/anu-qrng-data/latest.json';
const SOURCE = 'https://api.quantumnumbers.anu.edu.au/?length=1024&type=uint8';

export async function replayBlock(record) {
  if (record?.schema !== 'x6.anu-qrng/1' || record.source !== SOURCE ||
      record.provider !== 'Australian National University' ||
      record.usage_terms !== 'https://quantumnumbers.anu.edu.au/faq' ||
      record.type !== 'uint8' || record.length !== 1024 ||
      typeof record.data_hex !== 'string' || !/^[a-f0-9]{2048}$/.test(record.data_hex) ||
      !Number.isFinite(Date.parse(record.retrieved_at))) {
    throw new Error('Das Archivformat ist ungültig.');
  }
  const bytes = Uint8Array.from(record.data_hex.match(/../g), x => parseInt(x, 16));
  const hash = new Uint8Array(await crypto.subtle.digest('SHA-256', bytes));
  if (Array.from(hash, b => b.toString(16).padStart(2, '0')).join('') !== record.sha256) {
    throw new Error('Die Prüfsumme der Zahlen stimmt nicht mit dem Archiv überein.');
  }
  const {transfer} = analyze(makeModel({preset: 'cspp', n: 5, theta: 21}));
  // One byte per trial. The three low bits supply the three history signs.
  // eta=1. RMS is over trials, not the standard deviation about their sample mean.
  let sumSquares = 0;
  for (const b of bytes) {
    const response = transfer.reduce((sum, t, i) => sum + ((b >> i) & 1 ? t : -t), 0);
    sumSquares += response ** 2;
  }
  return {rms: Math.sqrt(sumSquares / bytes.length), expectedRms: Math.hypot(...transfer),
    trials: bytes.length};
}
