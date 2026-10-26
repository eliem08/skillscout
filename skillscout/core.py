"""Index, score, rate and search agent skills (SKILL.md)."""

from __future__ import annotations

import json
import math
import os
import re
from collections import Counter
from dataclasses import asdict, dataclass, field

__all__ = ["Skill", "parse_skill", "index_dir", "quality", "risk_flags", "Catalog"]

# Skills are instructions and code an agent will run, so a catalog must surface what they could do before ranking.
RISK_PATTERNS = {
    "pipe_to_shell": r"(curl|wget)[^\n|]*\|\s*(ba|z)?sh\b|iex\s*\(\s*(iwr|invoke-webrequest)",
    "destructive_command": r"\brm\s+-\w*r\w*f|\bformat\s+c:|\bmkfs\b|\bdel\s+/[sq]",
    "prompt_injection": r"\b(ignore|disregard)\b.{0,40}\b(previous|prior|above|system)\b.{0,20}\b(instructions?|prompt)",
    "credential_access": r"\.ssh/|id_rsa|\.aws/credentials|\.env\b|keychain|security\s+find-generic-password",
    "obfuscated_payload": r"base64\s+(-d|--decode)|frombase64string|eval\s*\(\s*(atob|base64)",
}
SCRIPT_EXTS = {".sh", ".bash", ".zsh", ".ps1", ".py", ".js", ".mjs", ".ts", ".rb", ".pl", ".bat", ".cmd"}


@dataclass
class Skill:
    name: str
    description: str
    path: str
    body: str = ""
    tags: list = field(default_factory=list)
    version: str = ""
    author: str = ""
    has_scripts: bool = False
    has_references: bool = False
    quality: int = 0
    ratings: dict = field(default_factory=dict)  # user -> {"stars": int, "text": str}
    risks: list = field(default_factory=list)


def _frontmatter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    meta, key = {}, None
    for line in m.group(1).splitlines():
        if re.match(r"^\s+-\s+", line) and key:
            meta.setdefault(key, [])
            if isinstance(meta[key], list):
                meta[key].append(line.split("-", 1)[1].strip().strip("\"'"))
            continue
        kv = re.match(r"^([\w-]+):\s*(.*)$", line)
        if kv:
            key, val = kv.group(1), kv.group(2).strip()
            if val.startswith("[") and val.endswith("]"):
                meta[key] = [v.strip().strip("\"'") for v in val[1:-1].split(",") if v.strip()]
            elif val in {"|", ">", ""}:
                meta[key] = ""
            else:
                meta[key] = val.strip("\"'")
        elif key and isinstance(meta.get(key), str):
            meta[key] = (meta[key] + " " + line.strip()).strip()
    return meta, m.group(2)


def risk_flags(text: str) -> list[str]:
    return [name for name, rx in RISK_PATTERNS.items() if re.search(rx, text, re.I | re.S)]


def _script_text(folder: str, limit: int = 200_000) -> str:
    chunks = []
    for r, _, files in os.walk(os.path.join(folder, "scripts")):
        for f in files:
            if os.path.splitext(f)[1].lower() in SCRIPT_EXTS:
                with open(os.path.join(r, f), encoding="utf-8", errors="ignore") as fh:
                    chunks.append(fh.read(limit))
    return "\n".join(chunks)


def quality(s: Skill) -> int:
    score = 0
    d = s.description.lower()
    if re.search(r"\buse (this )?(skill )?(when|whenever|for|to)\b|\btrigger", d):
        score += 25
    n = len(s.description)
    score += 20 if 80 <= n <= 600 else 10 if 30 <= n < 80 or 600 < n <= 1200 else 0
    if len(re.findall(r"^#{1,3} ", s.body, re.M)) >= 2:
        score += 15
    if re.search(r"```", s.body):
        score += 10
    if re.search(r"^\s*(\d+\.|-)\s+", s.body, re.M):
        score += 5
    if s.has_scripts:
        score += 10
    if s.has_references:
        score += 10
    if re.search(r"\b(TODO|TBD|lorem ipsum|FIXME)\b", s.body + s.description):
        score -= 15
    if s.version:
        score += 5
    if s.risks:
        score = min(score, 40)  # well-written is not the same as safe to run
    return max(0, min(100, score))


