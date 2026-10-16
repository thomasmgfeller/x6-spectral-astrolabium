#!/usr/bin/env python3
"""Build static research navigation from the authoritative register; stdlib only.

No research commands are executed. All registered claims and evidence summaries
are rendered verbatim and escaped. --check is a read-only freshness gate.
"""
import argparse
import hashlib
import html
import json
import posixpath
import shlex
from pathlib import Path
from urllib.parse import quote
from build_wiki import outputs as wiki_outputs

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://thomasmgfeller.github.io/x6-spectral-astrolabium/'
REPO = 'https://github.com/thomasmgfeller/x6-spectral-astrolabium'
E = html.escape
BROWSER_APPS = {
    'astrolabium': ('app/index.html', 'Astrolabium öffnen →'),
    'signal-lab': ('app/signal-lab.html', 'Signal Lab öffnen →'),
    'rax-cqg-benchmark': ('app/rax-cqg-lab.html', 'Causal-Set-Labor öffnen →'),
}
SETUP_IMAGE = 'experiments/photonic-two-qubit/figures/AI_CONCEPT_NOT_PHOTO.png'
CQG_PATH = 'docs/research/rax/cqg-v0.1/'
CQG_DOCUMENT = 'RAX_CQG_Forschungsarchitektur_v0_1'
CQG_BENCHMARK_PATH = 'docs/research/rax/cqg-benchmark-v0.2.0/'


def rel(source, target):
    return posixpath.relpath(target, posixpath.dirname(source) or '.')


def link(url, label, **attrs):
    extras = ''.join(' ' + k + '="' + E(v, quote=True) + '"' for k, v in attrs.items())
    return '<a href="' + E(url, quote=True) + '"' + extras + '>' + E(label) + '</a>'


def source_url(commit, path):
    return REPO + '/blob/' + quote(commit, safe='') + '/' + quote(path, safe='/')


def canonical(path):
    return BASE + (path[:-10] if path.endswith('index.html') else path)


def p(text):
    return '<p>' + E(text) + '</p>'


