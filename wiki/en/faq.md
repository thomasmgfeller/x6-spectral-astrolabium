# Frequently asked questions and help

Short answers for everyday use, with links to the details.

[Deutsch](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/de/faq.md) · [Wiki overview](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/en/)

Source snapshot: 2026-10-18 · `8ee417ba8c44c1f32f4e310a6566168d84982d3a`

## Do I need mathematics or an account?

You do not need a GitHub account to read the wiki or use the public browser labs. Curiosity is enough for the first signal experiment. Mathematics and programming become important when you want to check proofs, source code or new research questions yourself.

## Is X6 a quantum computer or a proven theory of gravity?

No. The project includes research questions about quantum physics and spacetime alongside classical computational tools and finite references. The browser benchmark assumes quantum mechanics for its two-qubit clock; it does not derive quantum mechanics from the causal order.

## Everything is green. Is my hypothesis proved?

Only the stated test conditions have passed. A mathematical proof needs an appropriate general argument. A claim about nature needs suitable physical data. Many copied or dependent trials are not automatically many independent confirmations.

## A filter shows FAIL. Is the app broken?

Not necessarily. The experiment may correctly show that this filter loses information under these settings. First check the reference, disturbances and criteria. Report a bug if the computation or interface itself contradicts the documentation.

## Local startup or export does not work

- Run the commands from the project directory containing x6.py.
- Check prerequisites using doctor --profile research.
- Use serve --port 8001 if the port is busy.
- Choose a new output directory instead of overwriting an earlier run.
- For JSON exports, use a browser supporting WebCrypto over HTTPS or localhost.
- After a failure, read the logs and error report; an incomplete run is not completed evidence.

- [Complete local workflow guide](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/INTEGRATION.md)

## How can I report a bug or contribute?

A useful report includes the commit, browser or runtime version, exact steps, input data or seed, expected and actual results, and the error message. Remove confidential data before posting it in a public issue.

Clear counterexamples, external repetitions and specific documentation corrections are particularly useful. A negative result also helps when the tested question is explicit.

- [GitHub issues](https://github.com/thomasmgfeller/x6-spectral-astrolabium/issues)
- [Contribution guidelines](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/CONTRIBUTING.md)

## May I reuse and cite X6?

Original project contributions use Apache-2.0. Third-party works and datasets retain their own terms; the included Paderborn data have a separately documented non-commercial licence. Check the licence scope of the particular file.

When citing, identify the project, exact commit or release, and the evidence report you used. Carry over its limitations. Citation metadata provide a starting point; a general wiki citation does not replace the specific result source.

- [Citation metadata](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/CITATION.cff)
- [Licence scope](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/LICENSE_SCOPE.md)

## How is this wiki maintained?

German and English are versioned together. Pages can be read without JavaScript and are also available as Markdown. Updates start from original sources and their executed reports; editing a description alone does not turn a planned test into a passed test.

- [Wiki source and maintenance guide](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/wiki/README.md)
