# docx-pro: 专业 Markdown 转 Word (DOCX) 排版生成器

专为技术人员与 AI Agent 打造的专业级 Word 文档生成工具。深度融合了企业级排版模板、微软原生 OMML 矢量数学公式、300 DPI 印刷级高清流程图渲染以及严格的中文出版级字体规范。

[English README](README.md) | [中文说明文档](README_ZH.md)

---

## 🌟 核心特性

### 1. 微软原生矢量数学公式 (OMML)
- 拒绝将公式渲染为低清位图或容易错位的 Unicode 字符。
- 自动提取 Markdown 中的块级与行内 LaTeX 公式（如 `$$...$$`），直接编译为 Word 官方原生的 **OMML 矢量公式 (`<m:oMath>`)**，支持在 Word 中使用原生公式编辑器二次编辑。
- 自动应用学术标准的三列无边框表格排版：**公式本体严格居中，公式编号如 `(1)` 严格靠右对齐**。

### 2. 印刷级 300 DPI 真流程图引擎
- 自动识别 Markdown 中的 ````mermaid` 代码块，告别纯文本拼凑的伪流程图。
- 内置 Playwright 无头浏览器与超采样渲染引擎：
  - **4x 超分辨率采样**（像素分辨率达 5000px+，线条与汉字绝无发虚毛刺）。
  - **打入 300 DPI 印刷出版级物理密度元数据**。
- **严格版面尺寸约束**：所有图片强制锁定为标准版心宽度（14.0cm）居中展示，自适应原图比例，并设置 16.0cm 防跨页高度限幅。
- **规范题注（Caption）**：自动在图下方生成规范的居中图题注（格式如 `图 1 飞拍系统全链路时序交互图`），采用小五号 9pt、加粗【黑体 + Helvetica Neue】单 Run 渲染。

### 3. 严谨的中文出版级字体系统
- **正文规范**：标准宋体（SimSun）+ Times New Roman，1.5 倍行距，段落严格首行缩进 2 字符。
- **标题规范**：黑体（SimHei）+ Helvetica Neue，层级大纲清晰，段前段后间距经工程微调。
- **代码与图表文本**：彻底剔除 Word 默认模板残留的等线体（DengXian），全量统一为【黑体 + Helvetica Neue】。

### 4. 丰富的预设模板与企业私有模板扩展
- 内置开箱即用模板：
  - `@spec`：**工程技术说明书/产品设计手册**（复刻自真实工业级说明书规范）。
  - `@tech_doc`：**系统架构设计书 / 技术方案 / PRD**。
  - `@paper`：**学术论文 / 毕业设计 / 课程设计**。
  - `@report`：**工作周报 / 月报 / 项目里程碑汇报**。
  - `@gov_notice`：**机关公文 / 标准通知红头体例**。
  - `@default`：通用中文文档模板。
- **支持企业私有模板**：可传入你单位或学校现成的 `.docx` 模板，直接继承其排版样式。

---

## 🛠️ 环境依赖与安装

- Python 3.9+
- Pandoc (`pandoc >= 2.0`)
- 运行时依赖包：
  ```bash
  pip install playwright Pillow lxml defusedxml
  playwright install chromium
  ```

---

## 🚀 使用指南

### 1. 基础命令行调用

```bash
# 使用默认技术方案模板 (@tech_doc)
python bin/docx_pro.py input.md -o output_V1.0.docx

# 使用工程技术说明书模板 (@spec)
python bin/docx_pro.py input.md -o output_V1.0.docx -t spec

# 使用学术论文模板 (@paper)
python bin/docx_pro.py input.md -o output_V1.0.docx -t paper

# 使用自定义企业/单位模板
python bin/docx_pro.py input.md -o output_V1.0.docx --custom-template /path/to/your_template.docx
```

### 2. 作为 Agent Skill 使用

在支持 Agent 规范的工具（如 Pi / Codex / Claude Code）中，直接将本仓库克隆至 `~/.agents/skills/docx-pro` 即可被大模型自动感知调用：

```bash
git clone https://github.com/GycUWU/docx-pro.git ~/.agents/skills/docx-pro
```

---

## 📄 许可证

MIT License
