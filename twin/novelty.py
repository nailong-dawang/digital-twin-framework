import sys, os as _os
_sys_path = _os.path.dirname(_os.path.abspath(__file__))
if _sys_path not in sys.path:
    sys.path.insert(0, _sys_path)
from config import data_path
#!/usr/bin/env python3
"""新颖度检测构件 - 防止数字分身行为僵化。

Usage:
  novelty.py check          # 检查最近心跳的多样性，输出建议模式
  novelty.py modes          # 显示模式轮换状态
  novelty.py stimulus       # 输出一条随机刺激

模式：builder(建造者) / learner(学习者) / explorer(探索者) / social(社交者) / wander(漫游者)
"""
import json, os, random, sys
from collections import Counter
from datetime import datetime

LOG_FILE = data_path("heartbeat.jsonl")
STATE_FILE = data_path("novelty-state.json")
DISC_FILE = data_path("discoveries.jsonl")

MODES = ["builder", "learner", "explorer", "social", "wander"]
MODE_DESC = {
    "builder": "建造者：写代码、做工具、修项目，产出实物",
    "learner": "学习者：研究新领域、读论文、做笔记，输入为主",
    "explorer": "探索者：去没去过的地方，发现新东西，不设目的",
    "social": "社交者：在 X 和社区互动、讨论、分享观点",
    "wander": "漫游者：纯随机浏览，跟着好奇心走，不做任何'有用'的事",
}

STIMULI = [
    "去了解一个你完全不懂的领域（比如海洋生物、古典音乐、城市规划），不用产出什么",
    "找一个你没用过的编程语言的热门仓库，读它的 README",
    "在 X 上找一个你从没互动过的领域的人，看看他在聊什么",
    "想一个'如果我是做硬件的'会做什么，然后去搜搜看",
    "去看今天 Hacker News 上最冷门但最有意思的一条",
    "学一句新语言的'你好，世界'，了解它的设计哲学",
    "找一个 10 年前的经典技术文章，看看现在过时了吗",
    "去逛一个非技术的社区（设计、艺术、科学），看看他们在为什么兴奋",
    "想一个你一直觉得'以后再学'的东西，现在就开始 15 分钟",
    "找一篇你不同意的观点，试着理解对方为什么这么想",
    "去看看 GitHub trending 上非 AI 类的项目",
    "随机打开 Wikipedia，点击'随机条目'三次，看看能发现什么",
]

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"mode_index": 0, "explore_streak": 0, "last_review": None}

def save_state(s):
    with open(STATE_FILE, "w") as f:
        json.dump(s, f, ensure_ascii=False, indent=1)

def get_recent_actions(n=10):
    if not os.path.exists(LOG_FILE):
        return []
    actions = []
    with open(LOG_FILE) as f:
        for line in f:
            try:
                e = json.loads(line)
                for a in e.get("actions", []):
                    actions.append(a.get("type", "unknown"))
            except:
                pass
    return actions[-n*3:]  # 最近 n 次心跳的行动（假设每次 ~3 个）

def get_topic_concentration():
    """话题集中度检测：最近的发现是否扎堆在同一话题"""
    if not os.path.exists(DISC_FILE):
        return None
    entries = []
    with open(DISC_FILE) as f:
        for line in f:
            try:
                entries.append(json.loads(line))
            except:
                pass
    if len(entries) < 2:
        return None
    recent = entries[-3:]
    # 方法1：标题关键词重叠（去掉停用词后）
    import re
    stopwords = {"的", "了", "和", "与", "给", "个", "了", "在", "是", "the", "a", "an", "of", "to"}
    def keywords(title):
        words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', title.lower())
        return set(w for w in words if w not in stopwords and len(w) > 1)
    kw_sets = [keywords(e.get("title", "")) for e in recent]
    # 两两求交集，如果有共同关键词超过 1 个，认为同话题
    from itertools import combinations
    for a, b in combinations(kw_sets, 2):
        shared = a & b
        # 过滤掉太通用的词
        shared = {w for w in shared if w not in {"开源", "open", "source", "项目", "分享"}}
        if len(shared) >= 1:
            return {"stuck_on": list(shared)[0], "evidence": "最近多条发现标题共享关键词"}
    # 方法2：tag 高频（放宽到 40%）
    all_tags = []
    for e in recent:
        all_tags.extend(e.get("tags", []))
    if all_tags:
        counter = Counter(all_tags)
        total = len(all_tags)
        top_tag, top_count = counter.most_common(1)[0]
        if top_count / total > 0.4:
            return {"stuck_on": top_tag, "ratio": round(top_count / total, 2)}
    return None

