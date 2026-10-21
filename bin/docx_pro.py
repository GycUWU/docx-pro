#!/usr/bin/env python3
"""
docx-pro: Professional Markdown to DOCX Converter with Word Native Formulas, Ultra-HD Vector Diagrams, Fixed Image Layout & Beautiful Templates.
Combines toolflow-labs/markdown2word (styles & templates) + docx-editor-cn (OMML native math) + Playwright 300DPI Rendering Engine + Strict Image & Caption Formatting.
"""

import sys
import os
import re
import argparse
import subprocess
import shutil
import base64
import json
import urllib.request
from pathlib import Path
from PIL import Image

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SKILL_DIR / "templates"
SCRIPTS_DIR = SKILL_DIR / "scripts"

sys.path.insert(0, str(SCRIPTS_DIR))

STANDARD_WIDTH_EMU = 5270500
DEFAULT_ASPECT_RATIO = 16 / 9

def render_mermaid_to_hd_png(mermaid_code: str, output_png_path: Path):
    payload = {"code": mermaid_code}
    json_str = json.dumps(payload)
    encoded = base64.b64encode(json_str.encode("utf-8")).decode("ascii")
    url = f"https://mermaid.ink/svg/{encoded}"
    
    proxy_handler = urllib.request.ProxyHandler({"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"})
    opener = urllib.request.build_opener(proxy_handler)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    with opener.open(req, timeout=20) as res:
        svg_content = res.read().decode("utf-8")

    from playwright.sync_api import sync_playwright
    html = f"""<!DOCTYPE html>
<html>
<head>
  <style>
    body {{
      margin: 0;
      padding: 16px;
      background: white;
      display: inline-block;
      font-family: "Helvetica Neue", "SimHei", Arial, sans-serif;
    }}
    svg {{
      width: 1400px;
      height: auto;
    }}
  </style>
</head>
<body>
  {svg_content}
</body>
</html>"""
    
    temp_raw_png = output_png_path.with_suffix(".raw.png")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(device_scale_factor=4)
        page.set_content(html)
        element = page.locator("svg")
        element.screenshot(path=str(temp_raw_png))
        browser.close()

    im = Image.open(temp_raw_png)
    im.save(str(output_png_path), dpi=(300, 300))
    if temp_raw_png.exists():
        temp_raw_png.unlink()

