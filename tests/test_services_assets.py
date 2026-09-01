from __future__ import annotations

import hashlib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SHA256 = {
    "wp-content/uploads/2021/11/servicos.jpg": "076DC8B0F8F69955C94DC400B334BC1E6E926AEEE6E600D7A3845CC352CFF4A0",
    "wp-content/uploads/2021/12/Projeto-Simplificado.jpg": "2F34D458D345A1CFB5E298E2FA2142D966247432BDEF737E53E788FCD31651C0",
    "wp-content/uploads/2022/01/2.jpg": "39286A4FD9E84C1A3251CE784790A850AD0113A04BF77F4D4BFD7B38D57E7E1C",
    "wp-content/uploads/2022/01/3.jpg": "4A56B9EAF968FC4FB86AAD9CB2ACE2B5093722639FC16E31068BF6C02CF497FC",
    "wp-content/uploads/2022/01/4.jpg": "D106942E553303B7A270940EEA63033773D5718E6EE02A006751B93AB4B8222D",
}


class ServicesAssetTests(unittest.TestCase):
    def test_original_services_images_are_bundled_without_reencoding(self):
        for relative_path, expected_hash in EXPECTED_SHA256.items():
            with self.subTest(asset=relative_path):
                asset = ROOT / relative_path
                self.assertTrue(asset.is_file(), f"Missing original asset: {relative_path}")
                payload = asset.read_bytes()
                self.assertTrue(payload.startswith(b"\xff\xd8\xff"), relative_path)
                self.assertEqual(hashlib.sha256(payload).hexdigest().upper(), expected_hash)


if __name__ == "__main__":
    unittest.main()
