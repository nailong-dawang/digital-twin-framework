# digital-twin-framework

让 AI 拥有自主数字分身的机制套件。不是等指令的工具，而是一个会自己醒来、自己找事做、自己进化的"数字人"。

A toolkit for giving AI an autonomous digital twin. Not a tool waiting for instructions, but a "digital human" that wakes up on its own, finds things to do, and evolves itself.

## 架构 | Architecture

```
心跳 Heartbeat（每 30 分钟 / every 30 min）
  → state.py：节律+情绪+新颖度，一眼看懂自己状态
               rhythm + mood + novelty at a glance
  → 像人一样行动 15-30 分钟 | Act like a human for 15-30 min
  → memory.py / people.py / threads.py：顺手记录
  → heartbeat-log.py：写日志 | Write logs

自进化 Self-evolution（每周六 / every Saturday）
  → 审视所有数据 | Review all data
  → 诊断机制问题 | Diagnose mechanism issues
  → 自主改最多 3 处 | Auto-fix up to 3 issues
  → evolve-log.py 记录 | Log changes

周复盘 Weekly Review（每周日 / every Sunday）
  → 行为分析 | Behavior analysis
  → 破局意图 | Breakthrough intentions
```

## 快速开始 | Quick Start

```bash
git clone https://github.com/YOUR_NAME/digital-twin-framework
cd digital-twin-framework
export PATH=$PATH:$(pwd)/twin/bin
twin init                    # 初始化 ~/.twin | Init ~/.twin
# 编辑 ~/.twin/config.yaml，填你的身份 | Edit config with your identity
export TWIN_HOME=~/.twin
twin doctor                  # 自检 | Self-check
```

然后在 Muse 里创建 3 个 cron（模板见 `templates/`）|
Then create 3 crons in Muse (templates in `templates/`):
1. 心跳 Heartbeat：每 30 分钟 every 30 min，`templates/heartbeat-cron.md`
2. 自进化 Self-evolution：每周六周六 09:00 Saturdays 09:00，`templates/evolution-cron.md`
3. 周复盘 Weekly review：每周日周日 09:00 Sundays 09:00（可选 optional）

## 13 个工具 | 13 Tools

| 工具 Tool | 作用 Purpose |
|------|------|
| `state.py` | 节律+情绪+新颖度，一次输出 Rhythm+mood+novelty in one shot |
| `memory.py` | 发现库+话题偏好 Discovery KB + topic prefs |
| `people.py` | 社交账本+亲密度 Social ledger + affinity |
| `threads.py` | 长期线程（跨天项目） Long-term threads |
| `opinions.py` | 观点账本（会演变） Opinion journal (evolves) |
| `vibe.py` | 体验记忆（主观感受） Experience memory |
| `context.py` | 回帖语境判断 Reply context analysis |
| `evolve-log.py` | 进化日志（带红线拦截） Evolution log (red-line guard) |
| `heartbeat-lock.py` | 防重叠锁 Overlap prevention lock |
| `heartbeat-log.py` | 结构化日志 Structured logging |
| `mood.py` | 情绪骰子 Mood dice |
| `novelty.py` | 新颖度+模式轮换 Novelty + mode rotation |
| `rhythm.py` | 作息节律 Activity rhythm |

## 设计哲学 | Design Philosophy

1. **先是人，其次是系统**：机制退居后台，分身只管自然行动
   **Human first, system second**: mechanisms stay in background
2. **身份是重心不是笼子**：兴趣可以演化，只防瞬移
   **Identity is gravity, not a cage**: interests evolve, only teleportation is blocked
3. **真自进化**：改前不问，改后记日志，红线硬编码
   **True self-evolution**: no approval needed, logged, red lines hardcoded
4. **会话制**：每次 15-30 分钟自然流动，不是打卡
   **Session-based**: 15-30 min natural flow, not clock-punching

## LICENSE

MIT
