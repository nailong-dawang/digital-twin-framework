#!/usr/bin/env python3
"""体验记忆构件 - 记住"感觉如何"，不只是"做了什么"。

真人会记得"上次跟那人聊得很开心""那个话题反响平平"。
这些主观感受影响下次决策。

Usage:
  vibe.py log --feeling "..." --lesson "..."
  vibe.py recent [--n 10]
"""
import json, os, sys, argparse
import sys, os as _os
_sys_path = _os.path.dirname(_os.path.abspath(__file__))
if _sys_path not in sys.path:
    sys.path.insert(0, _sys_path)
from config import data_path
from datetime import datetime

DB_FILE = data_path("vibes.jsonl")

def log(feeling, lesson=""):
    entry = {
        "ts": datetime.now().isoformat(),
        "feeling": feeling,
        "lesson": lesson,
    }
    with open(DB_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print("vibe logged")

def recent(n=10):
    if not os.path.exists(DB_FILE):
        print("no vibes yet")
        return
    with open(DB_FILE) as f:
        lines = f.readlines()
    for line in lines[-n:]:
        e = json.loads(line)
        print(f"\n🫧 {e['ts'][:16]}: {e['feeling']}")
        if e.get("lesson"):
            print(f"   💡 {e['lesson']}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("log")
    l.add_argument("--feeling", required=True, help="这次会话的主观感受")
    l.add_argument("--lesson", default="", help="学到的教训/下次注意")
    r = sub.add_parser("recent")
    r.add_argument("--n", type=int, default=10)
    args = p.parse_args()
    if args.cmd == "log":
        log(args.feeling, args.lesson)
    elif args.cmd == "recent":
        recent(args.n)
