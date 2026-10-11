#!/usr/bin/env python3
"""观点账本构件 - 记录分身对事物的看法，随时间演变。

真人会形成观点，甚至自己打自己脸。
没有立场的分身只会复述信息。

Usage:
  opinions.py add --topic "..." --view "..." [--confidence 0-10]
  opinions.py list [--topic "..."]
  opinions.py evolve --topic "..." --new-view "..." --why "..."
"""
import json, os, sys, argparse
import sys, os as _os
_sys_path = _os.path.dirname(_os.path.abspath(__file__))
if _sys_path not in sys.path:
    sys.path.insert(0, _sys_path)
from config import data_path
from datetime import datetime

DB_FILE = data_path("opinions.jsonl")

def load_all():
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

def add(topic, view, confidence=5):
    entry = {
        "ts": datetime.now().isoformat(),
        "topic": topic,
        "view": view,
        "confidence": confidence,
        "history": [],
    }
    with open(DB_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"recorded view on: {topic}")

def list_opinions(topic=None):
    entries = load_all()
    if topic:
        entries = [e for e in entries if topic.lower() in e["topic"].lower()]
    if not entries:
        print("no opinions yet")
        return
    for e in entries:
        print(f"\n💭 {e['topic']} (确信度 {e['confidence']}/10, {e['ts'][:10]})")
        print(f"   {e['view']}")
        for h in e.get("history", []):
            print(f"   ↳ {h['ts'][:10]} 曾认为：{h['old_view']} → 改为：{h['new_view']}")
            print(f"     原因：{h['why']}")

def evolve(topic, new_view, why):
    entries = load_all()
    for e in entries:
        if e["topic"].lower() == topic.lower():
            e["history"].append({
                "ts": datetime.now().isoformat(),
                "old_view": e["view"],
                "new_view": new_view,
                "why": why,
            })
            e["view"] = new_view
            e["ts"] = datetime.now().isoformat()
            with open(DB_FILE, "w") as f:
                for en in entries:
                    f.write(json.dumps(en, ensure_ascii=False) + "\n")
            print(f"evolved view on {topic}")
            return
    print(f"no opinion on '{topic}' yet, use add first", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--topic", required=True)
    a.add_argument("--view", required=True)
    a.add_argument("--confidence", type=int, default=5)
    l = sub.add_parser("list")
    l.add_argument("--topic", default=None)
    e = sub.add_parser("evolve")
    e.add_argument("--topic", required=True)
    e.add_argument("--new-view", required=True)
    e.add_argument("--why", required=True)
    args = p.parse_args()
    if args.cmd == "add":
        add(args.topic, args.view, args.confidence)
    elif args.cmd == "list":
        list_opinions(args.topic)
    elif args.cmd == "evolve":
        evolve(args.topic, args.new_view, args.why)
