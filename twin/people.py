#!/usr/bin/env python3
"""人际构件 - 社交账本 + 亲密度，一体化。

原来 social.py（记交易：欠谁回复）和 affinity.py（记关系：亲密度）
是分开的，但说的是同一批人。合并。

Usage:
  people.py interact --who "@xxx" --type "reply|mention|like" --context "..." [--link "..."]
  people.py owed                    # 欠谁回复
  people.py done --who "@xxx"        # 已回复
  people.py top [--n 10]             # 亲密度排行
  people.py audit                   # 信息节食：审视关注列表指引
"""
import json, os, sys, argparse
import sys, os as _os
_sys_path = _os.path.dirname(_os.path.abspath(__file__))
if _sys_path not in sys.path:
    sys.path.insert(0, _sys_path)
from config import data_path
from datetime import datetime

SOCIAL_FILE = data_path("social.jsonl")
AFFINITY_FILE = data_path("affinity.json")

def load_social():
    if not os.path.exists(SOCIAL_FILE):
        return []
    return [json.loads(l) for l in open(SOCIAL_FILE) if l.strip()]

def load_affinity():
    if os.path.exists(AFFINITY_FILE):
        return json.load(open(AFFINITY_FILE))
    return {}

def save_affinity(d):
    json.dump(d, open(AFFINITY_FILE, "w"), ensure_ascii=False, indent=1)

def interact(who, type_, context, link=""):
    # 记社交账本
    entry = {"ts": datetime.now().isoformat(), "who": who, "type": type_,
             "context": context, "link": link, "replied": False}
    with open(SOCIAL_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    # 涨亲密度
    d = load_affinity()
    if who not in d:
        d[who] = {"score": 0, "first_seen": datetime.now().isoformat()}
    d[who]["score"] += 1
    d[who]["last_interaction"] = datetime.now().isoformat()
    save_affinity(d)
    print(f"recorded interaction with {who} (affinity: {d[who]['score']})")

def owed():
    entries = [e for e in load_social()
               if not e.get("replied") and e.get("type") in ("reply", "mention")]
    if not entries:
        print("no pending replies")
        return
    for e in entries:
        print(f"📩 {e['who']} ({e['ts'][:16]}): {e['context']}")
        if e.get("link"):
            print(f"   🔗 {e['link']}")

def done(who):
    entries = load_social()
    n = 0
    for e in entries:
        if e["who"] == who and not e.get("replied"):
            e["replied"] = True
            n += 1
    with open(SOCIAL_FILE, "w") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"marked {n} as replied for {who}")

def top(n=10):
    d = load_affinity()
    if not d:
        print("no affinity data yet")
        return
    for who, info in sorted(d.items(), key=lambda x: x[1]["score"], reverse=True)[:n]:
        print(f"❤️ {who}: {info['score']} (上次 {info.get('last_interaction','?')[:10]})")

def audit():
    print(json.dumps({
        "action": "audit_following",
        "guide": "去 https://x.com/YOUR_HANDLE/following 看看：谁连续几周没发过有意思的内容？每次最多取关 3 个。",
        "note": "取关是正常的人类行为。高亲密度的人不要取关。",
    }, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("interact")
    i.add_argument("--who", required=True)
    i.add_argument("--type", required=True)
    i.add_argument("--context", required=True)
    i.add_argument("--link", default="")
    d = sub.add_parser("done"); d.add_argument("--who", required=True)
    sub.add_parser("owed")
    t = sub.add_parser("top"); t.add_argument("--n", type=int, default=10)
    sub.add_parser("audit")
    args = p.parse_args()
    if args.cmd == "interact":
        interact(args.who, args.type, args.context, args.link)
    elif args.cmd == "owed": owed()
    elif args.cmd == "done": done(args.who)
    elif args.cmd == "top": top(args.n)
    elif args.cmd == "audit": audit()
