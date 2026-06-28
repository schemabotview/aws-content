# Visual design — tuned for retention on mobile + Udemy video

Two delivery targets: a **mobile reel feed** and **recorded Udemy lessons**. Both
are served by the same dark, high-contrast, semantic-color system below.

## Style: calm filled blocks (NOT neon)

The diagram reads like a clean reference figure, not a glowing dashboard. Color
lives in a **muted filled block**, not a neon outline. Rules:

- **No glow** (no `box-shadow`), **no backdrop-blur**, **no dotted grid**.
- Nodes are **filled** with the role hue mixed into a dark base (`#14161c`) at
  ~30% — a desaturated block (deep teal-green, muted indigo, muted amber), with a
  thin solid border one step brighter. White bold title; sub-caption a soft tint
  of the role color.
- **Edges are plain gray (`#5b6270`), thin**, with a **small slow gray flow dot**
  (2.4s) as a gentle directional cue — calm, not neon. Brighter color/motion is
  *reserved* for the narration spotlight, so the spotlight still stands apart.
  Keep edge count low — prefer 2 clean arrows over many crossing ones.

## Background

- Scene canvas + app: **`#16181d`** (flat neutral dark — no blue tint, no grid;
  avoids OLED smear / video banding; portrait pillarbox bars vanish into it).
- Code panel: **`#0d1117`** (github-dark, matches highlight.js theme).

Rationale: filled-muted-on-flat-dark keeps the **diagram calm and legible**,
survives Udemy re-encoding, and reads at phone-thumbnail size without distraction.

## Semantic palette (FIXED roles — do not reuse a color for an unrelated concept)

| Token  | Hex       | Always means…                                         |
| ------ | --------- | ----------------------------------------------------- |
| BLUE   | `#5b8cff` | **Driver / control plane** — the brain, the plan      |
| GREEN  | `#37d39a` | **Executors / compute / data** — the muscle, success  |
| ORANGE | `#ff7a59` | **Storage / shuffle / I/O** — where data lands        |
| PURPLE | `#b98bff` | **API / abstraction layer** — DataFrame, lazy plan    |
| TEAL   | `#3fd0d6` | **Transformations / flow** — movement between stages  |
| RED    | `#ff5d6c` | **Wide op / danger / gotcha** — shuffle, exam traps   |
| GRAY   | `#9aa3b2` | **Inert / context** — supporting, non-focal nodes     |

Color is a *memory cue*: a learner who sees driver=blue every time encodes it
faster. Keep ≤4–5 colors live on screen at once; push everything supporting to
GRAY so the colored nodes actually *mean* something. The hues above are **fill
seeds** — rendered as muted filled blocks (see "calm filled blocks" above), never
as glowing outlines.

## Spotlight (the video attention lever)

- **AMBER `#ffc24b`** is reserved for the **one node the narration is on right now**
  — brighter glow + the animated flow-in-path edge converging on it.
- Nothing else uses amber. Motion + a reserved highlight color drives the eye to
  exactly the concept being spoken — the biggest retention win in video/feed.

## Typography (legibility on small screens + after compression)

- Labels **bold, large** (≥ ~18px equiv at the 800×1200 scale); avoid thin weights
  — compression eats them.
- 2px+ node borders and a soft `box-shadow` glow in the node color, so nodes read
  at thumbnail size.
- `term` chips (the label *is* the concept) use mono + a filled tint of the role
  color.

## Motion

- Edges animate a dot along the path (`flow-in-path`) to show direction/sequence.
- Reveal spine nodes in narration order; depth nodes appear with the panel.
- Keep it calm — one thing moving at a time, paced to the narration's 300 ms
  pauses (blank lines in the `.tts`).
