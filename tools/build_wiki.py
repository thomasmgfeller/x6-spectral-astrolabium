"""Render paired introductory articles; no research code is executed."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = html.escape


def outputs(page, link, rel, canonical):
    data = json.loads((ROOT / 'docs/wiki/content.json').read_text())
    articles = data['articles']
    ids = [a['id'] for a in articles]
    if len(ids) != len(set(ids)) or ids[0] != 'index':
        raise ValueError('unique chapter identifiers and initial index required')
    result = {}
    for a in articles:
        if [s['id'] for s in a['de']['sections']] != [s['id'] for s in a['en']['sections']]:
            raise ValueError('unpaired section identifiers: ' + a['id'])
        for lang in ['de', 'en']:
            de = lang == 'de'
            other = 'en' if de else 'de'
            t = a[lang]
            path = f'wiki/{lang}/{a["id"]}.html'
            translations = {code: f'wiki/{code}/{a["id"]}.html' for code in ['de', 'en']}
            def url(target):
                return target if target.startswith('https://') else rel(path, target)
            def mdurl(target):
                return target if target.startswith('https://') else canonical(target)
            body = '<section class="hero compact wiki-heading"><p class="eyebrow">X6 WIKI · ' + ('DEUTSCH' if de else 'ENGLISH') + '</p><h1>' + E(t['title']) + '</h1><p>' + E(t['lead']) + '</p></section>'
            body += '<div class="wiki-layout"><aside class="wiki-sidebar"><nav class="wiki-chapters" aria-label="' + ('Wiki-Kapitel' if de else 'Wiki chapters') + '">'
            for chapter in articles:
                attrs = {'aria-current': 'page'} if chapter['id'] == a['id'] else {}
                body += link(rel(path, f'wiki/{lang}/{chapter["id"]}.html'), chapter[lang]['title'], **attrs)
            body += '</nav><p class="wiki-stamp">' + ('Quellenstand: ' if de else 'Source snapshot: ') + E(data['snapshot_date']) + ' · <a href="https://github.com/thomasmgfeller/x6-spectral-astrolabium/commit/' + data['source_commit'] + '">' + data['source_commit'][:7] + '</a></p></aside><article class="wiki-article">'
            body += '<details class="wiki-toc" open><summary>' + ('Auf dieser Seite' if de else 'On this page') + '</summary><ul>'
            body += ''.join('<li>' + link('#' + s['id'], s['title']) + '</li>' for s in t['sections']) + '</ul></details>'
            md = '# ' + t['title'] + '\n\n' + t['lead'] + '\n\n'
            md += '[' + ('English' if de else 'Deutsch') + '](' + canonical(translations[other]).replace('.html', '.md') + ') · [' + ('Wiki-Übersicht' if de else 'Wiki overview') + '](' + canonical(f'wiki/{lang}/index.html') + ')\n\n'
            md += ('Quellenstand: ' if de else 'Source snapshot: ') + data['snapshot_date'] + ' · `' + data['source_commit'] + '`\n\n'
            for section in t['sections']:
                body += '<section class="prose" id="' + E(section['id'], quote=True) + '"><h2>' + E(section['title']) + '</h2>'
                md += '## ' + section['title'] + '\n\n'
                for b in section['blocks']:
                    kind = b['type']
                    if kind == 'paragraph':
                        body += '<p>' + E(b['text']) + '</p>'
                        md += b['text'] + '\n\n'
                    elif kind in {'list', 'steps'}:
                        tag = 'ol' if kind == 'steps' else 'ul'
                        body += '<' + tag + '>' + ''.join('<li>' + E(x) + '</li>' for x in b['items']) + '</' + tag + '>'
                        md += ''.join((str(i + 1) + '. ' if kind == 'steps' else '- ') + x + '\n' for i, x in enumerate(b['items'])) + '\n'
                    elif kind == 'code':
                        body += '<pre><code>' + E(b['text']) + '</code></pre>'
                        md += '```sh\n' + b['text'] + '\n```\n\n'
                    elif kind == 'links':
                        body += '<ul class="wiki-sources">' + ''.join('<li>' + link(url(x['url']), x['label']) + '</li>' for x in b['items']) + '</ul>'
                        md += ''.join('- [' + x['label'] + '](' + mdurl(x['url']) + ')\n' for x in b['items']) + '\n'
                    elif kind == 'table':
                        if any(len(row) != len(b['headers']) for row in b['rows']):
                            raise ValueError('table width: ' + a['id'])
                        body += '<div class="wiki-table"><table><thead><tr>' + ''.join('<th scope="col">' + E(x) + '</th>' for x in b['headers']) + '</tr></thead><tbody>'
                        body += ''.join('<tr>' + ''.join('<td>' + E(x) + '</td>' for x in row) + '</tr>' for row in b['rows']) + '</tbody></table></div>'
                        def mdrow(row):
                            return '| ' + ' | '.join(x.replace('|', '\\|') for x in row) + ' |\n'
                        md += mdrow(b['headers']) + mdrow(['---'] * len(b['headers'])) + ''.join(mdrow(row) for row in b['rows']) + '\n'
                    else:
                        raise ValueError('unsupported block: ' + kind)
                body += '</section>'
            body += '<p class="wiki-next">' + link(rel(path, f'wiki/{lang}/index.html'), 'Zur Wiki-Übersicht' if de else 'Back to the wiki overview') + '</p></article></div>'
            result[path] = (page(path, t['title'], t['lead'], body, lang, translations), md)
    chooser = '<section class="hero compact"><p class="eyebrow">X6 WIKI · DE / EN</p><h1>X6 verstehen.<br>Understand X6.</h1><p lang="de">Leicht verständliche Anleitungen und Forschungsbegriffe.</p><p>Plain-language guides and research concepts.</p></section><div class="tool-grid">'
    chooser += '<article class="card" lang="de"><h2>Deutsch</h2><p>Einsteigen, ausprobieren und Ergebnisse richtig einordnen.</p>' + link('de/', 'Wiki auf Deutsch lesen →', **{'class': 'button'}) + '</article>'
    chooser += '<article class="card"><h2>English</h2><p>Get started, try an experiment and understand its evidence.</p>' + link('en/', 'Read the English wiki →', **{'class': 'button'}) + '</article></div>'
    result['wiki/index.html'] = (page('wiki/index.html', 'X6 Wiki · Deutsch & English', 'Plain-language X6 guides in German and English.', chooser, 'en', {'de': 'wiki/de/index.html', 'en': 'wiki/en/index.html'}), '# X6 Wiki · Deutsch & English\n\n- [Deutsch](' + canonical('wiki/de/index.html') + ')\n- [English](' + canonical('wiki/en/index.html') + ')\n')
    return result
