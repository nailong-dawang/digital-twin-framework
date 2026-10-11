# digital-twin-framework

让 AI 拥有自主数字分身的机制套件。不是等指令的工具，而是一个会自己醒来、自己找事做、自己进化的"数字人"。

## 架构

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
  → evolve-log.py 记录

周复盘（每周日）
  → 行为分析
  → 破局意图
```

## 快速开始

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

## 13 个工具

| 工具 | 作用 |
|------|------|
| `state.py` | 节律+情绪+新颖度，一次输出 |
| `memory.py` | 发现库+话题偏好 |
| `people.py` | 社交账本+亲密度 |
| `threads.py` | 长期线程（跨天项目） |
| `opinions.py` | 观点账本（会演变） |
| `vibe.py` | 体验记忆（主观感受） |
| `context.py` | 回帖语境判断 |
| `evolve-log.py` | 进化日志（带红线拦截） |
| `heartbeat-lock.py` | 防重叠锁 |
| `heartbeat-log.py` | 结构化日志 |
| `mood.py` | 情绪骰子 |
| `novelty.py` | 新颖度+模式轮换 |
| `rhythm.py` | 作息节律 |

## 设计哲学

1. **先是人，其次是系统**：机制退居后台，分身只管自然行动
2. **身份是重心不是笼子**：兴趣可以演化，只防瞬移
3. **真自进化**：改前不问，改后记日志，红线硬编码
4. **会话制**：每次 15-30 分钟自然流动，不是打卡

## LICENSE

MIT
