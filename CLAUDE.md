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

The other **nine** modules (03, 04, 05, 07, 08, 11, 12, 13, 14) are also wired, but
each rides a topically related existing scene as a **full-strength backdrop**
(`backdrop=True` in `build_manifest.py`): no `highlight`/`focus`, since their content
has no matching scene nodes, every section on the spine, first section the hook.
Backdrop map: 03 → `aws-vpc` (it has EC2/ELB/ASG nodes), 04/07/13/14 → `aws-global`,
05/08 → `aws-data-engineering`, 11/12 → `aws-iam`. Give one its own diagram later by
authoring a scene in graphl-ux and replacing its `backdrop` entry with a real overlay map.

## Regenerating the manifest

`scripts/build_manifest.py` is the source of truth for `manifest.json`. It reads each
wired notebook's `## ` headings and applies the per-section overlay map (spine / role
/ highlight / focus) defined inline in the script, then writes `manifest.json`. Edit
the overlay map there — never hand-edit `manifest.json` (it'll drift from the
notebooks). Highlight/focus ids must be real node ids from the referenced scene.

## TTS / audio status

**Per-section `.tts` are authored** for all 14 notebooks — 234 scripts named
`tts/NN-SS-slug.tts` (the `SS` is the section's 1-based order in the notebook, so the
stem and the Colab sorted glob stay in order). They were written from scratch from
each `## ` section per the TTS guidelines (plain spoken prose — no markdown, tables,
or code; acronyms spelled out). **Intros and outros are silent** (no `.tts`): per
notebook, the framing-overview opener (e.g. "The database zoo at a glance") and the
recap/decision closer (e.g. "Picking the Right Tool") are skipped, leaving gaps in
the section numbering — that's intentional.

Regenerate the set from `scripts/_ttsgen.py` (the `author()` helper keys narration
by `## ` heading; duplicate headings use `Heading@@N`). **Next steps:** generate
`audio/<stem>.wav` with `scripts/colab_generate_audio.ipynb`, then add a per-section
`audio` field to the manifest. The 1 GB of whole-notebook `.wav` from `~/Projects/aws`
is intentionally **not** copied (it's not per-section).

## Source

Notebooks are copied from `~/Projects/aws` (the SAA curriculum).
