"""¿Quedó código fuente dentro de los .APP? Busca palabras clave de PRG."""
import json
import pathlib
import re

BASE = pathlib.Path(__file__).parent
spec = json.loads((BASE / "spec" / "cadenas.json").read_text(encoding="utf-8"))

KEYS = re.compile(r"^\s*(PROCEDURE|FUNCTION|ENDPROC|ENDFUNC|PARAMETERS|LPARAMETERS|LOCAL|SELECT |USE |SCATTER|GATHER)\b", re.I)
for mod in ("pr_cbte.APP", "jconta.APP", "cge.APP", "mant.APP"):
    data = spec.get(mod, {})
    nombres = data.get("nombres", [])
    hits = [s for s in nombres if KEYS.search(s)]
    print(f"{mod}: {len(nombres)} nombres; posibles palabras de código: {len(hits)}")
    for s in hits[:15]:
        print("   ", s)

# nombres de procedimientos/funciones típicos
print("\nMuestras de nombres (pr_cbte):")
for s in spec.get("pr_cbte.APP", {}).get("nombres", [])[:60]:
    print("   ", s)
