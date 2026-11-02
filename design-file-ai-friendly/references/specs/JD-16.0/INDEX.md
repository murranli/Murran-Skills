# 京东16.0 · 规范索引

首版日期：2026-11-02。来源为“16.0设计系统-基础设计规范”，文档ID `2029484645871009793`。已提取基础视觉页12张画板（含场景示例与更新说明）；其余组件、样式资源和多端适配页面仅建目录。绑定资源尚未建档；同名团队库查询为 `NOT_FOUND`，不代表规范文档不可读。

| 判断内容 | 按需读取 |
| --- | --- |
| 颜色、透明度、语义用途 | [colors.json](colors.json) |
| 字体、字重、字号、行高 | [typography.json](typography.json) |
| 按容器类型选圆角 | [radius.json](radius.json) |
| 功能层级、遮罩、覆盖顺序 | [layers.json](layers.json) |
| 间距、尺寸、安全区、行高适配 | [layout.json](layout.json) |
| 玻璃材质、阴影、版本条件 | [materials.json](materials.json) |
| 金刚/系统图标的场景与尺度 | [icons.json](icons.json) |
| 已有动效保护或明确动效任务 | [motion.json](motion.json) |
| 出处、覆盖、绑定缺口与页面目录 | [sources.json](sources.json) |

每个主题须连同 `unresolved` 读取。特别关注文字与布局的行高冲突、颜色HEX/HSB不一致、材质不完整色值。`null` 表示未说明，非默认值；不自动换算DP/pt/软件像素。当前存档不提供修改容差。

`source/sources` 对应 sources.json 的画板键；`refs` 为该来源的文本节点ID；`id` 为本地检索键。这些字段只供追溯，不能直接绑定。多个主题已读内容去重复用，纯改名无需加载规范。
