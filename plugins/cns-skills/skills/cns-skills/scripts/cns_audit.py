#!/usr/bin/env python3
"""CNS manuscript triage: evidence risks, repetition, and prose-pattern diagnostics.

This is deliberately not an AI detector. It uses transparent heuristics to identify
passages that deserve human review. It reads UTF-8 text/Markdown and DOCX files
using only the Python standard library.
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import re
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterable
from xml.etree import ElementTree as ET

VERSION = "0.7.0"
CROSSREF_PUBLIC_INTERVAL_SECONDS = 0.22

STOCK_PATTERNS: dict[str, str] = {
    "zh_this_shows": r"这(?:一结果|些结果|一发现)?(?:说明|表明|提示)",
    "zh_note": r"(?:值得注意的是|需要指出的是|不难发现)",
    "zh_future": r"未来(?:仍)?(?:需要|需|应当|可以|有必要)",
    "zh_significance": r"(?:具有|有着)(?:重要|重大)(?:的)?(?:意义|价值)",
    "zh_new_path": r"(?:提供|开辟)了?(?:一种)?新的?(?:思路|路径|可能性)",
    "zh_prospect": r"(?:广阔|巨大)(?:的)?(?:前景|潜力)",
    "en_note": r"\b(?:it is important to note that|notably|it should be noted that)\b",
    "en_landscape": r"\bin (?:today's|the) (?:rapidly )?evolving landscape\b",
    "en_hype": r"\b(?:revolutioni[sz]e|transformative|game[- ]changer|pave the way|unlock)\b",
    "en_future": r"\bfurther research is (?:needed|required)\b",
}

CONTRAST_PATTERNS: dict[str, str] = {
    "zh_not_but": r"不是.{0,45}?而是",
    "zh_not_only": r"不仅.{0,60}?(?:而且|还|也)",
    "en_not_but": r"\bnot\s+.{1,80}?\s+but\b",
    "en_not_only": r"\bnot only\s+.{1,100}?\s+but also\b",
}

# These patterns are deliberately narrower than a word list. The terms below
# can be correct scientific language; the audit flags compound editorial labels
# that often leak from a writer's planning notes into finished review prose.
SCAFFOLD_PATTERNS: dict[str, str] = {
    "zh_evidence_scaffold": (
        r"(?:证据链|证据剖面|证据矩阵|证据图谱|证据轴|证据层|证据边界|"
        r"(?:核心)?证据卡|证据拼接|拼接证据|编织证据)"
    ),
    "zh_generic_framework": (
        r"(?:本文|本综述|我们).{0,30}?(?:提出|构建|建立|采用|使用).{0,18}?"
        r"(?:统一|综合|比较|分析|决策)?框架"
    ),
    "zh_abstract_glue": r"(?:全链条|逻辑闭环|研究图谱|方法图谱|赋能.{0,12}?(?:研究|设计|创新))",
    "en_evidence_scaffold": (
        r"\b(?:evidence chain|evidence profile|evidence matrix|evidence landscape|"
        r"evidence layer|evidence axis|evidence boundary|evidence card|"
        r"evidence[- ]cent(?:er|re)ed)\b"
    ),
    "en_generic_framework": (
        r"\b(?:this review|we)\s+(?:therefore\s+)?(?:propose|present|establish|"
        r"introduce|adopt|use|develop)\b.{0,70}?\b(?:unified |comparison |"
        r"decision[- ]cent(?:er|re)ed )?framework\b"
    ),
    "en_evidence_stitching": r"\b(?:stitch|weav|assembl|bridg)\w*\s+(?:the\s+)?evidence\b",
    "en_abstract_landscape": r"\b(?:rapidly evolving|research|current|broader) landscape\b",
}

# These patterns target material that usually belongs in an author/editor
# handoff, not the reader-visible manuscript. They are anchored or action-based
# so ordinary scientific headings and uses of words such as "author" or
# "analysis" are not flagged by themselves.
READER_VISIBLE_PATTERNS: dict[str, dict[str, str]] = {
    "zh_analysis_label": {
        "pattern": (
            r"(?m)^[ \t]*(?:#{1,6}[ \t]+)?(?:中心判断|编辑判断|审稿判断|内部判断|"
            r"作者侧判断|编辑评估|审稿评估|内部分析|分析备注)[ \t]*[：:]?[ \t]*$"
        ),
        "reason": "The standalone label records an editorial or analytical judgment rather than naming manuscript content.",
        "action": "Move the judgment to the author decision log, or replace the label and prose with the scientific conclusion itself.",
    },
    "en_analysis_label": {
        "pattern": (
            r"(?mi)^[ \t]*(?:#{1,6}[ \t]+)?(?:central judgment|editorial judgment|"
            r"editorial assessment|reviewer assessment|internal analysis|analysis note)"
            r"[ \t]*[:：]?[ \t]*$"
        ),
        "reason": "The standalone label exposes an editor-facing assessment in reader-visible prose.",
        "action": "Move it to the handoff, or state the underlying scientific conclusion under a content heading.",
    },
    "zh_author_prompt": {
        "pattern": (
            r"(?m)^[ \t]*(?:#{1,6}[ \t]+)?(?:作者提示|作者注意|作者待确认|待作者确认|"
            r"写作提示|修改提示|修改建议|编辑提示|编辑备注|给作者的建议)"
            r"(?:[ \t]*[：:][^\r\n]{0,100})?[ \t]*$"
        ),
        "reason": "This is an author-facing prompt or revision label, not part of the scholarly argument.",
        "action": "Resolve it or move it to comments, tracked changes, or the decision log before creating the clean manuscript.",
    },
    "en_author_prompt": {
        "pattern": (
            r"(?mi)^[ \t]*(?:#{1,6}[ \t]+)?(?:note to (?:the )?author|author query|"
            r"author action|required author action|revision note|editor note|editorial note|"
            r"writing prompt)(?:[ \t]*[:：][^\r\n]{0,100})?[ \t]*$"
        ),
        "reason": "This heading belongs to an author/editor exchange rather than the submission text.",
        "action": "Resolve or relocate it outside the reader-visible artifact.",
    },
    "zh_agent_prompt": {
        "pattern": (
            r"(?mi)^[ \t]*(?:#{1,6}[ \t]+)?(?:AI提示|AI助手备注|助手备注|模型提示|"
            r"模型指令|智能体提示|智能体指令|代理提示)[ \t]*[:：]?[ \t]*$"
        ),
        "reason": "This label exposes model- or agent-facing process scaffolding in the manuscript.",
        "action": "Remove the process label and retain only scientifically warranted manuscript content.",
    },
    "en_agent_prompt": {
        "pattern": (
            r"(?mi)^[ \t]*(?:#{1,6}[ \t]+)?(?:AI assistant note|assistant note|"
            r"assistant analysis|agent note|agent instruction|model instruction|model prompt|"
            r"system prompt)[ \t]*[:：]?[ \t]*$"
        ),
        "reason": "This label exposes model- or agent-facing process scaffolding in the manuscript.",
        "action": "Remove the process label and retain only scientifically warranted manuscript content.",
    },
    "unresolved_placeholder": {
        "pattern": (
            r"(?i)(?:\[(?:TODO|TBD|TK|AUTHOR QUERY|AQ|CITATION NEEDED|INSERT(?: VALUE| TEXT)?|"
            r"VERIFY(?: CITATION| VALUE)?)[^\]\r\n]{0,100}\]|"
            r"\{\{(?:TODO|TBD|INSERT|VERIFY)[^}\r\n]{0,100}\}\})"
        ),
        "reason": "An unresolved production placeholder is visible in the manuscript.",
        "action": "Complete the action or record the unresolved item in the author handoff; do not submit the placeholder.",
    },
    "zh_revision_instruction": {
        "pattern": (
            r"(?:此处|这里|本段)(?:仍)?(?:需要|需|应当|应|可)(?:由作者)?"
            r"(?:补充|核对|确认|填写|插入|删除|改写|展开|压缩|移动)|"
            r"(?:请|建议|待)作者(?:补充|核对|确认|填写|插入|删除|改写)"
        ),
        "reason": "The sentence instructs the author how to revise instead of presenting the revision.",
        "action": "Perform the edit when authorized, or move the instruction to the decision log/comments.",
    },
    "en_revision_instruction": {
        "pattern": (
            r"(?mi)^[ \t]*(?:please[ \t]+)?(?:insert|add|verify|confirm|replace|rewrite|"
            r"expand|shorten|delete)\b[^\r\n]{0,90}\b(?:here|before submission|by the author|"
            r"placeholder|missing (?:citation|reference)|citation needed|figure number|table number)\b"
        ),
        "reason": "The passage reads as an editing instruction rather than manuscript content.",
        "action": "Complete or relocate the instruction before producing the clean artifact.",
    },
    "zh_output_label": {
        "pattern": (
            r"(?m)^[ \t]*(?:#{1,6}[ \t]+)?(?:润色后版本|改写后版本|修改后正文|"
            r"建议替换为|可直接用于正文|可直接粘贴版本)[ \t]*[：:]?[ \t]*$"
        ),
        "reason": "This labels an assistant/editor output variant, not a section of the paper.",
        "action": "Keep only the revised manuscript text and move version commentary to the handoff.",
    },
    "en_output_label": {
        "pattern": (
            r"(?mi)^[ \t]*(?:#{1,6}[ \t]+)?(?:polished version|revised version|"
            r"suggested rewrite|replacement text|manuscript-ready version)[ \t]*[:：]?[ \t]*$"
        ),
        "reason": "This is a workflow/output label rather than a scientific heading.",
        "action": "Remove the label from the clean manuscript and keep only the authorized revision.",
    },
    "zh_manuscript_process_meta": {
        "pattern": (
            r"(?:可|可以|建议)[^。；\r\n]{0,24}?(?:作为|用于|写入|放入)(?:正文|文中)"
            r"[^。；\r\n]{0,18}?(?:阅读)?(?:简写|缩写|标签|提示)"
        ),
        "reason": "The sentence discusses how an editor or author should package text instead of discussing the science.",
        "action": "Remove the process commentary; define and use a necessary scientific term directly, or keep the advice in the handoff.",
    },
    "en_manuscript_process_meta": {
        "pattern": (
            r"(?i)\b(?:can|may|should) be used (?:in|as)[^.;\r\n]{0,28}"
            r"(?:shorthand|abbreviation|reader label)[^.;\r\n]{0,28}(?:manuscript|main text|paper)\b|"
            r"\buse[^.;\r\n]{0,28}(?:shorthand|abbreviation|reader label) in (?:the )?"
            r"(?:manuscript|main text|paper)\b"
        ),
        "reason": "The sentence exposes manuscript-packaging advice rather than scholarly content.",
        "action": "Move the advice to the handoff; define and use any necessary scientific term directly in the manuscript.",
    },
    "zh_unfinished_submission_status": {
        "pattern": (
            r"(?:当前|本)(?:稿件|手稿|综述)(?:仍|尚|还)?(?:未|没有)(?:完成|纳入|补齐|核验|更新)|"
            r"(?:检索|筛选|核验|参考文献)(?:仍|尚|还)(?:未完成|不完整)|"
            r"投稿前[^。；\r\n]{0,80}(?:需要|需|应当|应|必须)(?:完成|补充|核验|更新|定稿)"
        ),
        "reason": "The passage exposes unfinished author-side work or a pre-submission TODO in the manuscript.",
        "action": "Complete the work and report the resulting method/boundary, or move the unresolved task to the handoff.",
    },
    "en_unfinished_submission_status": {
        "pattern": (
            r"(?i)\b(?:the )?(?:current )?(?:manuscript|review|draft)\b[^.;\r\n]{0,45}"
            r"\b(?:has not yet|have not yet|does not yet|remains incomplete|still needs? to)\b|"
            r"\b(?:the )?(?:search|screening|verification|reference check)\b[^.;\r\n]{0,35}"
            r"\b(?:remains incomplete|has not yet been (?:completed|finali[sz]ed))\b|"
            r"\b(?:before|prior to) (?:journal )?submission\b[^.;\r\n]{0,100}"
            r"\b(?:manuscript|search|screening|citation|reference|author|table|figure|format|"
            r"finali[sz]e|complete|update|verify)\w*\b"
        ),
        "reason": "The passage exposes unfinished author-side work or a pre-submission TODO in the manuscript.",
        "action": "Complete the work and report the resulting method/boundary, or move the unresolved task to the handoff.",
    },
    "argument_gap_development_workflow": {
        "pattern": (
            r"(?i)\b(?:papers?|studies|sources|references) (?:were )?(?:added|selected|included)"
            r" to fill (?:specific )?(?:argument|narrative) gaps?\b|"
            r"\b(?:we|the authors) (?:added|selected|included) (?:papers?|studies|sources|references)"
            r" to fill (?:specific )?(?:argument|narrative) gaps?\b|"
            r"(?:为(?:填补|补足)(?:论证|叙事)缺口(?:而)?(?:补充|选择|纳入)(?:论文|研究|来源|文献))"
        ),
        "reason": "The sentence narrates the editor's manuscript-development workflow rather than a reproducible literature method.",
        "action": "Replace it with the actual search, selection, or synthesis method, or keep the development note in the handoff.",
    },
}

INTERNAL_CODE_RANGE_RE = re.compile(
    r"(?<![A-Za-z0-9])([A-Z])(\d{1,2})\s*[-–—~至]\s*(?:\1)?(\d{1,2})(?![A-Za-z0-9])"
)
INTERNAL_CODE_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9])([A-Z])(\d{1,2})(?![A-Za-z0-9])")
INTERNAL_CODE_CUE_RE = re.compile(
    r"(?:阅读)?简写|内部(?:代码|分级|标签)|(?:代码|等级|层级|分级|编码|标签)(?:体系|方案|标准)?|"
    r"(?:本文|本综述|我们).{0,24}?(?:定义|采用|使用|引入|提出|记为|标记为)|"
    r"\b(?:internal codes?|shorthand|grading scheme|tier(?:ing)? scheme|level scheme|coding scheme)\b|"
    r"\b(?:we|this review).{0,30}?(?:define|use|introduce|label|code)\b",
    re.IGNORECASE,
)
PUBLIC_REFERENCE_CUE_RE = re.compile(
    r"(?:supplementary|supporting)\s+(?:figures?|tables?|equations?|appendices)|"
    r"(?:figures?|figs?\.?|tables?|equations?|eqs?\.?|appendices)\s*$",
    re.IGNORECASE,
)

HIGH_RISK_TERMS = re.compile(
    r"首次|首个|前所未有|最优|最佳|显著优于|临床可用|临床有效|安全有效|"
    r"因果|自主闭环|完全自主|普遍适用|state[- ]of[- ]the[- ]art|unprecedented|"
    r"first[- ]ever|clinically effective|causes?|universal|fully autonomous",
    re.IGNORECASE,
)

DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
CITATION_RE = re.compile(
    r"(?:\[(?:\d{1,3}(?:\s*[-,–]\s*\d{1,3})*)\])|"
    r"(?:\((?:[^()]{0,45}?\b(?:19|20)\d{2}[a-z]?[^()]*)\))|"
    r"(?:\b[A-Z][A-Za-z'’\-]+\s+et\s+al\.?,?\s*(?:19|20)\d{2})"
)
NUMBER_RE = re.compile(r"(?<![A-Za-z])(?:\d+(?:\.\d+)?\s*%?|[一二三四五六七八九十]+倍)")
REFERENCE_HEADING_RE = re.compile(
    r"^(?:(?:\d+|[IVX]+)[.)、]?\s*)?(?:references|bibliography|works cited|literature cited|参考文献)$",
    re.IGNORECASE,
)
TABLE_CAPTION_RE = re.compile(r"^(?:table\s+[A-Z]?\d+|表\s*[A-Z]?\d+)", re.IGNORECASE)
PROTECTED_CALLOUT_RE = re.compile(
    r"^(?:(?:box|textbox|case)\s*(?:no\.?\s*)?\d+[A-Z]?|(?:专栏|框)\s*\d+|key points?)\b",
    re.IGNORECASE,
)
TOOL_IDENTITY_RE = re.compile(
    r"\b(?:CNS[ _-]?Skills?|ChatGPT|OpenAI|Codex|Claude(?: Code)?|Gemini|"
    r"GitHub Copilot|python-docx|LibreOffice|Pandoc)\b",
    re.IGNORECASE,
)
FILENAME_CNS_RE = re.compile(r"(?:^|[ _.-])CNS(?:[ _.-]|$)", re.IGNORECASE)
PRODUCTION_TRACE_RE = re.compile(
    r"\b(?:draft|working copy|work in progress|WIP|revision|revised|polished|"
    r"generated|version|v\d+(?:\.\d+)+|TODO|clean copy|literature[- ]expansion edition)\b|"
    r"(?:初稿|工作稿|修订稿|修改稿|润色稿|完善稿|待定稿|版本|生成稿)",
    re.IGNORECASE,
)

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
CP_NS = "{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}"
DC_NS = "{http://purl.org/dc/elements/1.1/}"


def read_docx(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        try:
            xml_parts = [archive.read("word/document.xml")]
        except KeyError as exc:
            raise ValueError("DOCX has no word/document.xml") from exc
        for optional_part in ("word/footnotes.xml", "word/endnotes.xml"):
            if optional_part in archive.namelist():
                xml_parts.append(archive.read(optional_part))
    namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    math_text = "{http://schemas.openxmlformats.org/officeDocument/2006/math}t"
    paragraphs: list[str] = []
    for xml in xml_parts:
        root = ET.fromstring(xml)
        for paragraph in root.iter(namespace + "p"):
            parts: list[str] = []
            for node in paragraph.iter():
                if node.tag in {namespace + "t", math_text} and node.text:
                    parts.append(node.text)
                elif node.tag == namespace + "tab":
                    parts.append("\t")
                elif node.tag in {namespace + "br", namespace + "cr"}:
                    parts.append("\n")
            text = "".join(parts).strip()
            if text:
                paragraphs.append(text)
    return "\n\n".join(paragraphs)


def read_input(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        return read_docx(path)
    if path.suffix.lower() not in {".txt", ".md", ".markdown"}:
        raise ValueError("Supported inputs: .docx, .txt, .md, .markdown")
    return path.read_text(encoding="utf-8-sig")


def prose_analysis_scope(text: str) -> tuple[str, dict[str, Any]]:
    """Exclude the final reference list from prose-rhythm diagnostics by default."""
    paragraphs = split_paragraphs(text)
    reference_indices = [
        index
        for index, paragraph in enumerate(paragraphs)
        if REFERENCE_HEADING_RE.fullmatch(re.sub(r"^#{1,6}\s*", "", paragraph).strip())
    ]
    if not reference_indices:
        return text, {
            "reference_section_excluded": False,
            "analyzed_paragraphs": len(paragraphs),
        }
    index = reference_indices[-1]
    body = "\n\n".join(paragraphs[:index])
    return body, {
        "reference_section_excluded": True,
        "reference_heading": paragraphs[index],
        "analyzed_paragraphs": index,
        "excluded_reference_paragraphs": len(paragraphs) - index - 1,
    }


def _xml_text(element: ET.Element) -> str:
    parts: list[str] = []
    for node in element.iter():
        if node.tag in {W_NS + "t", "{http://schemas.openxmlformats.org/officeDocument/2006/math}t"} and node.text:
            parts.append(node.text)
        elif node.tag == W_NS + "tab":
            parts.append("\t")
        elif node.tag in {W_NS + "br", W_NS + "cr"}:
            parts.append("\n")
    return "".join(parts).strip()


def _attribute(element: ET.Element | None, name: str) -> str | None:
    if element is None:
        return None
    return element.get(W_NS + name)


def _run_size(element: ET.Element | None) -> int | None:
    if element is None:
        return None
    size = element.find(W_NS + "sz")
    if size is None:
        size = element.find(W_NS + "szCs")
    value = _attribute(size, "val")
    if value and value.isdigit():
        return int(value)
    return None


def _style_catalog(styles_root: ET.Element | None) -> tuple[dict[str, dict[str, Any]], int | None]:
    if styles_root is None:
        return {}, None
    default_size = _run_size(styles_root.find(f"{W_NS}docDefaults/{W_NS}rPrDefault/{W_NS}rPr"))
    styles: dict[str, dict[str, Any]] = {}
    for style in styles_root.findall(W_NS + "style"):
        style_id = _attribute(style, "styleId")
        if not style_id:
            continue
        styles[style_id] = {
            "name": _attribute(style.find(W_NS + "name"), "val") or style_id,
            "type": _attribute(style, "type") or "",
            "based_on": _attribute(style.find(W_NS + "basedOn"), "val"),
            "size": _run_size(style.find(W_NS + "rPr")),
        }
    return styles, default_size


def _resolved_style_size(style_id: str | None, styles: dict[str, dict[str, Any]]) -> int | None:
    visited: set[str] = set()
    while style_id and style_id not in visited:
        visited.add(style_id)
        style = styles.get(style_id)
        if not style:
            return None
        if style.get("size") is not None:
            return int(style["size"])
        style_id = style.get("based_on")
    return None


def _effective_run_size(
    run: ET.Element,
    paragraph_style: str | None,
    table_style: str | None,
    styles: dict[str, dict[str, Any]],
    default_size: int | None,
) -> int | None:
    run_properties = run.find(W_NS + "rPr")
    direct_size = _run_size(run_properties)
    if direct_size is not None:
        return direct_size
    run_style = _attribute(run_properties.find(W_NS + "rStyle") if run_properties is not None else None, "val")
    return (
        _resolved_style_size(run_style, styles)
        or _resolved_style_size(paragraph_style, styles)
        or _resolved_style_size(table_style, styles)
        or default_size
    )


def _nonwhite_fills(table: ET.Element) -> list[str]:
    fills: set[str] = set()
    for shading in table.iter(W_NS + "shd"):
        fill = (_attribute(shading, "fill") or "").upper()
        if fill and fill not in {"AUTO", "FFFFFF", "NONE", "NIL"}:
            fills.add(fill)
    return sorted(fills)


def _docx_clean_copy_candidates(path: Path) -> list[dict[str, Any]]:
    """Inspect DOCX packaging and OOXML structures that plain text misses."""
    if path.suffix.lower() != ".docx" or not path.exists():
        return []
    with zipfile.ZipFile(path) as archive:
        document_root = ET.fromstring(archive.read("word/document.xml"))
        styles_root = (
            ET.fromstring(archive.read("word/styles.xml"))
            if "word/styles.xml" in archive.namelist()
            else None
        )
        core_root = (
            ET.fromstring(archive.read("docProps/core.xml"))
            if "docProps/core.xml" in archive.namelist()
            else None
        )

    styles, default_size = _style_catalog(styles_root)
    candidates: list[dict[str, Any]] = []

    filename = path.name
    filename_scan_text = re.sub(r"[_-]+", " ", path.stem)
    filename_production_hits = PRODUCTION_TRACE_RE.findall(filename_scan_text)
    filename_tool_hits = TOOL_IDENTITY_RE.findall(filename)
    if FILENAME_CNS_RE.search(filename) and not filename_tool_hits:
        filename_tool_hits = ["CNS"]
    if filename_tool_hits and filename_production_hits:
        candidates.append(
            {
                "pattern": "filename_tool_identity_trace",
                "count": len(filename_tool_hits),
                "severity": "defect",
                "reason": "The external filename exposes an editing tool or workflow identity.",
                "action": "Rename the clean submission file with only the manuscript title or journal-required identifier.",
                "examples": [filename],
            }
        )
    if filename_production_hits:
        candidates.append(
            {
                "pattern": "filename_production_trace",
                "count": len(filename_production_hits),
                "severity": "defect",
                "reason": "The external filename still identifies a draft, revision, tool output, or internal version.",
                "action": "Use a clean distribution filename and keep version bookkeeping outside the submitted artifact.",
                "examples": [filename],
            }
        )

    if core_root is not None:
        core_fields = {
            "creator": core_root.findtext(DC_NS + "creator") or "",
            "lastModifiedBy": core_root.findtext(CP_NS + "lastModifiedBy") or "",
            "title": core_root.findtext(DC_NS + "title") or "",
            "subject": core_root.findtext(DC_NS + "subject") or "",
            "description": core_root.findtext(DC_NS + "description") or "",
        }
        tool_fields = {
            name: value
            for name, value in core_fields.items()
            if value
            and TOOL_IDENTITY_RE.search(value)
            and (
                name in {"creator", "lastModifiedBy"}
                or (name in {"subject", "description"} and PRODUCTION_TRACE_RE.search(value))
            )
        }
        production_fields = {
            name: value
            for name, value in core_fields.items()
            if name in {"lastModifiedBy", "subject", "description"}
            and value
            and PRODUCTION_TRACE_RE.search(value)
        }
        if tool_fields:
            candidates.append(
                {
                    "pattern": "core_property_tool_identity_trace",
                    "count": len(tool_fields),
                    "severity": "defect",
                    "reason": "A core document property identifies the editing tool or agent.",
                    "action": "Scrub tool identity from core properties while preserving intentional author and title metadata.",
                    "examples": [f"{name}: {value[:160]}" for name, value in tool_fields.items()],
                    "details": sorted(tool_fields),
                }
            )
        if production_fields:
            candidates.append(
                {
                    "pattern": "core_property_production_trace",
                    "count": len(production_fields),
                    "severity": "defect",
                    "reason": "A core document property exposes draft, revision, TODO, or internal version language.",
                    "action": "Replace it with stable publication-facing metadata or clear the field before distribution.",
                    "examples": [f"{name}: {value[:160]}" for name, value in production_fields.items()],
                    "details": sorted(production_fields),
                }
            )

    caption_findings: list[dict[str, Any]] = []
    for paragraph in document_root.iter(W_NS + "p"):
        text = _xml_text(paragraph)
        if not TABLE_CAPTION_RE.match(text):
            continue
        style_id = _attribute(paragraph.find(f"{W_NS}pPr/{W_NS}pStyle"), "val") or ""
        style_name = str(styles.get(style_id, {}).get("name", style_id))
        if re.search(r"(?:^|\s)(?:heading|标题)\s*\d*", f"{style_id} {style_name}", re.IGNORECASE):
            caption_findings.append({"text": text[:180], "style_id": style_id, "style_name": style_name})
    if caption_findings:
        candidates.append(
            {
                "pattern": "table_caption_uses_heading_style",
                "count": len(caption_findings),
                "severity": "defect",
                "reason": "A table title uses a Heading style, which pollutes document hierarchy and navigation.",
                "action": "Apply a Caption/Table Title style while retaining the visible table number and title.",
                "examples": [item["text"] for item in caption_findings[:3]],
                "details": caption_findings,
            }
        )

    tables = list(document_root.iter(W_NS + "tbl"))
    callouts: list[dict[str, Any]] = []
    size_findings: list[dict[str, Any]] = []
    for table_index, table in enumerate(tables, start=1):
        rows = table.findall(W_NS + "tr")
        cells = [cell for row in rows for cell in row.findall(W_NS + "tc")]
        fills = _nonwhite_fills(table)
        paragraphs = list(table.iter(W_NS + "p"))
        paragraph_texts = [text for paragraph in paragraphs if (text := _xml_text(paragraph))]
        label = paragraph_texts[0].rstrip("：:") if paragraph_texts else ""
        table_style = _attribute(table.find(f"{W_NS}tblPr/{W_NS}tblStyle"), "val")

        protected = bool(PROTECTED_CALLOUT_RE.match(label))
        if len(rows) == 1 and len(cells) == 1 and fills and label and not protected:
            callouts.append(
                {
                    "table": table_index,
                    "label": label[:160],
                    "fills": fills,
                    "paragraphs": len(paragraph_texts),
                    "table_style": table_style or "",
                }
            )

        size_records: list[dict[str, Any]] = []
        for row_index, row in enumerate(rows):
            for cell_index, cell in enumerate(row.findall(W_NS + "tc")):
                for paragraph in cell.iter(W_NS + "p"):
                    paragraph_style = _attribute(paragraph.find(f"{W_NS}pPr/{W_NS}pStyle"), "val")
                    for run in paragraph.findall(W_NS + "r"):
                        run_text = _xml_text(run)
                        if not run_text:
                            continue
                        size = _effective_run_size(run, paragraph_style, table_style, styles, default_size)
                        if size is not None:
                            size_records.append(
                                {
                                    "size": size,
                                    "weight": max(1, visible_length(run_text)),
                                    "row": row_index,
                                    "cell": cell_index,
                                    "text": run_text[:80],
                                }
                            )
        size_weights: Counter[int] = Counter()
        for record in size_records:
            size_weights[record["size"]] += record["weight"]
        if len(size_weights) >= 2:
            dominant_size = size_weights.most_common(1)[0][0]
            drift_records = [
                record for record in size_records if abs(record["size"] - dominant_size) >= 4
            ]
            same_cell_sizes: dict[tuple[int, int], set[int]] = {}
            for record in size_records:
                same_cell_sizes.setdefault((record["row"], record["cell"]), set()).add(record["size"])
            within_cell_drift = any(
                max(values) - min(values) >= 4 for values in same_cell_sizes.values() if len(values) >= 2
            )
            body_drift = any(record["row"] > 0 for record in drift_records)
            if drift_records and (within_cell_drift or body_drift or len(rows) == 1):
                size_findings.append(
                    {
                        "table": table_index,
                        "dominant_pt": dominant_size / 2,
                        "sizes_pt": [size / 2 for size in sorted(size_weights)],
                        "examples": [record["text"] for record in drift_records[:3]],
                    }
                )
    if size_findings:
        candidates.append(
            {
                "pattern": "within_table_font_size_drift",
                "count": len(size_findings),
                "severity": "defect",
                "reason": "One or more tables contain a clear font-size departure within the same table body or cell.",
                "action": "Restore the intended table style, retaining only deliberate header/body differences.",
                "examples": [
                    f"Table {item['table']}: {', '.join(str(value) for value in item['sizes_pt'])} pt"
                    for item in size_findings[:3]
                ],
                "details": size_findings,
            }
        )

    label_groups: dict[str, list[dict[str, Any]]] = {}
    structure_groups: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    for callout in callouts:
        label_groups.setdefault(callout["label"].casefold(), []).append(callout)
        signature = (
            tuple(callout["fills"]),
            callout["paragraphs"],
            callout["table_style"],
        )
        structure_groups.setdefault(signature, []).append(callout)
    repeated_tables: set[int] = set()
    repeated_groups: list[dict[str, Any]] = []
    for kind, groups in (("label", label_groups), ("structure", structure_groups)):
        for signature, group in groups.items():
            if len(group) < 3:
                continue
            table_numbers = {item["table"] for item in group}
            if table_numbers <= repeated_tables:
                continue
            repeated_tables.update(table_numbers)
            repeated_groups.append(
                {
                    "match": kind,
                    "tables": sorted(table_numbers),
                    "labels": sorted({item["label"] for item in group}),
                }
            )
    if repeated_groups:
        candidates.append(
            {
                "pattern": "repeated_unnumbered_shaded_callouts",
                "count": len(repeated_tables),
                "severity": "defect",
                "reason": "Three or more unnumbered 1x1 shaded tables repeat the same label or visual structure.",
                "action": "Convert repeated editorial callouts to ordinary manuscript prose/headings, or use a formally numbered Box required by the venue.",
                "examples": [label for group in repeated_groups for label in group["labels"]][:3],
                "details": repeated_groups,
            }
        )
    isolated_callouts = [item for item in callouts if item["table"] not in repeated_tables]
    if isolated_callouts:
        candidates.append(
            {
                "pattern": "unnumbered_shaded_callout_candidate",
                "count": len(isolated_callouts),
                "severity": "review",
                "reason": "An unnumbered 1x1 shaded table may be a reader-facing box or leaked author/editor scaffolding.",
                "action": "Keep only when the venue and scientific function justify it; otherwise integrate the content into normal prose.",
                "examples": [item["label"] for item in isolated_callouts[:3]],
                "details": isolated_callouts,
            }
        )

    return sorted(candidates, key=lambda item: (item["severity"] != "defect", item["pattern"]))


def split_paragraphs(text: str) -> list[str]:
    return [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n+", text) if p.strip()]


def split_sentences(text: str) -> list[str]:
    compact = re.sub(r"[\t ]+", " ", text)
    pieces = re.split(r"(?<=[。！？!?；;])\s*|(?<=[.!?])\s+(?=[A-Z0-9])", compact)
    return [re.sub(r"\s+", " ", item).strip() for item in pieces if item.strip()]


def visible_length(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def stats(values: Iterable[int]) -> dict[str, float | int]:
    data = list(values)
    if not data:
        return {"count": 0, "mean": 0.0, "median": 0.0, "stdev": 0.0, "cv": 0.0, "min": 0, "max": 0}
    mean = statistics.fmean(data)
    stdev = statistics.pstdev(data)
    return {
        "count": len(data),
        "mean": round(mean, 2),
        "median": round(statistics.median(data), 2),
        "stdev": round(stdev, 2),
        "cv": round(stdev / mean, 3) if mean else 0.0,
        "min": min(data),
        "max": max(data),
    }


def context_snippet(text: str, start: int, end: int, radius: int = 45) -> str:
    left = max(0, start - radius)
    right = min(len(text), end + radius)
    return re.sub(r"\s+", " ", text[left:right]).strip()


def pattern_hits(text: str, patterns: dict[str, str]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for label, pattern in patterns.items():
        matches = list(re.finditer(pattern, text, re.IGNORECASE | re.DOTALL))
        if matches:
            output.append(
                {
                    "pattern": label,
                    "count": len(matches),
                    "examples": [context_snippet(text, m.start(), m.end()) for m in matches[:3]],
                }
            )
    return sorted(output, key=lambda item: (-item["count"], item["pattern"]))


def guided_pattern_hits(text: str, patterns: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    """Return contextual candidates with an explanation and a repair action."""
    output: list[dict[str, Any]] = []
    for label, config in patterns.items():
        matches = list(re.finditer(config["pattern"], text))
        if matches:
            output.append(
                {
                    "pattern": label,
                    "count": len(matches),
                    "reason": config["reason"],
                    "action": config["action"],
                    "examples": [context_snippet(text, match.start(), match.end()) for match in matches[:3]],
                }
            )
    return sorted(output, key=lambda item: (-item["count"], item["pattern"]))


def code_is_defined(text: str, code: str) -> bool:
    """Detect a nearby manuscript-style definition, including simple table rows."""
    escaped = re.escape(code)
    definition_patterns = (
        rf"(?m)^[ \t|>*-]*(?:\*\*)?{escaped}(?:\*\*)?[ \t]*(?:[:：=]|[-–—](?!\s*[A-Z]\d))"
        rf"[ \t]*[^\r\n]{{3,}}$",
        rf"(?<![A-Za-z0-9]){escaped}(?![A-Za-z0-9])[ \t]*[:：=][ \t]*[^,，;；。.\r\n]{{3,}}",
        rf"(?<![A-Za-z0-9]){escaped}[ \t]*[（(][^()（）\r\n]{{3,}}[）)]",
        rf"(?:将|把)?[ \t]*{escaped}[ \t]*(?:定义为|指|表示|对应|记为)[ \t]*[^。；\r\n]{{3,}}",
        rf"(?<![A-Za-z0-9]){escaped}(?![A-Za-z0-9])[ \t]+(?:denotes|means|indicates|represents|"
        rf"is defined as|corresponds to)[ \t]+[^.;\r\n]{{3,}}",
        rf"(?<![A-Za-z0-9]){escaped}(?![A-Za-z0-9])[ \t]+(?:analy[sz]es|assigns|allows|"
        rf"captures|classifies|covers|describes|includes|lets|makes|records|requires|returns|"
        rf"selects|uses)[ \t]+[^.;\r\n]{{3,}}",
        rf"(?<![A-Za-z0-9]){escaped}(?![A-Za-z0-9])[ \t]*(?:只|仅)?(?:分析|推荐|返回|"
        rf"选择|要求|需要|允许|包括|涵盖|记录)[^。；\r\n]{{3,}}",
        rf"(?<![A-Za-z0-9]){escaped}(?![A-Za-z0-9])[ \t]*[,，][ \t]*"
        rf"(?!(?:[A-Z]\d{{1,2}})(?:\b|[ ,，;；]))[^,，;；。.\r\n]{{3,}}",
    )
    if any(re.search(pattern, text, re.IGNORECASE) for pattern in definition_patterns):
        return True

    paragraphs = split_paragraphs(text)
    for index, paragraph in enumerate(paragraphs[:-1]):
        if re.fullmatch(rf"(?:\*\*)?{escaped}(?:\*\*)?", paragraph, re.IGNORECASE):
            next_paragraph = paragraphs[index + 1]
            if 3 <= visible_length(next_paragraph) <= 240 and not INTERNAL_CODE_TOKEN_RE.fullmatch(next_paragraph):
                return True
    return False


def undefined_internal_code_candidates(text: str) -> list[dict[str, Any]]:
    """Find author-created compact code schemes whose categories are not defined.

    The detector requires internal-coding context (or a range standing alone) and
    deliberately ignores ordinary figure/table/supplement references. It is not
    a ban on alphanumeric scientific classifications.
    """
    findings: list[dict[str, Any]] = []
    seen: set[tuple[str, tuple[int, ...]]] = set()

    def consider(prefix: str, numbers: list[int], snippet: str, cue_text: str, standalone: bool = False) -> None:
        unique_numbers = sorted(set(numbers))
        if len(unique_numbers) < 2:
            return
        key = (prefix, tuple(unique_numbers))
        if key in seen:
            return
        if not standalone and not INTERNAL_CODE_CUE_RE.search(cue_text):
            return
        codes = [f"{prefix}{number}" for number in unique_numbers]
        missing = [code for code in codes if not code_is_defined(text, code)]
        if not missing:
            return
        seen.add(key)
        findings.append(
            {
                "family": prefix,
                "codes": codes,
                "missing_definitions": missing,
                "example": re.sub(r"\s+", " ", snippet).strip()[:220],
            }
        )

    for match in INTERNAL_CODE_RANGE_RE.finditer(text):
        prefix, start_text, end_text = match.groups()
        start, end = int(start_text), int(end_text)
        if end < start or end - start > 20:
            continue
        before = text[max(0, match.start() - 90) : match.start()]
        after = text[match.end() : min(len(text), match.end() + 120)]
        if PUBLIC_REFERENCE_CUE_RE.search(before[-55:]):
            continue
        line_start = text.rfind("\n", 0, match.start()) + 1
        line_end_index = text.find("\n", match.end())
        line_end = len(text) if line_end_index == -1 else line_end_index
        line = text[line_start:line_end].strip()
        standalone = bool(re.fullmatch(rf"(?:#{{1,6}}\s*)?{re.escape(match.group(0))}[：:]?", line))
        consider(prefix, list(range(start, end + 1)), before + match.group(0) + after, before + after, standalone)

    for paragraph in split_paragraphs(text):
        if not INTERNAL_CODE_CUE_RE.search(paragraph):
            continue
        families: dict[str, set[int]] = {}
        for prefix, number in INTERNAL_CODE_TOKEN_RE.findall(paragraph):
            families.setdefault(prefix, set()).add(int(number))
        for prefix, numbers in families.items():
            consider(prefix, sorted(numbers), paragraph, paragraph)

    merged: dict[str, dict[str, Any]] = {}
    for finding in findings:
        prefix = finding["family"]
        if prefix not in merged:
            merged[prefix] = finding
            continue
        merged[prefix]["codes"] = sorted(
            set(merged[prefix]["codes"]) | set(finding["codes"]),
            key=lambda code: int(code[1:]),
        )
        merged[prefix]["missing_definitions"] = sorted(
            set(merged[prefix]["missing_definitions"]) | set(finding["missing_definitions"]),
            key=lambda code: int(code[1:]),
        )
    return list(merged.values())


def reader_visible_output_candidates(text: str) -> list[dict[str, Any]]:
    output = guided_pattern_hits(text, READER_VISIBLE_PATTERNS)
    code_findings = undefined_internal_code_candidates(text)
    if code_findings:
        output.append(
            {
                "pattern": "undefined_internal_code_scheme",
                "count": len(code_findings),
                "reason": (
                    "A compact author-created code or grading scheme appears without definitions for every visible category."
                ),
                "action": (
                    "Define the scientific construct and each category at first use or in the adjacent legend/table, "
                    "or remove the shorthand. Preserve an existing defined project or field classification."
                ),
                "examples": [item["example"] for item in code_findings[:3]],
                "details": code_findings,
            }
        )
    return sorted(output, key=lambda item: (-item["count"], item["pattern"]))


def sentence_openers(sentences: list[str], width: int = 12) -> list[dict[str, Any]]:
    counter: Counter[str] = Counter()
    examples: dict[str, list[str]] = {}
    for sentence in sentences:
        cleaned = re.sub(r"^[\s\d.、（()\[\]【】]+", "", sentence)
        cleaned = re.sub(r"[\s，,。；;：:、“”‘’\-—]", "", cleaned).lower()
        if len(cleaned) < 6:
            continue
        opener = cleaned[:width]
        counter[opener] += 1
        examples.setdefault(opener, []).append(sentence[:140])
    return [
        {"opener": opener, "count": count, "examples": examples[opener][:3]}
        for opener, count in counter.most_common()
        if count >= 3
    ][:20]


def normalized_ngrams(text: str, size: int = 16) -> list[dict[str, Any]]:
    chunks = re.findall(r"[\u3400-\u9fffA-Za-z0-9]{%d,}" % size, re.sub(r"\s+", "", text))
    counter: Counter[str] = Counter()
    for chunk in chunks:
        if len(chunk) > 120:
            chunk = chunk[:120]
        for index in range(0, len(chunk) - size + 1, max(1, size // 2)):
            gram = chunk[index : index + size].lower()
            if not re.fullmatch(r"\d+", gram):
                counter[gram] += 1
    return [{"fragment": gram, "count": count} for gram, count in counter.most_common(20) if count >= 3]


def doi_list(text: str) -> list[str]:
    dois = []
    for match in DOI_RE.finditer(text):
        doi = match.group(0).rstrip(".,;:)]}，。；：）】").lower()
        if doi not in dois:
            dois.append(doi)
    return dois


def verify_doi(doi: str, timeout: float = 12.0, retries: int = 3) -> dict[str, Any]:
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
    request = urllib.request.Request(url, headers={"User-Agent": "CNS-Skills/0.7.0 (https://github.com/niuyupeng/CNS-Skills)"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            message = payload.get("message", {})
            title = (message.get("title") or [None])[0]
            issued = message.get("published-print") or message.get("published-online") or message.get("issued") or {}
            date_parts = issued.get("date-parts") or []
            year = date_parts[0][0] if date_parts and date_parts[0] else None
            return {
                "doi": doi,
                "status": "verified",
                "title": title,
                "publisher": message.get("publisher"),
                "type": message.get("type"),
                "year": year,
                "url": message.get("URL"),
            }
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt + 1 < retries:
                retry_value = exc.headers.get("Retry-After", "1") if exc.headers else "1"
                try:
                    delay = float(retry_value)
                except ValueError:
                    delay = 1.0
                time.sleep(min(max(delay, CROSSREF_PUBLIC_INTERVAL_SECONDS), 10.0))
                continue
            return {"doi": doi, "status": "not_found" if exc.code == 404 else "http_error", "http_code": exc.code}
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            return {"doi": doi, "status": "network_error", "error": str(exc)}
    return {"doi": doi, "status": "http_error", "http_code": 429}


def numeric_claims_without_citation(sentences: list[str]) -> list[str]:
    output = []
    for sentence in sentences:
        if NUMBER_RE.search(sentence) and not CITATION_RE.search(sentence) and not DOI_RE.search(sentence):
            output.append(sentence[:320])
    return output[:50]


def high_risk_claims(sentences: list[str]) -> list[str]:
    return [sentence[:320] for sentence in sentences if HIGH_RISK_TERMS.search(sentence)][:50]


def build_report(path: Path, text: str, verify_dois: bool = False) -> dict[str, Any]:
    paragraphs = split_paragraphs(text)
    analysis_text, analysis_scope = prose_analysis_scope(text)
    analysis_paragraphs = split_paragraphs(analysis_text)
    sentences = split_sentences(analysis_text)
    dois = doi_list(text)
    reader_candidates = reader_visible_output_candidates(text)
    docx_candidates = _docx_clean_copy_candidates(path)
    all_gate_candidates = reader_candidates + docx_candidates
    hard_reader_patterns = {
        "zh_analysis_label",
        "en_analysis_label",
        "zh_author_prompt",
        "en_author_prompt",
        "zh_agent_prompt",
        "en_agent_prompt",
        "unresolved_placeholder",
        "zh_revision_instruction",
        "en_revision_instruction",
        "zh_output_label",
        "en_output_label",
        "zh_manuscript_process_meta",
        "en_manuscript_process_meta",
        "zh_unfinished_submission_status",
        "en_unfinished_submission_status",
        "argument_gap_development_workflow",
        "undefined_internal_code_scheme",
    }
    hard_count = sum(
        item["count"]
        for item in reader_candidates
        if item["pattern"] in hard_reader_patterns
    ) + sum(item["count"] for item in docx_candidates if item.get("severity") == "defect")
    gate_status = "fail" if hard_count else ("review" if all_gate_candidates else "pass")
    report: dict[str, Any] = {
        "tool": "CNS Skills manuscript audit",
        "version": VERSION,
        "disclaimer": "Transparent writing triage; not an AI detector and not a substitute for source reading.",
        "source": str(path.resolve()),
        "counts": {
            "characters_no_space": visible_length(text),
            "paragraphs": len(paragraphs),
            "sentences": len(split_sentences(text)),
            "analyzed_body_characters_no_space": visible_length(analysis_text),
            "analyzed_body_paragraphs": len(analysis_paragraphs),
            "analyzed_body_sentences": len(sentences),
            "dois": len(dois),
        },
        "analysis_scope": analysis_scope,
        "clean_copy_gate": {
            "status": gate_status,
            "defect_hits": hard_count,
            "candidate_patterns": len(all_gate_candidates),
            "note": "References are excluded from prose-rhythm diagnostics, but the clean-copy gate still scans the complete artifact.",
        },
        "sentence_length": stats(visible_length(item) for item in sentences),
        "paragraph_length": stats(visible_length(item) for item in analysis_paragraphs),
        "stock_phrase_hits": pattern_hits(analysis_text, STOCK_PATTERNS),
        "repeated_contrast_hits": pattern_hits(analysis_text, CONTRAST_PATTERNS),
        "editorial_scaffolding_candidates": pattern_hits(analysis_text, SCAFFOLD_PATTERNS),
        "reader_visible_output_candidates": reader_candidates,
        "docx_clean_copy_candidates": docx_candidates,
        "repeated_sentence_openers": sentence_openers(sentences),
        "repeated_fragments": normalized_ngrams(analysis_text),
        "numeric_claims_without_nearby_citation": numeric_claims_without_citation(sentences),
        "high_risk_claim_language": high_risk_claims(sentences),
        "dois": dois,
    }
    if verify_dois:
        results = []
        for index, doi in enumerate(dois):
            if index:
                time.sleep(CROSSREF_PUBLIC_INTERVAL_SECONDS)
            results.append(verify_doi(doi))
        report["doi_verification"] = results
    return report


def render_text(report: dict[str, Any]) -> str:
    counts = report["counts"]
    lines = [
        "CNS manuscript audit",
        f"Source: {report['source']}",
        "Note: This is transparent writing triage, not an AI detector.",
        f"Clean-copy gate: {report['clean_copy_gate']['status'].upper()} ({report['clean_copy_gate']['defect_hits']} defect hit(s))",
        "",
        f"Characters: {counts['characters_no_space']} | paragraphs: {counts['paragraphs']} | analyzed body sentences: {counts['analyzed_body_sentences']} | DOIs: {counts['dois']}",
        "Reference list excluded from prose diagnostics: "
        + ("yes" if report["analysis_scope"]["reference_section_excluded"] else "no"),
        f"Sentence length mean/CV: {report['sentence_length']['mean']} / {report['sentence_length']['cv']}",
        f"Paragraph length mean/CV: {report['paragraph_length']['mean']} / {report['paragraph_length']['cv']}",
        "",
    ]
    for title, key in [
        ("Stock phrase patterns", "stock_phrase_hits"),
        ("Repeated contrast patterns", "repeated_contrast_hits"),
        ("Editorial-scaffolding candidates", "editorial_scaffolding_candidates"),
        ("Reader-visible output candidates", "reader_visible_output_candidates"),
        ("DOCX clean-copy candidates", "docx_clean_copy_candidates"),
        ("Repeated sentence openers", "repeated_sentence_openers"),
        ("Repeated fragments", "repeated_fragments"),
    ]:
        items = report[key]
        lines.append(f"{title}: {len(items)} pattern(s)")
        for item in items[:10]:
            label = item.get("pattern") or item.get("opener") or item.get("fragment")
            lines.append(f"  - {label}: {item['count']}")
        lines.append("")
    lines.append(f"Numeric sentences without a recognized nearby citation: {len(report['numeric_claims_without_nearby_citation'])}")
    lines.append(f"High-risk claim-language sentences: {len(report['high_risk_claim_language'])}")
    if "doi_verification" in report:
        counter = Counter(item["status"] for item in report["doi_verification"])
        lines.append("DOI verification: " + ", ".join(f"{key}={value}" for key, value in sorted(counter.items())))
        for item in report["doi_verification"]:
            if item["status"] != "verified":
                lines.append(f"  - {item['doi']}: {item['status']}")
    return "\n".join(lines)


def make_shareable(report: dict[str, Any]) -> dict[str, Any]:
    """Remove local paths and unpublished excerpts from a JSON report copy."""
    output = copy.deepcopy(report)
    output["source"] = Path(output["source"]).name
    output["shareable_redaction"] = "Local paths and manuscript excerpts removed; counts and diagnostics retained."
    for key in (
        "stock_phrase_hits",
        "repeated_contrast_hits",
        "editorial_scaffolding_candidates",
        "reader_visible_output_candidates",
        "docx_clean_copy_candidates",
        "repeated_sentence_openers",
    ):
        for item in output.get(key, []):
            item.pop("examples", None)
            if key in {"reader_visible_output_candidates", "docx_clean_copy_candidates"} and "details" in item:
                item["details_count"] = len(item["details"])
                item.pop("details", None)
    for item in output.get("repeated_sentence_openers", []):
        item["opener"] = None
    for item in output.get("repeated_fragments", []):
        item["fragment"] = None
    for key in ("numeric_claims_without_nearby_citation", "high_risk_claim_language"):
        output[key + "_count"] = len(output.get(key, []))
        output[key] = []
    return output


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="DOCX, TXT, or Markdown manuscript")
    parser.add_argument("--json", dest="json_path", type=Path, help="write the full report as UTF-8 JSON")
    parser.add_argument("--verify-dois", action="store_true", help="query Crossref for each DOI")
    parser.add_argument("--shareable", action="store_true", help="redact local paths and manuscript excerpts from JSON output")
    parser.add_argument("--strict", action="store_true", help="exit 2 if a DOI is not verified")
    parser.add_argument(
        "--strict-clean-copy",
        action="store_true",
        help="exit 3 unless the clean-copy gate passes without unresolved candidates",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    return parser.parse_args(argv)


def same_path(left: Path, right: Path) -> bool:
    return str(left.resolve()).casefold() == str(right.resolve()).casefold()


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.json_path and same_path(args.json_path, args.input):
        print("error: --json must not overwrite the input manuscript", file=sys.stderr)
        return 1
    try:
        text = read_input(args.input)
        report = build_report(args.input, text, verify_dois=args.verify_dois)
    except (OSError, ValueError, zipfile.BadZipFile, ET.ParseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(render_text(report))
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        json_report = make_shareable(report) if args.shareable else report
        args.json_path.write_text(json.dumps(json_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.strict and any(item.get("status") != "verified" for item in report.get("doi_verification", [])):
        return 2
    if args.strict_clean_copy and report["clean_copy_gate"]["status"] != "pass":
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
