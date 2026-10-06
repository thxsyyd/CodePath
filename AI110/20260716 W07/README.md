# Week 7 — RAG and Connected Intelligence

**AI110 · Module 4 · Lesson 1** · 2026-07-16 · **Project 3 截止**

| 类型 | 内容 |
|---|---|
| Lab | [DocuBot](Lab/docubot/)（Tinker Lab，不用交） |
| Project 3 | [Music Recommender Simulation](Project/music-recommender-simulation/)（21 + 8 分） |

## 课堂笔记

**一句话：** "让 AI 从闭卷考试变成开卷考试。"

- **幻觉 = Confident Autocomplete**：模型预测下一个 token，从不说"我不知道"。这不是 bug，是设计。
- **三类答不了的问题**：after cutoff / private / too specific。
- **Air Canada 案例（2024.2）**：AI 编造了丧亲退款政策，仲裁庭判公司按 AI 编的赔。"AI 编的东西你负责。"
- **Context Window**：训练数据（冻结、过时）vs 上下文窗口（每次从空开始、可以精准注入）。模型是 stateless 的。
- **Long Context 的成本**：5000 页 wiki ≈ 300 万 tokens，每问一次都要付全部 token 的钱 → 成本爆炸。
- **RAG**：问题 → Retriever 挑出相关段落 → LLM 读那几段 → 答案。Retriever 可以是任何搜索（关键词 / 数据库 / web / grep / embedding）。**RAG ≠ 向量数据库。**
- **Semantic Search / Embeddings**：文字变成高维向量，意思相近的点靠得近。**King − Man + Woman ≈ Queen**（语义变成几何）。cosine similarity。
- **RAG Pipeline**：INGEST（Chunk → Embed → Store，做一次）+ QUERY（Embed → Top-K → Inject → Generate，每次都做）。
- **RAG 的三种失败**：retrieval miss / docs wrong / model ignores context。Google "披萨抹胶水"案例（完美检索到 10 年前的 Reddit 玩笑）。
- **Connected Intelligence**：Parametric → RAG → Agentic。"Intelligence lives in the system, not the model alone."

## Lab — DocuBot

RAG 文档助手，对比三种模式，使用 Gemini API。

- **Part 1**：观察 Naive LLM——starter 故意 `# We ignore all_text`，Gemini 只讲通用知识，亲眼看到幻觉。"Fluent output is a signal to investigate, not to trust."
- **Part 2**：实现三个函数——`score_document`（关键词计数）、`build_index`（倒排索引，652 个词）、`retrieve`（索引过滤 → 打分 → 排序 → top_k）。踩坑：IDE 自动乱加 `from email.mime import text`、`__pycache__` 缓存。
- **Part 3**：chunking（按 `\n\n` 切成 163 段）+ `min_score` guardrail。
- **Part 4**：加 STOP_WORDS——发现 stop words 会污染分数（payment 靠 is / the 凑出高分），过滤后 auth 的正确段落排到第一。关键发现：**没有一个 `min_score` 能同时正确处理所有问题**（Precision / Recall 的取舍）。三种模式对比：Naive 流畅但胡说 / Retrieval 忠实但啰嗦 / RAG 精准又自然。
- **Part 5**：`model_card` 记录三种行为、关键词检索的局限，以及用 embeddings 改进的方向。

## Project 3 — Music Recommender Simulation

基于内容的推荐系统（不训练 ML 模型）。

- **概念**：collaborative（靠其他用户的行为）vs content-based（靠物品属性，本项目）。content-based 的主要缺陷是 filter bubble。Netflix "喜欢 A 的人也喜欢 B" 属于 collaborative。
- **Phase 1**：README 写两种推荐系统、特征和 Algorithm Recipe。
- **Phase 2**：数据集从 10 首扩到 15 首（加入 edm / r&b / hip-hop / classical，以及 energetic / romantic / sad）。
- **Phase 3**：`recommender.py` 两套 API——函数式（`load_songs` / `score_song` / `recommend_songs`）+ OOP（`Recommender`）。打分：genre +2、mood +1、energy 接近度 `2 × (1 − gap)`、acoustic +0.5。2 个 pytest 通过。
- **Phase 4**：用 3 个用户画像做压力测试，发现 filter bubble（Chill Lofi 的前 3 首全是 lofi）。
- **Phase 5**：`model_card`（VibeFinder 1.0，9 个 section）+ reflection。
- **Commit**：按 Phase 分开 commit，commit 说明里带 Phase 标签。

---

← [Week 6](../20260709%20W06/) · [AI110 总览](../) · [Week 8 →](../20260723%20W08/)
