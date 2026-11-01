import {ARCHIVE_URL, replayBlock} from './anu-control.mjs';

const button = document.getElementById('anu-load');
const status = document.getElementById('anu-status');
const link = document.getElementById('anu-download');
const format = value => value.toLocaleString('de-CH', {maximumSignificantDigits: 5});

button.addEventListener('click', async () => {
  button.disabled = true;
  link.hidden = true;
  status.textContent = 'Archivblock wird geladen und geprüft …';
  try {
    const response = await fetch(ARCHIVE_URL, {cache: 'no-store', credentials: 'omit',
      signal: AbortSignal.timeout(12000)});
    if (response.status === 404) {
      status.textContent = 'Es ist noch kein ANU-Block im öffentlichen Archiv verfügbar.';
      return;
    }
    if (!response.ok) throw new Error('Das Archiv ist zurzeit nicht erreichbar.');
    const record = await response.json();
    const result = await replayBlock(record);
    status.textContent = `Abruf ${new Date(record.retrieved_at).toLocaleString('de-CH', {timeZone: 'UTC'})} UTC · ` +
      `${result.trials} Eingaben · beobachtete RMS-Antwort ${format(result.rms)} · ` +
      `theoretische RMS-Antwort ${format(result.expectedRms)}. SHA-256 geprüft.`;
    // Link to the exact bytes just replayed, even if the weekly archive advances.
    if (link.href) URL.revokeObjectURL(link.href);
    link.href = URL.createObjectURL(new Blob([JSON.stringify(record, null, 2)], {type: 'application/json'}));
    link.hidden = false;
  } catch (err) {
    status.textContent = err instanceof Error ? 'Keine Auswertung. ' + err.message : 'Abruf fehlgeschlagen.';
  } finally {
    button.disabled = false;
  }
});