def page(path, title, description, body, lang='en', translations=None, script=False, software=False):
    de = lang == 'de'
    style_version = ('?v=' + hashlib.sha256((ROOT / 'assets/hub.css').read_bytes()).hexdigest()[:12]
                     if path in {'index.html', 'de/index.html'} else '')
    home = 'de/index.html' if de else 'index.html'
    guide = 'de/guide.html' if de else 'guide/index.html'
    md = str(Path(path).with_suffix('.md'))
    nav = [(home, 'Übersicht' if de else 'Overview'), (guide, 'Einstieg' if de else 'Start here'),
           ('modules/index.html', 'Module' if de else 'Modules'), ('wiki/de/index.html' if de else 'wiki/en/index.html', 'Wiki')]
    other = 'en' if de else 'de'
    language_target = (translations or {}).get(other, 'index.html' if de else 'de/index.html')
    language = link(rel(path, language_target), 'English' if de else 'Deutsch', hreflang=other)
    alternates = ''.join('<link rel="alternate" hreflang="' + code + '" href="' + canonical(dest) + '">\n'
                         for code, dest in (translations or {}).items())
    structured = {'@context': 'https://schema.org', '@type': 'WebPage', 'name': title,
                  'description': description, 'url': canonical(path), 'inLanguage': lang,
                  'isPartOf': {'@type': 'WebSite', 'name': 'X6 Spectral Astrolabium', 'url': BASE}}
    if software:
        structured['about'] = {'@type': 'SoftwareSourceCode', 'name': 'X6 Spectral Astrolabium',
                               'codeRepository': REPO, 'description': description,
                               'author': {'@type': 'Person', 'name': 'Thomas Gfeller'}}
    structured_json = json.dumps(structured, ensure_ascii=False).replace('<', '\\u003c')
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} | X6 Research Hub</title>
<meta name="description" content="{E(description, quote=True)}">
<link rel="canonical" href="{canonical(path)}">
{alternates}<link rel="alternate" type="text/markdown" href="{rel(path, md)}">
<link rel="describedby" href="{rel(path, 'llms.txt')}" type="text/plain">
<link rel="sitemap" href="{rel(path, 'sitemap.xml')}" type="application/xml">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(title, quote=True)}">
<meta property="og:description" content="{E(description, quote=True)}">
<meta property="og:url" content="{canonical(path)}">
<meta property="og:site_name" content="X6 Spectral Astrolabium">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{rel(path, 'assets/hub.css')}{style_version}">
{('<link rel="stylesheet" href="' + rel(path, 'assets/wiki.css') + '">') if path.startswith('wiki/') else ''}
<script type="application/ld+json">{structured_json}</script>
{('<script src="' + rel(path, 'assets/hub.js') + '" defer></script>') if script else ''}
</head>
<body>
<a class="skip" href="#main">{'Zum Inhalt' if de else 'Skip to content'}</a>
<header><a class="brand" href="{rel(path, home)}">X6 <span>Spectral Astrolabium</span></a>
<nav aria-label="{'Hauptnavigation' if de else 'Main navigation'}">{''.join(link(rel(path, dest), label) for dest, label in nav)}{language}{link(REPO, 'GitHub')}</nav></header>
<main id="main">{body}</main>
<footer><p>Thomas Gfeller · {'Offene Forschung' if de else 'Open research'} · {link(rel(path, 'CITATION.cff'), 'CITATION.cff')} · {link(rel(path, md), 'Markdown')} · {link(rel(path, 'llms.txt'), 'llms.txt')}</p>
<p>{'Eigene Beiträge: Apache-2.0. Drittinhalte und Daten behalten ihre eigenen Bedingungen.' if de else 'Original contributions: Apache-2.0. Third-party works and datasets retain their own terms.'} {link(REPO + '/blob/main/LICENSE_SCOPE.md', 'Lizenzumfang' if de else 'License scope')}.</p>
<p>{'Forschungssoftware und endliche Referenzrechnungen. Keine abgeschlossene physische Gerätequalifikation oder unabhängige externe Begutachtung.' if de else 'Research software and finite reference calculations. No completed physical device qualification or independent external review.'}</p></footer>
</body></html>
'''


def home(path, data, content, lang):
    t = content[lang]
    guide = 'de/guide.html' if lang == 'de' else 'guide/index.html'
    visual, feature = t['setup_visual'], t['cqg_feature']
    body = '<section class="hero hero-visual"><div class="hero-copy"><p class="eyebrow">OPEN RESEARCH · PUBLIC PREVIEW</p><h1>' + E(t['headline']) + '</h1>' + p(t['lead'])
    body += '<div class="actions">' + link(rel(path, 'app/index.html'), t['launch_astrolabium'], **{'class': 'button'}) + link(rel(path, 'app/signal-lab.html'), t['launch'], **{'class': 'button secondary'}) + link(rel(path, 'modules/index.html'), t['browse'], **{'class': 'button secondary'}) + link(rel(path, 'wiki/' + lang + '/index.html'), 'X6 verständlich erklärt →' if lang == 'de' else 'X6 explained simply →', **{'class': 'button secondary'}) + '</div></div>'
    body += '<figure class="setup-visual"><a href="' + rel(path, SETUP_IMAGE) + '" aria-label="' + E(visual['expand'], quote=True) + '"><img src="' + rel(path, SETUP_IMAGE) + '" width="1536" height="1024" fetchpriority="high" alt="' + E(visual['alt'], quote=True) + '"></a><figcaption><span class="eyebrow">' + E(visual['label']) + '</span><strong>' + E(visual['title']) + '</strong>' + p(visual['caption']) + link(REPO + '/blob/main/experiments/photonic-two-qubit/README.md', visual['details']) + '</figcaption></figure></section>'
    downloads = [(rel(path, 'app/rax-cqg-lab.html'), feature['benchmark']),
                 (rel(path, CQG_BENCHMARK_PATH + 'RAX_CQG_Benchmark_v0_2_0.zip'), feature['package']),
                 (rel(path, 'modules/rax-cqg-benchmark.html'), feature['scope']),
                 (rel(path, CQG_PATH + CQG_DOCUMENT + '.pdf'), feature['pdf']),
                 (REPO + '/blob/main/' + CQG_PATH + 'ARCHITECTURE.md', feature['read']),
                 (rel(path, CQG_PATH + CQG_DOCUMENT + '.docx'), feature['word'])]
    body += '<section class="research-feature" id="rax-cqg" aria-labelledby="cqg-title"><div><p class="eyebrow">' + E(feature['label']) + '</p><h2 id="cqg-title">RAX-CQG</h2><p class="feature-intro">' + E(feature['text']) + '</p><p class="feature-status">' + E(feature['status']) + '</p></div><div class="feature-links">'
    body += ''.join(link(url, label, **{'class': 'button' if i == 0 else 'feature-link'}) for i, (url, label) in enumerate(downloads)) + '</div></section>'
    body += '<section aria-labelledby="tools"><h2 id="tools">' + E(t['tools_title']) + '</h2>' + p(t['tools_intro']) + '<div class="tool-grid">'
    for item in t['tools']:
        body += '<article class="card tool-card"><p class="eyebrow">' + E(item['kind']) + '</p><h3>' + E(item['title']) + '</h3>' + p(item['text']) + link(rel(path, 'modules/' + item['module'] + '.html'), item['button'], **{'class': 'button secondary'}) + '</article>'
    body += '</div></section>'
    body += '<section aria-labelledby="paths"><h2 id="paths">' + E(t['paths_title']) + '</h2><div class="path-grid">'
    for i, card in enumerate(t['paths']):
        body += '<article class="card"><p class="number">0' + str(i + 1) + '</p><h3>' + E(card['title']) + '</h3>' + p(card['text']) + link(rel(path, guide) + '#' + card['id'], card['link']) + '</article>'
    body += '</div></section><section class="split"><div><p class="eyebrow">' + E(t['priority_label']) + '</p><h2>' + E(t['priority_title']) + '</h2>' + p(t['priority_text'])
    body += link(rel(path, 'modules/lorentz-n7-complete.html'), t['priority_link'], **{'class': 'button secondary'}) + '</div><aside class="note"><h2>' + E(t['limits_title']) + '</h2>' + p(t['limits']) + '</aside></section>'
    body += '<section aria-labelledby="topics"><h2 id="topics">' + E(t['topics_title']) + '</h2><ul class="topic-list">'
    for item in t['topics']:
        body += '<li>' + link(rel(path, 'modules/' + item['module'] + '.html'), item['title'], **{'class': 'button secondary'}) + '<span>' + E(item['text']) + '</span></li>'
    body += '</ul></section><section class="note"><h2>' + E(t['status_title']) + '</h2>'
    body += p(t['snapshot'].format(count=len(data['modules']), date=data['snapshot_date']))
    body += '<p>' + link(rel(path, 'docs/MODULE_REGISTRY.md'), t['register']) + ' · ' + link(rel(path, 'MODULE_REGISTRY.json'), 'JSON') + '</p>'
    body += p(t['window']) + '<p><time datetime="' + data['agent_window']['stop_local'] + '">19 October 2026, 00:00 Europe/Zurich</time> · <code>' + data['agent_window']['stop_utc'] + '</code></p></section>'
    md = '# ' + t['headline'] + '\n\n' + t['lead'] + '\n\n'
    md += '[' + ('Wiki: X6 verständlich erklärt' if lang == 'de' else 'Wiki: X6 explained simply') + '](' + canonical('wiki/' + lang + '/index.html') + ')\n\n'
    for target, label in [('app/index.html', t['launch_astrolabium']), ('app/signal-lab.html', t['launch']), ('modules/index.html', t['browse'])]:
        md += '- [' + label + '](' + canonical(target) + ')\n'
    md += '\n## ' + visual['title'] + '\n\n![' + visual['alt'] + '](' + BASE + SETUP_IMAGE + ')\n\n' + visual['caption'] + '\n\n[' + visual['details'] + '](' + REPO + '/blob/main/experiments/photonic-two-qubit/README.md)\n'
    md += '\n## RAX-CQG · ' + feature['label'] + '\n\n' + feature['text'] + '\n\n' + feature['status'] + '\n\n'
    for target, label in [(BASE + 'app/rax-cqg-lab.html', feature['benchmark']), (BASE + CQG_BENCHMARK_PATH + 'RAX_CQG_Benchmark_v0_2_0.zip', feature['package']), (BASE + 'modules/rax-cqg-benchmark.html', feature['scope']), (BASE + CQG_PATH + CQG_DOCUMENT + '.pdf', feature['pdf']), (REPO + '/blob/main/' + CQG_PATH + 'ARCHITECTURE.md', feature['read']), (BASE + CQG_PATH + CQG_DOCUMENT + '.docx', feature['word'])]:
        md += '- [' + label + '](' + target + ')\n'
    md += '\n## ' + t['tools_title'] + '\n\n' + t['tools_intro'] + '\n\n'
    for item in t['tools']:
        md += '### ' + item['title'] + '\n\n' + item['kind'] + '. ' + item['text'] + '\n\n[' + item['button'] + '](' + canonical('modules/' + item['module'] + '.html') + ')\n\n'
    for card in t['paths']:
        md += '## ' + card['title'] + '\n\n' + card['text'] + '\n\n[' + card['link'] + '](' + canonical(guide) + '#' + card['id'] + ')\n\n'
    md += '## ' + t['priority_title'] + '\n\n' + t['priority_text'] + '\n\n## ' + t['limits_title'] + '\n\n' + t['limits'] + '\n\n'
    for item in t['topics']:
        md += '- [' + item['title'] + '](' + canonical('modules/' + item['module'] + '.html') + '): ' + item['text'] + '\n'
    md += '\n' + t['snapshot'].format(count=len(data['modules']), date=data['snapshot_date']) + '\n\n' + t['window'] + '\n' + data['agent_window']['stop_local'] + '\n'
    return page(path, t['title'], t['description'], body, lang, {'en': 'index.html', 'de': 'de/index.html', 'x-default': 'index.html'}, software=True), md


def guide(path, content, lang):
    t = content[lang]
    body = '<section class="hero compact"><p class="eyebrow">' + E(t['guide_label']) + '</p><h1>' + E(t['guide_title']) + '</h1>' + p(t['guide_lead']) + '</section>'
    md = '# ' + t['guide_title'] + '\n\n' + t['guide_lead'] + '\n\n'
    for section in t['guide']:
        body += '<section class="prose" id="' + section['id'] + '"><h2>' + E(section['title']) + '</h2>'
        md += '## ' + section['title'] + '\n\n'
        for text in section['paragraphs']:
            body += p(text)
            md += text + '\n\n'
        if section.get('code'):
            body += '<pre><code>' + E(section['code']) + '</code></pre>'
            md += '```sh\n' + section['code'] + '\n```\n\n'
        body += '<ul>'
        for item in section['links']:
            url = item['url'] if item['url'].startswith('https://') else rel(path, item['url'])
            body += '<li>' + link(url, item['label']) + '</li>'
            md += '- [' + item['label'] + '](' + (item['url'] if item['url'].startswith('https://') else BASE + item['url']) + ')\n'
        body += '</ul></section>'
        md += '\n'
    return page(path, t['guide_title'], t['guide_lead'], body, lang, {'en': 'guide/index.html', 'de': 'de/guide.html'}), md


def module_page(m, data):
    s, entry = m['source'], m['entry']
    path = 'modules/' + m['id'] + '.html'
    body = '<p class="eyebrow">MODULREGISTER · ' + E(data['snapshot_date']) + '</p><h1>' + E(m['name']) + '</h1>'
    body += '<p><span class="tag">' + E(s['availability']) + '</span> <span class="tag">' + E(m['kind']) + '</span></p>'
    if m['id'] in BROWSER_APPS:
        target, label = BROWSER_APPS[m['id']]
        body += '<div class="actions">' + link(rel(path, target), label, **{'class': 'button'}) + '</div>'
    body += p('Datierter Registerstand, kein Live-Prüfsiegel. SOFTWARE bezeichnet den ausführbaren Prüfweg, nicht eine validierte physische Anwendung. Die Originalangaben bleiben in Deutsch.')
    body += '<section class="prose"><h2>1. Was wird untersucht?</h2>' + p(m['name'])
    body += '<p>' + link(source_url(s['commit'], s['path']), 'Gepinnte Originaldokumentation') + ' · ' + link(REPO + '/commit/' + s['commit'], 'Quellencommit ' + s['commit'][:12]) + '</p>'
    body += '<p>Branch: <code>' + E(s['branch']) + '</code>. <code>' + E(s['commit']) + '</code></p></section>'
    body += '<section class="prose"><h2>2. Was ist dokumentiert?</h2>' + p(m['claim']) + '<ul>'
    md = '# ' + m['name'] + '\n\nRegisterstand: ' + data['snapshot_date'] + '. ' + s['availability'] + ' / ' + m['kind'] + '. Kein Live-Prüfsiegel.\n\n'
    if m['id'] in BROWSER_APPS:
        target, label = BROWSER_APPS[m['id']]
        md += '[' + label + '](' + canonical(target) + ')\n\n'
    md += '## Quelle\n\nBranch: ' + s['branch'] + '\n\nCommit: ' + s['commit'] + '\n\n[Originaldokumentation](' + source_url(s['commit'], s['path']) + ')\n\n## Dokumentierte Aussage\n\n' + m['claim'] + '\n\n'
    for ev in m['evidence']:
        url = source_url(s['commit'], ev['path'])
        body += '<li>' + link(url, ev['path']) + p(ev['summary']) + '</li>'
        md += '- [' + ev['path'] + '](' + url + '): ' + ev['summary'] + '\n'
    body += '</ul>' + p('Evidenzberichte behalten ihre eigenen Prüfrevisionen. Ein Quellenpin belegt weder einen neuen Lauf noch unabhängige externe Begutachtung.') + '</section>'
    body += '<section class="prose"><h2>3. Wie lässt sich das prüfen?</h2>' + p(m['prerequisites'])
    md += '\n## Reproduzieren\n\n' + m['prerequisites'] + '\n\n'
    if entry['commands']:
        dirname = 'x6-' + m['id']
        commands = ['git clone --branch ' + shlex.quote(s['branch']) + ' ' + REPO + '.git ' + dirname,
                    'cd ' + dirname, 'git checkout --detach ' + s['commit']]
        if entry['archive']:
            a = entry['archive']
            dest = '/tmp/x6-hub-' + m['id']
            commands += ['python3 -m zipfile -e ' + shlex.quote(a['path']) + ' ' + dest,
                         'cd ' + shlex.quote(dest + '/' + a['root'])]
        elif entry['cwd'] != '.':
            commands += ['cd ' + shlex.quote(entry['cwd'])]
        commands += entry['commands']
        code = '\n'.join(commands)
        body += p('In einem neuen Ordner ausführen; vorhandene Ausgabeordner nicht überschreiben. Voraussetzungen und paketbezogene Hinweise in der Originaldokumentation beachten.') + '<pre><code>' + E(code) + '</code></pre>'
        md += 'Neue Arbeits- und Ausgabeordner verwenden; Voraussetzungen aus der Originaldokumentation beachten.\n\n```sh\n' + code + '\n```\n\n'
    body += '<h3>Erwartete Ausgabe</h3>' + p(entry['expected']) + '</section><section class="note"><h2>4. Was bleibt offen?</h2>' + p(m['next_acceptance']) + '</section>'
    md += 'Erwartete Ausgabe: ' + entry['expected'] + '\n\n## Offene Prüfung\n\n' + m['next_acceptance'] + '\n\nEvidenzberichte behalten ihre eigenen Prüfrevisionen. Keine neue Ausführung, externe Begutachtung oder physische Qualifikation durch diese Darstellung.\n'
    return page(path, m['name'], m['claim'][:240], body, 'de'), md


def catalogue(data):
    path = 'modules/index.html'
    body = '<p class="eyebrow">RESEARCH INDEX · DE / EN</p><h1>Module und Evidenz</h1>'
    body += p(f"{len(data['modules'])} Module · Registerstand {data['snapshot_date']}. Originalangaben in Deutsch; English introductions are available in the start guide.")
    body += p('MAIN / BRANCH_ONLY beschreiben den Quellenort. SOFTWARE / CONCEPT / DOSSIER beschreiben den dokumentierten Prüfweg. Keine dieser Angaben ist ein Qualitäts- oder Hardware-Prüfsiegel.')
    body += '<p>' + link('../guide/index.html', 'English guide to evidence and reproduction') + ' · ' + link('../MODULE_REGISTRY.json', 'Authoritative JSON register') + '</p>'
    body += '<form class="filters" id="filters" hidden role="search"><div><label for="search">Module durchsuchen / Search modules</label><input id="search" type="search" placeholder="Lorentz, Signal, RAX, Sagnac …"></div><div><label for="kind">Art / Kind</label><select id="kind"><option value="">Alle / All</option><option>SOFTWARE</option><option>CONCEPT</option><option>DOSSIER</option></select></div><div><label for="availability">Quelle / Source</label><select id="availability"><option value="">Alle / All</option><option>MAIN</option><option>BRANCH_ONLY</option></select></div><button type="reset">Zurücksetzen / Reset</button></form>'
    body += '<p id="count" role="status" aria-live="polite">' + str(len(data['modules'])) + ' Module</p><p id="empty" hidden>Keine Treffer / No matches. Filter ändern oder zurücksetzen.</p><div class="module-list">'
    md = '# Module und Evidenz\n\nRegisterstand: ' + data['snapshot_date'] + '. Kein Live-Prüfsiegel. Originalangaben in Deutsch.\n\n'
    for m in data['modules']:
        body += '<article class="module" data-kind="' + E(m['kind']) + '" data-availability="' + E(m['source']['availability']) + '"><div><span class="tag">' + E(m['source']['availability']) + '</span> <span class="tag">' + E(m['kind']) + '</span></div><h2>' + link(m['id'] + '.html', m['name']) + '</h2>' + p(m['claim'])
        if m['id'] in BROWSER_APPS:
            target, label = BROWSER_APPS[m['id']]
            body += link(rel(path, target), label, **{'class': 'button secondary'})
        body += '</article>'
        md += '- [' + m['name'] + '](' + BASE + 'modules/' + m['id'] + '.md): ' + m['source']['availability'] + ' / ' + m['kind'] + '. ' + m['claim'] + '\n'
        if m['id'] in BROWSER_APPS:
            target, label = BROWSER_APPS[m['id']]
            md += '  [' + label + '](' + canonical(target) + ')\n'
    body += '</div>'
    return page(path, 'Module und Evidenz', 'Durchsuchbarer Forschungsindex mit Quellenpins, Evidenz, Reproduktion und offenen Abnahmen.', body, 'de', script=True), md


def outputs():
    data = json.loads((ROOT / 'MODULE_REGISTRY.json').read_text())
    content = json.loads((ROOT / 'docs/hub/content.json').read_text())
    out = {}
    def add(path, pair):
        out[path], out[str(Path(path).with_suffix('.md'))] = pair[0], pair[1].rstrip() + "\n"
    add('index.html', home('index.html', data, content, 'en'))
    add('de/index.html', home('de/index.html', data, content, 'de'))
    add('guide/index.html', guide('guide/index.html', content, 'en'))
    add('de/guide.html', guide('de/guide.html', content, 'de'))
    add('modules/index.html', catalogue(data))
    for m in data['modules']:
        add('modules/' + m['id'] + '.html', module_page(m, data))
    for path, pair in wiki_outputs(page, link, rel, canonical).items():
        add(path, pair)
    out['sitemap.xml'] = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('  <url><loc>' + canonical(path) + '</loc></url>\n' for path in sorted(out) if path.endswith('.html')) + '</urlset>\n'
    digest = hashlib.sha256((ROOT / 'MODULE_REGISTRY.json').read_bytes()).hexdigest()
    index = {'schema': 'x6.research-hub-index/1', 'registry_snapshot_date': data['snapshot_date'],
             'registry_url': BASE + 'MODULE_REGISTRY.json', 'registry_sha256': digest,
             'scope': 'Navigation only. Source availability and executable kind are not evidence of physical validity.',
             'modules': [{'id': m['id'], 'name': m['name'], 'url': BASE + 'modules/' + m['id'] + '.html',
                          'markdown_url': BASE + 'modules/' + m['id'] + '.md', 'kind': m['kind'],
                          'source': m['source']} for m in data['modules']]}
    out['hub-index.json'] = json.dumps(index, ensure_ascii=False, indent=2) + '\n'
    out['llms.txt'] = '''# X6 Spectral Astrolabium

