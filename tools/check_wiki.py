#!/usr/bin/env python3
"""Check bilingual coverage and source destinations for the introductory wiki."""
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
REPO_PREFIX = 'https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/'


def main():
    data = json.loads((ROOT / 'docs/wiki/content.json').read_text())
    checks = 0
    links = 0
    for article in data['articles']:
        for lang in ['de', 'en']:
            text = article[lang]
            section_ids = [s['id'] for s in text['sections']]
            if len(section_ids) != len(set(section_ids)):
                raise ValueError('duplicate section anchors: ' + article['id'])
            other = article['en' if lang == 'de' else 'de']
            if section_ids != [s['id'] for s in other['sections']]:
                raise ValueError('translation coverage: ' + article['id'])
            checks += 2
            for section in text['sections']:
                for block in section['blocks']:
                    if block['type'] != 'links':
                        continue
                    for item in block['items']:
                        target = item['url']
                        links += 1
                        if target.startswith(REPO_PREFIX):
                            target = unquote(urlsplit(target[len(REPO_PREFIX):]).path)
                        elif target.startswith('https://'):
                            continue
                        dest = (ROOT / target).resolve()
                        if not dest.is_relative_to(ROOT) or not dest.is_file():
                            raise ValueError('missing local/source destination: ' + item['url'])
            for suffix in ['html', 'md']:
                path = ROOT / f'wiki/{lang}/{article["id"]}.{suffix}'
                if not path.is_file() or text['title'] not in path.read_text():
                    raise ValueError('missing article: ' + str(path))
                checks += 1
    print(json.dumps({'status': 'PASS', 'chapters_per_language': len(data['articles']),
                      'languages': ['de', 'en'], 'coverage_checks': checks,
                      'source_and_app_links_checked': links,
                      'scope': 'Documentation structure and source paths; no new scientific execution.'}))


if __name__ == '__main__':
    main()