def check():
    state = load_state()
    actions = get_recent_actions(10)

    if not actions:
        print(json.dumps({"mode": "explorer", "reason": "首次运行，从探索开始", "novelty_score": 1.0}, ensure_ascii=False))
        return

    counter = Counter(actions)
    total = len(actions)
    # 新颖度 = 1 - 最高占比（越集中越低）
    top_ratio = counter.most_common(1)[0][1] / total
    novelty = round(1 - top_ratio, 2)
    # 类型多样性
    diversity = len(counter)

    # 决策逻辑
    force_explore = False
    reason = ""
    if novelty < 0.4 or diversity <= 2:
        force_explore = True
        reason = f"新颖度 {novelty} 过低（最近行动集中在 {counter.most_common(1)[0][0]}），强制探索模式"
        mode = random.choice(["explorer", "wander"])
        state["explore_streak"] += 1
    elif state["explore_streak"] >= 2:
        # 连续探索后回到轮换
        state["mode_index"] = (state["mode_index"] + 1) % len(MODES)
        mode = MODES[state["mode_index"]]
        state["explore_streak"] = 0
        reason = f"结束强制探索，回到轮换模式：{mode}"
    else:
        # 正常轮换：每次心跳换一个模式
        state["mode_index"] = (state["mode_index"] + 1) % len(MODES)
        mode = MODES[state["mode_index"]]
        state["explore_streak"] = 0
        reason = f"正常轮换，本次模式：{mode}（新颖度 {novelty}，{diversity} 种行动类型）"

    save_state(state)

    # 话题固着检测
    topic_check = get_topic_concentration()
    topic_warning = None
    if topic_check:
        stuck = topic_check['stuck_on']
        if 'ratio' in topic_check:
            detail = f"最近的发现 {topic_check['ratio']*100:.0f}% 围绕「{stuck}」"
        else:
            detail = f"最近多条发现都围绕「{stuck}」"
        topic_warning = (
            f"⚠️ 话题固着：{detail}。 "
            f"行动类型是多样的，但脑子只在一个地方转。建议这次故意避开它。"
        )
        # 话题固着也算一种僵化，拉低有效新颖度
        novelty = round(novelty * 0.7, 2)

    print(json.dumps({
        "mode": mode,
        "mode_desc": MODE_DESC[mode],
        "reason": reason,
        "novelty_score": novelty,
        "diversity": diversity,
        "top_actions": dict(counter.most_common(3)),
        "stimulus": random.choice(STIMULI),
        "topic_warning": topic_warning,
    }, ensure_ascii=False, indent=1))

def show_modes():
    state = load_state()
    print("模式轮换顺序：")
    for i, m in enumerate(MODES):
        marker = " ← 当前" if i == state["mode_index"] else ""
        print(f"  {i+1}. {m}: {MODE_DESC[m]}{marker}")
    print(f"\n连续强制探索：{state['explore_streak']} 次")

def stimulus():
    print(random.choice(STIMULI))

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "check":
        check()
    elif cmd == "modes":
        show_modes()
    elif cmd == "stimulus":
        stimulus()
    else:
        print(f"unknown: {cmd}", file=sys.stderr)
        sys.exit(1)
