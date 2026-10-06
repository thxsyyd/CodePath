# Week 5 — How Machines Learn

**AI110 · Module 3 · Lesson 1** · 2026-07-02 · **Project 2 截止**

| 类型 | 内容 |
|---|---|
| Lab | [The Mood Machine](Lab/the-mood-machine/) |
| Project 2 | [PawPal+](Project/pawpal/)（20 + 10 分，20/20 完成） |

## Lab — The Mood Machine

情绪分析器，对比规则法和机器学习法。

- **Part 3（规则法）**：准确率 50% → 75%（加 POSITIVE / NEGATIVE 词表）。讽刺句无法用规则修复——这是规则法的根本局限。
- **Part 4（ML 法）**：`ml_experiments.py`（CountVectorizer + LogisticRegression）训练准确率 100%，但没见过的输入只有约 60%（"I feel amazing today" → negative）——16 个样本的小数据集过拟合。
- **Part 5**：填写 `model_card.md`（8 个 section）：使用场景、规则法三步流程、ML 机制、局限。

**踩坑**：装 scikit-learn 要用 miniconda 的 Python 3.13（系统 Python 3.14 缺包）。用 `which python` 确认解释器；VS Code 的 Run 按钮默认用系统 Python，会报 `ModuleNotFoundError`。

## Project 2 — PawPal+

**需求**：为宠物日常活动（喂食 / 散步 / 疫苗 / 洗澡）生成计划，能打勾完成、加新任务、编辑和删除任务。

**关键设计讨论**
- 为什么 Pet 通过 `tasks` 列表"知道"哪些任务属于它（Single Source of Truth）
- 改名场景 → 选设计 B（Task 不存 `pet_name`）
- Scheduler 选 X（持有 owner 引用，"一个账号一个 profile"）
- 工业级用法：`@dataclass`、`Enum`（Priority / Frequency）、`datetime.time`（不用字符串）、`task_id` 可靠删除、fail-fast `ValueError`、YAGNI（去掉没用的 `completed_at`）

**文件**：`pawpal_system.py`（4 个类 + 2 个 Enum）、`main.py`（CLI demo）、`tests/test_pawpal.py`（6 个测试全过）、`app.py`（Streamlit UI：增删改查 + 冲突检测 + 循环任务）、`diagrams/uml.mmd`、README、`reflection.md`

- **数据存储**：Streamlit `session_state` 内存存储，没有持久化，重启就重置
- **编辑功能**：提交后发现缺编辑功能，补上后又 commit 了一次

**Commit 习惯**：一句话总结、首字母大写、不加 `feat:` / `test:` 前缀。

**小知识**：`README` 大写、`reflection` 小写是约定俗成——README 是特殊的惯例文件名。

---

← [Week 4](../20260625%20W04/) · [AI110 总览](../) · [Week 6 →](../20260709%20W06/)
