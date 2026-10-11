import sys, os as _os
_sys_path = _os.path.dirname(_os.path.abspath(__file__))
if _sys_path not in sys.path:
    sys.path.insert(0, _sys_path)
from config import data_path
#!/usr/bin/env python3
"""数字分身心跳日志构件 - 结构化记录每次心跳。

Usage:
  heartbeat-log.py log --perception "..." --decision "..." --actions '[{"type": "...", "detail": "...", "link": "..."}]' [--ideas '["..."]'] [--cost 0.0]
  heartbeat-log.py recent [--n 10]     # 最近 N 条
  heartbeat-log.py stats               # 统计
"""
import json, sys, os, argparse
from datetime import datetime

LOG_FILE = data_path("heartbeat.jsonl")
MD_FILE = data_path("heartbeat-log.md")

def log_entry(perception, decision, actions, ideas=None, cost=0.0):
    entry = {
        "ts": datetime.now().isoformat(),
        "perception": perception,
        "decision": decision,
        "actions": actions or [],
        "ideas": ideas or [],
        "cost_usd": cost,
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    # 同时追加 markdown 人读版
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    md = f"\n## {ts}\n- 感知：{perception}\n- 决策：{decision}\n"
    for a in (actions or []):
        md += f"- 行动 [{a.get('type')}]: {a.get('detail')}"
        if a.get("link"):
            md += f" ({a['link']})"
        md += "\n"
    if cost:
        md += f"- 花费：${cost}\n"
    with open(MD_FILE, "a") as f:
        f.write(md)
    print(f"logged {entry['ts']}")

def recent(n=10):
    if not os.path.exists(LOG_FILE):
        print("no logs yet")
        return
    with open(LOG_FILE) as f:
        lines = f.readlines()
    for line in lines[-n:]:
        e = json.loads(line)
        n_act = len(e.get("actions", []))
        print(f"{e['ts'][:16]} | 行动{n_act}个 | {e['decision'][:60]}")

def stats():
    if not os.path.exists(LOG_FILE):
        print("no logs yet")
        return
    total = 0
    actions = 0
    cost = 0.0
    with open(LOG_FILE) as f:
        for line in f:
            e = json.loads(line)
            total += 1
            actions += len(e.get("actions", []))
            cost += e.get("cost_usd", 0)
    print(f"心跳 {total} 次 | 行动 {actions} 个 | 总花费 ${cost:.4f}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("log")
    l.add_argument("--perception", required=True)
    l.add_argument("--decision", required=True)
    l.add_argument("--actions", default="[]")
    l.add_argument("--ideas", default="[]")
    l.add_argument("--cost", type=float, default=0.0)
    r = sub.add_parser("recent")
    r.add_argument("--n", type=int, default=10)
    sub.add_parser("stats")
    a = p.parse_args()
    if a.cmd == "log":
        log_entry(a.perception, a.decision, json.loads(a.actions), json.loads(a.ideas), a.cost)
    elif a.cmd == "recent":
        recent(a.n)
    elif a.cmd == "stats":
        stats()
