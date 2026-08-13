# reading-notes-extractor

从书籍页面照片中提取**人工标注过**的段落与可视化对象（表格、矩阵、统计图、流程图、地图、插图等），按原书目录章节归类，输出结构化 Markdown 读书笔记。忠实转录原文并保留图表显式结构，不总结、不改写、不臆造数据或关系。

## 文件

- `SKILL.md` — skill 主文件（执行以此为准）
- `references/workflow.md` — 完整分步流程与跨页拼接记法
- `references/visual-extraction.md` — 图表选择范围、呈现路由、文字降级与三道质量门
- `references/svg-reconstruction.md` — Obsidian SVG Editor 围栏、固定画布、几何构造和校验约定
- `references/output-templates.md` — Markdown 模板、上标页码映射、识别说明格式
- `scripts/svg_geometry.py` — 连接端点、投影与平面裁剪的确定性计算辅助
- `scripts/validate_visual_markdown.py` — 表格、SVG 可移植性及带标签几何校验
- `*.zh.md` — 以上各文件的中文参考译本

## 安装

下载本目录打包成的 `.skill` 文件后，在支持 skill 导入的客户端中安装即可。新会话上传书籍目录页 + 正文页即可触发；在 Codex 中也可用 `$reading-notes-extractor` 显式调用。

## 使用要点

- 一本书一会话（skill 每会话独立、无跨会话记忆）；跨会话续接时，把上一版 md 一并上传作为上下文。
- 非简体中文书籍会先确认记录方式（保持原文 / 转简体）再开始提取。
- 星号、箭头等标记明确指向整张图表时，视为选中整个图表；用户声明“全部图表”后，每张已提供照片里的所有图表都纳入当前书籍会话范围。
- 默认生成单一 Markdown 文件：简单表格用兼容性 Markdown，统计图和结构图在可靠时使用 Obsidian SVG Editor 可识别的 `svg` 围栏，并始终附可搜索结构化转录。
- 默认不保存截图、图片链接或 Base64。只有用户明确要求证据模式时才为每个对象保存一张忠实裁图。
- SVG 首层使用 `#F5F7FA` 100% 填充及 `#000000` 8% 描边的固定画布，内部采用明确深色前景；连接线按形状边界计算，分层平面共边复用并裁剪内部分隔线。
- 交付前运行 `python3 scripts/validate_visual_markdown.py <文档.md> --strict`，并在 Obsidian 实时预览和阅读视图、应用明暗主题中做目视检查。
