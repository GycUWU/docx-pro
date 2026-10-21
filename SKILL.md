---
name: docx-pro
description: "Professional Word document generator and formatter with native OMML math formulas, three-line tables, and enterprise-grade Chinese templates (tech_doc, paper, report, gov_notice, default). Use whenever creating or converting Markdown to polished Word (.docx) documents, especially when documents contain mathematical formulas, academic citations, or require custom enterprise templates."
---

# docx-pro: All-in-One Professional Word Generator

Combines enterprise template styling (`toolflow-labs/markdown2word`) with native Word mathematical formula processing (`docx-editor-cn`).

## 1. Core Capabilities

1. **Native Mathematical Formulas (OMML)**:
   - Compiles both block (`$$...$$`) and inline math into native Word OMML vector formulas (`<m:oMath>`).
   - Automatically layouts block formulas with standard academic 3-column borderless tables (formula centered, equation number right-aligned).
   - Never outputs ugly Unicode approximations or image snapshots.

2. **Enterprise & Academic Built-in Templates**:
   - `@tech_doc`: Technical proposals, system architecture, PRDs, engineering design.
   - `@paper`: Academic thesis, course designs, graduation projects.
   - `@report`: Weekly/Monthly reports, project milestones, executive summaries.
   - `@gov_notice`: Standard administrative notices and government dispatches.
   - `@default`: General Chinese document style.

3. **Custom Enterprise Template Support**:
   - Directly inject custom corporate/university `.docx` templates to match mandatory corporate font, color, and heading specifications.

---

## 2. Usage Guide

### Basic Command

```bash
python ~/.agents/skills/docx-pro/bin/docx_pro.py input.md -o output.docx -t tech_doc
```

### Options

- `-o, --output`: Target `.docx` file path.
- `-t, --template`: Template identifier: `tech_doc` (default), `paper`, `report`, `gov_notice`, `default`.
- `--custom-template`: Path to a custom user `.docx` template.

---

## 3. Workflow Implementation

1. **Markdown AST & Math Extraction**: Extracts LaTeX formula blocks and marks alignment anchors.
2. **Template Style Binding**: Injects paragraphs, headings, bullet lists, and tables into the chosen Word template.
3. **OpenXML Unpack & OMML Injection**: Unpacks the document container, converts LaTeX via Pandoc into OMML `<m:oMath>`, and injects into standard numbered formula tables.
4. **Pack & Validation**: Compiles the modified XML tree back into a validated, portable `.docx` archive.
