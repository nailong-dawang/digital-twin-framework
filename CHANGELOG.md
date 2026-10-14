# CHANGELOG

## Unreleased
- `twin backup`: snapshot `TWIN_HOME/data` into a timestamped tarball under `TWIN_HOME/backups/`
- `twin doctor`: exits non-zero when any check fails; adds a backup round-trip smoke test in a sandbox `TWIN_HOME` (does not touch the real data dir)

## 2026-10-14 — CLI one-entry-point
- `twin <tool> [args...]` dispatcher with `TWIN_HOME` inheritance
- `twin doctor` smoke test (compile all tools + dispatch check)
- README: one-entry-point docs (EN/ZH)

## 2026-10-13 — Bilingual templates & README
- Templates and README in 中英双语

## 2026-10-12 — v0.1.0
- Initial commit: 13 tools (state, memory, people, threads, opinions, vibe, context, evolve-log, heartbeat-lock, heartbeat-log, mood, novelty, rhythm), config.yaml, cron templates
