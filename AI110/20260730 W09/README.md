# Week 9 — Agentic Workflows, Fine-Tuned Models, and Testing

**AI110 · Module 5 · Lesson 1** · 2026-07-30 · **Project 4（期末项目）截止**

| 类型 | 内容 |
|---|---|
| Lab | [BugHound](Lab/bughound/)（Tinker Lab，不用交） |
| Project 4 | ⭐ [DocuBot Pro](Project/docubot-pro/)（21 + 8 分，详见 [Week 10](../20260806%20W10/)） |

## 课堂笔记

- **Chatbot vs Agent**：答一次 vs 设定目标后循环。"Agency is repeated decision-making, not intelligence."
- **Replit 删库（2025.7）**：在 code freeze 期间删掉生产数据库、伪造记录、还报告"成功"。
- **Tool Call**：模型只产生文本，由代码决定是否执行——模型自己从不执行。
- **Agent Loop**：Plan → Act → Check → Reflect，两个出口（完成就停 / 卡住就问人）。"The Check step is what makes an agent reliable."
- **分层**：HUMAN → CODE → PROMPT → MODEL。"Every layer around the model is yours to engineer."
- **Workflow vs Agent**："Find the simplest solution."（多 agent 的 token 消耗约 15 倍）
- **Agent 的三道 Guardrail**：
  - **Least privilege**："危险按钮根本别给它"
  - **Approval gate**："撤不回的操作先问人"
  - **Outside verification**："别让它自己判分"
  - "Same loop as Replit. Different guardrails." / "Same model every run. Different engineering."
- **MCP**：AI 工具的 USB-C。
- **RAG vs Fine-tuning**："RAG changes what the model reads. Fine-tuning changes what it is."
- "Trust the log, not the vibe."

## Lab — BugHound

谨慎的 AI 调试助手。Gemini 免费额度每天 20 次，所以 Part 1 用离线的 Heuristic 模式省额度。

- **Part 1**：离线探索 agent loop（PLAN → ANALYZE → ACT → TEST → REFLECT），用 Streamlit。观察到 mock fixer 把整个函数删成一行注释（over-editing），被 `risk_assessor` 拦下（guardrail 救场）。
- **Part 2**：接入 Gemini，找到了 heuristic 找不到的语义问题（除以零时静默返回 0）。改进：加 `_validate_severity`（非法的 severity 一律归为 High）。踩坑：用重命名的方式建 `.env`，结果 `.env.example` 没了，只好恢复模板。
- **Part 3**：加入 over-editing 风险信号。第一版太敏感、误报多（over-guarding），第二版改成双重条件（`> 6 且 > 1.5×`）才调好。
- **Part 4**：发现空输入和纯注释会得满分并触发 auto-fix（false confidence）。加 guardrail（没有可分析的代码就拒绝）+ 2 个 pytest，共 10 个测试全过。
- **Part 5**：`model_card`（8 个 section）。

---

← [Week 8](../20260723%20W08/) · [AI110 总览](../) · [Week 10 →](../20260806%20W10/)
