import sys, os as _os
_sys_path = _os.path.dirname(_os.path.abspath(__file__))
if _sys_path not in sys.path:
    sys.path.insert(0, _sys_path)
from config import data_path
#!/usr/bin/env python3
"""作息节律构件 - 模拟人类的脉冲式活跃模式。

真人不是每 30 分钟准时上线，而是：活跃期高频 + 静默期完全消失。
根据当前时间决定本次心跳是活跃还是静默。

Usage:
  rhythm.py check    # 输出 active/silent 及原因
"""
import json, os, sys, random
from datetime import datetime

STATE_FILE = data_path("rhythm-state.json")

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"phase": "active", "phase_start": datetime.now().isoformat(), "phase_len_h": 3}

def save_state(s):
    with open(STATE_FILE, "w") as f:
        json.dump(s, f, ensure_ascii=False, indent=1)

def check():
    now = datetime.now()
    hour = now.hour
    state = load_state()
    phase_start = datetime.fromisoformat(state["phase_start"])
    elapsed_h = (now - phase_start).total_seconds() / 3600

    # 深夜 (1-6点)：大概率静默，人类在睡觉
    # 早高峰 (7-9点)：活跃，起床刷手机
    # 上午 (9-12点)：中等
    # 午休 (12-14点)：活跃，吃饭刷手机
    # 下午 (14-18点)：中等偏低，工作时间
    # 晚上 (18-23点)：活跃，黄金时间
    # 凌晨 (0-1点)：低，夜猫子
    hour_weights = {
        0: 0.2, 1: 0.1, 2: 0.05, 3: 0.05, 4: 0.05, 5: 0.05, 6: 0.1,
        7: 0.8, 8: 0.9, 9: 0.6, 10: 0.5, 11: 0.5,
        12: 0.8, 13: 0.8, 14: 0.4, 15: 0.4, 16: 0.4, 17: 0.5,
        18: 0.8, 19: 0.9, 20: 0.9, 21: 0.9, 22: 0.7, 23: 0.4,
    }
    base_prob = hour_weights.get(hour, 0.5)

    # 阶段逻辑：活跃期 2-4 小时 → 静默期 1-3 小时 → 循环
    if elapsed_h >= state["phase_len_h"]:
        # 切换阶段
        if state["phase"] == "active":
            state["phase"] = "silent"
            state["phase_len_h"] = random.uniform(1, 3)
        else:
            state["phase"] = "active"
            state["phase_len_h"] = random.uniform(2, 4)
        state["phase_start"] = now.isoformat()
        save_state(state)
        elapsed_h = 0

    if state["phase"] == "silent":
        # 静默期：小概率偷看一眼（人类也会忍不住看手机）
        if random.random() < 0.15:
            print(json.dumps({
                "rhythm": "active",
                "reason": f"静默期中忍不住看了一眼（{hour}点）",
                "phase": state["phase"],
            }, ensure_ascii=False))
        else:
            print(json.dumps({
                "rhythm": "silent",
                "reason": f"静默期（{hour}点，人类在忙别的）",
                "phase": state["phase"],
            }, ensure_ascii=False))
        return

    # 活跃期：按小时权重决定
    if random.random() < base_prob:
        print(json.dumps({
            "rhythm": "active",
            "reason": f"活跃期，{hour}点是高频时段",
            "phase": state["phase"],
        }, ensure_ascii=False))
    else:
        print(json.dumps({
            "rhythm": "silent",
            "reason": f"活跃期内随机跳过（模拟人类分心）",
            "phase": state["phase"],
        }, ensure_ascii=False))

if __name__ == "__main__":
    check()
