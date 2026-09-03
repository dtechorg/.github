# .github

Organization profile, governance, contribution standards, issue forms, and reusable workflow entry points.

> This private repository is a **midscale representative subsystem** of `dtechorg`. Its declared future home is `dte-governance`. Interfaces are versioned through `dtechorg/echo-platform`; cross-repository integration must use contracts and content-addressed artifacts rather than undocumented imports.

## Responsibilities

The maintained implementation belongs under `src/`, contract adapters under `contracts/`, evidence under `evidence/`, and preserved source histories under `sources/<owner>/<repo>`. Large model, dataset, media and container artifacts are referenced by manifests and are not committed as ordinary Git blobs.

## Known source placements

| Source repository | Intended prefix |
|---|---|
| None assigned in the initial migration matrix | — |

## Promotion gates

A change must pass schema validation, source-lineage validation, license checks, subsystem tests, and the relevant identity/capability gates before release. Imported source code is immutable; integration changes are made in maintained packages with explicit ancestry references.

## License status

The integrated project remains under provisional private review. Imported sources retain their original licenses and notices. See `LICENSE` and each `sources/**/SourceManifest.json`.
