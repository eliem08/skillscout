# skill-g2

[![CI](https://github.com/eliem08/skill-g2/actions/workflows/ci.yml/badge.svg)](https://github.com/eliem08/skill-g2/actions/workflows/ci.yml)

> **G2 for skills** — find the best skills for your agent.

Agent skills (`SKILL.md` folders for Claude Code and friends, MCP servers,
GPT actions) are exploding, and there's no way to tell the good ones from
the abandoned ones. `skill-g2` indexes skills, scores their quality, lets
users rate them, and ranks search results the way G2 ranks software.

## What the MVP does

- **Indexer**: walks a directory tree for `SKILL.md`, parses the YAML-style
  frontmatter (`name`, `description`, optional `tags`, `version`, `author`)
- **Quality score (0–100)** from static signals:
  - description says *when* to use it ("Use when…", triggers)
  - description length in the useful range
  - has a body with steps / headings, examples, bundled scripts or references
  - no TODO / placeholder text
- **Ratings**: 1–5 stars + review text per user (one per user per skill)
- **Search**: BM25-style keyword ranking over name/description/body,
  blended with quality and Bayesian-averaged ratings
- **Compare**: side-by-side grid for 2+ skills (G2 "compare" view)

## Quickstart

```bash
pip install -e .
skill-g2 index ~/.claude/skills -o skills.json
skill-g2 search skills.json "pdf forms"
skill-g2 rate skills.json pdf 5 --user alice --text "Fills forms flawlessly"
skill-g2 compare skills.json pdf docx
```

## Roadmap

- Crawl public GitHub skill repos and MCP registries
- Usage telemetry opt-in ("installed by 2.3k agents, 91% still enabled after 30 days")
- Security scan per skill (shell commands, network calls) — trust badge

## Development

Zero runtime dependencies; Python 3.10+.

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
python -m unittest discover -s tests -t .           # unit + CLI smoke tests
ruff check . && ruff format --check .               # lint + format
```

```
skill_g2/core.py       domain logic (pure, importable, fully tested)
skill_g2/__main__.py   CLI (`skill-g2 ...` / `python -m skill_g2 ...`)
tests/                unit tests + generated CLI smoke tests
examples/             sample inputs used by the docs and smoke tests
```

CI runs lint and tests on Ubuntu and Windows across Python 3.10, 3.12 and 3.13.
Design, data model, trade-offs and production path: **[ARCHITECTURE.md](ARCHITECTURE.md)**.

Part of the [agent-economy](https://github.com/eliem08/agent-economy) portfolio (idea #21).
