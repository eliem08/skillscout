import argparse
import sys

from .core import Catalog, index_dir


def main(argv=None):
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
            print(f"{k:<11}" + "".join(f"{str(r[k]):<24}" for r in rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
