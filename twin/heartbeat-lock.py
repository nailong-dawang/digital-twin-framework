import sys, os as _os
_sys_path = _os.path.dirname(_os.path.abspath(__file__))
if _sys_path not in sys.path:
    sys.path.insert(0, _sys_path)
from config import data_path
#!/usr/bin/env python3
"""心跳锁构件 - 防止 overlapping 的心跳互相阻塞。

Usage:
  heartbeat-lock.py acquire   # 尝试获取锁，成功返回 0，失败返回 1
  heartbeat-lock.py release   # 释放锁
  heartbeat-lock.py status    # 查看锁状态

锁超时 50 分钟：超过此时长视为上次已死，强制接管。
"""
import os, sys, time, json

LOCK_FILE = data_path("heartbeat.lock")
TIMEOUT_SECS = 50 * 60  # 50 分钟

def acquire():
    now = time.time()
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE) as f:
                data = json.load(f)
            age = now - data.get("started_at", 0)
            if age < TIMEOUT_SECS:
                print(f"locked by run started {age/60:.1f} min ago, skipping", file=sys.stderr)
                return 1
            else:
                print(f"stale lock ({age/60:.1f} min old), taking over", file=sys.stderr)
        except (json.JSONDecodeError, KeyError):
            print("corrupt lock file, taking over", file=sys.stderr)
    with open(LOCK_FILE, "w") as f:
        json.dump({"started_at": now, "pid": os.getpid()}, f)
    print("lock acquired")
    return 0

def release():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
        print("lock released")
    else:
        print("no lock to release")

def status():
    if not os.path.exists(LOCK_FILE):
        print("unlocked")
        return
    with open(LOCK_FILE) as f:
        data = json.load(f)
    age = time.time() - data.get("started_at", 0)
    print(f"locked, age {age/60:.1f} min, stale={age >= TIMEOUT_SECS}")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "acquire":
        sys.exit(acquire())
    elif cmd == "release":
        release()
    elif cmd == "status":
        status()
    else:
        print(f"unknown: {cmd}", file=sys.stderr)
        sys.exit(1)
