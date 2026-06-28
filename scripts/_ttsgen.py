"""Helper for authoring per-section .tts files from a content map keyed by heading.

Usage:
    import sys; sys.path.insert(0, 'scripts')
    from _ttsgen import author
    author(MODULE_NUM, 'notebooks/NN-....ipynb', content_dict, 'whole-notebook.tts')

content_dict maps an exact `## ` heading -> spoken-prose narration. Sections whose
heading is absent from the dict are skipped (intros/outros), keeping their section
slot number so the filename `NN-SS-slug` and the Colab sorted glob stay in order.
"""
import os, re, json
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def slug(h):
    s = h.lower().replace('`', '')
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return re.sub(r'^-+|-+$', '', s)


def author(module_num, notebook, content, whole_notebook_tts=None):
    nb = json.load(open(os.path.join(REPO, 'notebooks', os.path.basename(notebook))))
    headings = []
    for c in nb['cells']:
        if c['cell_type'] == 'markdown':
            s = ''.join(c['source'])
            headings += [ln[3:].strip() for ln in s.splitlines() if ln.startswith('## ')]
    # Validate every content key maps to a real heading. A key is either a plain
    # heading, or "Heading@@N" to target the Nth occurrence of a duplicated heading.
    counts = Counter(headings)
    for k in content:
        base = k.split('@@')[0]
        if base not in headings:
            raise SystemExit(f"M{module_num}: content key not found as heading: {k!r}")
    written = 0
    occ = {}
    for i, h in enumerate(headings, start=1):
        occ[h] = occ.get(h, 0) + 1
        keyed = f"{h}@@{occ[h]}"
        if keyed in content:
            body = content[keyed]
        elif counts[h] == 1 and h in content:
            body = content[h]
        else:
            continue
        stem = f"{module_num:02d}-{i:02d}-{slug(h)}"
        with open(os.path.join(REPO, 'tts', f'{stem}.tts'), 'w') as f:
            f.write(body.strip() + '\n')
        written += 1
    if whole_notebook_tts:
        wp = os.path.join(REPO, 'tts', whole_notebook_tts)
        if os.path.exists(wp):
            os.remove(wp)
    total = sum(len(v.split()) for v in content.values())
    print(f"module {module_num:02d}: wrote {written} files, skipped {len(headings) - written} (intro/outro), {total} words")
