# Week 1 — Thinking Like an AI-Native Programmer

**AI110 · Module 1 · Lesson 1** · 2026-06-04

| 类型 | 内容 |
|---|---|
| Lab | [Playlist Chaos](Lab/playlist-chaos/) |
| Project | — |

## 课堂笔记

- **旧模式 vs AI-Native**：传统是"记语法 → 写代码 → 独自 debug"；AI-Native 是"设计架构 → 与 AI 共同生成 → 验证优化"。核心比喻：**你是船长，AI 是领航员。船撞了，负责的是船长。**
- **Human-in-the-Loop 四步**：Intent（人定义问题）→ Generation（AI 生成）→ **Verification（人验证，最关键）** → Integration（人集成）。AI 像读过所有书但零实战的实习生，会"自信地胡说八道"。
- **Verification ≠ 能跑就行**：要阅读逻辑、追踪数据流、检查假设、测边界。
- **Specs 是新的 Syntax**：关键能力是清晰表达需求（Inputs / Outputs / Constraints / Edge Cases）。模糊指令 → 脆弱代码。
- **Git 的重要性**：风险管理（可回退）、审计记录、实验自由。
- **安全警示**：AI 给的 `eval()` 计算器能算 2+2，但用户能输入恶意代码删服务器。AI 优化的是便捷性，不是安全性。

## Lab — Playlist Chaos

一个 AI 写的智能歌单引擎，代码能跑但行为不可预测。练习：找出并修复逻辑 bug。

---

← [AI110 总览](../) · [Week 2 →](../20260611%20W02/)
