# Week 3 — Designing Systems with AI as a Partner

**AI110 · Module 2 · Lesson 1** · 2026-06-18 · **Project 1 截止**

| 类型 | 内容 |
|---|---|
| Lab | [ByteBites](Lab/bytebites/) |
| Project 1 | [Game Glitch Investigator](Project/game-glitch-investigator/)（18 + 10 分） |

## 课堂笔记

重大转变：从"调试 AI 写的代码"到"写代码前先设计系统"。

- **Module 1 vs Module 2**：造可靠的砖头 vs 当设计房子的建筑师。
- **Class = 蓝图**（数据 attributes + 行为 methods），一个蓝图可建多个实例。
- **继承（Inheritance）**：父类 Vehicle，子类 Car / Truck 共享代码。但 AI 经常把该用组合（has-a）的地方用了继承（is-a）。
- **UML 类图**：用 Mermaid.js 语法（mermaid.live 预览）。
- **核心工作流**：自然语言描述 → AI 生成类图（不是代码！）→ 批判审查关系 → 手动修正 → 才写代码。
- **Check 案例**：AI 给的图书馆 UML 把 Book 继承自 Library（书不是一种图书馆！应是包含关系），还加了没用的 `read_every_book()`。"AI 经常过度设计或搞混关系，你当那个说'不对'的建筑师。"
- **新术语**：Role / Persona Prompting、Composition vs Inheritance。

## Lab — ByteBites

设计一个校园订餐 app 的后端逻辑。先画架构图再写代码。涉及 `models.py`、UML、git commit、pytest。

## Project 1 — Game Glitch Investigator

"不可能的猜数字游戏"：starter 代码有 bug（输入 50 / 68 / 77 / 99 都提示 go higher，答案却是 32；难度范围 `get_range_for_difficulty` 也有问题）。

- **要求**：复现 bug（trace / 终端输出）、找出 ≥ 3 个不同的 bug、验证并批判 AI 的调试建议（1 个正确、1 个错误）、修好 ≥ 2 个 bug、修复后的游戏演示、文档 + reflection + ≥ 3 个 commit
- `reflection.md` 按"每个问题下面写答案"的格式填，保留原格式
- pytest：14 个测试全绿 ✅

---

← [Week 2](../20260611%20W02/) · [AI110 总览](../) · [Week 4 →](../20260625%20W04/)
