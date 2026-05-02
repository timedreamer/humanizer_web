# Task Plan: 系统提示词全面重构

## Goal

基于真实的人类化技能（humanizer skill v2.5.1，含29种AI写作模式）重构 `app.py` 的 `SYSTEM_PROMPT`，使 DeepSeek 模型能生成真正自然的人类化文本。

## Current Phase

Phase 4

## Phases

### Phase 1: 需求与发现
- [x] 阅读现有 app.py 代码及 SYSTEM_PROMPT
- [x] 阅读现有计划文档 doc/plan/20260501_system_prompt_overhaul.md
- [x] 阅读 humanizer skill 原始数据 data/raw_humanizer_skill_20260501.md
- [x] 理解项目结构和约束
- **Status:** complete

### Phase 2: 创建 prompts.py
- [x] 创建 `prompts.py`，包含：
  - 完整的 SYSTEM_PROMPT（~500行，7个章节，29种模式）
  - STRENGTH_INSTRUCTIONS 字典
  - STYLE_INSTRUCTIONS 字典
- **Status:** complete

### Phase 3: 更新 app.py
- [x] 移除旧的 SYSTEM_PROMPT，从 prompts.py 导入
- [x] 更新 `build_user_prompt()` — 更丰富的格式，支持分析模式
- [x] 在侧边栏添加"显示完整分析"复选框
- [x] 更新 `humanize_text()` 签名
- [x] 更新输出显示区域
- **Status:** complete

### Phase 4: 测试与验证
- [ ] 用户自行测试各强度级别
- [ ] 测试分析模式开/关
- [ ] 测试 Markdown 密集型文本
- [ ] 测试边界情况（空输入、超长输入）
- **Status:** deferred (user will test)

### Phase 5: 交付
- [ ] 运行 ruff lint/format
- [ ] 运行 pyright 类型检查
- [ ] 最终审查
- **Status:** pending

## Key Questions

1. 是否需要保留原有的 `check_password` 和模型选择功能？ — 保留不变
2. 分析模式如何展示输出？ — 使用 text_area 显示 draft→audit→final 格式

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| 新建 prompts.py | 系统提示词约500+行，放在 app.py 会严重膨胀 |
| 保留所有现有控件 | rewrite strength、output style、markdown/concise 选项仍有意义 |
| 新增"显示完整分析"复选框 | 让可选输出 draft→audit→final 格式 |
| 使用 text_area 展示输出 | 比 st.markdown 更好地处理 markdown 内容 |

## Errors Encountered

| Error | Attempt | Resolution |
|-------|---------|------------|
| — | — | — |

## Notes

- 按 AGENTS.md 要求，规划文件放项目根目录（本文件），设计文档放 doc/plans/
- 遵循最小改动原则，只改动必要部分
