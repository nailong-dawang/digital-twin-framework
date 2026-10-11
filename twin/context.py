#!/usr/bin/env python3
"""语境判断构件 - 回复前先看场合，像真人一样。

真人回帖是无意识匹配的：中文帖中文回，英文帖英文回，
技术帖认真，玩梗帖就接梗。从不用"Great point!"这种机器人话术。

Usage:
  context.py analyze --text "帖子内容" [--author "@xxx"]
"""
import json, sys, argparse, re

def detect_language(text):
    # 简单启发式：中文字符占比
    zh_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    en_chars = len(re.findall(r'[a-zA-Z]', text))
    total = zh_chars + en_chars
    if total == 0:
        return "unknown"
    zh_ratio = zh_chars / total
    if zh_ratio > 0.5:
        return "zh"
    elif zh_ratio < 0.2:
        return "en"
    else:
        return "mixed"

def detect_tone(text):
    t = text.lower()
    # 玩梗/轻松信号
    playful_signals = ["哈哈", "lol", "lmao", "😂", "🤣", "玩笑", "梗", "meme", "shitpost"]
    # 技术深度信号
    tech_signals = ["原理", "实现", "架构", "论文", "paper", "benchmark", "源码", "算法"]
    # 求助信号
    help_signals = ["求问", "请教", "怎么", "如何", "help", "question", "？", "?"]
    scores = {
        "playful": sum(1 for s in playful_signals if s in t),
        "technical": sum(1 for s in tech_signals if s in t),
        "question": sum(1 for s in help_signals if s in t),
    }
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "casual"

def analyze(text, author=""):
    lang = detect_language(text)
    tone = detect_tone(text)
    guide = {
        "language": lang,
        "tone": tone,
        "reply_language": {"zh": "中文", "en": "英文", "mixed": "跟帖子主语言走", "unknown": "中文（默认）"}[lang],
        "reply_tone": {
            "playful": "轻松接梗，别端着",
            "technical": "认真，有干货，引用具体细节",
            "question": "真诚帮忙，不懂就说不懂",
            "casual": "自然，像朋友聊天",
        }[tone],
        "anti_bot_rules": [
            "绝不用 'Great point!' 'Interesting!' '说得好' 这种空话",
            "必须引用帖子里的具体内容，证明你真的看了",
            "长度匹配：短帖短回，长帖可展开",
        ],
    }
    print(json.dumps(guide, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("analyze")
    a.add_argument("--text", required=True)
    a.add_argument("--author", default="")
    args = p.parse_args()
    analyze(args.text, args.author)
