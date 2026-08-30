from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
HERO_ASSETS = (
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


class StaticHeroAssetTests(unittest.TestCase):
    def test_every_referenced_static_hero_asset_is_bundled(self):
        missing = [
            asset
            for asset in HERO_ASSETS
            if not (ROOT / asset).is_file() or (ROOT / asset).stat().st_size == 0
        ]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
