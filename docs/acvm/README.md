# Astrolabium Control and Validation Module

**ACVM concept 0.1 · 13 October 2026 · CONCEPT ONLY**

ACVM is a proposed control and validation module for the Astrolabium project.
It defines how an experiment plan could be compiled, executed on a supported
device, independently measured and assessed against declared acceptance criteria.

- [Read the complete concept in German](ACVM_CONCEPT_v0_1_DE.md)
- [Download the original Word document](Astrolabium_ACVM_Konzept_v0_1.docx)
- [Publication provenance and SHA-256 inventory](manifest.json)

## Classification and evidence

| Attribute | Status |
| --- | --- |
| Main category | Control and measurement infrastructure |
| Artifact type | Engineering concept and proposed validation plan |
| Concept version | 0.1 |
| Implementation | Pending |
| Proposed ACVM checks V01–V10 | NOT RUN |
| Electrical and photonic measurements for ACVM | NOT PERFORMED |
| Astrolabium device integration | Proposed interface; compatibility not established |
| Quantum operation or industrial qualification | Not established |

The concept carries forward defensible architecture ideas and documented PMCS
failure classes as requirements. It does not adopt the earlier PMCS code as
qualified software. Numerical, software, electrical, photonic and quantum
evidence remain distinct.

The internal source reports cited as I1–I3 are identified in the document;
they are not bundled in this publication. Their reported historical tests were
not rerun for this publication and are not independently reproducible from
this folder alone. Source I4 is the supplied concept excerpt. External papers
and manufacturer materials are linked, not redistributed.

## First implementation steps

1. Specify one experiment-package profile, a compiler and an independent reader.
2. Implement the proposed software/model checks V01–V08 and preserve their results.
3. Select one device profile and qualify an electrical output channel with an
   independent measurement; repeat the applicable failure tests on the device.
4. Add a calibrated photonic actuator only after the electrical path is characterized.

Actual hardware error limits, supported rates and latency bounds remain open
until a device profile and experimental requirements are selected. No throughput
or quantum-performance promise is made by this concept.

## Relationship to existing work

- [Signal Validation Lab](../SIGNAL_VALIDATION_LAB.md): existing synthetic signal
  comparisons; possible future reuse of qualified metrics.
- [Sagnac integration](../SAGNAC_INTEGRATION.md): existing acquisition/import
  preview; no ACVM control compatibility is asserted.
- [Photonic two-qubit experiment](../../experiments/photonic-two-qubit/README.md):
  a possible future application of a qualified control and measurement path.

This publication adds documentation only. It does not add executable ACVM code,
activate devices or alter application code, tests, workflows or scheduled agents.
There is no ACVM software release or hardware approval associated with version 0.1.

## Publication provenance

The Word file is the exact concept document approved for publication. The Markdown
edition was converted from it with Pandoc, restoring the title and subtitle and
normalizing heading levels, equation markup and multiline table cells for GitHub. The concept
text and six equations are preserved. The Word file remains the source artifact
for this version; later scientific changes require a new recorded version.

SHA-256 values in `manifest.json` cover the two editions and this overview.
They bind the published bytes, not the truth of scientific claims. The manifest
does not hash itself. The repository inventory also records these four new
documentation files as non-historical additions while retaining its historical
hash values. These publication checks are separate from the NOT RUN
ACVM validation plan.

Original project documentation follows the repository's
[Apache-2.0 license](../../LICENSE) and [licensing scope](../../LICENSE_SCOPE.md).
Third-party sources retain their own terms.