def parse_skill(path: str) -> Skill | None:
    with open(path, encoding="utf-8", errors="ignore") as fh:
        meta, body = _frontmatter(fh.read())
    folder = os.path.dirname(path)
    name = meta.get("name") or os.path.basename(folder)
    if not meta.get("description"):
        return None
    tags = meta.get("tags", [])
    s = Skill(
        name=name,
        description=meta["description"],
        path=folder,
        body=body,
        tags=tags if isinstance(tags, list) else [tags],
        version=meta.get("version", ""),
        author=meta.get("author", ""),
        has_scripts=os.path.isdir(os.path.join(folder, "scripts")),
        has_references=os.path.isdir(os.path.join(folder, "references")),
    )
    s.risks = risk_flags(f"{s.description}\n{body}\n{_script_text(folder)}")
    s.quality = quality(s)
    return s


def index_dir(root: str) -> list[Skill]:
    out = []
    for r, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "node_modules"]
        if "SKILL.md" in files:
            s = parse_skill(os.path.join(r, "SKILL.md"))
            if s:
                out.append(s)
    return out


def _tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())


class Catalog:
    def __init__(self, skills: list[Skill] | None = None):
        self.skills = {}
        for s in skills or []:
            if s.name in self.skills:  # never let a second skill silently shadow the first
                s.risks = sorted({*s.risks, "name_collision"})
                s.name = f"{s.name}@{os.path.basename(s.path) or s.path}"
            self.skills[s.name] = s

    @classmethod
    def load(cls, path):
        with open(path, encoding="utf-8-sig") as fh:
            return cls([Skill(**d) for d in json.load(fh)])

    @classmethod
    def seed(cls):
        """The bundled starter catalog, so search and compare work before anyone runs `index`."""
        from .seed import SEED

        return cls([Skill(**d) for d in SEED])

    def save(self, path):
        with open(path, "w", encoding="utf-8") as fh:
            json.dump([asdict(s) for s in self.skills.values()], fh, indent=2)

    def rate(self, name, user, stars, text=""):
        if not 1 <= stars <= 5:
            raise ValueError("stars must be 1-5")
        skill = self.skills[name]
        user = " ".join(str(user).split()).casefold()
        if skill.author and user == " ".join(skill.author.split()).casefold():
            raise ValueError("authors cannot rate their own skill")
        skill.ratings[user] = {"stars": stars, "text": text}

    def avg_rating(self, s: Skill, prior=3.5, weight=3) -> float:
        stars = [r["stars"] for r in s.ratings.values()]
        return (prior * weight + sum(stars)) / (weight + len(stars))

    def search(self, query: str, top=10) -> list[tuple[str, float]]:
        q = _tokens(query)
        docs = {
            n: _tokens(f"{s.name} {s.name} {s.description} {s.description} {' '.join(s.tags)} {s.body}")
            for n, s in self.skills.items()
        }
        N = len(docs) or 1
        avgdl = sum(len(d) for d in docs.values()) / N if docs else 1
        df = Counter(t for d in docs.values() for t in set(d))
        results = []
        for n, d in docs.items():
            tf = Counter(d)
            bm25 = 0.0
            for t in q:
                if t not in tf:
                    continue
                idf = math.log(1 + (N - df[t] + 0.5) / (df[t] + 0.5))
                bm25 += idf * tf[t] * 2.2 / (tf[t] + 1.2 * (0.25 + 0.75 * len(d) / avgdl))
            if bm25 <= 0:
                continue
            s = self.skills[n]
            score = bm25 * (0.6 + 0.4 * s.quality / 100) * (0.7 + 0.3 * self.avg_rating(s) / 5)
            if s.risks:  # a safe skill outranks a risky one of similar relevance
                score *= 0.5
            results.append((n, round(score, 4)))
        return sorted(results, key=lambda x: -x[1])[:top]

    def compare(self, names: list[str]) -> list[dict]:
        rows = []
        for n in names:
            s = self.skills[n]
            rows.append(
                {
                    "name": n,
                    "quality": s.quality,
                    "rating": round(self.avg_rating(s), 2),
                    "reviews": len(s.ratings),
                    "scripts": s.has_scripts,
                    "references": s.has_references,
                    "version": s.version or "-",
                    "tags": ", ".join(s.tags) or "-",
                    "risks": ", ".join(s.risks) or "none found",
                }
            )
        return rows
