# ACVM Experiment Records

**Concept 0.1 · 13 October 2026 · CONCEPT ONLY**

Experiment Records specifies the proposed experiment-record and provenance layer
of the Run Archive in [ACVM concept 0.1](../README.md). It connects a versioned
experiment plan, compiled execution data, execution reports, original acquisition
data, analysis and review while keeping their evidence limits separate.

- [Read the complete German concept](ACVM_EXPERIMENT_RECORDS_CONCEPT_v0_1_DE.md)
- [Download the original Word document](ACVM_Experiment_Records_Konzept_v0_1.docx)
- [Publication metadata and file hashes](manifest.json)

## Scope and evidence status

| Item | Status |
| --- | --- |
| Category | Experiment documentation, research data management and provenance |
| Architecture, data model and requirements | Concept specified |
| Executable schema and Records implementation | Not delivered by this publication |
| Adapters to Signal Validation Lab and Sagnac | Proposed; compatibility not established |
| Proposed Records checks ER01–ER14 | NOT_RUN |
| Electrical or optical qualification of this extension | Not performed |
| Scientific, security or industrial certification | Not established |

The document defines identities, a portable package layout, independent status
fields, time and unit semantics, calibration references, integrity checks,
failure preservation and a staged acceptance plan. Hashes bind bytes; they do
not establish truthful provenance or correct measurements. A completed device
run, a sealed package and a passing scientific criterion are separate states.

The ACVM checks V01–V10 retain their own scope. The new Records checks do not
inherit their results or replace physical device testing. No earlier tests were
rerun for this documentation publication.

## Connection to existing work

- [ACVM](../README.md): specifies the Run Archive contract and its experiment package.
- [Signal Validation Lab](../../SIGNAL_VALIDATION_LAB.md): possible import of
  preserved synthetic exports, including their source and replay limits.
- [Sagnac integration](../../SAGNAC_INTEGRATION.md): possible import of original
  SGNCv007 snapshots without adding actuator control or per-photon time tags.
- [Photonic two-qubit experiment](../../../experiments/photonic-two-qubit/README.md):
  potential future use after its applicable device and measurement qualification.

The concept's internal references are pinned to repository commit
`c20c2b306e8785f79a431bdd9becec57acb95cec`. This is the reference baseline,
not a claim that an Experiment Records implementation exists at that commit.

The first proposed implementation is an offline package profile, writer and
independent reader, followed by ER01–ER14 in their declared software scope.
Device-model tests do not qualify real hardware. Schema details, numerical
tolerances, resource limits and storage policy remain implementation decisions
that must be fixed before their corresponding acceptance tests.

## Publication provenance

The Word file is the unchanged approved source document, containing 13 pages.
The Markdown edition preserves its prose, tables and source hyperlinks. Pandoc
3.1.3 converted the document; title metadata and heading levels were restored,
and multiline table cells use slash-separated text. Page layout and page numbers
belong to the Word edition. No scientific content was revised for publication.

`manifest.json` records SHA-256 values and byte counts for the two editions and
this overview. It is publication metadata, not an implemented Records schema
or a report of executed ER acceptance tests. The repository inventory records
the new files as non-historical documentation additions and retains pre-existing
historical digest values. The current Sagnac integration inventory updates only
the changed root README entry and records its previous digest.

Original project documentation follows the repository's [Apache-2.0 license](../../../LICENSE)
and [licensing scope](../../../LICENSE_SCOPE.md). Third-party sources are linked,
not redistributed. This publication changes documentation and the associated
inventories; it does not implement Records, issue device commands or alter agents.
