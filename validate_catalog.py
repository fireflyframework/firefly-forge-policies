# Copyright 2026 Firefly Software Foundation. SPDX-License-Identifier: Apache-2.0
"""Validate policy data before it reaches a project's coding worker."""
import json
from pathlib import Path

from jsonschema import Draft202012Validator


def validate(document):
    schema = json.loads(Path(__file__).with_name("catalog.schema.json").read_text())
    failures = list(Draft202012Validator(schema).iter_errors(document))
    if failures:
        raise ValueError(f"Invalid policy catalog: {failures[0].message}")
    policies = document["skills"]
    if len({policy["id"] for policy in policies}) != len(policies):
        raise ValueError("Policy IDs must be unique")
    for policy in policies:
        commands = policy.get("commands", [])
        if policy.get("kind", "recommendation") == "quality_gate" and not commands:
            raise ValueError("Quality gates require executable commands")
        if policy.get("kind", "recommendation") == "recommendation" and commands:
            raise ValueError("Recommendations cannot execute commands")
        if any(not arg or "\x00" in arg or len(arg) > 8192 for command in commands for arg in command["argv"]):
            raise ValueError("Command arguments must be nonempty, bounded strings")


if __name__ == "__main__":
    validate(json.loads(Path(__file__).with_name("catalog.json").read_text()))
    print("Policy catalog and executable gate contracts passed.")
