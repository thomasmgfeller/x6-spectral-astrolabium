/* Local companion UI. Displayed curves come only from the current computed run.
 * Parameter edits and failed imports invalidate results; exports never use stale runs.
 */
(function () {
  'use strict';
  const $ = id => document.getElementById(id);
  const core = window.X6SignalLab;
  const evidence = window.X6SignalLabEvidence;
  const methods = ['identity', 'moving_average', 'fft_lowpass', 'x6_phase'];
  const metricKeys = ['rmse', 'nrmse', 'gain_error_pct', 'phase_error_deg', 'delay_samples', 'spectral_error', 'coherence_mean', 'snr_db'];
  const words = {
    de: {
      skip: 'Zum Inhalt', openX6: 'X6 öffnen', language: 'Sprache', eyebrow: 'Research companion / Signalprüfung',
      intro: 'Erzeuge einen bekannten Sollverlauf, füge definierte Störungen hinzu und prüfe vier Verfahren am unveränderten Referenzsignal.', synthetic: 'SYNTHETISCH',
      scope: 'Bekannte Sollwerte. Reproduzierbare Fehlerfälle. Ergebnisse gelten für den gewählten Test.', scopeFoot: 'Lokale Auswertung · keine physische Messung',
      stepSetup: 'Signal definieren', stepCompare: 'Verfahren vergleichen', stepEvidence: 'Prüfen & exportieren', configuration: 'KONFIGURATION', setupTitle: 'Dein Testsignal', reset: 'Standard',
      signal: 'Sollsignal', sine: 'Sinus', multitone: 'Mehrtonsignal', chirp: 'Chirp', pulse: 'Puls', zero: 'Kein Signal / Nullkontrolle', frequency: 'Grundfrequenz (Hz)', amplitude: 'Amplitude (a.u.)', samples: 'Abtastwerte N', sampleRate: 'Abtastrate (Hz)',
      frequencyHelp: 'Mehrtonsignal und Chirp reichen bis 2,5 × Grundfrequenz. Alle modellierten Frequenzen müssen unter der Nyquist-Grenze bleiben.', seed: 'Zufallsseed', noise: 'Rausch-σ (a.u.)', noiseHelp: 'Gaußsches weißes Rauschen; gleicher Seed und gleiche Parameter erzeugen dieselben Daten.',
      distortions: 'Weitere Störungen', gain: 'Verstärkung', phase: 'Phasenfehler (°)', delay: 'Zeitversatz (Samples)', clipping: 'Clipping ± (a.u.)', quantBits: 'Quantisierung (Bit)', quantRange: 'Quantisierungsbereich ±', distortionHelp: 'Clipping = 0 und Bit = 0 deaktivieren die Störung. Für Puls und Nullsignal muss der Phasenfehler 0 sein. a.u. bezeichnet willkürliche Amplitudeneinheiten.',
      processing: 'Parameter der Verfahren', maWindow: 'Gleitender Mittelwert: Fenster', cutoff: 'FFT-Tiefpass: Grenze (Hz)', phaseCenter: 'X6: Winkelmitte (°)', phaseWidth: 'X6: gesamte Breite (°)', phaseMode: 'X6: Winkelmodus', phasePass: 'Winkelbereich durchlassen', phaseStop: 'Winkelbereich sperren', processingHelp: 'Alle vier Verfahren erhalten dieselben gestörten Daten. Die X6-Winkelmaske ist ein experimenteller Vergleichskandidat.',
      acceptance: 'Akzeptanzgrenzen festlegen', acceptanceHelp: 'Diese veränderbaren Startwerte sind Prüfkriterien für diesen Test, keine allgemeine Qualitätsnorm. Lege sie vor dem Vergleich fest.', gainMax: 'Verstärkungsfehler % ≤', phaseMax: 'Phasenfehler ° ≤', delayMax: 'Zeitversatz Samples ≤', spectralMax: 'Spektralfehler ≤', coherenceMin: 'Kohärenz ≥', phaseCoherenceMin: 'Mindestkohärenz für Phasenwertung', run: 'Test ausführen', runHelp: 'Änderungen verwerfen die vorherige Auswertung. Berechnet wird erst beim Start.',
      actualArrays: 'BERECHNETE DATEN', waveTitle: 'Soll, Eingang und Ergebnis', displayMethod: 'Angezeigtes Verfahren', identity: 'Identität / unverändert', moving_average: 'Gleitender Mittelwert', fft_lowpass: 'FFT-Tiefpass', x6_phase: 'X6-Winkelmaske',
      reference: 'Bekannter Sollverlauf', observed: 'Gestörter Eingang', output: 'Verfahrensergebnis', referenceShort: 'Soll', outputShort: 'Ergebnis', emptyTitle: 'Hier erscheinen deine Testdaten', emptyDetail: 'Keine Beispielkurve vor der Berechnung.', timeCaption: 'Alle Kurven stammen aus den exportierbaren Arrays. Keine nachträgliche Phasen- oder Zeitkorrektur zur Verbesserung der Fehlerwerte.',
      selectedCriteria: 'Kriterien dieses Verfahrens', gainError: 'Verstärkungsfehler', phaseError: 'Phasenfehler', sameInput: 'IDENTISCHER EINGANG', compareTitle: 'Vier Verfahren, ein Maßstab', comparisonHelp: 'Fehler werden gegen das bekannte Sollsignal gemessen. Hohe Kohärenz allein belegt keine korrekte Rekonstruktion. „Offen“ kennzeichnet fehlende oder mehrdeutige Diagnosen.',
      method: 'Verfahren', gainColumn: 'Gainfehler %', phaseColumn: 'Phase °', delayColumn: 'Versatz', coherenceColumn: 'Kohärenz', criteria: 'Kriterien', tableHelp: 'Wähle ein Verfahren in der Tabelle, um dessen Kurven und Einzelkriterien zu sehen. Auf kleinen Bildschirmen ist die Tabelle seitlich scrollbar.', individualCriteria: 'Einzelkriterien und Diagnosen des angezeigten Verfahrens',
      spectralView: 'SPEKTRALDIAGNOSE', psdTitle: 'Leistungsdichte', awaitingData: 'Wartet auf Berechnung', psdCaption: 'Welch-Leistungsdichte, logarithmische y-Achse. Nullwerte bleiben Lücken; es wird kein künstlicher Mindestwert eingesetzt. Eine ähnliche PSD schließt Zeit- und Phasenfehler nicht aus.', relationToTruth: 'BEZUG ZUM SOLLSIGNAL', coherenceTitle: 'Kohärenz & Phase', phaseShort: 'Phase', coherenceCaption: 'Kohärenz links (0–1), Kreuzspektralphase rechts (°). Undefinierte Werte bleiben Lücken. Hohe Kohärenz kann trotz falscher Verstärkung oder Phase auftreten.',
      challengeAssumptions: 'ANNAHMEN PRÜFEN', suiteTitle: 'Gegenbeispiele statt guter Noten', boundedSuite: 'Begrenzte Prüfsuite', suiteIntro: 'Prüfe gezielte Fälle, in denen PSD oder Kohärenz allein ein irreführendes Urteil erlauben. Ein bestandener Prüffall bedeutet, dass der erwartete Fehler erkannt wurde.', runSuite: 'Gegenbeispiele prüfen', suiteIdle: 'Noch nicht ausgeführt.', suiteRunning: 'Gegenbeispiele werden berechnet …', suitePassed: 'Erwartete Befunde bestätigt', suiteFailed: 'Mindestens ein erwarteter Befund fehlt', cases: 'Fälle', checks: 'Einzelprüfungen', expected: 'Erwartung', confirmed: 'Bestätigt', notConfirmed: 'Nicht bestätigt', coreChecks: 'Prüfdetails des Kerns (EN)',
      reproducibility: 'REPRODUZIERBARKEIT', evidenceTitle: 'Ergebnis mit Herkunft', evidenceIntro: 'JSON enthält Parameter, Arrays, Diagnosen und Prüfinformationen für die erneute Berechnung. CSV enthält die tatsächlich berechneten Zeitreihen.', exportJson: 'Prüfbericht JSON', exportCsv: 'Zeitreihen CSV', importLabel: 'JSON-Prüfbericht wiederholen', replay: 'Prüfen & wiederholen', importHelp: 'Der Import verwirft vorherige Ergebnisse. Erst nach Integritätsprüfung und Neuberechnung werden Ergebnisse und Exporte freigegeben. Eine Prüfsumme bestätigt keine physische Herkunft.', methodology: 'Methodik, Grenzen & Versionsdaten', methodologyHelp: 'Einzelne synthetische Läufe sind keine allgemeine Validierung. PSD, Kohärenz und Zeitfehler beantworten unterschiedliche Fragen. Nutze weitere, vorab festgelegte Seeds und echte Messdaten, bevor du Aussagen verallgemeinerst.', readDocs: 'Dokumentation öffnen ↗', footer: 'Experimentelle Signalprüfung · keine Hardwaresteuerung', backProject: 'Zur Projektübersicht ↗',
      idle: 'Bereit für den ersten Test', idleDetail: 'Wähle ein Sollsignal und starte die Auswertung.', pending: 'Parameter geändert · neu berechnen', pendingDetail: 'Vorherige Kurven und Exporte sind verworfen. Starte den Test mit diesen Einstellungen.', running: 'Signaltest wird berechnet …', runningDetail: 'Vier Verfahren, identische Daten und die festgelegten Kriterien.', ready: 'Ausgewertet · synthetischer Test', readyDetail: 'Die Ergebnisse gehören zu den angezeigten Parametern. Die Kriterien bewerten nur diesen Test.', error: 'Prüfung abgebrochen · keine gültige Auswertung', importing: 'Prüfbericht wird überprüft …', importingDetail: 'Integrität, deklarierter Softwarestand und Neuberechnung werden verglichen.', replayReady: 'Replay geprüft · synthetischer Test', replayReadyDetail: 'Datei und Neuberechnung stimmen innerhalb der deklarierten Toleranzen überein. Physische Herkunft und Authentizität sind nicht bewertet.', filePending: 'Datei ausgewählt · Replay ausführen', filePendingDetail: 'Vorherige Ergebnisse sind verworfen. „Prüfen & wiederholen“ berechnet den Inhalt erneut.', defaultsPending: 'Standardwerte geladen · neu berechnen', suiteBusy: 'Gegenbeispiele werden geprüft …', suiteBusyDetail: 'Die feste Prüfsuite ändert keine Parameter des Signaltests.', exporting: 'Export wird geprüft …', exportingDetail: 'Die aktuelle Auswertung wird vor dem Export erneut nachvollzogen.', exportDone: 'Export erstellt',
      PASS: 'Erfüllt', FAIL: 'Verfehlt', INCONCLUSIVE: 'Offen', UNDEFINED: 'Undefiniert', AMBIGUOUS: 'Mehrdeutig', PARTIAL: 'Teilweise', DEFINED: 'Definiert', EXACT_MATCH: 'Exakte Übereinstimmung', noCurrentRun: 'Noch kein aktueller Test.', noPositivePsd: 'Keine positive PSD für diese Kurven', noSpectralRelation: 'Kohärenz und Phase hier undefiniert', validParameters: 'Bitte die markierten Parameter prüfen.', requiredNumber: 'Eine endliche Zahl ist erforderlich.', noFile: 'Wähle zuerst einen JSON-Prüfbericht.', oversized: 'Die Datei überschreitet die zulässigen 32 MiB.', unavailable: 'Benötigte lokale Module fehlen. Öffne die vollständige App mit allen Begleitdateien.', badReplay: 'Der Replay hat keine gültige, vollständig geprüfte Auswertung geliefert.',
      timeAxis: 'Zeit (s)', amplitudeAxis: 'Amplitude (a.u.)', frequencyAxis: 'f (Hz)', psdAxis: 'PSD (a.u.²/Hz)', metricValue: 'Wert', threshold: 'Grenze', absolute: 'Betrag', noGate: 'Dieses Kriterium kann mit einer fehlenden, teilweisen oder mehrdeutigen Diagnose nicht erfüllt sein.', technicalReason: 'Unveränderte Diagnose (EN)', partialMark: '* Teilweise definierter Wert; Kriterium bleibt offen.', verificationPassed: 'SHA-256 stimmt überein · Neuberechnung innerhalb der Toleranzen · deklarierter Build passt · Authentizität nicht bewertet.',
      rmse: 'RMSE', nrmse: 'NRMSE', gain_error_pct: 'RMS-Verstärkungsfehler', phase_error_deg: 'Gewichteter RMS-Phasenfehler', delay_samples: 'Geschätzter Zeitversatz', spectral_error: 'Relativer PSD-Fehler', coherence_mean: 'Gewichtete Kohärenz', snr_db: 'Rekonstruktions-SNR',
      case_polarity_inversion: 'Vorzeichenumkehr: gleiche PSD, falsches Signal', case_positive_delay: 'Puls um +7 Samples verzögert', case_negative_delay: 'Puls um −7 Samples vorgezogen', case_clipping: 'Clipping: kohärent und trotzdem verzerrt', case_zero_signal: 'Nullsignal: undefiniert bleibt undefiniert', case_dc_only: 'DC-Fehler hinter einer detrendeten PSD', case_periodic_delay_ambiguity: 'Periodischer Sinus: Zeitversatz mehrdeutig', case_x6_clean_signal_removal: 'X6-Winkelmaske entfernt ein sauberes Signal',
      expect_polarity_inversion: 'PSD und Kohärenz stimmen überein; NRMSE = 2 und ein Phasenfehler von 180° decken die Vorzeichenumkehr auf.', expect_positive_delay: 'Der geschätzte Versatz beträgt +7. Die Fehlerwerte werden ohne nachträgliche Ausrichtung berechnet.', expect_negative_delay: 'Der geschätzte Versatz beträgt −7. Das Vorzeichen darf weder verloren gehen noch durch eine zyklische Verschiebung ersetzt werden.', expect_clipping: 'Clipping verändert die Kurve und ihre Energie. Deterministische Abhängigkeit allein belegt keine Signalqualität.', expect_zero_signal: 'RMSE = 0 ist definiert. Normierte Fehler, Kohärenz, Phase und Zeitversatz bleiben ohne Signalenergie undefiniert.', expect_dc_only: 'Das segmentweise Entfernen des Mittelwerts verbirgt den DC-Unterschied im Spektrum. Zeitfehler und RMS-Verstärkungsfehler müssen ihn erkennen.', expect_periodic_delay_ambiguity: 'Identische Samples beseitigen die periodischen Mehrdeutigkeiten der Verzögerungsschätzung nicht.', expect_x6_clean_signal_removal: 'Eine Winkelmaske um 0° kann einen sauberen Sinus mit Fourierphase −90° entfernen. Der Verlust muss als Fehler erscheinen.'
    },
    en: {
      skip: 'Skip to content', openX6: 'Open X6', language: 'Language', eyebrow: 'Research companion / Signal validation', intro: 'Generate a known reference, add defined impairments and compare four methods against the unchanged reference signal.', synthetic: 'SYNTHETIC', scope: 'Known truth. Reproducible failure cases. Results apply to the selected test.', scopeFoot: 'Local analysis · no physical measurement',
      stepSetup: 'Define a signal', stepCompare: 'Compare methods', stepEvidence: 'Check & export', configuration: 'CONFIGURATION', setupTitle: 'Your test signal', reset: 'Defaults', signal: 'Reference signal', sine: 'Sine', multitone: 'Multitone', chirp: 'Chirp', pulse: 'Pulse', zero: 'No signal / null control', frequency: 'Base frequency (Hz)', amplitude: 'Amplitude (a.u.)', samples: 'Samples N', sampleRate: 'Sample rate (Hz)', frequencyHelp: 'Multitone and chirp reach 2.5 × the base frequency. All modeled frequencies must remain below Nyquist.', seed: 'Random seed', noise: 'Noise σ (a.u.)', noiseHelp: 'Gaussian white noise; the same seed and parameters generate the same data.',
      distortions: 'Additional impairments', gain: 'Gain', phase: 'Phase offset (°)', delay: 'Delay (samples)', clipping: 'Clipping ± (a.u.)', quantBits: 'Quantization (bits)', quantRange: 'Quantizer range ±', distortionHelp: 'Clipping = 0 and bits = 0 disable those impairments. Phase offset must be 0 for pulse and zero signals. a.u. denotes arbitrary amplitude units.', processing: 'Method parameters', maWindow: 'Moving average: window', cutoff: 'FFT low-pass: cutoff (Hz)', phaseCenter: 'X6: angle center (°)', phaseWidth: 'X6: full width (°)', phaseMode: 'X6: angle mode', phasePass: 'Pass the angle interval', phaseStop: 'Reject the angle interval', processingHelp: 'All four methods receive the same impaired data. The X6 phase mask is an experimental comparison candidate.',
      acceptance: 'Set acceptance limits', acceptanceHelp: 'These editable starting limits are criteria for this test, not a universal quality standard. Set them before comparing results.', gainMax: 'Gain error % ≤', phaseMax: 'Phase error ° ≤', delayMax: 'Delay samples ≤', spectralMax: 'Spectral error ≤', coherenceMin: 'Coherence ≥', phaseCoherenceMin: 'Minimum coherence for phase scoring', run: 'Run signal test', runHelp: 'Edits discard the previous analysis. Computation starts only when you run the test.', actualArrays: 'COMPUTED DATA', waveTitle: 'Reference, input and result', displayMethod: 'Displayed method', identity: 'Identity / unchanged', moving_average: 'Moving average', fft_lowpass: 'FFT low-pass', x6_phase: 'X6 phase mask',
      reference: 'Known reference', observed: 'Impaired input', output: 'Method output', referenceShort: 'Reference', outputShort: 'Output', emptyTitle: 'Your test data will appear here', emptyDetail: 'No example curve before computation.', timeCaption: 'Every curve comes from the exportable arrays. No post-hoc phase or time alignment improves the error metrics.', selectedCriteria: 'Criteria for this method', gainError: 'Gain error', phaseError: 'Phase error', sameInput: 'IDENTICAL INPUT', compareTitle: 'Four methods, one reference', comparisonHelp: 'Errors are measured against known truth. High coherence alone does not establish correct reconstruction. “Open” marks missing or ambiguous diagnostics.', method: 'Method', gainColumn: 'Gain error %', phaseColumn: 'Phase °', delayColumn: 'Delay', coherenceColumn: 'Coherence', criteria: 'Criteria', tableHelp: 'Select a method in the table to see its curves and individual criteria. Scroll the table horizontally on smaller screens.', individualCriteria: 'Individual criteria and diagnostics for the displayed method',
      spectralView: 'SPECTRAL DIAGNOSTIC', psdTitle: 'Power spectral density', awaitingData: 'Waiting for computation', psdCaption: 'Welch power spectral density, logarithmic y-axis. Zero values remain gaps; no artificial floor is inserted. Similar PSD does not rule out time or phase errors.', relationToTruth: 'RELATION TO THE REFERENCE', coherenceTitle: 'Coherence & phase', phaseShort: 'Phase', coherenceCaption: 'Coherence on the left (0–1), cross-spectral phase on the right (°). Undefined values remain gaps. High coherence can coexist with incorrect gain or phase.',
      challengeAssumptions: 'CHALLENGE ASSUMPTIONS', suiteTitle: 'Counterexamples, not good grades', boundedSuite: 'Bounded test suite', suiteIntro: 'Check targeted cases where PSD or coherence alone permits a misleading judgment. A passed case means that the expected failure was recognized.', runSuite: 'Check counterexamples', suiteIdle: 'Not run yet.', suiteRunning: 'Computing counterexamples …', suitePassed: 'Expected findings confirmed', suiteFailed: 'At least one expected finding is missing', cases: 'cases', checks: 'checks', expected: 'Expected', confirmed: 'Confirmed', notConfirmed: 'Not confirmed', coreChecks: 'Core check details',
      reproducibility: 'REPRODUCIBILITY', evidenceTitle: 'A result with provenance', evidenceIntro: 'JSON includes parameters, arrays, diagnostics and verification information for computational replay. CSV contains the actual computed time series.', exportJson: 'Evidence JSON', exportCsv: 'Time series CSV', importLabel: 'Replay a JSON evidence file', replay: 'Verify & replay', importHelp: 'Import discards previous results. Results and exports become available only after integrity checks and recomputation. A checksum does not establish physical provenance.', methodology: 'Methodology, limits & versions', methodologyHelp: 'Individual synthetic runs do not establish general validity. PSD, coherence and time errors answer different questions. Use further seeds chosen in advance and real measurements before generalizing.', readDocs: 'Open documentation ↗', footer: 'Experimental signal validation · no hardware control', backProject: 'Back to the project ↗',
      idle: 'Ready for the first test', idleDetail: 'Choose a reference signal and run the analysis.', pending: 'Parameters changed · recomputation required', pendingDetail: 'Previous curves and exports have been discarded. Run the test with these settings.', running: 'Computing signal test …', runningDetail: 'Four methods, identical data and the declared criteria.', ready: 'Computed · synthetic test', readyDetail: 'The results belong to the displayed parameters. The criteria assess this test only.', error: 'Check stopped · no valid analysis', importing: 'Verifying evidence …', importingDetail: 'Comparing integrity, declared build and computational replay.', replayReady: 'Replay verified · synthetic test', replayReadyDetail: 'File and recomputation agree within declared tolerances. Physical origin and authenticity have not been assessed.', filePending: 'File selected · run replay', filePendingDetail: 'Previous results have been discarded. “Verify & replay” recomputes the content.', defaultsPending: 'Defaults loaded · recomputation required', suiteBusy: 'Checking counterexamples …', suiteBusyDetail: 'The fixed suite does not change the signal-test parameters.', exporting: 'Verifying export …', exportingDetail: 'Reconstructing the current analysis before export.', exportDone: 'Export created',
      PASS: 'Met', FAIL: 'Failed', INCONCLUSIVE: 'Open', UNDEFINED: 'Undefined', AMBIGUOUS: 'Ambiguous', PARTIAL: 'Partial', DEFINED: 'Defined', EXACT_MATCH: 'Exact match', noCurrentRun: 'No current test yet.', noPositivePsd: 'No positive PSD for these curves', noSpectralRelation: 'Coherence and phase are undefined here', validParameters: 'Please check the marked parameters.', requiredNumber: 'A finite number is required.', noFile: 'Choose a JSON evidence file first.', oversized: 'The file exceeds the 32 MiB limit.', unavailable: 'Required local modules are missing. Open the complete app with all companion files.', badReplay: 'Replay did not return a valid, fully verified analysis.',
      timeAxis: 'Time (s)', amplitudeAxis: 'Amplitude (a.u.)', frequencyAxis: 'f (Hz)', psdAxis: 'PSD (a.u.²/Hz)', metricValue: 'Value', threshold: 'Limit', absolute: 'Absolute value', noGate: 'A missing, partial or ambiguous diagnostic cannot meet this criterion.', technicalReason: 'Original diagnostic', partialMark: '* Partially defined value; the criterion remains open.', verificationPassed: 'SHA-256 matches · replay within tolerances · declared build matches · authenticity not assessed.',
      rmse: 'RMSE', nrmse: 'NRMSE', gain_error_pct: 'RMS gain error', phase_error_deg: 'Weighted RMS phase error', delay_samples: 'Estimated delay', spectral_error: 'Relative PSD error', coherence_mean: 'Weighted coherence', snr_db: 'Reconstruction SNR',
      case_polarity_inversion: 'Polarity reversal: same PSD, wrong signal', case_positive_delay: 'Pulse delayed by +7 samples', case_negative_delay: 'Pulse advanced by −7 samples', case_clipping: 'Clipping: coherent but distorted', case_zero_signal: 'Zero signal: undefined stays undefined', case_dc_only: 'DC error behind a detrended PSD', case_periodic_delay_ambiguity: 'Periodic sine: ambiguous delay', case_x6_clean_signal_removal: 'X6 phase mask removes a clean signal',
      expect_polarity_inversion: 'PSD and coherence agree; NRMSE = 2 and a 180° phase error reveal the polarity reversal.', expect_positive_delay: 'The estimated delay is +7. Error metrics are computed without post-hoc alignment.', expect_negative_delay: 'The estimated delay is −7. Its sign must not be lost or replaced by a circular shift.', expect_clipping: 'Clipping changes the waveform and its energy. Deterministic dependence alone does not establish signal quality.', expect_zero_signal: 'RMSE = 0 is defined. Without signal energy, normalized error, coherence, phase and delay remain undefined.', expect_dc_only: 'Removing segment means hides the DC difference in the spectrum. Time error and RMS gain error must reveal it.', expect_periodic_delay_ambiguity: 'Identical samples do not resolve periodic ambiguities in the delay estimate.', expect_x6_clean_signal_removal: 'A phase mask around 0° can remove a clean sine with Fourier phase −90°. That loss must be reported as a failure.'
    },
    fr: {
      skip: 'Aller au contenu', openX6: 'Ouvrir X6', language: 'Langue', eyebrow: 'Outil de recherche / Validation des signaux', intro: 'Générez une référence connue, ajoutez des perturbations définies et comparez quatre méthodes au signal de référence inchangé.', synthetic: 'SYNTHÉTIQUE', scope: 'Référence connue. Cas d’échec reproductibles. Résultats limités au test choisi.', scopeFoot: 'Analyse locale · aucune mesure physique',
      stepSetup: 'Définir le signal', stepCompare: 'Comparer les méthodes', stepEvidence: 'Vérifier et exporter', configuration: 'CONFIGURATION', setupTitle: 'Votre signal de test', reset: 'Valeurs initiales', signal: 'Signal de référence', sine: 'Sinusoïde', multitone: 'Signal multiton', chirp: 'Chirp', pulse: 'Impulsion', zero: 'Aucun signal / contrôle nul', frequency: 'Fréquence de base (Hz)', amplitude: 'Amplitude (u.a.)', samples: 'Échantillons N', sampleRate: 'Échantillonnage (Hz)', frequencyHelp: 'Le multiton et le chirp atteignent 2,5 × la fréquence de base. Toutes les fréquences modélisées doivent rester sous la limite de Nyquist.', seed: 'Graine aléatoire', noise: 'Bruit σ (u.a.)', noiseHelp: 'Bruit blanc gaussien ; graine et paramètres identiques produisent les mêmes données.',
      distortions: 'Autres perturbations', gain: 'Gain', phase: 'Décalage de phase (°)', delay: 'Retard (échantillons)', clipping: 'Écrêtage ± (u.a.)', quantBits: 'Quantification (bits)', quantRange: 'Plage du quantificateur ±', distortionHelp: 'Écrêtage = 0 et bits = 0 désactivent ces perturbations. La phase doit être 0 pour l’impulsion et le signal nul. u.a. indique des unités d’amplitude arbitraires.', processing: 'Paramètres des méthodes', maWindow: 'Moyenne mobile : fenêtre', cutoff: 'Passe-bas FFT : coupure (Hz)', phaseCenter: 'X6 : angle central (°)', phaseWidth: 'X6 : largeur totale (°)', phaseMode: 'X6 : mode angulaire', phasePass: 'Conserver l’intervalle', phaseStop: 'Rejeter l’intervalle', processingHelp: 'Les quatre méthodes reçoivent les mêmes données perturbées. Le masque de phase X6 est un candidat expérimental.',
      acceptance: 'Définir les seuils d’acceptation', acceptanceHelp: 'Ces seuils modifiables sont des critères pour ce test, pas une norme universelle. Fixez-les avant de comparer les résultats.', gainMax: 'Erreur de gain % ≤', phaseMax: 'Erreur de phase ° ≤', delayMax: 'Retard échantillons ≤', spectralMax: 'Erreur spectrale ≤', coherenceMin: 'Cohérence ≥', phaseCoherenceMin: 'Cohérence minimale pour évaluer la phase', run: 'Exécuter le test', runHelp: 'Toute modification annule l’analyse précédente. Le calcul commence uniquement au lancement.', actualArrays: 'DONNÉES CALCULÉES', waveTitle: 'Référence, entrée et résultat', displayMethod: 'Méthode affichée', identity: 'Identité / inchangé', moving_average: 'Moyenne mobile', fft_lowpass: 'Passe-bas FFT', x6_phase: 'Masque de phase X6',
      reference: 'Référence connue', observed: 'Entrée perturbée', output: 'Résultat de la méthode', referenceShort: 'Référence', outputShort: 'Résultat', emptyTitle: 'Vos données de test apparaîtront ici', emptyDetail: 'Aucune courbe d’exemple avant le calcul.', timeCaption: 'Chaque courbe provient des tableaux exportables. Aucun ajustement de phase ou de temps après calcul n’améliore les erreurs.', selectedCriteria: 'Critères de cette méthode', gainError: 'Erreur de gain', phaseError: 'Erreur de phase', sameInput: 'ENTRÉE IDENTIQUE', compareTitle: 'Quatre méthodes, une référence', comparisonHelp: 'Les erreurs sont mesurées par rapport à la référence connue. Une forte cohérence ne suffit pas à établir une reconstruction correcte. « Ouvert » indique un diagnostic manquant ou ambigu.',
      method: 'Méthode', gainColumn: 'Erreur gain %', phaseColumn: 'Phase °', delayColumn: 'Retard', coherenceColumn: 'Cohérence', criteria: 'Critères', tableHelp: 'Sélectionnez une méthode dans le tableau pour afficher ses courbes et ses critères. Le tableau défile horizontalement sur petit écran.', individualCriteria: 'Critères individuels et diagnostics de la méthode affichée', spectralView: 'DIAGNOSTIC SPECTRAL', psdTitle: 'Densité spectrale', awaitingData: 'En attente du calcul', psdCaption: 'Densité spectrale de Welch, axe vertical logarithmique. Les zéros restent absents, sans plancher artificiel. Une DSP similaire n’exclut pas les erreurs de temps ou de phase.', relationToTruth: 'RELATION À LA RÉFÉRENCE', coherenceTitle: 'Cohérence et phase', phaseShort: 'Phase', coherenceCaption: 'Cohérence à gauche (0–1), phase interspectrale à droite (°). Les valeurs indéfinies restent absentes. Une forte cohérence peut coexister avec un gain ou une phase incorrects.',
      challengeAssumptions: 'ÉPROUVER LES HYPOTHÈSES', suiteTitle: 'Des contre-exemples, pas des notes', boundedSuite: 'Suite de tests limitée', suiteIntro: 'Examinez des cas où DSP ou cohérence seules autorisent un jugement trompeur. Un cas réussi signifie que le défaut attendu a été reconnu.', runSuite: 'Vérifier les contre-exemples', suiteIdle: 'Pas encore exécuté.', suiteRunning: 'Calcul des contre-exemples …', suitePassed: 'Résultats attendus confirmés', suiteFailed: 'Au moins un résultat attendu manque', cases: 'cas', checks: 'vérifications', expected: 'Résultat attendu', confirmed: 'Confirmé', notConfirmed: 'Non confirmé', coreChecks: 'Détails des tests du noyau (EN)',
      reproducibility: 'REPRODUCTIBILITÉ', evidenceTitle: 'Un résultat avec sa provenance', evidenceIntro: 'Le JSON contient paramètres, tableaux, diagnostics et informations de vérification pour le recalcul. Le CSV contient les séries temporelles effectivement calculées.', exportJson: 'Rapport JSON', exportCsv: 'Séries temporelles CSV', importLabel: 'Rejouer un rapport JSON', replay: 'Vérifier et rejouer', importHelp: 'L’import annule les résultats précédents. Les résultats et exports sont activés après vérification d’intégrité et recalcul. Une empreinte ne confirme pas une origine physique.', methodology: 'Méthodologie, limites et versions', methodologyHelp: 'Un calcul synthétique isolé ne démontre pas une validité générale. DSP, cohérence et erreurs temporelles répondent à des questions distinctes. Utilisez d’autres graines fixées à l’avance et des mesures réelles avant de généraliser.', readDocs: 'Ouvrir la documentation ↗', footer: 'Validation expérimentale des signaux · aucune commande matérielle', backProject: 'Retour au projet ↗',
      idle: 'Prêt pour le premier test', idleDetail: 'Choisissez une référence et lancez l’analyse.', pending: 'Paramètres modifiés · recalcul nécessaire', pendingDetail: 'Les courbes et exports précédents ont été annulés. Lancez le test avec ces paramètres.', running: 'Calcul du test en cours …', runningDetail: 'Quatre méthodes, données identiques et critères déclarés.', ready: 'Calculé · test synthétique', readyDetail: 'Les résultats correspondent aux paramètres affichés. Les critères évaluent uniquement ce test.', error: 'Vérification arrêtée · aucune analyse valide', importing: 'Vérification du rapport …', importingDetail: 'Comparaison de l’intégrité, de la version déclarée et du recalcul.', replayReady: 'Recalcul vérifié · test synthétique', replayReadyDetail: 'Fichier et recalcul concordent dans les tolérances déclarées. Origine physique et authenticité non évaluées.', filePending: 'Fichier choisi · lancer le recalcul', filePendingDetail: 'Les résultats précédents ont été annulés. « Vérifier et rejouer » recalcule le contenu.', defaultsPending: 'Valeurs initiales chargées · recalcul nécessaire', suiteBusy: 'Vérification des contre-exemples …', suiteBusyDetail: 'La suite fixe ne modifie pas les paramètres du test de signal.', exporting: 'Vérification de l’export …', exportingDetail: 'Reconstruction de l’analyse actuelle avant export.', exportDone: 'Export créé',
      PASS: 'Satisfait', FAIL: 'Échec', INCONCLUSIVE: 'Ouvert', UNDEFINED: 'Indéfini', AMBIGUOUS: 'Ambigu', PARTIAL: 'Partiel', DEFINED: 'Défini', EXACT_MATCH: 'Concordance exacte', noCurrentRun: 'Aucun test actuel.', noPositivePsd: 'Aucune DSP positive pour ces courbes', noSpectralRelation: 'Cohérence et phase indéfinies ici', validParameters: 'Vérifiez les paramètres signalés.', requiredNumber: 'Un nombre fini est requis.', noFile: 'Choisissez d’abord un rapport JSON.', oversized: 'Le fichier dépasse la limite de 32 Mio.', unavailable: 'Des modules locaux sont absents. Ouvrez l’application complète avec tous ses fichiers.', badReplay: 'Le recalcul n’a pas produit une analyse valide et entièrement vérifiée.',
      timeAxis: 'Temps (s)', amplitudeAxis: 'Amplitude (u.a.)', frequencyAxis: 'f (Hz)', psdAxis: 'DSP (u.a.²/Hz)', metricValue: 'Valeur', threshold: 'Seuil', absolute: 'Valeur absolue', noGate: 'Un diagnostic manquant, partiel ou ambigu ne peut satisfaire ce critère.', technicalReason: 'Diagnostic original (EN)', partialMark: '* Valeur partiellement définie ; le critère reste ouvert.', verificationPassed: 'SHA-256 concordant · recalcul dans les tolérances · version déclarée concordante · authenticité non évaluée.',
      rmse: 'RMSE', nrmse: 'NRMSE', gain_error_pct: 'Erreur de gain RMS', phase_error_deg: 'Erreur de phase RMS pondérée', delay_samples: 'Retard estimé', spectral_error: 'Erreur relative de DSP', coherence_mean: 'Cohérence pondérée', snr_db: 'SNR de reconstruction',
      case_polarity_inversion: 'Inversion de signe : même DSP, signal faux', case_positive_delay: 'Impulsion retardée de +7 échantillons', case_negative_delay: 'Impulsion avancée de −7 échantillons', case_clipping: 'Écrêtage : cohérent mais déformé', case_zero_signal: 'Signal nul : indéfini reste indéfini', case_dc_only: 'Erreur continue cachée par la DSP', case_periodic_delay_ambiguity: 'Sinusoïde périodique : retard ambigu', case_x6_clean_signal_removal: 'Le masque X6 supprime un signal propre',
      expect_polarity_inversion: 'DSP et cohérence concordent ; NRMSE = 2 et une erreur de phase de 180° révèlent l’inversion.', expect_positive_delay: 'Le retard estimé vaut +7. Les erreurs sont calculées sans alignement ultérieur.', expect_negative_delay: 'Le retard estimé vaut −7. Son signe doit être conservé, sans substitution par un décalage circulaire.', expect_clipping: 'L’écrêtage modifie le signal et son énergie. Une dépendance déterministe ne démontre pas la qualité du signal.', expect_zero_signal: 'RMSE = 0 est défini. Sans énergie de référence, erreur normalisée, cohérence, phase et retard restent indéfinis.', expect_dc_only: 'Soustraire la moyenne de chaque segment cache la différence continue. L’erreur temporelle et le gain RMS doivent la détecter.', expect_periodic_delay_ambiguity: 'Des échantillons identiques ne résolvent pas les ambiguïtés périodiques de l’estimation du retard.', expect_x6_clean_signal_removal: 'Un masque autour de 0° peut supprimer une sinusoïde propre de phase de Fourier −90°. Cette perte doit apparaître comme un échec.'
    }
  };
  let language = 'de';
  try { const saved = localStorage.getItem('x6-signal-lab-language'); if (Object.hasOwn(words, saved)) language = saved; } catch (_) { /* File mode may restrict storage. */ }
  const state = { phase: 'idle', revision: 0, result: null, suite: null, verification: null, selectedMethod: 'identity', statusKey: 'idle', detailKey: 'idleDetail', errorText: '', suiteBusy: false, exportBusy: false };
  const controls = Array.from(document.querySelectorAll('[data-param]'));
  const text = (id, value) => { $(id).textContent = value; };
  const t = key => words[language][key] || words.en[key] || key;
  const create = (tag, className, content) => { const node = document.createElement(tag); if (className) node.className = className; if (content !== undefined) node.textContent = content; return node; };
  const finite = value => typeof value === 'number' && Number.isFinite(value);
  const clone = value => JSON.parse(JSON.stringify(value));
  const nextPaint = () => new Promise(resolve => setTimeout(resolve, 20));
  const isBusy = () => ['running', 'importing'].includes(state.phase) || state.suiteBusy || state.exportBusy;

  function setParameters(parameters) {
    controls.forEach(input => {
      const keys = input.dataset.param.split('.');
      const value = keys.reduce((object, key) => object && object[key], parameters);
      input.value = value === undefined ? '' : String(value);
    });
  }

  function fieldName(path) {
    const input = controls.find(item => item.dataset.param === path);
    return input && input.labels && input.labels[0] ? input.labels[0].textContent : path;
  }

  function parameterErrors(errors) {
    controls.forEach(input => input.removeAttribute('aria-invalid'));
    const box = $('sl-errors'); box.replaceChildren(); box.hidden = !errors.length;
    if (!errors.length) return;
    const list = create('ul');
    errors.forEach(error => {
      const input = controls.find(item => item.dataset.param === error.field);
      if (input) { input.setAttribute('aria-invalid', 'true'); const details = input.closest('details'); if (details) details.open = true; }
      list.append(create('li', '', fieldName(error.field) + ': ' + error.message));
    });
    box.append(list);
  }

  function readParameters() {
    const parameters = {acceptance: {}};
    const errors = [];
    controls.forEach(input => {
      const keys = input.dataset.param.split('.');
      const numeric = input.type === 'number' || input.dataset.number === 'true';
      const raw = input.value.trim();
      const value = numeric ? Number(raw) : raw;
      if (numeric && (!raw || !finite(value))) errors.push({field: input.dataset.param, message: t('requiredNumber')});
      if (keys.length === 2) parameters[keys[0]][keys[1]] = value;
      else parameters[keys[0]] = value;
    });
    if (errors.length) { parameterErrors(errors); throw new Error(t('validParameters')); }
    const checked = core.validate(parameters);
    parameterErrors(checked.errors || []);
    if (!checked.valid) throw new Error(t('validParameters'));
    return checked.parameters;
  }

  function invalidate(statusKey = 'pending', detailKey = 'pendingDetail') {
    state.revision++;
    state.phase = 'pending'; state.statusKey = statusKey; state.detailKey = detailKey;
    state.result = null; state.suite = null; state.verification = null; state.errorText = '';
    state.suiteBusy = false; state.exportBusy = false;
    parameterErrors([]);
    render();
  }

  function fail(error, ticket) {
    if (ticket !== state.revision) return;
    state.phase = 'error'; state.statusKey = 'error'; state.detailKey = '';
    state.result = null; state.suite = null; state.verification = null;
    state.suiteBusy = false; state.exportBusy = false;
    state.errorText = error && error.message ? error.message : String(error);
    render();
  }

  function begin(phase, detail) {
    const ticket = ++state.revision;
    state.result = null; state.suite = null; state.verification = null; state.errorText = '';
    state.phase = phase; state.statusKey = phase; state.detailKey = detail;
    state.suiteBusy = false; state.exportBusy = false;
    parameterErrors([]); render();
    return ticket;
  }

  function accept(result, suite, verification) {
    if (!result || result.evidenceClass !== 'SYNTHETIC_RESULT' || !result.arrays || !result.parameters || !methods.every(method => Array.isArray(result.arrays.outputs[method]) && result.analysis[method])) throw new Error(t('badReplay'));
    state.result = result; state.suite = suite || null; state.verification = verification || null;
    state.phase = 'ready'; state.statusKey = verification ? 'replayReady' : 'ready'; state.detailKey = verification ? 'replayReadyDetail' : 'readyDetail'; state.errorText = '';
    render();
  }

  async function run() {
    const ticket = begin('running', 'runningDetail');
    await nextPaint();
    if (ticket !== state.revision) return;
    try {
      if (!core || !evidence) throw new Error(t('unavailable'));
      const parameters = readParameters();
      const result = core.run(parameters);
      if (ticket === state.revision) accept(result, null, null);
    } catch (error) { fail(error, ticket); }
  }

  async function runSuite() {
    const ticket = ++state.revision;
    state.suite = null; state.suiteBusy = true; state.exportBusy = false;
    state.errorText = ''; render();
    await nextPaint();
    if (ticket !== state.revision) return;
    try {
      if (!core) throw new Error(t('unavailable'));
      const suite = core.runCounterexamples();
      if (ticket !== state.revision) return;
      state.suite = suite; state.suiteBusy = false; render();
    } catch (error) { fail(error, ticket); }
  }

  async function replay() {
    const ticket = begin('importing', 'importingDetail');
    try {
      const file = $('sl-import-file').files[0];
      if (!file) throw new Error(t('noFile'));
      if (!evidence) throw new Error(t('unavailable'));
      if (file.size > evidence.MAX_BYTES) throw new Error(t('oversized'));
      const content = await file.text();
      if (ticket !== state.revision) return;
      const envelope = JSON.parse(content);
      await nextPaint();
      if (ticket !== state.revision) return;
      const restored = await evidence.verifyAndReplay(envelope);
      if (ticket !== state.revision) return;
      if (!restored || !restored.verification || restored.verification.passed !== true) throw new Error(t('badReplay'));
      setParameters(restored.result.parameters);
      accept(restored.result, restored.suite, restored.verification);
    } catch (error) { fail(error, ticket); }
  }

  function download(name, mime, content) {
    const url = URL.createObjectURL(new Blob([content], {type: mime}));
    const link = create('a'); link.href = url; link.download = name; link.hidden = true;
    document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  async function exportResult(format) {
    if (!state.result || isBusy()) return;
    const ticket = state.revision;
    const result = state.result, suite = state.suite;
    state.exportBusy = true; renderStatus();
    try {
      await nextPaint();
      if (ticket !== state.revision || !state.result) return;
      if (!evidence) throw new Error(t('unavailable'));
      if (format === 'json') {
        const envelope = await evidence.create(result, suite);
        if (ticket !== state.revision || state.result !== result) return;
        download('X6_Signal_Validation_Lab_Evidence.json', 'application/json', JSON.stringify(envelope, null, 2));
      } else {
        const csv = evidence.toCSV(result);
        if (ticket !== state.revision || state.result !== result) return;
        download('X6_Signal_Validation_Lab_TimeSeries.csv', 'text/csv;charset=utf-8', csv);
      }
      if (ticket === state.revision) { state.exportBusy = false; renderStatus(); }
    } catch (error) { fail(error, ticket); }
  }

  function number(value, digits = 3) {
    if (!finite(value)) return '—';
    if (value === 0) return '0';
    if (Math.abs(value) < 0.001 || Math.abs(value) >= 1e5) return value.toExponential(2);
    return value.toLocaleString(language === 'de' ? 'de-CH' : language === 'fr' ? 'fr-CH' : 'en-GB', {maximumFractionDigits: digits});
  }

  function metricText(metric, unit = false) {
    if (!metric) return '—';
    if (metric.status === 'EXACT_MATCH') return '∞ (' + t('EXACT_MATCH') + ')';
    if (!finite(metric.value)) return '—';
    const suffix = unit ? ({'%': ' %', deg: '°', samples: ' samples', dB: ' dB', amplitude: ' a.u.'}[metric.unit] || '') : '';
    return number(metric.value) + suffix + (metric.status === 'PARTIAL' ? ' *' : '');
  }

  function metricTitle(metric) {
    return metric ? t(metric.status) + ' · ' + metric.reason : t('noCurrentRun');
  }

  function pill(status, override) { return create('span', 'status-pill status-' + status, override || t(status)); }

  function renderStatus() {
    const status = $('sl-status');
    const busy = isBusy();
    document.body.classList.toggle('busy', busy);
    let key = state.statusKey, detail = state.detailKey;
    if (state.suiteBusy) { key = 'suiteBusy'; detail = 'suiteBusyDetail'; }
    if (state.exportBusy) { key = 'exporting'; detail = 'exportingDetail'; }
    status.textContent = t(key); status.dataset.state = state.phase;
    text('sl-status-detail', state.errorText || (detail ? t(detail) : ''));
    const parameters = state.result && state.result.parameters;
    text('sl-run-meta', parameters ? 'N ' + parameters.samples + ' · ' + number(parameters.sampleRate) + ' Hz · seed ' + parameters.seed : '');
    $('sl-run').disabled = busy || !core;
    $('sl-counterexamples').disabled = busy || !core;
    $('sl-import').disabled = busy || !evidence;
    $('sl-export-json').disabled = !state.result || busy || !evidence;
    $('sl-export-csv').disabled = !state.result || busy || !evidence;
    text('sl-verification', state.verification ? t('verificationPassed') : '');
    text('sl-suite-status', state.suiteBusy ? t('suiteRunning') : state.suite ? (t(state.suite.passed ? 'suitePassed' : 'suiteFailed') + ' · ' + state.suite.cases.filter(item => item.passed).length + '/' + state.suite.cases.length + ' ' + t('cases') + ' · ' + (state.suite.passedChecks === undefined ? state.suite.cases.reduce((sum, item) => sum + item.checks.filter(check => check.passed).length, 0) : state.suite.passedChecks) + '/' + (state.suite.totalChecks === undefined ? state.suite.cases.reduce((sum, item) => sum + item.checks.length, 0) : state.suite.totalChecks) + ' ' + t('checks')) : t('suiteIdle'));
    $('sl-suite-status').className = 'suite-status' + (state.suite ? (state.suite.passed ? ' status-PASS' : ' status-FAIL') : '');
  }

  function renderTable() {
    const tbody = $('sl-comparison').querySelector('tbody'); tbody.replaceChildren();
    methods.forEach(method => {
      const analysis = state.result && state.result.analysis[method];
      const row = create('tr'); row.dataset.method = method; row.dataset.selected = String(method === state.selectedMethod);
      const name = create('td'), button = create('button', '', t(method)); button.type = 'button'; button.dataset.selectMethod = method; button.setAttribute('aria-pressed', String(method === state.selectedMethod)); button.addEventListener('click', () => selectMethod(method)); name.append(button); row.append(name);
      ['nrmse', 'gain_error_pct', 'phase_error_deg', 'delay_samples', 'coherence_mean'].forEach(key => {
        const metric = analysis && analysis.metrics[key];
        const cell = create('td', metric && metric.status !== 'DEFINED' ? 'status-' + metric.status : '', metricText(metric));
        cell.dataset.metric = key; cell.title = metricTitle(metric);
        if (metric && !finite(metric.value)) cell.setAttribute('aria-label', t(key) + ': ' + t(metric.status));
        row.append(cell);
      });
      const status = create('td'); if (analysis) status.append(pill(analysis.status)); else status.textContent = '—'; row.append(status); tbody.append(row);
    });
  }

  function renderSelected() {
    const analysis = state.result && state.result.analysis[state.selectedMethod];
    const status = $('sl-selected-status'); status.className = analysis ? 'status-' + analysis.status : ''; status.textContent = analysis ? t(analysis.status) : '—';
    [['sl-selected-nrmse', 'nrmse'], ['sl-selected-gain', 'gain_error_pct'], ['sl-selected-phase', 'phase_error_deg']].forEach(([id, key]) => {
      const metric = analysis && analysis.metrics[key]; text(id, metricText(metric, key !== 'nrmse')); $(id).title = metricTitle(metric);
    });
    const gateList = $('sl-gates'); gateList.replaceChildren();
    const metricList = $('sl-metrics-detail'); metricList.replaceChildren();
    if (!analysis) { gateList.append(create('p', 'field-help', t('noCurrentRun'))); return; }
    analysis.gates.forEach(gate => {
      const item = create('article', 'gate-item'); item.dataset.gate = gate.id;
      item.append(create('strong', '', t(gate.id)), pill(gate.status));
      const absolute = ['gain_error_pct', 'delay_samples'].includes(gate.id);
      item.append(create('span', 'gate-value', t('metricValue') + ' ' + number(gate.value) + ' · ' + t('threshold') + ' ' + (absolute ? t('absolute') + ' ' : '') + (gate.id === 'coherence_mean' ? '≥ ' : '≤ ') + number(gate.limit)));
      if (gate.status === 'UNDEFINED') item.append(create('p', '', t('noGate')));
      item.title = gate.reason;
      gateList.append(item);
    });
    metricKeys.forEach(key => {
      const metric = analysis.metrics[key]; if (!metric) return;
      const card = create('article', 'metric-detail'); card.append(create('strong', '', t(key)));
      card.append(create('span', metric.status === 'DEFINED' || metric.status === 'EXACT_MATCH' ? '' : 'status-' + metric.status, metricText(metric, true) + ' · ' + t(metric.status)));
      card.append(create('p', '', metric.reason));
      metricList.append(card);
    });
  }

  function renderSuite() {
    const parent = $('sl-suite-results'); parent.replaceChildren();
    if (!state.suite) return;
    state.suite.cases.forEach(item => {
      const card = create('article', 'case-card'); card.dataset.case = item.id; card.dataset.passed = String(item.passed);
      const heading = create('div', 'case-heading');
      heading.append(create('h3', '', t('case_' + item.id) === 'case_' + item.id ? item.description : t('case_' + item.id)), pill(item.passed ? 'PASS' : 'FAIL', t(item.passed ? 'confirmed' : 'notConfirmed')));
      card.append(heading);
      card.append(create('p', '', t('expected') + ': ' + (t('expect_' + item.id) === 'expect_' + item.id ? item.expected : t('expect_' + item.id))));
      const analysis = item.result && item.result.analysis && item.result.analysis.identity;
      if (analysis) {
        card.append(create('p', 'case-measures', ['nrmse', 'spectral_error', 'coherence_mean', 'phase_error_deg'].map(key => t(key) + ': ' + metricText(analysis.metrics[key], key === 'phase_error_deg')).join(' · ')));
      }
      const details = create('details'); details.append(create('summary', '', t('coreChecks')));
      const checks = create('ul');
      item.checks.forEach(check => checks.append(create('li', check.passed ? '' : 'status-FAIL', (check.passed ? '✓ ' : '× ') + check.id + ': ' + check.reason)));
      details.append(checks); card.append(details); parent.append(card);
    });
  }

  function renderMethodology() {
    const content = {evidenceClass: 'SYNTHETIC_RESULT', coreVersion: core ? core.VERSION : null, build: window.X6SignalLabBuild || null};
    if (state.result) { content.parameters = state.result.parameters; content.methodology = state.result.methodology; }
    if (state.verification) content.replayVerification = state.verification;
    text('sl-methodology', JSON.stringify(content, null, 2));
  }

  function tickLabel(value) {
    if (value === 0 || Math.abs(value) < 1e-14) return '0';
    if (Math.abs(value) >= 1e5 || Math.abs(value) < 0.001) return value.toExponential(1);
    return number(value, Math.abs(value) < 1 ? 3 : 2);
  }

  function lineChart(canvas, series, options) {
    const cssWidth = canvas.getBoundingClientRect().width;
    if (cssWidth < 1) return;
    const cssHeight = canvas.getBoundingClientRect().height || 235;
    const ratio = Math.min(window.devicePixelRatio || 1, 3);
    canvas.width = Math.round(cssWidth * ratio); canvas.height = Math.round(cssHeight * ratio);
    const ctx = canvas.getContext('2d'); ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    ctx.clearRect(0, 0, cssWidth, cssHeight);
    if (!series.length) return;
    const margin = {left: options.log ? 48 : 47, right: options.rightAxis ? 41 : 11, top: 25, bottom: 36};
    const width = Math.max(1, cssWidth - margin.left - margin.right), height = Math.max(1, cssHeight - margin.top - margin.bottom);
    let xMin = Infinity, xMax = -Infinity, yMin = Infinity, yMax = -Infinity;
    series.forEach(item => {
      item.x.forEach(value => { if (finite(value)) { xMin = Math.min(xMin, value); xMax = Math.max(xMax, value); } });
      if (item.right) return;
      item.y.forEach(value => {
        if (!finite(value) || (options.log && value <= 0)) return;
        const y = options.log ? Math.log10(value) : value; yMin = Math.min(yMin, y); yMax = Math.max(yMax, y);
      });
    });
    if (!finite(xMin) || !finite(xMax)) return;
    if (xMax === xMin) xMax = xMin + 1;
    if (options.yRange) { yMin = options.yRange[0]; yMax = options.yRange[1]; }
    else if (!finite(yMin) || !finite(yMax)) { yMin = 0; yMax = 1; }
    else if (options.log) { yMin = Math.floor(yMin); yMax = Math.ceil(yMax); if (yMin === yMax) { yMin--; yMax++; } }
    else {
      const spread = yMax - yMin;
      const padding = spread > 0 ? spread * 0.12 : Math.max(Math.abs(yMax) * 0.12, 0.1);
      yMin -= padding; yMax += padding;
    }
    const px = value => margin.left + (value - xMin) / (xMax - xMin) * width;
    const py = (value, right) => margin.top + height - (right ? (value + 180) / 360 : ((options.log ? Math.log10(value) : value) - yMin) / (yMax - yMin)) * height;
    ctx.font = '9px system-ui, sans-serif'; ctx.lineWidth = 1;
    const divisions = 4;
    for (let i = 0; i <= divisions; i++) {
      const y = margin.top + height * i / divisions;
      ctx.strokeStyle = '#223340'; ctx.beginPath(); ctx.moveTo(margin.left, y); ctx.lineTo(margin.left + width, y); ctx.stroke();
      const value = yMax - (yMax - yMin) * i / divisions;
      ctx.textAlign = 'right'; ctx.fillStyle = '#8fa3b5';
      ctx.fillText(options.log ? '10^' + number(value, 1) : tickLabel(value), margin.left - 7, y + 3);
      if (options.rightAxis) { ctx.textAlign = 'left'; ctx.fillStyle = '#cfad83'; ctx.fillText(String(180 - 360 * i / divisions), margin.left + width + 6, y + 3); }
    }
    const xDivisions = cssWidth < 330 ? 3 : 4;
    for (let i = 0; i <= xDivisions; i++) {
      const x = margin.left + width * i / xDivisions;
      ctx.strokeStyle = '#1a2b38'; ctx.beginPath(); ctx.moveTo(x, margin.top); ctx.lineTo(x, margin.top + height); ctx.stroke();
      ctx.textAlign = i === 0 ? 'left' : i === xDivisions ? 'right' : 'center'; ctx.fillStyle = '#8fa3b5';
      ctx.fillText(tickLabel(xMin + (xMax - xMin) * i / xDivisions), x, margin.top + height + 16);
    }
    ctx.fillStyle = '#a2b3c0'; ctx.font = '9px system-ui, sans-serif'; ctx.textAlign = 'left'; ctx.fillText(options.yLabel, margin.left, 11);
    if (options.rightAxis) { ctx.textAlign = 'right'; ctx.fillStyle = '#cfad83'; ctx.fillText('Δφ (°)', margin.left + width, 11); }
    ctx.textAlign = 'right'; ctx.fillStyle = '#a2b3c0'; ctx.fillText(options.xLabel, margin.left + width, cssHeight - 2);
    ctx.save(); ctx.beginPath(); ctx.rect(margin.left, margin.top, width, height); ctx.clip();
    series.forEach(item => {
      ctx.beginPath(); ctx.strokeStyle = item.color; ctx.lineWidth = item.width || 1.4; ctx.setLineDash(item.dash || []); ctx.globalAlpha = item.opacity === undefined ? 1 : item.opacity;
      let open = false;
      for (let i = 0; i < item.x.length; i++) {
        const value = item.y[i];
        if (!finite(item.x[i]) || !finite(value) || (options.log && value <= 0)) { open = false; continue; }
        const x = px(item.x[i]), y = py(value, item.right);
        if (open) ctx.lineTo(x, y); else { ctx.moveTo(x, y); open = true; }
      }
      ctx.stroke();
    });
    ctx.restore();
  }

  function renderCharts() {
    const result = state.result;
    const analysis = result && result.analysis[state.selectedMethod];
    $('sl-time-empty').hidden = Boolean(result);
    $('sl-psd-empty').hidden = false; $('sl-coherence-empty').hidden = false;
    text('sl-psd-empty', result ? t('noPositivePsd') : t('awaitingData'));
    text('sl-coherence-empty', result ? t('noSpectralRelation') : t('awaitingData'));
    $('sl-time-chart').setAttribute('aria-label', t('waveTitle') + ' · ' + t(state.selectedMethod));
    $('sl-psd-chart').setAttribute('aria-label', t('psdTitle') + ' · ' + t(state.selectedMethod));
    $('sl-coherence-chart').setAttribute('aria-label', t('coherenceTitle') + ' · ' + t(state.selectedMethod));
    if (!result || !analysis) {
      ['sl-time-chart', 'sl-psd-chart', 'sl-coherence-chart'].forEach(id => lineChart($(id), [], {})); return;
    }
    const a = result.arrays;
    $('sl-time-chart').setAttribute('aria-label', t('waveTitle') + ' · ' + t(state.selectedMethod) + ' · N=' + a.time.length + ' · ' + t('nrmse') + ': ' + metricText(analysis.metrics.nrmse) + ' · ' + t('gain_error_pct') + ': ' + metricText(analysis.metrics.gain_error_pct, true));
    lineChart($('sl-time-chart'), [
      {x: a.time, y: a.observed, color: '#7b90a6', width: 0.9, opacity: 0.66},
      {x: a.time, y: a.reference, color: '#73e0d0', width: 1.6, dash: [5, 3]},
      {x: a.time, y: a.outputs[state.selectedMethod], color: '#f2bf82', width: 1.45}
    ], {xLabel: t('timeAxis'), yLabel: t('amplitudeAxis')});
    const spectrum = analysis.spectrum;
    const positive = spectrum.referencePSD.some(value => finite(value) && value > 0) || spectrum.outputPSD.some(value => finite(value) && value > 0);
    $('sl-psd-chart').setAttribute('aria-label', t('psdTitle') + ' · ' + t(state.selectedMethod) + ' · ' + (positive ? t('spectral_error') + ': ' + metricText(analysis.metrics.spectral_error) : t('noPositivePsd')));
    $('sl-psd-empty').hidden = positive;
    lineChart($('sl-psd-chart'), positive ? [
      {x: spectrum.frequencies, y: spectrum.referencePSD, color: '#73e0d0', width: 1.5, dash: [4, 3]},
      {x: spectrum.frequencies, y: spectrum.outputPSD, color: '#f2bf82', width: 1.4}
    ] : [], {xLabel: t('frequencyAxis'), yLabel: t('psdAxis'), log: true});
    const defined = spectrum.coherence.some(finite) || spectrum.phaseDeg.some(finite);
    $('sl-coherence-chart').setAttribute('aria-label', t('coherenceTitle') + ' · ' + t(state.selectedMethod) + ' · ' + (defined ? t('coherence_mean') + ': ' + metricText(analysis.metrics.coherence_mean) + ' · ' + t('phase_error_deg') + ': ' + metricText(analysis.metrics.phase_error_deg, true) : t('noSpectralRelation')));
    $('sl-coherence-empty').hidden = defined;
    lineChart($('sl-coherence-chart'), defined ? [
      {x: spectrum.frequencies, y: spectrum.coherence, color: '#b4a1fb', width: 1.55},
      {x: spectrum.frequencies, y: spectrum.phaseDeg, color: '#f2bf82', width: 1.2, right: true}
    ] : [], {xLabel: t('frequencyAxis'), yLabel: 'γ²', yRange: [0, 1], rightAxis: true});
  }

  function selectMethod(method) {
    if (!methods.includes(method)) return;
    state.selectedMethod = method; $('sl-method').value = method;
    renderTable(); renderSelected(); renderCharts();
  }

  function render() {
    renderStatus(); renderTable(); renderSelected(); renderSuite(); renderMethodology(); renderCharts();
  }

  function applyLanguage() {
    document.documentElement.lang = language;
    $('sl-language').value = language;
    document.querySelectorAll('[data-i18n]').forEach(node => { node.textContent = t(node.dataset.i18n); });
    document.title = 'Signal Validation Lab · X6';
    render();
  }

  $('sl-form').addEventListener('submit', event => { event.preventDefault(); run(); });
  $('sl-form').addEventListener('input', event => { if (event.target.matches('[data-param]')) invalidate(); });
  $('sl-reset').addEventListener('click', () => { if (!core) return; setParameters(core.defaults()); invalidate('defaultsPending'); });
  $('sl-method').addEventListener('change', () => selectMethod($('sl-method').value));
  $('sl-language').addEventListener('change', () => {
    language = Object.hasOwn(words, $('sl-language').value) ? $('sl-language').value : 'de';
    try { localStorage.setItem('x6-signal-lab-language', language); } catch (_) { /* Optional preference only. */ }
    applyLanguage();
  });
  $('sl-counterexamples').addEventListener('click', runSuite);
  $('sl-import-file').addEventListener('change', () => invalidate('filePending', 'filePendingDetail'));
  $('sl-import').addEventListener('click', replay);
  $('sl-export-json').addEventListener('click', () => exportResult('json'));
  $('sl-export-csv').addEventListener('click', () => exportResult('csv'));
  let resizeQueued = false;
  const redrawOnResize = () => {
    if (resizeQueued) return; resizeQueued = true;
    requestAnimationFrame(() => { resizeQueued = false; renderCharts(); });
  };
  if (typeof ResizeObserver !== 'undefined') {
    const observer = new ResizeObserver(redrawOnResize);
    ['sl-time-chart', 'sl-psd-chart', 'sl-coherence-chart'].forEach(id => observer.observe($(id).parentElement));
  } else window.addEventListener('resize', redrawOnResize);
  window.X6SignalLabUI = Object.freeze({getState: () => clone({phase: state.phase, revision: state.revision, result: state.result, suite: state.suite, verification: state.verification, selectedMethod: state.selectedMethod})});
  if (core) setParameters(core.defaults());
  text('sl-version', core ? 'v' + core.VERSION : '');
  applyLanguage();
  if (!core || !evidence) fail(new Error(t('unavailable')), state.revision);
})();
