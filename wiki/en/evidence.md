# Understanding evidence

For every result, ask: which claim was tested, using what data and under which conditions?

[Deutsch](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/de/evidence.md) · [Wiki overview](https://thomasmgfeller.github.io/x6-spectral-astrolabium/wiki/en/)

Source snapshot: 2026-10-18 · `e947dfbdd49890dcb119940548537d1db59272c2`

## Four different kinds of evidence

| Kind | What it can establish | What does not follow automatically |
| --- | --- | --- |
| Software check | A program satisfies the tested rules and control cases. | That its model describes nature. |
| Exact finite calculation | A mathematical statement holds for the specified finite objects. | That it holds at every size or in a continuum limit. |
| Synthetic simulation | Behaviour occurs under the programmed model assumptions. | That real equipment exhibits the same effect. |
| Physical measurement | Data from a real setup support a limited measurement claim. | General validity without calibration, uncertainty analysis and repetition. |

An archived laboratory dataset comes from real measurements. Analysing it in this project is still not a new qualification of the project’s own equipment. An AI concept illustration is not a photograph of an assembled experiment.

## Reading status labels

| Status | Meaning |
| --- | --- |
| PASS | The explicitly tested criteria were met. |
| QUALIFIED_IN_DECLARED_MODEL | All specified primary criteria are met in the explicitly declared model; this is not general physical validation. |
| FAIL | At least one specified criterion was violated. |
| INCONCLUSIVE | This test leaves the question undecided. |
| NOT_RUN / NOT_PERFORMED / NOT_EXECUTED | The relevant test was not executed. |
| INSUFFICIENT_COMMON_SUPPORT | Too few matching cases are available for the specified analysis. |
| MAIN / BRANCH_ONLY | Describes where source code is stored, not its scientific maturity. |

The precise meaning belongs to the relevant test contract. For example, a counterexample test may show PASS because an unsuitable filter was correctly rejected.

## Reproduction is more than a checksum

A checksum such as SHA-256 helps detect changes to bytes. On its own, it proves neither the origin nor the correctness of a result. A replay runs the calculation again. A separately programmed checker reduces certain shared error risks; common authorship or libraries can still create dependencies.

External replication here means that other people repeat the result with their own scrutiny. Automated GitHub checks and internal counterchecks are useful, but do not replace that step.

1. Read the precise claim and its limits.
2. Record the source commit, dataset revision, random seed and software versions.
3. Find the executed report, not just a planned test.
4. Check that counterexamples and undecided cases were preserved.
5. Compare the reported result with the criterion specified in advance.

- [Reference edition and external reproduction](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/reference-qe-v0.1/EXTERNAL_REPRODUCTION.md)
- [Numerical repair and preserved original failures](https://github.com/thomasmgfeller/x6-spectral-astrolabium/blob/main/docs/numerics-v1/README.md)

## What an uncertainty interval tells you

An interval describes uncertainty under a particular analysis model. If an interval for incremental benefit includes both negative and positive values, it does not establish an advantage. That is not proof of exact equality.

Paired comparisons analyse matching cases together. Some bootstrap intervals hold training and case selection fixed. They therefore do not additionally cover uncertainty from different training data, new generators or another selection process.
