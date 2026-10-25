<!-- sell-kit:start -->
# SkillScout

[![CI](https://github.com/eliem08/skillscout/actions/workflows/ci.yml/badge.svg)](https://github.com/eliem08/skillscout/actions/workflows/ci.yml)

> **Find the best and safest skills for your AI agent.**

**Who it's for:** Developers and teams installing third-party agent skills.

**The problem:** Agent skill libraries are exploding, and there's no way to tell a well-built skill from a broken or malicious one.

**What you get:** Index SKILL.md folders, score quality, flag risky scripts (pipe-to-shell, credential access, prompt injection), and search and compare with ratings.

## Quickstart

Customers receive a release archive with the wheel and the examples. Python 3.10+ and no other dependencies.

```bash
pip install skillscout-0.1.0-py3-none-any.whl
skillscout index examples/skills -o skills.json
skillscout search skills.json "fill pdf forms"
skillscout rate skills.json pdf 5 --user alice
```

## Web app and API

Every command is also a JSON API endpoint and a browser form, served by the built-in web app.

```bash
skillscout-web --port 8000          # then open http://127.0.0.1:8000
skillscout-web keys create --label "first customer"   # prints an API key (stored hashed)
docker build -t skillscout . && docker run -p 8000:8000 -e API_KEYS=sk_... -v skillscout-data:/data skillscout
```

Every API call needs `Authorization: Bearer <key>` once any key exists; a server on a public address refuses to start without one. Calls are rate-limited per key (60/min, `--rate`) and metered: `skillscout-web usage` prints calls per key for billing.

Endpoints: `POST /api/index`, `POST /api/search`, `POST /api/rate`, `POST /api/compare`, plus `GET /healthz` and `GET /api/spec` (machine-readable field list).
Files are sent as `{"name": ..., "content": ...}`, folders as `{"files": [...]}` or a base64 zip.

## Pricing

Every plan starts with a 14-day free trial. Prices in USD, billed monthly unless noted.

| Plan | Price | Includes |
|---|---|---|
| **Developer** | $9 per month | Unlimited indexing; Risk flags; Search and compare |
| **Team** | $49 per month | Shared catalog; Ratings and reviews; Approved-skill lists |
| **Business** | $299 per month | Policy enforcement; Audit export; Priority support |

To start a trial or buy a plan, email **sales@YOUR-DOMAIN.com**.

## Licence

Proprietary. Copyright (c) 2026 eliem08. All rights reserved. Use requires a paid plan or an active trial; see [LICENSE](LICENSE).
<!-- sell-kit:end -->

## What it does

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
skillscout index ~/.claude/skills -o skills.json
skillscout search skills.json "pdf forms"
skillscout rate skills.json pdf 5 --user alice --text "Fills forms flawlessly"
skillscout compare skills.json pdf docx
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
skillscout/core.py       domain logic (pure, importable, fully tested)
skillscout/__main__.py   CLI (`skillscout ...` / `python -m skillscout ...`)
tests/                unit tests + generated CLI smoke tests
examples/             sample inputs used by the docs and smoke tests
```

CI runs lint and tests on Ubuntu and Windows across Python 3.10, 3.12 and 3.13.
Design, data model, trade-offs and production path: **[ARCHITECTURE.md](ARCHITECTURE.md)**.

Part of the [agent-economy](https://github.com/eliem08/agent-economy) portfolio (idea #21).
