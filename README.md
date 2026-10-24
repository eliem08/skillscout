# skill-g2

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
