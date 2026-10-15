#!/usr/bin/env python3
"""Render and check the dated module register. Never execute registered commands."""
import argparse
import io
import json
import re
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path, PurePosixPath
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'MODULE_REGISTRY.json'
DOC = ROOT / 'docs/MODULE_REGISTRY.md'
TICK = chr(96)
FENCE = TICK * 3


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, stderr=subprocess.PIPE)


def url(doc, commit, path):
    return 'https://github.com/' + doc['repository'] + '/blob/' + commit + '/' + path


def render(doc):
    repo = 'https://github.com/' + doc['repository']
    main = doc['main_snapshot']
    q = lambda s: TICK + s + TICK
    rows = [
        '# X6 — zentrales Modul- und Evidenzregister', '',
        '**Geprüfter Quellenstand: ' + doc['snapshot_date'] + '.** Dieses Register ist der gemeinsame Einstieg in die veröffentlichten Module.', '',
        'Es beschreibt einen datierten Snapshot, keinen Live-Monitor. Massgeblicher main-Ausgangscommit: [' + main + '](' + repo + '/commit/' + main + '). Dokumentationsänderungen nach diesem Snapshot sind über die Git-Historie nachvollziehbar. Die Quellpins bezeichnen die verfügbare Implementierung; ältere Evidenzberichte behalten ihre eigenen Prüfrevisionen.', '',
        '[Maschinenlesbare Quelle](../MODULE_REGISTRY.json) · [Installation und Bedienung](INTEGRATION.md) · [Register-Abnahme](MODULE_REGISTRY_ACCEPTANCE.md) · [Offline-Referenzsuite](OFFLINE_REFERENCE.md)', '',
        '## Schnellstart aus main', '', FENCE + 'sh',
        'git clone --branch main https://github.com/' + doc['repository'] + '.git x6',
        'cd x6',
        'python3 x6.py setup --profile core',
        'python3 x6.py doctor --profile core',
        'python3 x6.py run spectral --output runs/first-spectral',
        'python3 x6.py verify runs/first-spectral',
        'python3 x6.py serve', FENCE, '',
        'Voraussetzungen: Git, Python 3.12, Node.js >=22; Referenzplattform Linux/POSIX x86-64. Browser für die gemeldete lokale URL. Der Spektrallauf prüft fünf rationale Referenzfälle; er qualifiziert keine Hardware. Für RAX folgt ' + q('python3 x6.py setup --profile research') + '. Server mit Strg+C beenden. Ausgabepfade müssen jeweils neu sein.', '',
        '## Status richtig lesen', '',
        '- **MAIN:** im veröffentlichten Hauptzweig verfügbar. **BRANCH_ONLY:** im main-Snapshot nicht enthalten; den unten gepinnten Stand separat auschecken.',
        '- **SOFTWARE:** ausführbarer, begrenzter Prüfweg. **CONCEPT/DOSSIER:** kein eigenständiger ausführbarer Gesamtbaustein; Unterlagen und nächste Abnahme sind benannt.',
        '- Ein erfolgreicher Lauf kann einen fachlichen FAIL, BLOCKED, NOT_READY oder INCONCLUSIVE korrekt reproduzieren. Erwartete Exitcodes stehen beim Modul.',
        '- Gespeicherte interne Prüfungen sind keine externe Begutachtung. Simulation, exakte endliche Rechnung und physische Messung bleiben unterschiedliche Evidenzklassen. Kein Registereintrag behauptet hier eine abgeschlossene physische Gerätequalifikation.', '',
        '## Agentenfenster', '',
        '**Exklusives Ende: 19. Oktober 2026, 00:00:00 Europe/Zurich** (' + q(doc['agent_window']['stop_utc']) + '), also einschliesslich Sonntag, 18. Oktober. Vier Datenjobs in zwei Workflows plus ein Mathematikagent teilen dieses Ende. Die drei Workflows und die Mathematikkonfiguration werden auf Übereinstimmung geprüft.', '',
        'NOAA-/Quellenjobs haben keine Push-/PR-Starts. Der Mathematikworkflow besitzt zusätzlich quellbezogene Push-/PR-Prüfungen, ebenfalls mit Zeitfensterprüfung. Zulassungsreserven: NOAA 15 Minuten, Quellen 25 Minuten, Mathematik 6 Minuten. Der konfigurierte Zeitraum beweist keine tatsächliche Ausführung; verzögerte/ausgelassene GitHub-Starts bleiben möglich. [Betriebsregeln und Reparaturbeleg](AGENT_WINDOW_REPAIR_2026_10_13.md).', '',
        '| Am Snapshot beobachteter Workflow | Run / geprüfter Quellencommit | Aussage |',
        '| --- | --- | --- |',
    ]
    for run in doc['observed_agent_runs']:
        rows.append('| ' + run['name'] + ' | [' + str(run['id']) + '](' + repo + '/actions/runs/' + str(run['id']) + '), ' + q(run['commit']) + ' | ' + run['conclusion'] + ': ' + run['evidence_scope'] + ' |')
    rows += ['', '## Modulübersicht', '', '| Modul | Verfügbarkeit / Art | Branch / Quellcommit |', '| --- | --- | --- |']
    for m in doc['modules']:
        s = m['source']
        rows.append('| [' + m['name'] + '](#' + m['id'] + ') | ' + s['availability'] + ' / ' + m['kind'] + ' | ' + q(s['branch']) + ' / [' + s['commit'][:12] + '](' + repo + '/commit/' + s['commit'] + ') |')
    rows += ['', '## Einzelne Module ausführen', '',
        'Alle Befehle beziehen sich auf den Quellencommit des jeweiligen Moduls. Für einen exakt gepinnten main-Lauf nach dem Klonen ' + q('git checkout --detach ' + main) + ' verwenden. Für Branch-Module folgt jeweils ein eigenes Klonrezept; danach ist der Checkout absichtlich detached. Nicht wahllos zwischen divergierenden Branches wechseln oder deren Versionsinventare mischen.', '',
        'Archivmodule werden in neue Ordner unter /tmp entpackt. Eine erneute Ausführung benötigt einen neuen Zielnamen. Paketinterne Befehle starten aus dem angegebenen Wurzelordner. Installation externer Abhängigkeiten benötigt Netzwerk oder vorbereitete Wheels; der eigentliche Offline-Replay startet keinen Wolfram-Dienst.', '']
    for m in doc['modules']:
        s, e = m['source'], m['entry']
        rows += ['<a id="' + m['id'] + '"></a>', '### ' + m['name'], '',
                 '**Stand:** ' + s['availability'] + ' / ' + m['kind'] + '; Branch ' + q(s['branch']) + '; Commit ' + q(s['commit']) + '.', '',
                 '**Anleitung:** [' + ('aktuelle main-Dokumentation' if s['availability']=='MAIN' else 'gepinntes Quelldokument') + '](' + url(doc,'main' if s['availability']=='MAIN' else s['commit'],s['path']) + '). **Voraussetzungen:** ' + m['prerequisites'], '',
                 '**Geprüfte Aussage:** ' + m['claim'], '']
        if s['availability'] == 'BRANCH_ONLY':
            rows += [FENCE + 'sh', 'git clone --branch ' + s['branch'] + ' ' + repo + '.git x6-' + m['id'], 'cd x6-' + m['id'], 'git checkout --detach ' + s['commit'], FENCE, '']
        if e['commands']:
            rows += [FENCE + 'sh']
            if e['archive']:
                a=e['archive']; dest='/tmp/x6-register-'+m['id']
                rows += ['python3 -m zipfile -e ' + a['path'] + ' ' + dest, 'cd ' + dest + '/' + a['root']]
            elif e['cwd'] != '.':
                rows += ['cd '+e['cwd']]
            rows += e['commands'] + [FENCE, '']
        rows += ['**Erwartung:** ' + e['expected'], '', '**Vorhandene Evidenz:**', '']
        for ev in m['evidence']:
            rows.append('- [' + ev['path'] + '](' + url(doc,s['commit'],ev['path']) + '): ' + ev['summary'])
        rows += ['', '**Nächste Abnahme:** ' + m['next_acceptance'], '']
    rows += ['## Branch-Inventar und Pflege', '',
        'Die drei aufeinander aufbauenden Branches Fingerprint → Fabric → Neutral Discovery enthalten auch frühere Module. Zum Snapshot sind die registrierten n=6-, V1-, Fingerprint- und Fabric-Dateien in den jeweiligen späteren Zweigen bytegleich. Die obigen eigenen Modulzweige bleiben die minimalen nachvollziehbaren Einstiege. NQK und Photonic Link bleiben eigenständig.', '',
        'Ein historischer Branch kann ungemergte Commits haben, obwohl sein Modul bereits via Squash/Cherry-pick in main angekommen ist. Daher sind Commit-Vorsprünge keine Modulreife- oder Integrationsnachweise. Alte Feature-/Publikationsbranches unten sind keine alternativen Empfehlungen zu den main-Einträgen.', '',
        '| Beobachteter Branch | Tip-Commit | Commits nur dort / nur main | Rolle |', '| --- | --- | --- |']
    for b in doc['branches']:
        rows.append('| ' + q(b['name']) + ' | [' + b['commit'][:12] + '](' + repo + '/commit/' + b['commit'] + ') | ' + str(b['ahead_of_main']) + ' / ' + str(b['behind_main']) + ' | ' + (', '.join(b['registered_modules']) or 'Historischer Entwicklungs-/Publikationszweig') + ' |')
    rows += ['', 'Bei einer Modulfreigabe zuerst MODULE_REGISTRY.json aktualisieren: Quellencommit, Einstieg, erwartete Ausgabe, Evidenzrevision und nächste Abnahme. Danach rendern und prüfen:', '', FENCE + 'sh', 'python3 tools/module_registry.py --write', 'python3 tools/module_registry.py --check --git-objects', 'python3 tests/python/verify_manifest.py', FENCE, '',
        'Die Prüfung vergleicht JSON und Markdown, vorhandene Hauptzweigpfade, optional alle gepinnten Git-Objekte samt Archiv-Einstiegen sowie UTC/Zürich-Frist und Workflows. Ein Checkout mit vollständiger Git-Historie wird für --git-objects benötigt; bei fehlenden Forschungsobjekten zuerst die im Register genannten Branches fetch-en. Sie führt keine Forschungskommandos, Geräteaktionen oder Agentenläufe aus. Neue wissenschaftliche Befunde benötigen eigene versionierte Evidenz; redaktionelle Registerpflege darf historische Archive und Prüfberichte nicht umschreiben.', '']
    return '\n'.join(rows)


