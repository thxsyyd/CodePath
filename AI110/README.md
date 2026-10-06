# AI110 — Foundations of AI Engineering

**CodePath · Summer 2026 · 2026-06-04 – 2026-08-06** · 结课获 Honors Certificate of Achievement

这门课在 AI 辅助的工作流里打 CS 基础：用 AI 写代码、调试、做系统设计，同时学会审查 AI 的输出。后半段进入机器学习、RAG、Agent 和 Guardrail。

每个周文件夹的 README 是那一周的课堂笔记，以及 Lab 和 Project 的说明。项目代码保留了完整的提交历史：从 CodePath 的 starter 代码开始，到我的最后一次提交。

---

## 每周内容

| 周 | 主题 | Lab | Project |
|---|---|---|---|
| [W01](20260604%20W01/) | Thinking Like an AI-Native Programmer | [Playlist Chaos](20260604%20W01/Lab/playlist-chaos/) | |
| [W02](20260611%20W02/) | Debugging and Refactoring with AI Tools | | |
| [W03](20260618%20W03/) | Designing Systems with AI as a Partner | [ByteBites](20260618%20W03/Lab/bytebites/) | **P1** [Game Glitch Investigator](20260618%20W03/Project/game-glitch-investigator/) |
| [W04](20260625%20W04/) | Algorithmic Thinking in AI Workflows | | |
| [W05](20260702%20W05/) | How Machines Learn | [The Mood Machine](20260702%20W05/Lab/the-mood-machine/) | **P2** [PawPal+](20260702%20W05/Project/pawpal/) |
| [W06](20260709%20W06/) | Data, Bias, and Evaluation | | |
| [W07](20260716%20W07/) | RAG and Connected Intelligence | [DocuBot](20260716%20W07/Lab/docubot/) | **P3** [Music Recommender Simulation](20260716%20W07/Project/music-recommender-simulation/) |
| [W08](20260723%20W08/) | Human + AI Collaboration | | |
| [W09](20260730%20W09/) | Agentic Workflows, Fine-Tuned Models, and Testing | [BugHound](20260730%20W09/Lab/bughound/) | **P4** ⭐ [DocuBot Pro](20260730%20W09/Project/docubot-pro/) |
| [W10](20260806%20W10/) | Presentation and Portfolio Showcase | | 期末项目总结 |

Project 按**截止周**放置。PawPal+ 从 W04 开始，DocuBot Pro 从 W08 开始。

## 课程结构

5 个模块，每个模块 2 周：

| 模块 | 周 | 重点 |
|---|---|---|
| 1 | W01–W02 | AI-Native 编程思维、调试和重构 |
| 2 | W03–W04 | 系统设计（OOP、UML）、算法思维 |
| 3 | W05–W06 | 机器学习原理、数据偏差和评估 |
| 4 | W07–W08 | RAG、人与 AI 协作 |
| 5 | W09–W10 | Agent、Fine-tuning、测试、期末展示 |

## 项目一览

| 项目 | 周 | 分值 | 能讲什么 |
|---|---|---|---|
| Game Glitch Investigator | W03 | 18 + 10 | AI 辅助调试、Triage → Prompt → Verify、pytest |
| ByteBites（Lab） | W03 | — | OOP 系统设计、UML |
| PawPal+ | W05 | 20 + 10 | 工业级 Python（dataclass / Enum / datetime）、调度算法、Streamlit |
| The Mood Machine（Lab） | W05 | — | 规则法 vs ML、过拟合、Model Card |
| Music Recommender Simulation | W07 | 21 + 8 | 基于内容的推荐算法、bias / filter bubble |
| DocuBot（Lab）→ DocuBot Pro | W07, W09 | 21 + 8 | RAG、confidence / guardrail、可靠性工程、trace logging |
| BugHound（Lab） | W09 | — | Agentic workflow、风险评估 |

---

## 课程关键词总结

**核心技术概念**
- Retrieval-Augmented Generation (RAG)
- Agentic Workflows（plan → act → check 循环）
- Prompt Engineering（Specs as Syntax、Persona Prompting）
- Guardrails & Reliability Engineering（least privilege / approval gate / outside verification）
- Confidence Scoring / Self-Critique
- Embeddings & Semantic Search（King − Man + Woman ≈ Queen、cosine similarity）
- Chunking & Inverted Index
- Human-in-the-Loop（Intent → Generation → Verification → Integration）
- Hallucination Mitigation
- Trace Logging / Observability（"trust the log, not the vibe"）
- Bias Detection & Evaluation（Precision / Recall、confusion matrix、Model Cards）
- OOP & System Design（UML、composition vs inheritance）

**技术栈 / 工具**
- Python 3.13（miniconda）
- Google Gemini API
- Streamlit
- pytest
- Git / GitHub + GitHub Desktop
- Mermaid（UML + 架构图）
- scikit-learn（CountVectorizer + LogisticRegression）
- dotenv / 环境变量管理

**工程实践**
- AI 辅助开发：用 AI，但要审查复核
- Model Cards（负责任 AI 的文档）
- 用测试锁住 guardrail 的行为
- Failure Mode Analysis
- Accountability：锅自己背

---

← [CodePath](../)
