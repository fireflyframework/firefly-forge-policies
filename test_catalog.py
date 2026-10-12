# Copyright 2026 Firefly Software Foundation. SPDX-License-Identifier: Apache-2.0
import copy
import json
import unittest
from pathlib import Path

from validate_catalog import validate


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.document = json.loads(Path("catalog.json").read_text())

    def test_published_catalog_is_valid(self):
        validate(self.document)

    def test_duplicate_policy_identity_is_rejected(self):
        self.document["skills"].append(copy.deepcopy(self.document["skills"][0]))
        with self.assertRaises(ValueError):
            validate(self.document)

    def test_unknown_policy_fields_are_rejected(self):
        self.document["skills"][0]["execute_script"] = "untrusted source"
        with self.assertRaises(ValueError):
            validate(self.document)

    def test_quality_gate_requires_a_real_command(self):
        self.document["skills"][0].update(kind="quality_gate", commands=[])
        with self.assertRaises(ValueError):
            validate(self.document)

    def test_recommendation_cannot_execute_commands(self):
        self.document["skills"][0]["commands"] = [{"argv": ["make", "check"], "backends": ["pyfly"]}]
        with self.assertRaises(ValueError):
            validate(self.document)

    def test_community_hash_tampering_is_rejected(self):
        entry = next(item for item in self.document["skills"] if item.get("provenance"))
        entry["instructions"] = "Unreviewed adaptation"
        with self.assertRaises(ValueError):
            validate(self.document)

    def test_community_license_tampering_is_rejected(self):
        entry = next(item for item in self.document["skills"] if item.get("provenance"))
        entry["provenance"]["license_text"] = "Missing license"
        with self.assertRaises(ValueError):
            validate(self.document)


if __name__ == "__main__":
    unittest.main()
