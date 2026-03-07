from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path.home() / ".codex/skills/xhs-longform-private-publisher/scripts/publish_longform.py"


def load_module():
    spec = importlib.util.spec_from_file_location("publish_longform", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class TestPublishLongformHelpers(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module()
        self.tempdir = tempfile.TemporaryDirectory()
        self.base = Path(self.tempdir.name)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def write_payload(self, payload: dict) -> Path:
        path = self.base / "payload.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return path

    def test_load_payload_accepts_valid_structure(self) -> None:
        image1 = self.base / "1.png"
        image2 = self.base / "2.png"
        image1.write_bytes(b"one")
        image2.write_bytes(b"two")
        payload_path = self.write_payload(
            {
                "title": "作为一名在读博士生，我在日常是如何与AI协作的？",
                "parts": ["<p>part1</p>", "<p>part2</p>", "<p>part3</p>"],
                "images": [str(image1), str(image2)],
            }
        )

        payload = self.module.load_payload(payload_path)

        self.assertEqual(payload.title, "作为一名在读博士生，我在日常是如何与AI协作的？")
        self.assertEqual(len(payload.parts), 3)
        self.assertEqual(payload.images, [image1.resolve(), image2.resolve()])

    def test_load_payload_rejects_parts_and_images_mismatch(self) -> None:
        image1 = self.base / "1.png"
        image1.write_bytes(b"one")
        payload_path = self.write_payload(
            {
                "title": "标题",
                "parts": ["<p>part1</p>", "<p>part2</p>", "<p>part3</p>"],
                "images": [str(image1)],
            }
        )

        with self.assertRaises(self.module.PayloadValidationError):
            self.module.load_payload(payload_path)

    def test_build_title_prefix_normalizes_whitespace_and_length(self) -> None:
        prefix = self.module.build_title_prefix(
            "  作为一名在读博士生，我在日常是如何与AI协作的？  ", limit=10
        )

        self.assertEqual(prefix, "作为一名在读博士生，")

    def test_card_matches_requires_prefix_and_visibility(self) -> None:
        card_text = "仅自己可见\n作为一名在读博士生，我在日常是如何与AI协\n发布于 2026年03月07日 00:42"

        self.assertTrue(
            self.module.card_matches(
                card_text=card_text,
                title_prefix="作为一名在读博士生",
                visibility_text="仅自己可见",
            )
        )
        self.assertFalse(
            self.module.card_matches(
                card_text=card_text,
                title_prefix="别的标题",
                visibility_text="仅自己可见",
            )
        )


if __name__ == "__main__":
    unittest.main()
