# CLAUDE.md — aws-content

Guidance for working in this repo. Read alongside `README.md` and `DESIGN.md` —
this file is the orientation; those are the source contracts.

## What this is

A **content repo**, not an app. It holds the **AWS** topic that the `graphl-ux`
app (sibling repo) loads **at runtime**. No content logic, no render engine, and no
scenes live here — the app fetches this repo's `manifest.json` + notebooks over the
network and renders them.

There is **nothing to build, run, or test** in this repo. Changes are content and
JSON. The two executables are `scripts/build_manifest.py` (regenerates
`manifest.json` from the notebooks + an overlay map) and
`scripts/colab_generate_audio.ipynb` (a Colab tool that turns `tts/` scripts into
`audio/` `.wav`s).

## The core contract (do not break)

1. **The notebook is the single source of truth** for a module's prose and code.
   `manifest.json` only *wires* — it must never duplicate notebook content.
2. The app splits each notebook at every `## ` heading into **sections** (= pages).
   Sections match the manifest overlay by **normalized heading text** — a heading
   edit in a notebook must be mirrored in the manifest `heading` field (re-run
   `scripts/build_manifest.py`, which reads headings straight from the notebooks).
3. A section's diagram **images (`![]()`) are stripped** by the app — a **scene**
   replaces them. Don't rely on inline notebook images surviving.
4. **Scenes live in the `graphl-ux` app** (`src/scenes/aws-global.ts`,
   `aws-iam.ts`, `aws-vpc.ts`, `aws-data-engineering.ts`), authored with the
   engine's pattern helpers — **not** in this repo. The local `scenes/` dir is
   reserved (`.gitkeep`). Here you only reference a scene **by id**.

## Content (the curriculum)

14 notebooks, a beginner→SAA-C03 textbook (see `~/Projects/aws/CLAUDE.md` for the
full consolidation plan). The four scenes cover four of those modules' topics:

| # | Module | Scene |
|---|---|---|
| 01 | Cloud & AWS Foundations | `aws-global` |
| 02 | IAM, Organizations & Account Security | `aws-iam` |
| 06 | VPC & Connectivity | `aws-vpc` |
| 09 | NoSQL & Analytics | `aws-data-engineering` |
| 10 | Integration & Streaming | `aws-data-engineering` |

The other nine notebooks (03, 04, 05, 07, 08, 11–14) ship in `notebooks/` but are
not yet wired — they have no dedicated scene. Wire a module by adding a scene in the
app, then adding the module (with its overlay) to `scripts/build_manifest.py`.

## Regenerating the manifest

`scripts/build_manifest.py` is the source of truth for `manifest.json`. It reads each
wired notebook's `## ` headings and applies the per-section overlay map (spine / role
/ highlight / focus) defined inline in the script, then writes `manifest.json`. Edit
the overlay map there — never hand-edit `manifest.json` (it'll drift from the
notebooks). Highlight/focus ids must be real node ids from the referenced scene.

## TTS / audio status

Audio is **pending**. The source repo (`~/Projects/aws`) carries only
**whole-notebook** `.tts`/`.wav` (one ~25-min clip per module). The whole-notebook
`.tts` are copied into `tts/` as raw material; they still need **splitting into
per-section `NN-MM-section-slug.tts`** (one per manifest section, plain spoken prose
— see the TTS guidelines in a sibling content repo's CLAUDE.md), after which
`scripts/colab_generate_audio.ipynb` generates `audio/<stem>.wav` and the manifest
gains a per-section `audio` field. The 1 GB of whole-notebook `.wav` is intentionally
**not** copied (it's not per-section and would replay a full module on every page).

## Source

Notebooks are copied from `~/Projects/aws` (the SAA curriculum).
