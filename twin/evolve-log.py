#!/usr/bin/env python3
"""进化日志构件 - 记录自进化系统的每一次改动。

真自进化：改之前不问，改之后记下来，随时可回滚。

Usage:
  evolve-log.py record --area "工具/指令/参数" --change "..." --reason "..." --before "..." --after "..."
  evolve-log.py recent [--n 10]
  evolve-log.py revert-check     # 列出可回滚的改动
"""
import json, os, sys, argparse
import sys, os as _os
_sys_path = _os.path.dirname(_os.path.abspath(__file__))
if _sys_path not in sys.path:
    sys.path.insert(0, _sys_path)
from config import data_path
from datetime import datetime

LOG_FILE = data_path("evolution-log.jsonl")

# 红线：进化系统绝不能碰的（硬编码，不是 prompt 约束）
RED_LINES = [
    "身份定位：全栈开发者、AI 博主",
    "硬边界：大额支付走审批",
    "硬边界：不做违法的事",
    "不能删除历史数据",
    "不能关闭心跳锁机制",
]

def record(area, change, reason, before="", after=""):
    # 红线检查
    for red in RED_LINES:
        if any(kw in change.lower() for kw in ["身份", "支付", "违法", "删除历史", "关闭锁"]):
            print(f"🛑 红线拦截：改动涉及 '{change}'，拒绝执行", file=sys.stderr)
            sys.exit(1)
    entry = {
        "ts": datetime.now().isoformat(),
        "area": area,
        "change": change,
        "reason": reason,
        "before": before,
        "after": after,
        "reverted": False,
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"evolution recorded: [{area}] {change}")

def recent(n=10):
    if not os.path.exists(LOG_FILE):
        print("no evolutions yet")
        return
    with open(LOG_FILE) as f:
        lines = f.readlines()
    for line in lines[-n:]:
        e = json.loads(line)
        status = "↩️已回滚" if e.get("reverted") else "✅"
        print(f"{status} {e['ts'][:16]} [{e['area']}] {e['change']}")
        print(f"   原因：{e['reason']}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("record")
    r.add_argument("--area", required=True)
    r.add_argument("--change", required=True)
    r.add_argument("--reason", required=True)
    r.add_argument("--before", default="")
    r.add_argument("--after", default="")
    s = sub.add_parser("recent")
    s.add_argument("--n", type=int, default=10)
    args = p.parse_args()
    if args.cmd == "record":
        record(args.area, args.change, args.reason, args.before, args.after)
    elif args.cmd == "recent":
        recent(args.n)
