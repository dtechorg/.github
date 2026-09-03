# dtechorg Midscale Federated Platform Plan

**Author:** Manus AI  
**Status:** Ready for external-creation confirmation  
**Organization handle:** `dtechorg` (appeared unclaimed when checked on 2026-09-03)

## Decision

`dtechorg` should be a **single free GitHub organization containing one bounded repository for every future enterprise domain**, plus one org-wide GitHub App. It should not be a monorepo and it should not duplicate every source repository as another top-level repository. Instead, each representative subsystem repository owns its stable contract and implementation, while known sources are imported under `sources/<owner>/<repo>` with preserved Git ancestry, a `SourceManifest`, and their original license material.

This topology is intentionally split-ready. Each repository declares its future specialist organization in `dte-subsystem.yaml`, so a later move from `dtechorg/echo-memory` to `dte-memory/echo-memory` does not change contracts, artifact identifiers, or package names.

## Repository topology

| Repository | Midscale responsibility | Future enterprise organization |
|---|---|---|
| `.github` | Organization profile, governance, issue forms, and reusable workflow entry points | `dte-governance` |
| `dtechorg-app` | Org-wide GitHub App, policy checks, orchestration adapters, event contracts | `dte-control` |
| `echo-platform` | Identity compiler control plane, canonical contracts, registry, CLI, integration tests | `dte-platform` |
| `echo-kern` | Stable cognitive-kernel ABI, tensor/signature contracts, capability negotiation | `dte-kernel` |
| `echo-os` | Namespaces, scheduling, policy, discovery, lifecycle control | `dte-os` |
| `echo-d` | Node daemon, telemetry, workload execution, artifact transfer | `dte-runtime` |
| `echo-api` | Public API and event envelope, SDK generation, service authentication | `dte-api` |
| `echo-models` | EchoSelf/NanEcho/reservoir architectures, tokenizers, model cards, checkpoint manifests | `dte-models` |
| `echo-persona` | IdentityGraph, traits, cognitive episodes, character contracts, compiler inputs | `dte-persona` |
| `echo-memory` | Working, semantic, episodic, procedural, perspectival, participatory memory | `dte-memory` |
| `echo-affect` | Endocrine/affective state, valence, arousal, somatic markers, moral perception | `dte-affect` |
| `echo-avatar` | Live2D, MetaHuman, FACS, Rig Logic, embodiment and expression adapters | `dte-avatar` |
| `echo-gateway` | Messaging, chat, channels, application adapters, direct inference gateway | `dte-gateway` |
| `echo-train` | Corpus compiler, Unsloth/CPT/SFT integration, autoresearch and experiments | `dte-training` |
| `echo-eval` | Identity, capability, novelty, calibration, memorization and CKA gates | `dte-evaluation` |
| `echo-rl` | RL environments, trajectories, rewards, simulations and policy experiments | `dte-rl` |
| `echo-data` | Dataset registry, consent, provenance, lineage splits, novelty/session policy | `dte-data` |
| `echo-artifacts` | Content-addressed model/data/artifact manifests and promotion records | `dte-artifacts` |
| `echo-infra` | Containers, Kubernetes, GPU infrastructure, observability and deployment | `dte-infrastructure` |
| `echo-research` | Reproducible architecture experiments, notebooks and scaling studies | `dte-research` |
| `echo-archive` | Preserved histories, superseded derivatives, mirrors and migration evidence | `dte-archive` |

## Source placement

The completed migration matrix covers **36 known repositories**. Every source is assigned one destination repository and prefix. A source imported under `sources/o9nn/deltecho`, for example, retains its source URL, original HEAD, import commit, license status, canonical/derivative classification and history strategy.

| Classification outcome | Count | dtechorg treatment |
|---|---:|---|
| Direct transfer candidate | 12 | Prefer preserved-history import first; transfer ownership only after lineage and dependency review |
| Preserved-history import | 11 | Import under the assigned subsystem prefix using `git subtree add` or commit-object import |
| Reference-only source | 9 | Record in `SourceManifest`; do not vendor large upstream mirrors unless an offline build requires it |
| Archive | 3 | Preserve under `echo-archive/sources/...` and make read-only by policy |
| Subtree import | 1 | Import the DTE-specific subtree while retaining ancestry references |

Fourteen source classifications require a license review. Those sources may be preserved privately for provenance, but they cannot be released, relicensed or promoted into public packages until ownership and license terms are resolved.

## Org-wide GitHub App

The app name is **`dtechorg-app`** and it is private to the organization. Phase 1 is deliberately **Actions-first**: the app coordinates `repository_dispatch`, check runs, pull requests and release evidence without requiring an always-on webhook server. EchoD hosting is introduced only when event volume or cross-cloud workloads justify a persistent receiver.

| Permission | Level | Reason |
|---|---|---|
| Metadata | Read | Resolve repositories and installations |
| Contents | Write | Commit generated manifests and open controlled update branches |
| Pull requests | Write | Create and annotate integration PRs |
| Issues | Write | Open drift, validation and migration findings |
| Checks and statuses | Write | Publish contract, lineage, experiment and release gates |
| Actions | Read | Observe workflow outcomes without editing workflow definitions |
| Deployments | Write | Record promoted artifact deployments |
| Administration | Read | Inspect repository settings and policy drift |
| Members | Read | Resolve CODEOWNERS and team policy |

The app subscribes to installation, repository, push, pull request, issue, check, release, workflow-run and deployment events. Private keys and webhook secrets are never committed. Any future permission addition requires a manifest change, security review and installation reapproval.

## Teams

| Team | Repository scope |
|---|---|
| `platform-maintainers` | `.github`, app, platform, kernel, OS, daemon and API |
| `identity-maintainers` | Persona, memory, affect, avatar and gateway |
| `model-maintainers` | Models, training, evaluation, RL and data |
| `operations-maintainers` | Artifacts, infrastructure, research and archive |

## Migration invariants

A source import is acceptable only when its commit ancestry remains inspectable, its source remote and HEAD are recorded, its license material is retained, large generated artifacts are excluded, and the destination receives a passing contract and build check. Canonical and derivative implementations cannot silently overwrite one another. Source imports are immutable inputs; integrated code enters maintained packages only through reviewed extraction commits.

## External operations requiring confirmation

Creating the organization, creating the GitHub App, installing it across all repositories, creating 21 private repositories, and importing histories are external account changes. The complete topology and permission set must therefore be confirmed before those operations begin.
