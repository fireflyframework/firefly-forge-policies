# firefly forge policies

Versioned development guidance and executable quality checks for [firefly forge](https://github.com/fireflyframework/firefly-forge). Projects choose their own selection. Each run keeps the catalog revision, content digest and selected instructions, so a later catalog update cannot change a queued run.

## Use the catalog

In forge, open **Agents & skills**, expand **Use a central policy repository**, and enter this repository's HTTPS clone URL and a full Git commit. Sync the catalog, choose a project, and save its policy selection. New runs inherit those defaults; a run can override them explicitly.

```text
https://github.com/fireflyframework/firefly-forge-policies.git
```

Use a reviewed commit. forge imports only `catalog.json`, validates it, and retains its digest. It does not check out or execute repository scripts during synchronization.

## Recommendations and quality gates

Recommendations add instructions to the selected coding worker. They guide implementation and do not establish that a project follows a practice. Quality gates execute bounded command argument arrays after the project's normal verification. A failed gate makes the run fail or enter its bounded repair loop.

The catalog includes framework implementation, behavioral verification, application security, accessibility, documentation, requirements, architecture, dependency maintenance, observability, release preparation, readable documentation, maintainability and browser acceptance. The optional `repository-check` gate runs `make check`; enable it only in projects with that executable target.

Workspace isolation, credential protection, source integrity and passing verification are platform controls. Disabling a recommendation does not disable them.

## Edit a policy

Keep policy IDs stable. Use a new ID when its meaning changes. Edit the instructions and descriptions for the intended developer, then update the catalog version and review the changes.

```json
{
  "id": "repository-check",
  "name": "Repository check gate",
  "description": "Require the project's executable make check target.",
  "category": "verification",
  "kind": "quality_gate",
  "default": false,
  "instructions": "Run the repository's make check target successfully.",
  "commands": [{"argv": ["make", "check"], "timeout": 600, "backends": ["pyfly", "larafly"]}]
}
```

Command arguments are separate strings. Shell expressions have no implicit interpreter. Treat a quality-gate change as code execution: it runs with the trusted worker host's permissions.

## Validate and release

```sh
uv sync --locked
uv run python validate_catalog.py
uv run python -m unittest
```

CI validates the production-compatible schema, unique identities and command semantics. Releases contain the reviewed catalog, schema and SHA-256 checksums. Pin the release's Git commit when importing it into forge.

First-party code and policy text use Apache 2.0. Community adaptations retain the MIT or Apache 2.0 notices embedded in each entry. Firefly product names retain their trademark rights.

## Community instruction sources

Version 1.1.0 includes adapted thinking, test-driven development, debugging and evidence instructions from [Superpowers](https://github.com/obra/superpowers), frontend design and browser QA from [Anthropic skills](https://github.com/anthropics/skills), and prose editing from [Humanizer](https://github.com/blader/humanizer). Each entry identifies its exact source commit and file, source SHA-256, adaptation SHA-256 and license text. The two selected Anthropic skills have individually verified Apache 2.0 licenses; this does not characterize other skills in that repository.

These are instruction adaptations. Forge does not install upstream plugins, execute their helper scripts, grant native tools or automatically perform their suggested publication steps. Codex and Claude use their official worker tooling; native Agentic uses confined workspace tools. Product-owner decisions and factory permissions take precedence over optional guidance. The role registry freezes selected adaptations into each run separately from executable repository quality gates.
