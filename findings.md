# Findings & Decisions

## Requirements

1. 基于 humanizer skill v2.5.1 的 29 种 AI 写作模式重构 SYSTEM_PROMPT
2. 保留所有现有功能：密码验证、模型选择、强度/风格/选项
3. 新增"显示完整分析"模式（可选）
4. 不要改变现有的 DeepSeek API 调用方式

## Research Findings

### 当前 SYSTEM_PROMPT 问题（来自 app.py）
- 只有 ~20 行通用建议，缺乏具体模式指引
- 没有 AI 词汇表（如 "crucial", "delve", "showcase", "tapestry" 等）
- 没有具体示例（before/after 对比）
- 没有明确的处理流程

### Humanizer Skill v2.5.1 核心结构

**29 种模式分 6 大类：**

**内容模式 (1-6):**
1. 不当强调重要性/意义 — 含完整触发词列表
2. 不当强调知名度/媒体覆盖
3. 肤浅的 -ing 分析（highlighting, underscoring, fostering...）
4. 广告化语言（vibrant, nestled, breathtaking, stunning...）
5. 模糊归因/推诿词汇（Industry reports, Experts argue...）
6. 公式化的"挑战与展望"章节

**语言语法 (7-13):**
7. AI 词汇表 — 核心高频词（crucial, delve, enhance, intricate, pivotal, showcase, tapestry...）
8. 系词回避（serves as→is, boasts→has）
9. 否定排比（Not only...but...）
10. 三一律过度使用
11. 优雅变体（同义词循环）
12. 虚假范围（from X to Y 但无意义尺度的连接）
13. 被动语态和无主语句

**风格格式 (14-19):**
14. 破折号过度使用
15. 粗体过度使用
16. 行内标题式列表
17. 标题大写
18. Emoji 装饰
19. 弯引号→直引号

**交流模式 (20-22):**
20. 协作式聊天痕迹（I hope this helps, Certainly!...）
21. 知识截止日期声明
22. 奉承语气

**填充与犹豫 (23-25):**
23. 填充短语（In order to→To, Due to the fact that→Because...）
24. 过度模糊限定
25. 模糊积极结尾

**其他 (26-29):**
26. 连字符词组过度使用
27. 说教式权威句式（The real question is, at its core...）
28. 预告/引导句式（Let's dive in, here's what you need to know...）
29. 碎片化标题

### 输出格式
- Draft rewrite → "What makes this AI?" audit → Final rewrite → Summary
- 支持两种输出模式：仅最终结果 / 完整分析

## Technical Decisions

| Decision | Rationale |
|----------|-----------|
| 新建 prompts.py 模块 | 保持 app.py 精简，关注点分离 |
| 提示词用常量字符串而非模板 | 提示词是一个整体文档，拆分无益 |
| Voice Calibration 暂不纳入 | 已明确标为本次范围外 |
| 保持现有 API 调用方式不变 | `stream=False`, `thinking: disabled`, DeepSeek base_url |

## Issues Encountered

| Issue | Resolution |
|-------|------------|
| — | — |
| 用户反馈：输出破折号过多 | 扩展 Pattern 14 为绝对禁止所有破折号 |
| 用户反馈：句子太长 | 在 Personality 部分添加具体句子长度约束 |

## Resources

- 现有计划: doc/plan/20260501_system_prompt_overhaul.md
- Humanizer skill 原始数据: data/raw_humanizer_skill_20260501.md
- 现有代码: app.py
- Wikipedia Signs of AI writing: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
