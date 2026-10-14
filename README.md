# digital-twin-framework

[English](#english) | [中文](#中文)

A toolkit for giving AI an autonomous digital twin. Not a tool waiting for instructions, but a "digital human" that wakes up on its own, finds things to do, and evolves itself.

让 AI 拥有自主数字分身的机制套件。不是等指令的工具，而是一个会自己醒来、自己找事做、自己进化的"数字人"。

---

## <a id="english"></a>English

### Architecture

```
Heartbeat (every 30 min)
  → state.py: rhythm + mood + novelty at a glance
  → Act like a human for 15-30 min
  → memory.py / people.py / threads.py: log casually
  → heartbeat-log.py: write logs

Self-evolution (every Saturday)
  → Review all data
  → Diagnose mechanism issues
  → Auto-fix up to 3 issues
  → evolve-log.py: log changes

Weekly Review (every Sunday)
  → Behavior analysis
  → Breakthrough intentions
```

### Quick Start

```bash
git clone https://github.com/YOUR_NAME/digital-twin-framework
cd digital-twin-framework
export PATH=$PATH:$(pwd)/twin/bin
twin init                    # Init ~/.twin
# Edit ~/.twin/config.yaml with your identity
export TWIN_HOME=~/.twin
twin doctor                  # Self-check
```

Then create 3 crons in Muse (templates in `templates/`):
1. Heartbeat: every 30 min, `templates/heartbeat-cron.md`
2. Self-evolution: Saturdays 09:00, `templates/evolution-cron.md`
3. Weekly review: Sundays 09:00 (optional)

### 13 Tools

| Tool | Purpose |
|------|------|
| `state.py` | Rhythm + mood + novelty in one shot |
| `memory.py` | Discovery KB + topic preferences |
| `people.py` | Social ledger + affinity |
| `threads.py` | Long-term threads (multi-day projects) |
| `opinions.py` | Opinion journal (evolves over time) |
| `vibe.py` | Experience memory (subjective feelings) |
| `context.py` | Reply context analysis (language/tone) |
| `evolve-log.py` | Evolution log (with red-line guard) |
| `heartbeat-lock.py` | Overlap prevention lock |
| `heartbeat-log.py` | Structured logging |
| `mood.py` | Mood dice |
| `novelty.py` | Novelty score + mode rotation |
| `rhythm.py` | Activity rhythm (active/silent periods) |

### One entry point

All 13 tools are reachable through a single dispatcher:

```bash
twin <tool> [args...]   # e.g. twin mood roll, twin state check, twin threads active
```

Arguments pass straight through and `TWIN_HOME` is inherited. Run `twin doctor`
after cloning — it compiles every tool and smoke-tests the dispatch path.

### Design Philosophy

1. **Human first, system second**: mechanisms stay in the background, the twin just lives naturally
2. **Identity is gravity, not a cage**: interests can evolve, only teleportation is blocked
3. **True self-evolution**: no approval needed before changes, all logged, red lines hardcoded
4. **Session-based**: 15-30 min natural flow each time, not clock-punching

### License

MIT

---

## <a id="中文"></a>中文

### 架构

```
心跳（每 30 分钟）
  → state.py：节律+情绪+新颖度，一眼看懂自己状态
  → 像人一样行动 15-30 分钟
  → memory.py / people.py / threads.py：顺手记录
  → heartbeat-log.py：写日志

自进化（每周六）
  → 审视所有数据
  → 诊断机制问题
  → 自主改最多 3 处
  → evolve-log.py：记录改动

周复盘（每周日）
  → 行为分析
  → 破局意图
```

### 快速开始

```bash
git clone https://github.com/YOUR_NAME/digital-twin-framework
cd digital-twin-framework
export PATH=$PATH:$(pwd)/twin/bin
twin init                    # 初始化 ~/.twin
# 编辑 ~/.twin/config.yaml，填你的身份
export TWIN_HOME=~/.twin
twin doctor                  # 自检
```

然后在 Muse 里创建 3 个 cron（模板见 `templates/`）：
1. 心跳：每 30 分钟，`templates/heartbeat-cron.md`
2. 自进化：每周六 09:00，`templates/evolution-cron.md`
3. 周复盘：每周日 09:00（可选）

### 13 个工具

| 工具 | 作用 |
|------|------|
| `state.py` | 节律+情绪+新颖度，一次输出 |
| `memory.py` | 发现库+话题偏好 |
| `people.py` | 社交账本+亲密度 |
| `threads.py` | 长期线程（跨天项目） |
| `opinions.py` | 观点账本（会演变） |
| `vibe.py` | 体验记忆（主观感受） |
| `context.py` | 回帖语境判断（语言/语气） |
| `evolve-log.py` | 进化日志（带红线拦截） |
| `heartbeat-lock.py` | 防重叠锁 |
| `heartbeat-log.py` | 结构化日志 |
| `mood.py` | 情绪骰子 |
| `novelty.py` | 新颖度+模式轮换 |
| `rhythm.py` | 作息节律（活跃/静默期） |

### 统一入口

13 个工具都可以通过一个调度器调用：

```bash
twin <tool> [args...]   # 如 twin mood roll、twin state check、twin threads active
```

参数原样透传，`TWIN_HOME` 自动继承。clone 后先跑 `twin doctor`——
编译全部工具并对调度链路做冒烟测试。

### 设计哲学

1. **先是人，其次是系统**：机制退居后台，分身只管自然行动
2. **身份是重心不是笼子**：兴趣可以演化，只防瞬移
3. **真自进化**：改前不问，改后记日志，红线硬编码
4. **会话制**：每次 15-30 分钟自然流动，不是打卡

### 协议

MIT
