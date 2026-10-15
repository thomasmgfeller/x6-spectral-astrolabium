# Research hub: accessibility and discovery

The public portal provides English/German introductions, three routes
(understand, try, verify) and a static page for every registered module.
Every module page contains the original claim, pinned source, evidence summaries,
reproduction context, expected output and next acceptance gate.

## Direct entry points

Both language homepages launch the Astrolabium and Signal Validation Lab directly.
The module catalogue and their detail pages also provide application buttons.
Four additional cards lead to the local workflow, Sagnac import instructions,
reference edition and Edge example. They explicitly state when setup or local
execution is required. Research-topic buttons retain their module/evidence pages.
The Markdown alternatives include the same destinations. No application kernels,
scientific claims or historical evidence are changed by these navigation links.

## Authoritative inputs

- `MODULE_REGISTRY.json`: dated scientific/source register; no automatic upgrades.
- `docs/hub/content.json`: English/German editorial introductions and guides.
- `tools/build_hub.py`: deterministic standard-library generator.
- `assets/hub.css`, `assets/hub.js`: presentation and optional local filtering.

The catalogue and all module text/links are available with JavaScript disabled.
JavaScript only reveals search and kind/source filters. No external fonts, frontend
packages, analytics, trackers or runtime API calls are used by this portal.
The original applications have their own behaviour and evidence scopes.

Generated HTML, Markdown alternatives, `hub-index.json`, `llms.txt` and
`sitemap.xml` are committed so the existing GitHub Pages root publishing can
serve them directly. The existing `.nojekyll` remains in place.

## Maintain and verify

```sh
python3 tools/build_hub.py --write
python3 tools/build_hub.py --check
python3 tools/check_hub.py
python3 tools/module_registry.py --check --git-objects
python3 tests/python/verify_manifest.py
```

After an intentional source edit, regenerate outputs and refresh only the affected
current source-inventory hashes. Do not rewrite historical reports or inventories.
Removed registry entries cause stale generated pages to fail the build; review and
remove those pages explicitly. Browser smoke checks run with the existing project
Playwright pin; the CI workflow also checks mobile layout, filtering, keyboard
navigation and content availability without JavaScript.

`--check` and the navigation check do not execute research commands, connect to
hardware, change scheduled-agent windows or independently validate scientific claims.

## Discovery and crawler scope

The portal uses semantic HTML, visible text, real links, canonical addresses,
English/German alternate links, matching WebPage/SoftwareSourceCode JSON-LD and
Open Graph metadata. The sitemap lists the canonical documentation pages; source
archives and every historical evidence file are intentionally not duplicated in it.
`llms.txt` is an optional navigation convention, not an access policy or an indexing
requirement. Search ranking and use in AI answers are not guaranteed.

No `robots.txt` is placed in this project directory: the project is hosted below
`/x6-spectral-astrolabium/`, while robots rules are fetched from the origin root
`https://thomasmgfeller.github.io/robots.txt`. Crawling controls for `github.com`
are operated by GitHub. This change does not modify origin-wide crawler rules,
training permissions or dataset licenses. A custom domain is not required.

Repository About settings are prepared in `github-metadata.json`; that file is not
proof of account-setting changes. Applying them requires the repository settings
interface or an authenticated administrative API. Sitemap submission and private
search analytics require the relevant webmaster account and are separate from
publishing crawlable pages.

References:

- [Google: AI features and websites](https://developers.google.com/search/docs/appearance/ai-features)
- [Google: robots.txt location and scope](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec)
- [llms.txt proposal](https://llmstxt.org/)

These references explain navigation/crawling conventions, not scientific validation.
