# aws-content

Content repo for the **AWS** topic in graphl-ux. Designed to load at runtime; no
content logic lives in the app code. Follows the **manifest + notebook-as-source-of-truth**
contract.

## Layout

```
aws-content/
  manifest.json     # wires modules: notebook ref + per-section overlay (scene/spine/role/highlight/focus/audio)
  DESIGN.md         # the visual house style (calm filled blocks, palette, reel chrome)
  notebooks/        # the 14 teaching .ipynb (the prose + code source of truth)
  scenes/           # reserved — scenes live in the graphl-ux app (src/scenes), not here
  tts/              # narration scripts (whole-notebook today; per-section split pending)
  audio/            # generated .wav narration (pending)
  scripts/          # build_manifest.py (regenerate manifest), colab_generate_audio.ipynb (.tts -> .wav)
```

## Contract

- The **notebook is the single source of truth** for a module's prose and code.
  The manifest only *wires* — it never duplicates notebook content.
- The app splits each notebook at every `## ` heading into **sections** (= pages).
  A section's diagram **images (`![]()`) are stripped** — the scene replaces them.
- The manifest overlay attaches, per section: a `scene` id (the diagram), a
  `spine` flag (drives feed-mode flow), an optional `role` (e.g. `hook`), optional
  `highlight`/`focus` (scene node ids the camera frames / lights), and an `audio`
  stem. Sections are matched to the overlay by normalized heading.
- **Scenes live in the graphl-ux app** (`src/scenes/aws-*.ts`), authored with the
  engine's pattern helpers — **not** here. The local `scenes/` dir is reserved
  (`.gitkeep`). Here you only reference a scene **by id**.

## Scenes (built, in the app)

Four faithful ports of the NodeMap `aws*` scenes, one per topic:

| Scene id | Covers | Module(s) it rides |
|---|---|---|
| `aws-global` | service/deployment models · connecting to AWS · Region ⊃ AZ ⊃ DC global infra | 01 |
| `aws-iam` | Organizations → accounts → roles · assume-role handshake · policy evaluation | 02 |
| `aws-vpc` | Internet → IGW → public subnet (ALB) → private subnets (SG → ASG → EC2); SG vs NACL | 06 |
| `aws-data-engineering` | Ingest → S3 lake zones → Process/Orchestrate → Query/BI | 09, 10 |

## Status

- **14 notebooks** copied from `~/Projects/aws` (a 14-module beginner→SAA curriculum).
- **5 modules wired** in `manifest.json` (01, 02, 06, 09, 10 → the four scenes,
  82 sections, per-section `highlight`/`focus`). The other nine notebooks ship in
  `notebooks/` but are **not yet wired** (no dedicated scene yet).
- **Audio pending.** The source repo carries only **whole-notebook** `.tts`/`.wav`;
  the whole-notebook `.tts` are copied into `tts/` as raw material. Per-section
  splitting and `.wav` generation (`scripts/colab_generate_audio.ipynb`) are the
  next step; the manifest does not reference `audio/` yet.

## Serving

graphl-ux fetches this repo at runtime over raw GitHub
(`https://raw.githubusercontent.com/schemabotview/aws-content/main/…`). No app build
bundles this content; the app ships only the render engine + scenes + concept registry.
