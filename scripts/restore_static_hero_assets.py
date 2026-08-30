"""Bundle background images that the original WordPress templates reference.

The static replica keeps original asset paths.  This helper restores only the
missing hero media required by those already-exported templates; it never
rewrites page markup or downloads a whole media library.
"""

from __future__ import annotations

from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://indafire.com.br/"
ASSETS = (
    "wp-content/uploads/2021/10/inda-fire.jpg",
    "wp-content/uploads/2021/11/b.jpg",
    "wp-content/uploads/2021/11/PRONTA-4.jpg",
    "wp-content/uploads/2021/11/inda-fundo.jpg",
    "wp-content/uploads/2021/11/Repeticao-de-grade-1.jpg",
    "wp-content/uploads/2021/11/fogu.jpg",
    "wp-content/uploads/2021/11/contato.jpg",
    "wp-content/uploads/2021/11/cidade.jpg",
    "wp-content/uploads/2021/12/shutterstock_1868912746.jpg",
)


def restore_assets() -> int:
    restored = 0
    for relative_path in ASSETS:
        target = ROOT / relative_path
        if target.is_file() and target.stat().st_size > 0:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        request = Request(
            ORIGIN + relative_path,
            headers={"User-Agent": "Indafire static build asset restorer"},
        )
        with urlopen(request, timeout=30) as response:
            target.write_bytes(response.read())
        if target.stat().st_size == 0:
            raise RuntimeError(f"Downloaded an empty asset: {relative_path}")
        restored += 1
    return restored


if __name__ == "__main__":
    print(f"Restored {restore_assets()} static hero asset(s).")