def convert(input_md: str, output_docx: str, template: str = "tech_doc", custom_template: str = None):
    input_path = Path(input_md).resolve()
    output_path = Path(output_docx).resolve()
    
    if not input_path.exists():
        print(f"Error: input file {input_md} does not exist", file=sys.stderr)
        sys.exit(1)

    if custom_template:
        tpl_path = Path(custom_template).resolve()
    else:
        t_name = template.lstrip("@")
        tpl_candidates = [
            TEMPLATES_DIR / f"{t_name}_zh.docx",
            TEMPLATES_DIR / f"{t_name}.docx",
            TEMPLATES_DIR / f"default_zh.docx"
        ]
        tpl_path = None
        for cand in tpl_candidates:
            if cand.exists():
                tpl_path = cand
                break
        if not tpl_path:
            tpl_path = TEMPLATES_DIR / "tech_doc_zh.docx"

    print(f"[*] 使用 Word 模板: {tpl_path.name}")
    print(f"[*] 解析并处理 Markdown 内容...")

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    temp_dir = Path("temp_docx_pro_build")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

    mermaid_pattern = re.compile(r'```mermaid\n(.*?)\n```', re.DOTALL)
    mermaid_blocks = []
    
    def infer_caption_name(code: str, idx: int):
        if "sequenceDiagram" in code:
            return f"图 {idx} 飞拍系统全链路时序交互图"
        elif "stateDiagram" in code:
            return f"图 {idx} 实时内核锁存状态迁移流程图"
        elif "graph" in code or "flowchart" in code:
            return f"图 {idx} 业务流程控制图"
        return f"图 {idx} 架构与流程图"

    def mermaid_replacer(match):
        idx = len(mermaid_blocks) + 1
        m_code = match.group(1).strip()
        mermaid_blocks.append((idx, m_code))
        img_filename = f"diagram_{idx}.png"
        img_file = temp_dir / img_filename
        caption_text = infer_caption_name(m_code, idx)
        try:
            print(f"[*] 发现流程图代码块 [{idx}]，执行 4x 超采样 + 300DPI 编译...")
            render_mermaid_to_hd_png(m_code, img_file)
            return f"\n\n![]({img_filename})\n\n[DOCX_PRO_CAPTION_{idx}:{caption_text}]\n\n"
        except Exception as e:
            print(f"[!] 流程图渲染失败，降级保留代码块: {e}")
            return match.group(0)

    content = mermaid_pattern.sub(mermaid_replacer, content)

    formula_pattern = re.compile(r'\$\$(.*?)\$\$', re.DOTALL)
    formulas = []
    
    def formula_replacer(match):
        idx = len(formulas) + 1
        formula_latex = match.group(1).strip()
        formulas.append((idx, formula_latex))
        return f"\n\n[DOCX_PRO_FORMULA_{idx}]\n\n"

    processed_md = formula_pattern.sub(formula_replacer, content)

    temp_md = temp_dir / "preprocessed.md"
    temp_docx = temp_dir / "base.docx"
    unpacked_dir = temp_dir / "unpacked"

    with open(temp_md, "w", encoding="utf-8") as f:
        f.write(processed_md)

    print(f"[*] 应用模板样式与图片排版...")
    pandoc_cmd = [
        "pandoc",
        str(temp_md.name),
        f"--reference-doc={str(tpl_path)}",
        "-o",
        str(temp_docx.name)
    ]
    subprocess.run(pandoc_cmd, cwd=str(temp_dir), check=True)

    print(f"[*] 执行底层 XML 深度优化（图片固定规格化 + 题注纯黑体注入 + 公式注入）...")
    unpack_script = SCRIPTS_DIR / "office" / "unpack.py"
    subprocess.run([sys.executable, str(unpack_script), str(temp_docx), str(unpacked_dir)], check=True)

    if formulas:
        print(f"[*] 检测到 {len(formulas)} 个独立数学公式，正在注入微软原生 OMML 矢量公式...")
        formula_script = SCRIPTS_DIR / "formula.py"
        for idx, latex in formulas:
            anchor = f"[DOCX_PRO_FORMULA_{idx}]"
            subprocess.run([
                sys.executable,
                str(formula_script),
                str(unpacked_dir),
                latex,
                str(idx),
                "--anchor",
                anchor
            ], check=True)

    doc_xml = unpacked_dir / "word" / "document.xml"
    with open(doc_xml, "r", encoding="utf-8") as f:
        d_xml = f.read()

    for idx, _ in formulas:
        d_xml = d_xml.replace(f"[DOCX_PRO_FORMULA_{idx}]", "")

    # (A) 图片尺寸规格化：固定居中 14.0cm，高度限幅 16.0cm
    def fix_image_extent(match):
        orig_cx = int(match.group(1))
        orig_cy = int(match.group(2))
        target_cx = 5040000
        target_cy = int(target_cx * (orig_cy / orig_cx)) if orig_cx > 0 else 2835000
        if target_cy > 5760000:
            target_cy = 5760000
            target_cx = int(target_cy * (orig_cx / orig_cy))
        return f'<wp:extent cx="{target_cx}" cy="{target_cy}"/>'

    d_xml = re.sub(r'<wp:extent\s+cx="(\d+)"\s+cy="(\d+)"/>', fix_image_extent, d_xml)

    def fix_a_ext(match):
        orig_cx = int(match.group(1))
        orig_cy = int(match.group(2))
        target_cx = 5040000
        target_cy = int(target_cx * (orig_cy / orig_cx)) if orig_cx > 0 else 2835000
        if target_cy > 5760000:
            target_cy = 5760000
            target_cx = int(target_cy * (orig_cx / orig_cy))
        return f'<a:ext cx="{target_cx}" cy="{target_cy}"/>'

    d_xml = re.sub(r'<a:ext\s+cx="(\d+)"\s+cy="(\d+)"/>', fix_a_ext, d_xml)

    # (B) 图片段落强制居中
    def center_drawing_paragraph(match):
        p_content = match.group(0)
        if "<w:jc" not in p_content:
            p_content = re.sub(r'(<w:pPr>.*?)', r'\1<w:jc w:val="center"/>', p_content)
        else:
            p_content = re.sub(r'<w:jc\s+w:val="[^"]*"/>', '<w:jc w:val="center"/>', p_content)
        return p_content

    d_xml = re.sub(r'<w:p\b[^>]*>(?:(?!</w:p>).)*?<w:drawing>.*?</w:p>', center_drawing_paragraph, d_xml, flags=re.DOTALL)

    # (C) 彻底统一题注：不管是指令标记还是已有的 af8 段落，强制抹平所有子元素，重建为绝对单 Run 纯黑体段落！
    def build_unified_caption(raw_p):
        all_text = "".join(re.findall(r'<w:t[^>]*>(.*?)</w:t>', raw_p))
        all_text = re.sub(r'\[DOCX_PRO_CAPTION_\d+:([^\]]+)\]', r'\1', all_text)
        all_text = all_text.strip()
        if not all_text:
            return ""
        caption_rfonts = '<w:rFonts w:ascii="Helvetica Neue" w:hAnsi="Helvetica Neue" w:eastAsia="SimHei" w:cs="Helvetica Neue"/>'
        return f'<w:p><w:pPr><w:pStyle w:val="af8"/><w:jc w:val="center"/><w:spacing w:before="60" w:after="160" w:line="240" w:lineRule="auto"/><w:ind w:firstLine="0"/></w:pPr><w:r><w:rPr>{caption_rfonts}<w:b/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr><w:t xml:space="preserve">{all_text}</w:t></w:r></w:p>'

    # 替换两处可能的题注源
    d_xml = re.sub(r'<w:p\b[^>]*>(?:(?!</w:p>).)*?\[DOCX_PRO_CAPTION_\d+:[^\]]+\].*?</w:p>', lambda m: build_unified_caption(m.group(0)), d_xml, flags=re.DOTALL)
    d_xml = re.sub(r'<w:p\b[^>]*>(?:(?!</w:p>).)*?<w:pStyle\s+w:val="af8"/>.*?</w:p>', lambda m: build_unified_caption(m.group(0)), d_xml, flags=re.DOTALL)

    # (D) 代码块文本字体注入
    target_rfonts = '<w:rFonts w:ascii="Helvetica Neue" w:hAnsi="Helvetica Neue" w:eastAsia="SimHei" w:cs="Helvetica Neue"/>'
    def inject_fonts_to_rpr(match):
        rpr_content = match.group(0)
        if "w:rFonts" in rpr_content:
            return re.sub(r'<w:rFonts[^>]*/>', target_rfonts, rpr_content)
        return rpr_content.replace('</w:rPr>', target_rfonts + '</w:rPr>')

    d_xml = re.sub(r'<w:rPr>(?:(?!</w:rPr>).)*?<w:rStyle\s+w:val="VerbatimChar"/>.*?</w:rPr>', inject_fonts_to_rpr, d_xml, flags=re.DOTALL)

    with open(doc_xml, "w", encoding="utf-8") as f:
        f.write(d_xml)

    pack_script = SCRIPTS_DIR / "office" / "pack.py"
    cwd = SCRIPTS_DIR / "office"
    subprocess.run([
        sys.executable,
        str(pack_script),
        str(unpacked_dir.resolve()),
        str(output_path.resolve()),
        "--validate", "false"
    ], cwd=cwd, check=True)

    shutil.rmtree(temp_dir, ignore_errors=True)
    print(f"[SUCCESS] 成功生成符合工程出版规范的 Word 文档: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Professional Markdown to Word (.docx) Converter with Math, Ultra-HD Diagrams & Template Support.")
    parser.add_argument("input", help="Input Markdown file (.md)")
    parser.add_argument("-o", "--output", required=True, help="Output Word document (.docx)")
    parser.add_argument("-t", "--template", default="tech_doc", help="Template name: tech_doc, paper, report, gov_notice, default, spec")
    parser.add_argument("--custom-template", help="Path to custom reference .docx template")

    args = parser.parse_args()
    convert(args.input, args.output, args.template, args.custom_template)

if __name__ == "__main__":
    main()