> Open research software for signal validation, finite spectral graph references and Lorentzian causal-order research. Maintained by Thomas Gfeller. Public research preview.

The module register is a dated source of truth, not a live qualification badge.
MAIN/BRANCH_ONLY identify source locations; SOFTWARE/CONCEPT/DOSSIER identify
entry-point kinds. Exact finite calculations, synthetic simulations, archived
laboratory data and new physical measurements have different evidence scopes.
Internal counterchecks are not independent person-level review. No validated
quantum processor, general spacetime theory or industrial filter superiority is claimed.
Use the specific source commit and the evidence report's own revision when citing.
Original contributions use Apache-2.0; third-party works and data retain their
separate terms, including CC BY-NC 4.0 for the included Paderborn data.
This optional navigation file neither grants access nor guarantees indexing,
ranking, inclusion in AI responses or permission to reuse third-party material.

## Start

''' + f'''- [English overview]({BASE}index.md)
- [Deutscher Einstieg]({BASE}de/index.md)
- [English reproduction and evidence guide]({BASE}guide/index.md)
- [Deutsche Anleitung]({BASE}de/guide.md)
- [Wiki auf Deutsch]({BASE}wiki/de/index.md)
- [English wiki]({BASE}wiki/en/index.md)
- [Module summaries and links]({BASE}modules/index.md)
- [Authoritative module register]({BASE}MODULE_REGISTRY.json)
- [Derived navigation index]({BASE}hub-index.json)
- [Citation metadata]({BASE}CITATION.cff)
- [License scope]({BASE}LICENSE_SCOPE.md)

## Modules

''' + ''.join('- [' + m['name'] + '](' + BASE + 'modules/' + m['id'] + '.md): ' + m['source']['availability'] + ' / ' + m['kind'] + '\n' for m in data['modules'])
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', action='store_true')
    group.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = outputs()
    stale = []
    for path, value in result.items():
        target = ROOT / path
        if args.write:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(value, encoding='utf-8')
        elif not target.is_file() or target.read_text(encoding='utf-8') != value:
            stale.append(path)
    for folder in ['modules', 'guide', 'de']:
        for target in (ROOT / folder).glob('*'):
            path = target.relative_to(ROOT).as_posix()
            if target.suffix in {'.md', '.html'} and path not in result:
                stale.append(path + ' (obsolete generated page; review before removal)')
    if stale:
        raise SystemExit('FAIL stale hub outputs: ' + ', '.join(stale))
    print(json.dumps({'status': 'PASS', 'generated_files': len(result), 'mode': 'write' if args.write else 'check'}))


if __name__ == '__main__':
    main()
