#!/usr/bin/env python3
"""Check crawlable content, exact register projection and local navigation."""
import hashlib
import importlib.util
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build_hub', ROOT / 'tools/build_hub.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.duplicates = []
        self.links = []
        self.canonical = []
        self.meta = {}
        self.h1 = 0
        self.lang = None
        self.jsonld = []
        self.in_json = False
        self.visible = []
        self.script = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        ident = attrs.get('id')
        if ident:
            if ident in self.ids:
                self.duplicates.append(ident)
            self.ids.add(ident)
        if tag == 'html':
            self.lang = attrs.get('lang')
        if tag == 'h1':
            self.h1 += 1
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical.append(attrs.get('href'))
        if tag == 'meta':
            self.meta[attrs.get('name', attrs.get('property'))] = attrs.get('content')
        if tag in {'a', 'link', 'script'}:
            value = attrs.get('href') or attrs.get('src')
            if value:
                self.links.append(value)
        if tag == 'script':
            self.script = True
            self.in_json = attrs.get('type') == 'application/ld+json'

    def handle_data(self, text):
        if self.in_json:
            self.jsonld.append(text)
        elif not self.script:
            self.visible.append(text)

    def handle_endtag(self, tag):
        if tag == 'script':
            self.script = False
            self.in_json = False


def main():
    expected = builder.outputs()
    pages = {name: Document((ROOT / name).read_text()) for name in expected if name.endswith('.html')}
    checks = 0
    errors = []
    def require(ok, message):
        nonlocal checks
        checks += 1
        if not ok:
            errors.append(message)
    for name, value in expected.items():
        require((ROOT / name).read_text() == value, 'stale generated output: ' + name)
    for name, doc in pages.items():
        require(doc.lang in {'en', 'de'}, name + ': language')
        require(doc.h1 == 1 and not doc.duplicates, name + ': heading/unique anchors')
        require(doc.canonical == [builder.canonical(name)], name + ': canonical')
        require(bool(doc.meta.get('description')), name + ': description')
        require('noindex' not in doc.meta.get('robots', ''), name + ': unexpected noindex')
        require('main' in doc.ids, name + ': skip target')
        data = json.loads(''.join(doc.jsonld))
        require(data['url'] == doc.canonical[0] and data['inLanguage'] == doc.lang, name + ': structured data mismatch')
        for href in doc.links:
            u = urlsplit(href)
            if u.scheme or u.netloc:
                require(u.scheme == 'https', name + ': unexpected external scheme ' + href)
                continue
            dest = (ROOT / name).parent / unquote(u.path) if u.path else ROOT / name
            if dest.is_dir():
                dest = dest / 'index.html'
            dest = dest.resolve()
            require(dest.is_relative_to(ROOT) and dest.is_file(), name + ': missing/unsafe link ' + href)
            if u.fragment and dest.suffix == '.html' and dest.is_file():
                target_name = dest.relative_to(ROOT).as_posix()
                target = pages.get(target_name) or Document(dest.read_text())
                require(unquote(u.fragment) in target.ids, name + ': missing anchor ' + href)
    registry = json.loads((ROOT / 'MODULE_REGISTRY.json').read_text())
    index = json.loads((ROOT / 'hub-index.json').read_text())
    require(index['registry_sha256'] == hashlib.sha256((ROOT / 'MODULE_REGISTRY.json').read_bytes()).hexdigest(), 'registry digest')
    require([m['id'] for m in registry['modules']] == [m['id'] for m in index['modules']], 'complete registry coverage')
    catalogue = '\n'.join(pages['modules/index.html'].visible)
    for m in registry['modules']:
        name = 'modules/' + m['id'] + '.html'
        text = '\n'.join(pages[name].visible)
        require(m['name'] in catalogue and m['claim'] in catalogue, m['id'] + ': missing no-JS catalogue content')
        require(m['claim'] in text and m['next_acceptance'] in text and m['entry']['expected'] in text, m['id'] + ': changed/omitted claim, gate or expectation')
        require(m['source']['commit'] in text and m['source']['availability'] in text, m['id'] + ': missing source context')
        require(all(e['summary'] in text for e in m['evidence']), m['id'] + ': missing evidence scope')
        require(all(c in text for c in m['entry']['commands']), m['id'] + ': missing command')
        require(builder.source_url(m['source']['commit'], m['source']['path']) in pages[name].links, m['id'] + ': missing pinned source')
        require(all(e['path'] in (ROOT / name).read_text() for e in m['evidence']), m['id'] + ': missing evidence paths')
    urls = [e.text for e in ET.parse(ROOT / 'sitemap.xml').findall('{*}url/{*}loc')]
    require(len(urls) == len(set(urls)) and set(urls) == {builder.canonical(p) for p in pages}, 'sitemap coverage')
    for href in re.findall(r'\]\(([^)]+)\)', (ROOT / 'llms.txt').read_text()):
        require(href.startswith(builder.BASE) and (ROOT / unquote(href[len(builder.BASE):])).is_file(), 'llms link: ' + href)
    require(not (ROOT / 'robots.txt').exists(), 'ineffective project-level robots.txt introduced')
    print(json.dumps({'status': 'FAIL' if errors else 'PASS', 'checks': checks, 'html_pages': len(pages), 'modules': len(registry['modules']), 'errors': errors}, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
