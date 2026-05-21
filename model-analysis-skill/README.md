<div align="center">

**中文** · [English](./Readme%20En.md)

</div>

# 引导式模型分析 · Guided Model Analysis

以引导式提问，聚焦你的分析诉求与目标。在收录的 30+ 分析模型中，自动路由 3-4 个模型深度分析。

---

## 使用场景

| 场景 | 示例提问 |
|------|---------|
| 发现问题 | "帮我分析一下我们 App 的用户转化在哪里断掉了" |
| 寻找机会 | "我想切入 XX 市场，对比一下几个主要竞品" |
| 了解市场 | "我刚进入这个行业，帮我建立对竞争格局的认知" |

---

## 📦 安装方式

在 Claude Code、Codex、OpenClaw 等支持 Skill 的 Agent 里，直接说：

```
帮我安装这个 skill: https://github.com/murranli/Murran-Skills/tree/main/model-analysis-skill
```

Agent 会自动拉取并完成安装，无需手动下载文件。

<details>
<summary>手动安装（claude.ai 网页端）</summary>

1. 前往本仓库下载 `model-analysis.skill` 文件
2. 打开 [claude.ai](https://claude.ai) 并进入 **Settings → Skills**
3. 点击 **Upload Skill**，选择下载的 `.skill` 文件

</details>

安装完成后，以下任意表达都会触发本 Skill：

```
帮我分析一下 Notion 的产品策略
对比一下微信和 Telegram 的竞争定位
我想了解国内短视频市场的竞争格局
```

或输入

```
/model-analysis + 关键词输入（或直接上传产品截图）
```

---

## 模型覆盖

Skill 目前选取 30+ 个分析模型，按三个层次组织。模型覆盖范围将持续迭代。

| 层次 | 核心问题 | 覆盖模型 |
|------|---------|---------|
| **市场与商业战略层** | 竞品在什么环境中，赚谁的钱，靠什么活下来 | PESTEL · 波特五力 · 波特竞争战略 · 竞争战略轮盘 · 安索夫成长矩阵 · VRIO · 价值曲线 · 商业模式画布 · SWOT · 4Ps/7Ps · 知觉地图 · 行业生命周期 · Gartner Hype Cycle · 基准比较法 · RIIF |
| **产品与业务架构层** | 产品为了实现商业目的，提供了哪些解决方案 | BCG 矩阵 · KANO · 利益相关者分析 · MECE · 服务蓝图 · 系统图 · Stage-Gate · 哈里斯图表 · EVR 决策表 · PMI · CBox · 目标权重 · vALUe |
| **用户体验与执行层** | 用户在屏幕上看到什么、点什么、感受到什么 | Fogg 行为模型 · 用户旅程 · HMW · 卡片分类法 · 古腾堡图表 · 焦点流转 · 席克定律 · 费茨定律 · 关键任务路径 · 原子设计理论 |

完整模型定义与使用说明见 → [`references/Model-Library.md`](./references/Model%20Library.md)

---

## Prompt 版本

如果你不使用 Skill 功能，也可以直接将以下文件内容复制为系统提示词（System Prompt）使用：

📄 **[Skill.md](./Skills/Skill.md)** — 主 Prompt，包含角色定义与完整工作流  
📄 **[references/model-library.md](./references/Model%20Library.md)** — 模型库附录，建议拼接在主 Prompt 末尾

> 使用方式：将两个文件的内容合并后，粘贴至对话的 System Prompt 区域，或在支持自定义指令的客户端中配置。
