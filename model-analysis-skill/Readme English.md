<div align="center">

[中文](./Readme.md) · **English**

</div>

# Model Analysis · model-analysis

Guided questioning to focus your analysis needs. Auto-routes to 3–4 models from a library of 30+ for in-depth analysis.

---

## Use Cases

| Scenario | Example Prompt |
|----------|---------------|
| Diagnose problems | "Help me figure out where our app's conversion funnel breaks down" |
| Find opportunities | "I want to enter the X market — compare the main competitors" |
| Understand a market | "I'm new to this industry, help me map the competitive landscape" |

---

## 📦 Installation

In any Skill-compatible Agent (Claude Code, Codex, OpenClaw, etc.), just say:

```
Install this skill: https://github.com/YOUR_USERNAME/YOUR_REPO/tree/main/model-analysis-skill
```

The Agent will fetch and install it automatically — no manual download needed.

<details>
<summary>Manual installation (claude.ai web)</summary>

1. Download `model-analysis.skill` from this repository
2. Go to [claude.ai](https://claude.ai) and navigate to **Settings → Skills**
3. Click **Upload Skill** and select the downloaded `.skill` file

</details>

Once installed, any of the following will activate the Skill:

```
Analyze Notion's product strategy
Compare the competitive positioning of Slack vs. Teams
Give me an overview of the short-video market landscape
```

Or type:

```
/model-analysis + keywords (or upload product screenshots directly)
```

---

## Model Coverage

The Skill includes 30+ analytical models organized across three layers. Coverage will continue to expand.

| Layer | Core Question | Models |
|-------|--------------|--------|
|**Market & Business Strategy** | Who does the competitor sell to, how do they make money, what keeps them alive? | PESTEL · Porter's Five Forces · Competitive Strategy · Strategy Wheel · Ansoff Matrix · VRIO · Value Curve · Business Model Canvas · SWOT · 4Ps/7Ps · Perceptual Mapping · Industry Life Cycle · Gartner Hype Cycle · Benchmarking · RIIF |
|**Product & Business Architecture** | What solutions has the product built to achieve its commercial goals? | BCG Matrix · KANO · Stakeholder Analysis · MECE · Service Blueprint · System Map · Stage-Gate · Harris Profile · EVR Matrix · PMI · CBox · Objective Weighting · vALUe |
|**UX & Execution** | What does the user see, click, and feel on screen? | Fogg Behavior Model · User Journey · HMW · Card Sorting · Gutenberg Diagram · Focus Flow · Hick's Law · Fitts's Law · Critical Path · Atomic Design |

Full model definitions and usage notes → [`references/model-library.md`](./references/model-library.md)

---

## Prompt Version

If you don't have access to the Skill feature, you can use these files directly as a System Prompt:

📄 **[SKILL.md](./SKILL.md)** — Main prompt with role definition and full workflow  
📄 **[references/model-library.md](./references/model-library.md)** — Model library appendix; recommended to append after the main prompt

> **How to use**: Merge the contents of both files and paste into the System Prompt field of your Claude client, or configure it in any client that supports custom instructions.
