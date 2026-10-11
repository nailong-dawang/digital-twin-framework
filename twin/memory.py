#!/usr/bin/env python3
"""记忆构件 - 发现库 + 话题偏好，一体化。

原来 discoveries.py 和 topics.py 是分开的，
但 topics 本质上就是 discoveries 的 tags 聚合。合并。

Usage:
  memory.py add --title "..." --summary "..." --why "..." --links '[]' --tags '[]' [--details "..."]
  memory.py search "关键词"
  memory.py recent [--n 5]
  memory.py prefs          # 话题偏好
  memory.py stats
"""
import json, os, sys, argparse
import sys, os as _os
_sys_path = _os.path.dirname(_os.path.abspath(__file__))
if _sys_path not in sys.path:
    sys.path.insert(0, _sys_path)
from config import data_path
from datetime import datetime, timedelta
from collections import defaultdict

DB_FILE = data_path("discoveries.jsonl")
PREF_FILE = data_path("topic-prefs.json")
IDEAS_FILE = data_path("ideas.md")

# 不应作为话题 tag 的词（模式名、无意义词）
TAG_BLOCKLIST = {"builder", "learner", "explorer", "social", "wander",
                 "test", "测试", "misc", "其他", "todo"}

def clean_tags(tags):
    """过滤掉不应作为话题的 tag"""
    return [t for t in tags if t.lower() not in TAG_BLOCKLIST and len(t.strip()) > 0]

# 不自然的瞬移（身份是重心，不是笼子）
INCOHERENT_JUMPS = ["美食博主", "情感博主", "星座占卜", "饭圈", "微商"]

def load_discoveries():
    if not os.path.exists(DB_FILE):
        return []
    entries = []
    with open(DB_FILE) as f:
        for line in f:
            try:
                entries.append(json.loads(line))
            except:
                pass
    return entries

def load_prefs():
    if os.path.exists(PREF_FILE):
        with open(PREF_FILE) as f:
            return json.load(f)
    return {"topics": {}}

def save_prefs(d):
    with open(PREF_FILE, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)

def add(title, summary, why, links=None, tags=None, details=""):
    tags = clean_tags(tags or [])
    entry = {
        "ts": datetime.now().isoformat(),
        "title": title, "summary": summary,
        "why_interesting": why,
        "links": links or [], "tags": tags or [],
        "details": details,
    }
    with open(DB_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    # 自动更新话题偏好
    if tags:
        d = load_prefs()
        now = datetime.now().isoformat()
        for t in tags:
            if t not in d["topics"]:
                d["topics"][t] = {"score": 0, "last_seen": now, "count": 0}
            last = datetime.fromisoformat(d["topics"][t]["last_seen"])
            if datetime.now() - last > timedelta(days=30):
                d["topics"][t]["score"] *= 0.5
            d["topics"][t]["score"] += 1
            d["topics"][t]["count"] += 1
            d["topics"][t]["last_seen"] = now
        save_prefs(d)
    print(f"added: {title}")

def search(query):
    entries = load_discoveries()
    q = query.lower()
    hits = [e for e in entries if q in " ".join([
        e.get("title",""), e.get("summary",""), e.get("why_interesting",""),
        e.get("details",""), " ".join(e.get("tags",[]))]).lower()]
    if not hits:
        print(f"no hits for: {query}")
        return
    for e in hits:
        print(f"\n📌 {e['title']} ({e['ts'][:10]})")
        print(f"   {e['summary']}")
        if e.get("links"):
            for l in e["links"]:
                print(f"   🔗 {l}")

def recent(n=5):
    entries = load_discoveries()
    if not entries:
        print("no discoveries yet")
        return
    for e in entries[-n:]:
        print(f"{e['ts'][:16]} | {e['title']}")

def prefs():
    d = load_prefs()
    scores = {t: info["score"] for t, info in d["topics"].items()}
    if not scores:
        print(json.dumps({"prefs": [], "note": "还没有偏好数据"}, ensure_ascii=False))
        return
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top = [t for t, _ in ranked[:5]]
    incoherent = [t for t in top if any(b in t for b in INCOHERENT_JUMPS)]
    print(json.dumps({
        "prefs": [{"topic": t, "score": round(s,1)} for t, s in ranked[:10]],
        "incoherent_warning": incoherent or None,
        "note": "偏好决定深度（高偏好→深入），新颖度保证广度",
    }, ensure_ascii=False, indent=1))

def stats():
    entries = load_discoveries()
    d = load_prefs()
    print(f"发现 {len(entries)} 条，话题 {len(d['topics'])} 个")

def ideas_pending():
    """列出未完成的想法"""
    if not os.path.exists(IDEAS_FILE):
        print("no ideas yet")
        return
    with open(IDEAS_FILE) as f:
        for line in f:
            if line.strip().startswith("- [ ]"):
                print(line.strip())

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--title", required=True)
    a.add_argument("--summary", required=True)
    a.add_argument("--why", required=True)
    a.add_argument("--links", default="[]")
    a.add_argument("--tags", default="[]")
    a.add_argument("--details", default="")
    s = sub.add_parser("search"); s.add_argument("query")
    r = sub.add_parser("recent"); r.add_argument("--n", type=int, default=5)
    sub.add_parser("prefs"); sub.add_parser("stats")
    sub.add_parser("ideas")
    args = p.parse_args()
    if args.cmd == "add":
        add(args.title, args.summary, args.why, json.loads(args.links), json.loads(args.tags), args.details)
    elif args.cmd == "search": search(args.query)
    elif args.cmd == "recent": recent(args.n)
    elif args.cmd == "prefs": prefs()
    elif args.cmd == "stats": stats()
    elif args.cmd == "ideas": ideas_pending()
