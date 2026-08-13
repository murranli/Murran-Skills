# 面向 Obsidian 的围栏 SVG 形态还原

凡需将统计图或结构图还原为 SVG，先阅读本文件。目标是制作适用于 Obsidian 的信息副本，不是艺术性临摹。默认使用环境为已启用 SVG Editor 插件的 Obsidian。

## 保真顺序与停止条件

按以下优先级保留：

1. 印刷文字、数值、单位、来源和图注；
2. 明确的信息关系；
3. 拓扑、分组、相对位置与方向；
4. 视觉样式。

不要模仿纸张纹理、拍摄透视、阴影、虚焦或印刷瑕疵。不得补画照片里看不到的箭头、节点、单元格、数值、边界或因果关系。若照片不足以支持可靠拓扑，应停止绘图，改用结构化转录并注明不确定性。

## Obsidian SVG Editor 外壳

每个 SVG 单独放入一个不缩进的代码围栏，语言标识必须准确写成小写 `svg`。不得把围栏或 SVG 包在 `div`、`figure`、引用块、列表项或其他 HTML 元素内。起始标签保持在同一行：

````markdown
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="100%" role="img" aria-labelledby="visual-title visual-desc">
  <title id="visual-title">原印刷标题或中性对象名</title>
  <desc id="visual-desc">简要说明所编码的信息结构。</desc>
  <rect data-role="canvas-background" x="0" y="0" width="800" height="500" fill="#F5F7FA" fill-opacity="1" stroke="#000000" stroke-opacity="0.08" stroke-width="1"/>
  ...
</svg>
```
````

要求：

- 必须有 `viewBox`、`width="100%"`、`<title>` 与 `<desc>`。由插件依据 `viewBox` 计算响应式高度，不写固定像素高度。
- `<title>`/`<desc>` 元数据之后的第一个图形子元素必须是覆盖完整画布的 `<rect data-role="canvas-background">`：`x`/`y` 为 `0`，`width`/`height` 与 `viewBox` 尺寸一致，填充严格为 `#F5F7FA` 且 100% 不透明，描边严格为 `#000000` 且 8% 不透明。除非原图确需更明显边框，否则使用 `stroke-width="1"`。
- 只使用基础 SVG 元素：`g`、`line`、`polyline`、`polygon`、`path`、`rect`、`circle`、`ellipse`、`text`。
- 不使用脚本、外部样式表、外部字体、`foreignObject` 或嵌入/外链图片。
- 由于画布有意固定且不透明，不继承宿主主题色，也不使用 `currentColor`、CSS 变量、`light-dark()` 或宿主编辑器主题类。SVG 内使用明确深色前景：正文文字/主要描边默认 `#1F2328`，次级描边 `#57606A`，弱化参考线 `#8C959F`，中性填充可用 `#D0D7DE`/`#AFB8C1`。透明度只用于表达层级，不得让关键信息变淡难读。
- 若原图确实以颜色承载数据，必须同时用标签、线型或纹理冗余编码。只有在固定原色确有必要且已核实时，才给根节点添加 `data-allow-fixed-color="true"`。

## 绘制层序

除非原图明确要求遮叠，否则按以下顺序：

1. 背景参考线与关系线；
2. 形状、平面或节点；
3. 内部分隔；
4. 标签与数值；
5. 最外轮廓。

层序不能替代正确几何。即使节点透明，连接线也必须缩短到边界外。

## 连接线端点

连接线必须终止于圆、椭圆或矩形边界，并留出 2–6 个坐标单位的视觉间隙。不得先画中心到中心的线，再靠不透明填充遮住错误。

使用 `scripts/svg_geometry.py` 计算确定性端点：

```bash
python3 scripts/svg_geometry.py circle-endpoint --source 250,220 --center 250,90 --radius 65 --gap 4
python3 scripts/svg_geometry.py ellipse-endpoint --source 250,220 --center 400,150 --rx 75 --ry 50 --gap 4
python3 scripts/svg_geometry.py rect-endpoint --source 250,220 --center 400,150 --width 140 --height 70 --gap 4
```

给需要自动校验的几何加元数据：

```html
<line data-role="connector" data-from="hub" data-to="node-a" x1="..." y1="..." x2="..." y2="..."/>
<circle data-node-id="node-a" cx="..." cy="..." r="..."/>
```

若一端是自由汇聚点而非形状，可省略相应的 `data-from` 或 `data-to`。只有原印刷图明确如此表达时，连接线才可进入节点内部。

## 分层与伪三维图

将每个可见平面视为具有同一坐标系的多边形；所有共边和分隔线都从同一组坐标派生。

- 先确定顶面、正面和侧面多边形，再放文字。
- 共边必须复用完全相同的端点，不重复画几条“几乎相等”的线。
- 所有平行深度边保持一致投影偏移。
- 平面上的分隔线必须起止于该平面；应裁剪，而非延长后遮盖。
- 不得为了制造立体感，凭空加入竖直折点、拐线或深度线。
- 通过分组、透明度和元数据区分语义流程箭头与装饰性深度边。

必要时使用裁剪辅助：

```bash
python3 scripts/svg_geometry.py clip-segment \
  --start 620,430 --end 555,480 \
  --polygon '390,480;455,430;790,430;725,480' --inset 1
```

给平面几何加元数据：

```html
<polygon data-plane-id="range-top" points="390,480 455,430 790,430 725,480"/>
<line data-role="partition" data-plane="range-top" x1="620" y1="430" x2="555" y2="480"/>
```

## 统计图与坐标图

- 只编码印刷数值。曲线没有标值时，只保留相对变化，不臆造坐标或插值。
- 保留原有坐标轴、单位、图例、基线、阈值虚线和预测标记。
- 数值标签不得与图形或彼此碰撞；空间不足时扩展 `viewBox`，或用明确引线把标签移到外部。
- 使用冗余编码：每个系列都要有文字标签，同时以形状、虚实线或位置区分，不能只靠深浅。
- 只要原图给出精确数值，统计 SVG 后必须附紧凑数据表。

## 文字与布局

- 标签优先逐字保留；只有空间确实不足时才用多个 `<tspan>` 换行。
- 文字与边界、连接线之间要留足间距，不允许线穿过标签。
- 邻近和包围本身就是关系，优先保留，再处理装饰性对齐。
- 结构化转录应描述相对空间关系；除非原图给出尺度，否则不得声称精确比例。

## 必做校验

完成草稿后运行：

```bash
python3 scripts/validate_visual_markdown.py path/to/note.md --strict
```

随后在 Obsidian 实时预览和阅读视图中，以正常/放大比例及应用明暗主题检查渲染，确认 SVG Editor 在两种视图均能呈现围栏。可选检查 VS Code 或 Cursor；若未安装 SVG 围栏扩展，它们可能只显示代码块，结构化转录仍作为可移植兜底。脚本可验证围栏/画布结构与带标签几何；文字遮挡、语义保真及与原照片的对照仍需人工检查。

最终图表语义单元还必须附结构化转录，确保在不渲染围栏 SVG 的编辑器中信息仍可读取。
