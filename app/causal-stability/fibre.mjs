const entry = document.getElementById('faser-load');
const slider = document.getElementById('faser-phase');
const status = document.getElementById('faser-status');
let channels;

function update() {
  const [a,b] = channels.T1.coefficients;
  const delta = Number(slider.value);
  const theta = Math.PI + Math.atan2(a[1],a[0]) - Math.atan2(b[1],b[0]) + delta*Math.PI/180;
  const c = Math.cos(theta), s = Math.sin(theta);
  function intensity([[ar,ai],[br,bi]]) {
    return ((ar+br*c-bi*s)**2 + (ai+br*s+bi*c)**2)/2;
  }
  const t1 = intensity(channels.T1.coefficients), t2 = intensity(channels.T2.coefficients);
  const reference = (Math.hypot(...a)+Math.hypot(...b))**2/2;
  document.getElementById('faser-angle').textContent = delta+'°';
  document.getElementById('faser-values').textContent =
    `T1: ${(100*t1/reference).toFixed(3)} % der konstruktiven T1-Referenz · Modellintensität (relative Einheiten): T1 ${t1.toExponential(3)}, T2 ${t2.toExponential(3)}, Summe ${(t1+t2).toExponential(3)}`;
}

entry.addEventListener('click',async () => {
  entry.disabled = true;
  try {
    const url = new URL('./fibre-data/record.json',import.meta.url);
    const result = await fetch(url,{cache:'no-cache'});
    if (!result.ok) throw Error('HTTP '+result.status);
    const data = await result.json();
    if (data.schema !== 'x6-mit-fibre-v1' || data.source.doi !== 'doi:10.5061/dryad.wdbrv15wk')
      throw Error('Unerwartete Archivquelle');
    if (data.status === 'METADATA_ONLY') {
      status.textContent = 'Dryad-Metadaten vorhanden. Der Import der geprüften Matrix steht aus.';
      return;
    }
    if (data.status !== 'VERIFIED_MATRIX_SLICE' || data.model !== 'two-equal-inputs-phase-error-v1')
      throw Error('Unbekannte Mess- oder Modellversion');
    channels = data.measurement.channels;
    for (const name of ['T1','T2']) {
      const row = channels[name].coefficients;
      if (row.length!==2 || !row.every(z=>z.length===2 && z.every(Number.isFinite))) throw Error('Ungültige Koeffizienten');
    }
    if (!channels.T1.coefficients.every(z=>Math.hypot(...z)>0)) throw Error('Undefinierte Phasenreferenz');
    status.textContent = 'Originaldatei beim Import per SHA-256 geprüft · Ausgangszeile 0 · Eingangsspalten 0 und 1';
    update();
    document.getElementById('faser-result').hidden = false;
    entry.hidden = true;
  } catch (error) { status.textContent = 'Messarchiv nicht verfügbar: '+error.message; }
  finally { entry.disabled = false; }
});
slider.addEventListener('input', update);