def check(doc, objects=False):
    errors=[]
    def require(ok, msg):
        if not ok: errors.append(msg)
    require(doc.get('schema')=='x6.module-register/1','wrong schema')
    ids=[m['id'] for m in doc['modules']]
    require(len(ids)==len(set(ids)), 'duplicate module ids')
    branch_map={b['name']:b for b in doc['branches']}
    require(len(branch_map)==len(doc['branches']), 'duplicate branches')
    for m in doc['modules']:
        s,e=m['source'],m['entry']; label=m['id']
        require(bool(re.fullmatch('[a-z0-9-]+',label)),label+': invalid anchor')
        require(bool(re.fullmatch('[a-f0-9]{40}',s['commit'])),label+': invalid commit')
        require(branch_map.get(s['branch'],{}).get('commit')==s['commit'],label+': branch snapshot mismatch')
        require(bool(m['claim'] and m['next_acceptance'] and m['evidence'] and e['expected'] and m['prerequisites']),label+': missing required explanation')
        require(bool(e['commands']) == (m['kind']=='SOFTWARE'),label+': executable classification mismatch')
        require(s['availability']==('MAIN' if s['branch']=='main' else 'BRANCH_ONLY'),label+': availability mismatch')
        paths=[s['path']]+[ev['path'] for ev in m['evidence']]
        if e['archive']: paths.append(e['archive']['path'])
        else: paths+=e['paths']
        for p in paths:
            require(not PurePosixPath(p).is_absolute() and '..' not in PurePosixPath(p).parts,label+': unsafe path '+p)
            if s['availability']=='MAIN': require((ROOT/p).is_file(),label+': current path missing '+p)
            if objects:
                try: git('cat-file','-e',s['commit']+':'+p)
                except subprocess.CalledProcessError: errors.append(label+': pinned path/object missing '+p)
        if e['archive']:
            a=e['archive']
            try:
                raw=git('show',s['commit']+':'+a['path']) if objects else (ROOT/a['path']).read_bytes()
                with zipfile.ZipFile(io.BytesIO(raw)) as z:
                    for p in e['paths']: require(a['root']+'/'+p in z.namelist(),label+': archive entry missing '+p)
            except (OSError,zipfile.BadZipFile,subprocess.CalledProcessError) as exc: errors.append(label+': unreadable archive '+str(exc))
    w=doc['agent_window']
    stop=datetime.fromisoformat(w['stop_utc'].replace('Z','+00:00'))
    require(stop.astimezone(ZoneInfo(w['timezone'])).isoformat()==w['stop_local'],'UTC/local cutoff mismatch')
    require(w['exclusive'] is True,'cutoff must be exclusive')
    config=json.loads((ROOT/w['source']).read_text())
    require(config['stop_utc']==w['stop_utc'],'math configuration cutoff mismatch')
    for name in ['x6-data-agent.yml','x6-source-agents.yml']:
        text=(ROOT/'.github/workflows'/name).read_text()
        require(stop.isoformat() in text,name+': cutoff mismatch')
    math=(ROOT/'.github/workflows/x6-math-agent.yml').read_text()
    require('agent/run_math_agent.py --guard' in math,'math workflow guard missing')
    for p in ['README.md','docs/LORENTZ_RESEARCH.md','docs/INTEGRATION.md','index.html']:
        text=(ROOT/p).read_text()
        require('MODULE_REGISTRY.md' in text,p+': register link missing')
        require('00:26:52' not in text and '22:26:52' not in text and '11–13 October' not in text,p+': obsolete current cutoff')
    require(w['stop_utc'] in (ROOT/'README.md').read_text(),'README UTC cutoff missing')
    require(w['stop_local'] in (ROOT/'index.html').read_text(),'portal local cutoff missing')
    require(DOC.exists() and DOC.read_text()==render(doc),'generated Markdown is stale; run --write')
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--git-objects',action='store_true')
    args=parser.parse_args()
    doc=json.loads(DATA.read_text())
    if args.write: DOC.write_text(render(doc))
    errors=check(doc,args.git_objects)
    print(json.dumps(dict(status='FAIL' if errors else 'PASS',modules=len(doc['modules']),branches=len(doc['branches']),pinned_git_objects_checked=args.git_objects,errors=errors),ensure_ascii=False,indent=2))
    raise SystemExit(bool(errors))


if __name__=='__main__': main()
