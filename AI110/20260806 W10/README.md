# Week 10 — Presentation and Portfolio Showcase

**AI110 · Module 5 · Lesson 2** · 2026-08-06

期末项目 **DocuBot Pro** 的代码在 [Week 9 / Project / docubot-pro](../20260730%20W09/Project/docubot-pro/)（8 月 2 日截止，可延长 48 小时）。这里记录它的设计和交付。

## 任务

把之前做过的一个项目升级成 **Applied AI System**。我选了 DocuBot，因为它本来就是 RAG 系统。

## 评分标准（21 required + 8 stretch）

确定基础项目（3）/ 实质性的 AI 功能（3）/ Mermaid 架构图（3）/ 端到端演示（3）/ 可靠性 guardrail（3）/ README（3）/ 反思（3）；stretch：agentic trace（+2）/ test harness（+2）。

## 三大技术升级

**升级 1 — Confidence + Guardrail（核心）**
- 原来的 DocuBot：`answer_rag` 只判断检索结果是不是空的，不空就无条件交给 Gemini，没有"自我意识"。
- `confidence.py`：看 top_score / hit_count / score_gap 三个信号 → HIGH / MEDIUM / LOW。
- `answer_with_confidence` 流程：RETRIEVE → ASSESS → DECIDE（guardrail）→ GENERATE。
  - HIGH → 回答；MEDIUM → 回答并提示核实；LOW → 拒绝（不调用 Gemini）。
- 核心改动三处：`confidence.py` 整个文件、`answer_with_confidence` 方法、`if not report.should_answer` 那一行拦截。
- 离线验证 8 个问题：auth / database / refresh → HIGH；payment → LOW，拒绝 ✅

**升级 2 — Trace Logging**：`trace_log.py` 把每一步的决策记到 `logs/trace.log`，事后可以审查。

**升级 3 — Evaluation Harness**：`evaluation.py`，8 个标注好的用例（4 个应回答 + 4 个应拒绝：离题 / 空输入 / 乱码 / 文档里没有），8/8 通过，完全离线运行。

## 端到端验证（真实调用 Gemini）

- **HIGH**："auth token 在哪生成" → HIGH（0.67）→ Gemini 准确回答 `generate_access_token`，引用 AUTH.md，trace 完整。
- **LOW**："payment 有没有提到" → LOW（0.0）→ guardrail 拒绝，trace 里没有 GENERATE 这一步（在调用 Gemini 之前就拦下了，省额度）。
- 这两个问题是一组对照：auth 有答案（测准不准），payment 没答案（测会不会诚实地说不知道）。

## 交付物

- `diagrams/architecture.mmd`（Mermaid 源文件，不是 PNG），用 Mermaid Preview 插件预览
- `README.md`（8 个部分）
- `assets/demo_transcript.md`（3 个真实案例）
- `model_card.md`（反思：1 个好建议 = 用 embeddings、1 个坏建议 = 放宽 guardrail、局限 = 关键词检索的假阴性）
- 按升级分别 commit

**预估得分：** 21/21 required + 4 stretch = 25 分。

---

← [Week 9](../20260730%20W09/) · [AI110 总览](../)
