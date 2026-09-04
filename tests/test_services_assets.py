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
    "wp-content/uploads/2021/11/ico-1.svg": "330E61A00336B9D27EEFB8D90148914706A0E588002F87222745D137C541EE45",
    "wp-content/uploads/2021/11/ico-2.svg": "971CE22425B80F5AE27E9561C6BA098A1BFE994D146ACD0E8B62A2ED68867B37",
    "wp-content/uploads/2021/11/ico-3.svg": "100FC94A5929D3B72264F76C75666ECEAB72BCF199F00ABE8E0F977C2D092ECE",
    "wp-content/uploads/2021/11/ico-4.svg": "97B5327D4DD1455E1BA25DB81EF1222BD69F2520CA298E89FFC0DCCBC7F0D4A4",
    "wp-content/uploads/2021/11/ico-4-1.svg": "1C1B2B9774757404A291C705A6EBDE4182E752C752F7EB6829B7DEB2E19518D3",
    "wp-content/uploads/2021/11/10639604_1538289183049362_3959369163680743290_n.jpg": "E5D97DAA57F2F12FA82F0DF5519DA867154072C8AA29AEC3DF38CCD3E464ECF6",
}


class ServicesAssetTests(unittest.TestCase):
    def test_original_services_images_are_bundled_without_reencoding(self):
        for relative_path, expected_hash in EXPECTED_SHA256.items():
            with self.subTest(asset=relative_path):
                asset = ROOT / relative_path
                self.assertTrue(asset.is_file(), f"Missing original asset: {relative_path}")
                payload = asset.read_bytes()
                if asset.suffix.lower() in {".jpg", ".jpeg"}:
                    self.assertTrue(payload.startswith(b"\xff\xd8\xff"), relative_path)
                else:
                    self.assertIn(b"<svg", payload[:500].lower(), relative_path)
                self.assertEqual(hashlib.sha256(payload).hexdigest().upper(), expected_hash)


if __name__ == "__main__":
    unittest.main()
