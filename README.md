# docx-pro: Professional Markdown to DOCX Converter

An all-in-one Agent Skill and CLI tool for converting Markdown to publication-grade Microsoft Word (`.docx`) documents with native OMML vector math, ultra-HD 300 DPI diagrams, and customizable corporate/academic templates.

## Key Features

1. **Native Microsoft OMML Formulas**:
   - Converts LaTeX formulas into true native Word vector formulas (`<m:oMath>`), eliminating ugly raster images or garbled Unicode characters.
   - Automatic 3-column academic alignment: formulas are centered with right-aligned numbering `(1)`.

2. **Ultra-HD Diagrams & Charts (300 DPI)**:
   - Compiles Mermaid diagrams (flowcharts, sequence diagrams, state machines) via Playwright headless Chromium.
   - Enforces **4x super-resolution sampling** with embedded **300 DPI print-grade metadata**.
   - Applies strict layout rules: fixed 14.0cm page-width constraint, proportional aspect-ratio scaling, and 16.0cm max-height page-break prevention.

3. **Strict Engineering Typography**:
   - **Body text**: SimSun (宋体) + Times New Roman, 1.5x line spacing.
   - **Headings & Code/Diagrams**: SimHei (黑体) + Helvetica Neue (eliminates unwanted DengXian/等线 fallback).
   - **Captions**: Centered, single-run, 9pt (小五), bold SimHei + Helvetica Neue.

4. **Template Support**:
   - Built-in templates: `@spec` (Engineering specifications), `@tech_doc` (Technical proposals), `@paper` (Academic papers), `@report` (Progress reports), `@gov_notice` (Official dispatches), and `@default`.
   - Supports passing custom corporate `.docx` reference templates.

## Prerequisites

- Python 3.9+
- Pandoc (`pandoc >= 2.0`)
- Node.js & Playwright:
  ```bash
  pip install playwright Pillow lxml defusedxml
  playwright install chromium
  ```

## Usage

```bash
# Basic usage with the default tech_doc template
python bin/docx_pro.py input.md -o output.docx

# Using the engineering specification template
python bin/docx_pro.py input.md -o output.docx -t spec

# Using a custom Word template
python bin/docx_pro.py input.md -o output.docx --custom-template /path/to/template.docx
```
