#!/usr/bin/env python3
"""长期线程构件 - 跨心跳、跨天的连续性项目。

真人做事是跨天的：一个工具写三天，一个话题追一周。
分身不能每次会话都是独立的。

Usage:
  threads.py create --title "..." --desc "..."     # 新建线程
  threads.py list                                   # 列出活跃线程
  threads.py update --id <id> --note "..."          # 推进线程
  threads.py close --id <id> --result "..."         # 完结线程
  threads.py active                                  # 输出当前最该推进的线程（给心跳用）
"""
import json, os, sys, argparse
import sys, os as _os
_sys_path = _os.path.dirname(_os.path.abspath(__file__))
if _sys_path not in sys.path:
    sys.path.insert(0, _sys_path)
from config import data_path
from datetime import datetime

DB_FILE = data_path("threads.jsonl")

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

def save_all(entries):
    with open(DB_FILE, "w") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

def create(title, desc):
    tid = f"th-{datetime.now().strftime('%m%d')}-{len(load_all())+1:02d}"
    entry = {
        "id": tid,
        "title": title,
        "desc": desc,
        "status": "active",
        "created": datetime.now().isoformat(),
        "updates": [],
    }
    with open(DB_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"created thread {tid}: {title}")

def list_active():
    entries = [e for e in load_all() if e.get("status") == "active"]
    if not entries:
        print("no active threads")
        return
    for e in entries:
        n = len(e.get("updates", []))
        print(f"🧵 {e['id']}: {e['title']} ({n} 次推进, 创建于 {e['created'][:10]})")
        print(f"   {e['desc'][:80]}")

def update(tid, note):
    entries = load_all()
    for e in entries:
        if e["id"] == tid:
            e["updates"].append({"ts": datetime.now().isoformat(), "note": note})
            save_all(entries)
            print(f"updated {tid}")
            return
    print(f"thread {tid} not found", file=sys.stderr)
    sys.exit(1)

def close(tid, result):
    entries = load_all()
    for e in entries:
        if e["id"] == tid:
            e["status"] = "done"
            e["result"] = result
            e["closed"] = datetime.now().isoformat()
            save_all(entries)
            print(f"closed {tid}: {result}")
            return
    print(f"thread {tid} not found", file=sys.stderr)
    sys.exit(1)

def suggest():
    """给心跳用：输出最该推进的线程"""
    entries = [e for e in load_all() if e.get("status") == "active"]
    if not entries:
        print(json.dumps({"has_thread": False}, ensure_ascii=False))
        return
    # 选更新最少的（最需要推进的）
    e = sorted(entries, key=lambda x: len(x.get("updates", [])))[0]
    print(json.dumps({
        "has_thread": True,
        "id": e["id"],
        "title": e["title"],
        "desc": e["desc"],
        "updates": e.get("updates", [])[-3:],
    }, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("create")
    c.add_argument("--title", required=True)
    c.add_argument("--desc", required=True)
    sub.add_parser("list")
    u = sub.add_parser("update")
    u.add_argument("--id", required=True)
    u.add_argument("--note", required=True)
    cl = sub.add_parser("close")
    cl.add_argument("--id", required=True)
    cl.add_argument("--result", required=True)
    sub.add_parser("active")
    args = p.parse_args()
    if args.cmd == "create":
        create(args.title, args.desc)
    elif args.cmd == "list":
        list_active()
    elif args.cmd == "update":
        update(args.id, args.note)
    elif args.cmd == "close":
        close(args.id, args.result)
    elif args.cmd == "active":
        suggest()
