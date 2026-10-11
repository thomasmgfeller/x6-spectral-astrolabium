/* Experimental integration preview. Scientific decisions use raw counts only. */
(function () {
  'use strict';
  const $ = id => document.getElementById(id), core = window.X6Sagnac;
  let latest = null, revision = 0, polling = null, state = 'idle', detail = '';
  const words = {
    de: { title: 'Sagnac · Messdaten und Gerätestatus', subtitle: 'Integrationsvorschau 0.1 · SGNCv007 · lokale Auswertung',
      source: 'Datenquelle', demo: 'Synthetisches Beispiel laden', origin: 'Herkunft der Datei', choose: 'Bitte ausdrücklich wählen', synthetic: 'Synthetisch', hardware: 'Hardware — von dir deklariert',
      sequence: 'Erwartete erste Sequenznummer', file: 'Binäre Aufzeichnung (.bin)', import: 'Datei prüfen', connect: 'Lokale Messbrücke abfragen', poll: 'Automatisch alle 2 Sekunden abfragen',
      bridgeHelp: 'Für die lokale Messbrücke: python3 device/sagnac_bridge.py starten und die dort angezeigte Adresse öffnen. Ohne Brücke funktionieren Beispiel und Dateiimport.',
      status: 'Erfassungsstatus', idle: 'Noch keine Daten', loading: 'Daten werden geprüft', valid: 'Datenprüfung bestanden', invalid: 'Ungültig — Ergebnisse gesperrt', waiting: 'Warte auf vollständige Aufnahme',
      physical: 'Physikalischer Quantennachweis: nicht bewertet', calibration: 'Kalibrier-ID vorhanden; reale Kalibrierung nicht geprüft.', provenance: 'Herkunft ist eine Deklaration, keine Authentifizierung.',
      measurements: 'Unveränderte Zähler', setting: 'Einstellung', seq: 'Sequenz', cal: 'Kalibrier-ID', trials: 'Zeitfenster', clicks: 'Klicks A+ / A− / B+ / B−', coinc: 'Ausgewählte Koinzidenzen',
      statistics: 'CHSH · zwei getrennte Statistiken', conditional: 'Bedingte Koinzidenzen', all: 'Alle Zeitfenster, feste Zuordnung', statisticHelp: 'Nur vier unterschiedliche Einstellungen mit gleicher Kalibrier-ID und Fensterbreite werden kombiniert. Grenzen setzen unabhängige, gleich verteilte Trials voraus; Drift und Kalibrierfehler sind nicht enthalten.',
      control: 'Regelung: nicht verfügbar', controlHelp: 'v0.7 besitzt keinen Befehlsweg und keine bestätigten optischen Aktuatoren. Start, Wellenplattensteuerung und geschlossener Regelkreis sind deaktiviert. Eine Kalibrier-ID ist keine Freigabe.',
      disabled: 'Optische Regelung gesperrt', export: 'Prüfbericht mit Rohdaten exportieren', raw: 'Details und Annahmen',
      frames: 'Frames', bytes: 'Bytes', mode: 'Quelle', received: 'Importiert', noChsh: 'Vier unterschiedliche Einstellungen erforderlich.',
      noFile: 'Bitte eine Binärdatei auswählen.', noBridge: 'Messbrücke nur unter http://127.0.0.1 oder http://localhost verfügbar.',
      noSHA: 'SHA-256 ist in diesem Browser nicht verfügbar.', declared: 'Hardwareangabe ist unbestätigt', demoState: 'SYNTHETISCH · keine physische Messung',
      hash: 'SHA-256 der unveränderten Bytes', lower: 'Untere Schranke für −S', gate: 'Modellbedingtes Kriterium', yes: 'erfüllt', no: 'nicht erfüllt',
      sumHelp: 'Klickraten und Korrelationen sind Diagnosen. Die Snapshots enthalten keine einzelnen Photonen-Zeitstempel; daraus lassen sich keine Jitterverteilung oder Drift innerhalb eines Laufs rekonstruieren.' },
    en: { title: 'Sagnac · measurement data and device status', subtitle: 'Integration preview 0.1 · SGNCv007 · local analysis',
      source: 'Data source', demo: 'Load synthetic example', origin: 'File provenance', choose: 'Choose explicitly', synthetic: 'Synthetic', hardware: 'Hardware — declared by you', sequence: 'Expected first sequence number', file: 'Binary capture (.bin)', import: 'Validate file', connect: 'Read local bridge', poll: 'Refresh every 2 seconds',
      bridgeHelp: 'Start python3 device/sagnac_bridge.py and open its local URL. Example and file import also work without the bridge.',
      status: 'Acquisition status', idle: 'No data', loading: 'Validating data', valid: 'Data checks passed', invalid: 'Invalid — results blocked', waiting: 'Waiting for a complete capture',
      physical: 'Physical quantum claim: not assessed', calibration: 'Calibration ID present; physical calibration not verified.', provenance: 'Origin is declared, not authenticated.', measurements: 'Unmodified counts', setting: 'Setting', seq: 'Sequence', cal: 'Calibration ID', trials: 'Time bins', clicks: 'Clicks A+ / A− / B+ / B−', coinc: 'Selected coincidences',
      statistics: 'CHSH · separate statistics', conditional: 'Conditional coincidences', all: 'All trials, fixed assignment', statisticHelp: 'Only four distinct settings with matching calibration and bin width are combined. Bounds require iid trials; drift and calibration errors are not included.',
      control: 'Control unavailable', controlHelp: 'v0.7 has no command path or qualified optical actuators. Start, waveplate control and closed-loop operation are disabled. A calibration ID is not qualification.', disabled: 'Optical control blocked', export: 'Export evidence and raw bytes', raw: 'Details and assumptions', frames: 'Frames', bytes: 'Bytes', mode: 'Source', received: 'Imported', noChsh: 'Four distinct settings required.', noFile: 'Select a binary file.', noBridge: 'Bridge available only on http://127.0.0.1 or http://localhost.', noSHA: 'SHA-256 unavailable in this browser.', declared: 'Hardware provenance is unverified', demoState: 'SYNTHETIC · no physical measurement', hash: 'SHA-256 of unmodified bytes', lower: 'Lower bound for −S', gate: 'Model-conditional criterion', yes: 'met', no: 'not met', sumHelp: 'Rates and correlations are diagnostic. Snapshots contain no per-photon time tags; timing jitter and within-run drift cannot be reconstructed.' },
    fr: { title: 'Sagnac · mesures et état du dispositif', subtitle: 'Aperçu d’intégration 0.1 · SGNCv007 · analyse locale', source: 'Source des données', demo: 'Charger l’exemple synthétique', origin: 'Origine du fichier', choose: 'Choisir explicitement', synthetic: 'Synthétique', hardware: 'Matériel — déclaré par vous', sequence: 'Premier numéro de séquence attendu', file: 'Acquisition binaire (.bin)', import: 'Vérifier le fichier', connect: 'Lire le pont local', poll: 'Actualiser toutes les 2 secondes', bridgeHelp: 'Démarrer python3 device/sagnac_bridge.py et ouvrir son adresse locale. Exemple et import fonctionnent aussi sans pont.', status: 'État de l’acquisition', idle: 'Aucune donnée', loading: 'Vérification en cours', valid: 'Vérifications réussies', invalid: 'Invalide — résultats bloqués', waiting: 'En attente d’une acquisition complète', physical: 'Preuve quantique physique : non évaluée', calibration: 'Identifiant présent ; calibration physique non vérifiée.', provenance: 'Origine déclarée, non authentifiée.', measurements: 'Comptages non modifiés', setting: 'Réglage', seq: 'Séquence', cal: 'Calibration', trials: 'Fenêtres', clicks: 'Clics A+ / A− / B+ / B−', coinc: 'Coïncidences sélectionnées', statistics: 'CHSH · statistiques séparées', conditional: 'Coïncidences conditionnelles', all: 'Tous les essais, attribution fixe', statisticHelp: 'Quatre réglages distincts avec calibration et largeur identiques sont nécessaires. Les bornes supposent des essais iid ; dérive et erreurs de calibration exclues.', control: 'Régulation indisponible', controlHelp: 'v0.7 ne dispose pas de protocole de commande ni d’actionneurs optiques qualifiés. Démarrage, réglage des lames et boucle fermée désactivés.', disabled: 'Régulation optique bloquée', export: 'Exporter le rapport et les données brutes', raw: 'Détails et hypothèses', frames: 'Trames', bytes: 'Octets', mode: 'Source', received: 'Importé', noChsh: 'Quatre réglages distincts requis.', noFile: 'Choisir un fichier binaire.', noBridge: 'Pont disponible uniquement sur http://127.0.0.1 ou http://localhost.', noSHA: 'SHA-256 indisponible.', declared: 'Origine matérielle non vérifiée', demoState: 'SYNTHÉTIQUE · aucune mesure physique', hash: 'SHA-256 des octets non modifiés', lower: 'Borne inférieure de −S', gate: 'Critère conditionnel au modèle', yes: 'satisfait', no: 'non satisfait', sumHelp: 'Les taux et corrélations sont diagnostiques. Les instantanés ne contiennent pas les horodatages individuels ; gigue et dérive interne ne sont pas reconstructibles.' }
  };
  function lang() { return words[$('lang').value] || words.de; }
  function text(id, value) { $(id).textContent = value; }
  function fromBase64(value) { return Uint8Array.from(atob(value), c => c.charCodeAt(0)); }
  function base64(bytes) { let out = ''; for (let i = 0; i < bytes.length; i += 8192) out += String.fromCharCode(...bytes.subarray(i, i + 8192)); return btoa(out); }
  function clear(nextState, reason = '') {
    latest = null; state = nextState; detail = reason;
    $('sg-export').disabled = true; render();
  }
  function stopPoll() { clearTimeout(polling); polling = null; $('sg-poll').checked = false; }
  function render() {
    const t = lang();
    document.querySelectorAll('[data-sg]').forEach(el => el.textContent = t[el.dataset.sg]);
    text('sg-status', t[state] + (detail ? ' · ' + detail : ''));
    $('sg-status').dataset.state = state;
    text('sg-origin-badge', latest ? (latest.origin === 'synthetic' ? t.demoState : t.declared) : '—');
    text('sg-summary', latest ? `${t.frames}: ${latest.records.length} · ${t.bytes}: ${latest.input.bytes} · ${t.mode}: ${latest.input.mode}` : '—');
    text('sg-hash', latest ? latest.input.sha256 : '—');
    $('sg-counts').replaceChildren();
    if (latest) for (const r of latest.summaries.slice(0, 100)) {
      const row = document.createElement('tr');
      for (const value of [r.setting_index, r.sequence, r.calibration_id, r.trials, r.clicks.join(' / '), r.conditional_coincidences.n]) {
        const td = document.createElement('td'); td.textContent = value; row.append(td);
      }
      $('sg-counts').append(row);
    }
    for (const [id, key] of [['sg-conditional', 'conditional_coincidences'], ['sg-all', 'all_trials_fixed_assignment']]) {
      const r = latest?.chsh[key];
      text(id, r?.S != null ? `S = ${r.S.toFixed(6)}\n${t.lower}: ${r.singlet_T_lower_hoeffding.toFixed(6)}\n${t.gate}: ${r.model_conditional_gate ? t.yes : t.no}` : t.noChsh);
    }
    text('sg-details', latest ? JSON.stringify({ ...latest, input: { ...latest.input, raw_base64: '(included in export)' } }, null, 2) : '{}');
  }
  async function accept(bytes, origin, sequence, mode, ticket, recorded = null) {
    const result = core.decode(bytes, origin, sequence);
    if (!crypto.subtle) throw Error(lang().noSHA);
    const digest = await crypto.subtle.digest('SHA-256', bytes);
    if (ticket !== revision) return;
    latest = { ...result, imported_at_utc: new Date().toISOString(), bridge_recorded_at_utc: recorded,
      input: { mode, bytes: bytes.length, expected_first_sequence: sequence,
        sha256: Array.from(new Uint8Array(digest), x => x.toString(16).padStart(2, '0')).join(''), raw_base64: base64(bytes) } };
    state = 'valid'; detail = ''; $('sg-export').disabled = false; render();
  }
  async function manual(action) {
    stopPoll(); const ticket = ++revision; clear('loading');
    try { await action(ticket); } catch (e) { if (ticket === revision) clear('invalid', e.message); }
  }
  $('sg-demo').onclick = () => manual(ticket => accept(fromBase64(window.X6SagnacDemo), 'synthetic', '100', 'BUILT_IN_SYNTHETIC_FIXTURE', ticket));
  $('sg-import').onclick = () => manual(async ticket => {
    const f = $('sg-file').files[0]; if (!f) throw Error(lang().noFile);
    if (f.size > core.FRAME_BYTES * 4096) throw Error('Maximum 4096 frames');
    const origin = $('sg-origin').value, sequence = $('sg-sequence').value;
    await accept(new Uint8Array(await f.arrayBuffer()), origin, sequence, 'LOCAL_FILE_REPLAY', ticket);
  });
  async function bridge() {
    const ticket = ++revision; clear('loading');
    const controller = new AbortController(), timer = setTimeout(() => controller.abort(), 5000);
    try {
      if (location.protocol !== 'http:' || !['localhost', '127.0.0.1'].includes(location.hostname)) throw Error(lang().noBridge);
      const response = await fetch('/api/sagnac/capture', { cache: 'no-store', signal: controller.signal });
      if (!response.ok) throw Error('Local bridge HTTP ' + response.status);
      const r = await response.json();
      if (ticket !== revision) return;
      if (r.schema !== 'x6.sagnac.bridge/1' || r.capabilities?.closed_loop !== false) throw Error('Unexpected bridge contract');
      if (r.status === 'WAITING') { clear('waiting'); return; }
      if (r.status !== 'COMPLETE') throw Error(r.reason || 'Incomplete capture');
      if (typeof r.raw_base64 !== 'string' || r.raw_base64.length > 1400000) throw Error('Invalid bridge payload');
      await accept(fromBase64(r.raw_base64), r.origin, r.first_sequence, r.mode, ticket, r.recorded_at_utc);
      if (latest && latest.input.sha256 !== r.raw_sha256) throw Error('Bridge SHA-256 mismatch');
    } catch (e) { if (ticket === revision) clear('invalid', e.message); }
    finally {
      clearTimeout(timer);
      if (ticket === revision && $('sg-poll').checked) polling = setTimeout(bridge, 2000);
    }
  }
  $('sg-connect').onclick = () => { stopPoll(); bridge(); };
  $('sg-poll').onchange = () => { if ($('sg-poll').checked) bridge(); else { stopPoll(); ++revision; clear('idle'); } };
  $('sg-export').onclick = () => {
    if (!latest) return;
    const u = URL.createObjectURL(new Blob([JSON.stringify(latest, null, 2)], { type: 'application/json' }));
    const a = document.createElement('a'); a.href = u; a.download = 'X6_Sagnac_Evidence_' + latest.origin + '.json'; a.click();
    setTimeout(() => URL.revokeObjectURL(u), 1000);
  };
  $('lang').addEventListener('change', render);
  render();
})();
