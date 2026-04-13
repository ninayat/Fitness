import re
import zlib
from collections import Counter, defaultdict
from pathlib import Path

PDF = Path("PROCEDURES _ SMQ 2025 - Réseau franchise.pdf")
OUT = Path("sources/SMQ-2025-ocr-brut.txt")

b = PDF.read_bytes()

# 1) Build a global codepoint map from embedded ToUnicode CMaps.
votes = defaultdict(Counter)
for m in re.finditer(rb"stream\r?\n", b):
    s = m.end()
    e = b.find(b"endstream", s)
    if e < 0:
        continue
    d = b[s:e]
    if d.endswith(b"\r\n"):
        d = d[:-2]
    elif d.endswith(b"\n"):
        d = d[:-1]
    try:
        dec = zlib.decompress(d)
    except Exception:
        continue
    if b"begincmap" not in dec:
        continue
    text = dec.decode("latin1", "ignore")

    for _, blk in re.findall(r"(\d+) beginbfchar\s*(.*?)\s*endbfchar", text, re.S):
        for src, dst in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blk):
            try:
                votes[int(src, 16)][bytes.fromhex(dst).decode("utf-16-be", "ignore")] += 1
            except Exception:
                pass

    for _, blk in re.findall(r"(\d+) beginbfrange\s*(.*?)\s*endbfrange", text, re.S):
        for a, b2, c in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", blk):
            a_i = int(a, 16)
            b_i = int(b2, 16)
            c_i = int(c, 16)
            for i, code in enumerate(range(a_i, b_i + 1)):
                votes[code][chr(c_i + i)] += 1

code_map = {k: v.most_common(1)[0][0] for k, v in votes.items() if v}

# 2) Decode text-showing strings from PDF streams.
lines = []
for m in re.finditer(rb"stream\r?\n", b):
    s = m.end()
    e = b.find(b"endstream", s)
    if e < 0:
        continue
    d = b[s:e]
    if d.endswith(b"\r\n"):
        d = d[:-2]
    elif d.endswith(b"\n"):
        d = d[:-1]
    try:
        dec = zlib.decompress(d)
    except Exception:
        continue
    if b"BT" not in dec:
        continue

    for sm in re.finditer(rb"\((.*?)\)", dec, re.S):
        raw = sm.group(1)
        raw = raw.replace(b"\\)", b")").replace(b"\\(", b"(").replace(b"\\\\", b"\\")
        raw = re.sub(rb"\\([0-7]{1,3})", lambda x: bytes([int(x.group(1), 8)]), raw)
        if len(raw) % 2 == 1:
            raw = b"\x00" + raw

        chars = []
        for i in range(0, len(raw), 2):
            code = (raw[i] << 8) | raw[i + 1]
            chars.append(code_map.get(code, ""))
        txt = "".join(chars).strip()
        if len(txt) > 1:
            lines.append(txt)

# Deduplicate while preserving order.
seen = set()
clean = []
for l in lines:
    if l in seen:
        continue
    seen.add(l)
    clean.append(l)

OUT.write_text("\n".join(clean) + "\n", encoding="utf-8")
print(f"Wrote {OUT} with {len(clean)} unique extracted lines")
