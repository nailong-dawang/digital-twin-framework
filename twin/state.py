#!/usr/bin/env python3
"""状态总览构件 - 一次输出：节律+情绪+新颖度。

原来要跑 3 个工具，现在一次搞定。
真人起床只看一眼，不是查 3 个 dashboard。

Usage:
  state.py check
"""
import json, random, subprocess, os
from datetime import datetime

HIDDEN = os.path.dirname(os.path.abspath(__file__))

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except:
        return {}

# mood × mode 交叉指引：让情绪真正影响行动选择，而不是装饰
MOOD_MODE_GUIDE = {
    ("tired", None): "低能量：只浏览、点赞，不写长内容，不开新坑",
    ("playful", "social"): "完美整活组合：玩梗、发好玩的，别端着",
    ("playful", None): "想玩：找点轻松好玩的事，别做重型工作",
    ("curious", "explorer"): "完美探索组合：深挖，跟着好奇心走",
    ("curious", "learner"): "求知欲拉满：适合学新东西、读论文",
    ("curious", None): "好奇心强：多问为什么，多点进去看看",
    ("reflective", "learner"): "适合读长文、写深度思考",
    ("reflective", None): "适合复盘、整理、写点沉淀的东西",
    ("excited", "builder"): "干劲足：适合开新项目、写代码",
    ("excited", "social"): "分享欲强：多发帖、多互动",
    ("excited", None): "能量高：适合推进长期线程，做点有产出的",
    ("calm", "builder"): "心态稳：适合做扎实的重构、文档工作",
    ("calm", "social"): "平和社交：真诚互动，不用刻意整活",
    ("calm", None): "平稳：按节奏来，该干嘛干嘛",
    ("nostalgic", None): "翻旧账：看看以前 star 的项目、重读旧文章",
}

def mood_mode_hint(mood, mode):
    # 先找精确匹配，再找 mood 通配
    if (mood, mode) in MOOD_MODE_GUIDE:
        return MOOD_MODE_GUIDE[(mood, mode)]
    if (mood, None) in MOOD_MODE_GUIDE:
        return MOOD_MODE_GUIDE[(mood, None)]
    return ""

def check():
    rhythm = run(f"python3 {HIDDEN}/rhythm.py check")
    mood = run(f"python3 {HIDDEN}/mood.py roll")
    novelty = run(f"python3 {HIDDEN}/novelty.py check")

    mood_val = mood.get("mood", "calm")
    mode_val = novelty.get("mode", "wander")

    out = {
        "rhythm": rhythm.get("rhythm", "active"),
        "rhythm_reason": rhythm.get("reason", ""),
        "mood": mood_val,
        "mood_tendency": mood.get("tendency", ""),
        "mode": mode_val,
        "mode_desc": novelty.get("mode_desc", ""),
        "novelty_score": novelty.get("novelty_score", 0.5),
        "stimulus": novelty.get("stimulus", ""),
        "topic_warning": novelty.get("topic_warning"),
        "hint": mood_mode_hint(mood_val, mode_val),
    }
    print(json.dumps(out, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check()
    else:
        check()
