"""Lector mínimo de tablas Visual FoxPro (DBF + FPT/FRT).

Permite inspeccionar los reportes (.frx) y tablas (.dbf) del SIGEP oficial
sin Visual FoxPro instalado. Solo lectura.

Uso:
    python vfp.py <archivo.dbf> [--limit N] [--memo] [--json]
"""
from __future__ import annotations

import json
import struct
import sys
from pathlib import Path

MEMO_TYPES = {"M", "G", "P"}


def _decode(raw: bytes, encoding: str = "cp1252") -> str:
    return raw.decode(encoding, errors="replace").rstrip("\x00 ").strip()


def _memo_path(dbf: Path) -> Path | None:
    for ext in (".fpt", ".frt", ".sct", ".dbt"):
        p = dbf.with_suffix(ext)
        if p.exists():
            return p
        # VFP usa el mismo nombre base, en minúsculas a veces
        for cand in dbf.parent.glob(f"{dbf.stem}.*"):
            if cand.suffix.lower() == ext:
                return cand
    return None


class MemoFile:
    def __init__(self, path: Path):
        self.data = path.read_bytes()
        self.block_size = struct.unpack_from(">H", self.data, 6)[0] or 64

    def get(self, block: int) -> str:
        if not block:
            return ""
        pos = block * self.block_size
        if pos + 8 > len(self.data):
            return ""
        length = struct.unpack_from(">I", self.data, pos + 4)[0]
        raw = self.data[pos + 8: pos + 8 + length]
        return raw.decode("cp1252", errors="replace")


def read_dbf(path: str | Path) -> tuple[list[dict], list[dict]]:
    dbf = Path(path)
    data = dbf.read_bytes()
    nrec = struct.unpack_from("<I", data, 4)[0]
    hlen = struct.unpack_from("<H", data, 8)[0]
    rlen = struct.unpack_from("<H", data, 10)[0]

    fields: list[dict] = []
    off = 32
    while off + 32 <= hlen and data[off] != 0x0D:
        raw = data[off: off + 32]
        ftype = chr(raw[11])
        fields.append(
            {
                "name": raw[:11].split(b"\x00")[0].decode("cp1252"),
                "type": ftype,
                "offset": struct.unpack_from("<I", raw, 12)[0],
                "length": raw[16],
                "dec": raw[17],
            }
        )
        off += 32

    memo = None
    if any(f["type"] in MEMO_TYPES for f in fields):
        mp = _memo_path(dbf)
        if mp:
            memo = MemoFile(mp)

    rows: list[dict] = []
    for i in range(nrec):
        base = hlen + i * rlen
        if base + rlen > len(data):
            break
        rec = data[base: base + rlen]
        row: dict = {"_recno": i + 1, "_deleted": rec[0:1] == b"*"}
        for f in fields:
            raw = rec[f["offset"]: f["offset"] + f["length"]]
            t = f["type"]
            if t in MEMO_TYPES:
                row[f["name"]] = memo.get(struct.unpack_from("<I", raw.ljust(4, b"\x00"))[0]) if memo else ""
            elif t == "C":
                row[f["name"]] = _decode(raw)
            elif t == "N" or t == "F":
                txt = _decode(raw)
                try:
                    row[f["name"]] = float(txt) if txt else None
                except ValueError:
                    row[f["name"]] = txt
            elif t == "I":
                row[f["name"]] = struct.unpack("<i", raw)[0]
            elif t == "L":
                row[f["name"]] = raw[:1] in (b"T", b"t", b"Y", b"y")
            elif t == "D":
                s = _decode(raw)
                row[f["name"]] = s or None
            elif t == "T":
                row[f["name"]] = raw.hex()
            else:
                row[f["name"]] = _decode(raw)
        rows.append(row)
    return fields, rows


def parse_props(text: str) -> dict:
    """Los memo de .frx/.scx guardan pares clave=valor separados por CR."""
    props: dict[str, str] = {}
    for line in text.replace("\r\n", "\r").split("\r"):
        if "=" in line:
            k, v = line.split("=", 1)
            props[k.strip().upper()] = v.strip()
    return props


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if not args:
        print(__doc__)
        return 2
    fields, rows = read_dbf(args[0])
    limit = None
    if "--limit" in flags:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    if "--json" in flags:
        print(json.dumps({"fields": fields, "rows": rows[:limit] if limit else rows}, ensure_ascii=False, indent=1))
        return 0

    print(f"== {Path(args[0]).name} ==")
    print(f"registros={len(rows)}  campos={len(fields)}")
    print("campos: " + ", ".join(f"{f['name']}:{f['type']}{f['length']}" for f in fields))
    print()
    for row in (rows[:limit] if limit else rows):
        print(f"--- registro {row['_recno']} ---")
        for k, v in row.items():
            if k.startswith("_"):
                continue
            if v in (None, "", False):
                continue
            if isinstance(v, str) and ("\r" in v or "\n" in v):
                if "--memo" not in flags:
                    print(f"  {k}: <memo {len(v)} chars>")
                    continue
                print(f"  {k}:")
                for line in v.replace("\r\n", "\r").split("\r"):
                    if line.strip():
                        print(f"      {line}")
            else:
                print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
