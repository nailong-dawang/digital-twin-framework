#!/usr/bin/env python3
"""状态骰构件 - 模拟人类的情绪波动。

真人有情绪：兴奋、平静、好奇、疲惫……影响语气和选题。
不是演戏，是让输出有自然波动。

Usage:
  mood.py roll    # 掷一次，输出本次状态
"""
import json, random
from datetime import datetime

# (状态, 权重, 行为倾向)
MOODS = [
    ("excited",   15, "看到什么都想分享，语气上扬，多发帖"),
    ("curious",   25, "求知欲强，适合探索和学习模式，深挖"),
    ("calm",      20, "平静，适合整理、写文档、做扎实的工作"),
    ("playful",   10, "想整活，可以发点没营养但好玩的，玩梗"),
    ("reflective",15, "适合复盘、写长思考、整理观点"),
    ("tired",     10, "低能量，只浏览点赞，不发长内容，早点休息"),
    ("nostalgic",  5, "翻旧东西：看看以前 star 的项目、重读旧文章"),
]

def roll():
    hour = datetime.now().hour
    # 深夜加权：更容易 reflective/tired
    weights = [w for _, w, _ in MOODS]
    if 0 <= hour < 6:
        weights = [5, 10, 10, 2, 30, 35, 8]
    elif 6 <= hour < 9:
        weights = [20, 30, 15, 10, 10, 5, 10]
    # 周末加权：更容易 playful
    if datetime.now().weekday() >= 5:
        weights[3] += 10  # playful

    mood, _, tendency = random.choices(MOODS, weights=weights, k=1)[0]
    print(json.dumps({
        "mood": mood,
        "tendency": tendency,
        "hour": hour,
    }, ensure_ascii=False))

if __name__ == "__main__":
    roll()
