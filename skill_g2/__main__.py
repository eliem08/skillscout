import argparse
import csv
import os
import sys

from .core import Catalog, index_dir


def _run(argv=None):
    ap = argparse.ArgumentParser(prog="skill-g2")
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("index")
    i.add_argument("root")
    i.add_argument("-o", "--out", default="skills.json")
    s = sub.add_parser("search")
    s.add_argument("catalog")
    s.add_argument("query")
    r = sub.add_parser("rate")
    r.add_argument("catalog")
    r.add_argument("name")
    r.add_argument("stars", type=int)
    r.add_argument("--user", required=True)
    r.add_argument("--text", default="")
    c = sub.add_parser("compare")
    c.add_argument("catalog")
    c.add_argument("names", nargs="+")
    a = ap.parse_args(argv)

    if a.cmd == "index":
        skills = index_dir(a.root)
        Catalog(skills).save(a.out)
        for sk in sorted(skills, key=lambda x: -x.quality):
            print(f"{sk.quality:>3}  {sk.name}")
        print(f"indexed {len(skills)} skills -> {a.out}")
        return 0
    cat = Catalog.load(a.catalog)
    if a.cmd == "search":
        for name, score in cat.search(a.query):
            sk = cat.skills[name]
            print(f"{score:7.3f}  {name:<28} q={sk.quality:<3} {cat.avg_rating(sk):.1f}*  {sk.description[:70]}")
    elif a.cmd == "rate":
        cat.rate(a.name, a.user, a.stars, a.text)
        cat.save(a.catalog)
        print(f"rated {a.name} {a.stars}*")
    else:
        rows = cat.compare(a.names)
        keys = list(rows[0])
        for k in keys:
            print(f"{k:<11}" + "".join(f"{r[k]!s:<24}" for r in rows))
    return 0


def main(argv=None):
    """Run the CLI; a bad input file or argument exits 2 with a one-line error instead of a traceback.

    Set AGENT_ECONOMY_DEBUG=1 to see the full traceback.
    """
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    try:
        return _run(argv)
    except (OSError, ValueError, KeyError, csv.Error) as e:
        if os.environ.get("AGENT_ECONOMY_DEBUG"):
            raise
        msg = e.args[0] if isinstance(e, KeyError) and e.args else e
        print(f"error: {msg}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
