"""Reconstruye visualmente un reporte VFP (.frx) desde sus objetos.

Unidades: FRU, 10000 por pulgada (constante $FRUs de VFP 9).
Genera un PNG con la geometría y el texto de cada objeto.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from vfp import parse_props, read_dbf  # noqa: E402

FRU = 10000.0
DPI = 100.0
PX = DPI / FRU


def first_block(rows):
    """El .frx puede traer un segundo reporte escalado; nos quedamos con el primero."""
    out = []
    visto = 0
    for r in rows:
        if r.get("OBJTYPE") == 1:
            visto += 1
            if visto > 1:
                break
        out.append(r)
    return out


def main() -> int:
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".png")
    _, rows = read_dbf(src)
    rows = first_block(rows)

    maxv = max((r.get("VPOS") or 0) + (r.get("HEIGHT") or 0) for r in rows)
    maxh = max((r.get("HPOS") or 0) + (r.get("WIDTH") or 0) for r in rows)
    img = Image.new("RGB", (int(maxh * PX) + 40, int(maxv * PX) + 40), "white")
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 7)
    except Exception:
        font = ImageFont.load_default()

    for r in rows:
        v, h = (r.get("VPOS") or 0), (r.get("HPOS") or 0)
        w, ht = (r.get("WIDTH") or 0), (r.get("HEIGHT") or 0)
        box = [h * PX + 10, v * PX + 10, (h + w) * PX + 10, (v + ht) * PX + 10]
        ot = r.get("OBJTYPE")
        expr = (r.get("EXPR") or "").strip()
        if ot in (5, 8) and expr:
            d.rectangle(box, outline=(200, 60, 60), width=1)
            txt = expr.replace("\r", " ")[:80]
            d.text((box[0] + 1, box[1]), txt, fill=(0, 0, 0), font=font)
        elif ot == 6:
            d.rectangle(box, outline=(60, 60, 200), width=1)
        elif ot == 7:
            d.rectangle(box, outline=(0, 150, 0), width=1)
        elif ot == 9:
            d.line([(10, (v + ht) * PX + 10), (img.width - 20, (v + ht) * PX + 10)], fill=(120, 120, 120), width=1)
    img.save(dst)
    print(f"{dst}  {img.width}x{img.height}px  ({maxh/FRU:.2f} x {maxv/FRU:.2f} in)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
