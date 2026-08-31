#!/usr/bin/env python3
"""Audit how a review manuscript reports literature search and selection.

The audit is deliberately diagnostic. It distinguishes a concise narrative
scope note from a structurally complete systematic-search disclosure and identifies an
ambiguous middle pattern: a long keyword inventory that looks systematic but
cannot be rerun. It does not infer review quality from the presence or absence
of a Methods section, and it never treats corpus frequencies as venue rules.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


VERSION = "0.9.0"
W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
MATH_T = "{http://schemas.openxmlformats.org/officeDocument/2006/math}t"

DATABASE_PATTERNS: dict[str, str] = {
    "PubMed": r"(?<![A-Za-z])PubMed(?![A-Za-z])",
    "MEDLINE": r"(?<![A-Za-z])MEDLINE(?![A-Za-z])",
    "Embase": r"(?<![A-Za-z])Embase(?![A-Za-z])",
    "Scopus": r"(?<![A-Za-z])Scopus(?![A-Za-z])",
    "Web of Science": r"(?<![A-Za-z])Web of Science(?![A-Za-z])",
    "Cochrane Library": r"(?<![A-Za-z])Cochrane Library(?![A-Za-z])",
    "IEEE Xplore": r"(?<![A-Za-z])IEEE Xplore(?![A-Za-z])",
    "ACM Digital Library": r"(?<![A-Za-z])ACM Digital Library(?![A-Za-z])",
    "Google Scholar": r"(?<![A-Za-z])Google Scholar(?![A-Za-z])",
    "Europe PMC": r"(?<![A-Za-z])Europe PMC(?![A-Za-z])",
    "CINAHL": r"(?<![A-Za-z])CINAHL(?![A-Za-z])",
    "PsycINFO": r"(?<![A-Za-z])PsycINFO(?![A-Za-z])",
    "BIOSIS": r"(?<![A-Za-z])BIOSIS(?![A-Za-z])",
    "CNKI": r"(?<![A-Za-z])CNKI(?![A-Za-z])|中国知网",
    "Wanfang": r"(?<![A-Za-z])Wan[Ff]ang(?![A-Za-z])|万方",
    "SinoMed": r"(?<![A-Za-z])SinoMed(?![A-Za-z])|中国生物医学文献数据库",
    "Crossref": r"(?<![A-Za-z])Crossref(?![A-Za-z])",
    "Dimensions": r"(?<![A-Za-z])Dimensions(?:\.ai)?\s+(?:database|index|platform)(?![A-Za-z])",
}

DISCOVERY_OR_VERIFICATION_PATTERNS: dict[str, str] = {
    "publisher_platforms": r"publisher(?:s|')?\s+platforms?|出版社平台",
    "doi_landing_pages": r"DOI\s+(?:landing\s+)?pages?|DOI落地页",
    "author_curated_collection": (
        r"author[- ]curated(?:\s+full[- ]text)?\s+collection|"
        r"author[- ]maintained\s+(?:Zotero\s+)?full[- ]text\s+(?:library|collection)|"
        r"作者(?:整理|保存|汇编|自建)的?(?:全文)?(?:资料|文献|集合|库)"
    ),
}

SELECTION_PATTERNS: dict[str, str] = {
    "eligibility": (
        r"inclusion\s+(?:and\s+)?exclusion|eligibility\s+(?:criteria|rules)|"
        r"included\s+(?:if|when)|excluded\s+(?:if|when)|"
        r"(?:reports?|studies|articles?)\s+were\s+eligible\s+(?:if|when)|"
        r"(?:items?|records?)\s+meeting[^.。;；]{0,80}(?:same\s+)?inclusion\s+rule|"
        r"same\s+inclusion\s+rule|"
        r"纳入(?:与|和|/)?排除(?:标准|条件)|纳入标准|排除标准"
    ),
    "selection_logic": (
        r"(?:cases?|studies|papers?)\s+(?:were\s+)?prioriti[sz]ed|"
        r"(?:cases?|studies|papers?)\s+(?:were\s+)?selected\s+(?:to|for|when|because)|"
        r"(?:cases?|studies|papers?)\s+(?:were\s+)?chosen\s+(?:to|for|when|because)|"
        r"we\s+(?:selected|chose|prioriti[sz]ed|focused\s+on)|"
        r"(?:uses?|using|based\s+on|built\s+from)\s+"
        r"(?:purposive|illustrative|representative)\s+(?:examples?|studies|cases)|"
        r"(?:cases?|studies|papers?|experiments?)\s+(?:were\s+)?selected\s+as\s+"
        r"(?:purposive|illustrative|representative)\s+(?:examples?|cases)|"
        r"selected\s+(?:purposive|illustrative|representative)[^.。;；]{0,35}"
        r"(?:examples?|studies|cases|experiments?)|"
        r"(?:案例|研究|论文)(?:优先)?纳入|优先选择|选择逻辑|"
        r"(?:以|使用)(?:代表性|目的性)[^。；]{0,30}(?:研究|案例)|"
        r"选择[^。；]{0,45}(?:研究|论文)[^。；]{0,20}(?:作为|用作)(?:案例|示例)"
    ),
    "deduplication": (
        r"deduplicat(?:e|ed|ion|ing)?\s+(?:the\s+)?(?:records?|citations?|references?|articles?|search\s+results?)|"
        r"(?:records?|citations?|references?|articles?|search\s+results?)\s+(?:were\s+)?deduplicat|"
        r"duplicate\s+(?:bibliographic\s+)?records?|"
        r"(?:this\s+)?bibliographic\s+(?:set|record\s+set)\s+(?:was\s+)?deduplicat|"
        r"search\s+exports?\s+(?:were\s+|was\s+)?deduplicat|"
        r"文献去重|去除重复(?:文献|记录)|重复(?:文献|记录)(?:被|予以)?(?:删除|去除)|"
        r"(?:完成|进行)(?:文献|记录)?去重|"
        r"(?:they|these|those)\s+(?:were\s+)?deduplicat(?:ed|ion|ing)?"
    ),
    "screening": (
        r"title[- /]abstract\s+screen|full[- ]text\s+screen|"
        r"(?:two\s+reviewers?|two\s+authors?)\s+screened\s+titles?,\s*abstracts?,\s*(?:and\s+)?full[- ]texts?|"
        r"(?:two\s+reviewers?\s+)?independent(?:ly)?\s+screen[^.。\n]{0,90}"
        r"(?:titles?|abstracts?|full[- ]texts?|records?|articles?)|"
        r"(?:every|all)\s+(?:record|records|article|articles)\s+(?:was|were)\s+screened|"
        r"题名[、/]摘要筛选|全文筛选|独立筛选|双人筛选|两名审阅"
    ),
    "flow_accounting": (
        r"PRISMA(?:-ScR)?\s+(?:flow\s+)?(?:diagram|chart)|"
        r"(?:literature|study|record)\s+(?:selection\s+)?flow\s+(?:diagram|chart)|"
        r"records?\s+(?:identified|screened|excluded)|"
        r"PRISMA(?:-ScR)?流程图|文献筛选流程图?|检出\s*\d+|筛选\s*\d+|排除\s*\d+"
    ),
    "version_handling": (
        r"preprints?|versions?|corrections?|retractions?|publication\s+status|"
        r"预印本|版本处理|更正|撤稿|发表状态"
    ),
}

DATE_PATTERNS = (
    r"(?:updated|searched|searches?\s+(?:were\s+)?conducted|through|until|up\s+to|as\s+of)"
    r"[^.。\n]{0,70}(?:19|20)\d{2}|"
    r"(?:检索|更新|截止|截至)[^。\n]{0,50}(?:19|20)\d{2}|"
    r"截至\s*(?:19|20)\d{2}年(?:\d{1,2}月(?:\d{1,2}日)?)?"
)
KEYWORD_LABEL = (
    r"(?:search|query)\s+(?:terms?|keywords?|combinations?|concepts?)|"
    r"search\s+vocabulary|"
    r"检索词|关键词|检索式|检索概念|查询概念"
)
EXACT_QUERY_MARKERS = (
    r"\[(?:tiab|mesh(?:\s+terms?)?|majr|publication\s+type|pt|mh|tw|"
    r"title|abstract|title/abstract|text\s+word|all\s+fields?)\]|"
    r"(?:TITLE-ABS-KEY|TS\s*=|NEAR/\d+|W/\d+|exp\s+[^;\n]+/|\.ti,ab\.|"
    r"\.(?:mp|tw|ti|ab)\.|\badj\d*\b|\bN\d+\b|\bMH\s+[\"']|\bTX\s+[\"'])"
)
COVERAGE_BOUNDARY = (
    r"not\s+(?:an?\s+)?(?:systematic|comprehensive|exhaustive)|"
    r"does\s+not\s+support\s+estimates?\s+of\s+(?:literature\s+)?coverage|"
    r"not\s+(?:intended\s+)?(?:as\s+)?an?\s+exhaustive\s+census|"
    r"rather\s+than\s+an?\s+exhaustive\s+(?:census|corpus)|"
    r"rather\s+than\s+(?:to\s+)?estimate\s+(?:literature\s+)?coverage|"
    r"completeness\s+is\s+not\s+claimed|"
    r"(?:we\s+)?do(?:es)?\s+not\s+claim\s+(?:complete|comprehensive|exhaustive)\s+coverage|"
    r"not\s+intended\s+to\s+be\s+(?:complete|comprehensive|exhaustive)|"
    r"we\s+do\s+not\s+aim\s+to\s+(?:exhaust|cover\s+all)|"
    r"not\s+interpreted\s+as\s+(?:the\s+)?prevalence[^.。\n]{0,80}(?:field|literature)|"
    r"(?:did\s+not|do\s+not|does\s+not)\s+(?:conduct|perform|undertake)\s+(?:an?\s+)?systematic\s+review|"
    r"no\s+systematic\s+review\s+(?:was\s+)?(?:conducted|performed|undertaken)|"
    r"(?:不|未)(?:按|采用)?系统综述|不(?:据此)?估计文献覆盖率|不推断.*发生比例|"
    r"(?:并未|没有|未曾)(?:开展|进行|实施)系统综述|"
    r"(?:并非|并不是)系统综述|"
    r"而非估计文献覆盖率|"
    r"不是(?:对)?全部文献的穷尽性统计|非穷尽|不追求全面覆盖|不声称全面覆盖"
    r"|未声称穷尽(?:全部)?(?:研究|文献)|不作穷尽性统计"
)
SUPPLEMENT_SEARCH = (
    r"supplement(?:ary|al).{0,80}(?:search|query|queries|strategy)|"
    r"(?:attached|accompanying|included|provided)?\s*supplement(?:ary|al)?\s*\w*"
    r".{0,120}(?:platform[- ]specific\s+)?(?:commands?|syntax|strings?)"
    r".{0,100}(?:execution|run)\s+dates?.{0,80}"
    r"(?:databases?|bibliographic\s+searches?|literature\s+searches?)|"
    r"(?:database[- ]specific\s+)?(?:search\s+)?(?:strings?|queries|strategies)"
    r".{0,100}(?:are\s+|were\s+)?(?:provided|reported|listed|available)"
    r".{0,80}supplement(?:ary|al)|"
    r"(?:完整|详细)?检索式.{0,40}(?:补充|附录)|"
    r"(?:补充(?:材料|方法|表)|附录(?:\s*S?\d+)?)\s*[^。\n]{0,80}(?:检索|策略)"
)
PLANNED_SUPPLEMENT = (
    r"(?:supplement(?:ary|al)?|appendix).{0,100}(?:under\s+preparation|will|shall|to\s+be|planned|forthcoming)"
    r".{0,60}(?:add|provide|include|list|upload|report|make\s+available)|"
    r"(?:will|shall|to\s+be|planned|forthcoming).{0,100}"
    r"(?:supplement(?:ary|al)?|appendix).{0,60}(?:search|query|strategy)|"
    r"(?:supplement(?:ary|al)?|appendix).{0,120}"
    r"(?:slated|scheduled|intended|due)\s+for\s+(?:deposit|upload|release|publication)|"
    r"(?:supplement(?:ary|al)?|appendix).{0,120}"
    r"(?:not\s+(?:included|attached|available|provided)|(?:is\s+)?(?:absent|missing)\s+from|"
    r"absent\s+from\s+the\s+current)|"
    r"(?:will|shall|is\s+to|are\s+to).{0,120}(?:receive|deposit|upload|release|archive)"
    r".{0,100}(?:supplement(?:ary|al)?|appendix)|"
    r"(?:supplement(?:ary|al)?|appendix).{0,160}"
    r"(?:will|shall|is\s+to|are\s+to).{0,100}(?:deposit|upload|release|archive)|"
    r"supplement(?:ary|al)?\s+files?.{0,60}(?:did|do|does)\s+not\s+include"
    r".{0,60}(?:search|query)\s+(?:strategy|strategies|record|records|string|strings)|"
    r"(?:补充材料|补充方法|补充表|附录).{0,80}(?:将|拟|计划|待)(?:补充|提供|加入|上传|列出)|"
    r"(?:将|拟|计划|待).{0,80}(?:补充材料|补充方法|补充表|附录).{0,60}(?:检索|策略|检索式)|"
    r"(?:补充材料|补充方法|补充表|附录).{0,120}(?:尚在整理|定稿后才会|当前(?:文件)?未附|"
    r"投稿包中(?:并)?无|没有归档)|"
    r"(?:投稿包中(?:并)?无|当前(?:文件)?未附)[^。\n]{0,80}(?:该文件|该表|补充材料|补充方法|补充表)|"
    r"(?:逐库|各数据库)?检索式[^。\n]{0,50}(?:没有|尚未|未)(?:归档|附上|提供)"
)
CURRENT_SUPPLEMENT = (
    r"(?:supplement(?:ary|al)?(?:\s+(?:data|methods?|table))?|appendix)\s*S?\d*"
    r"[^.。\n]{0,80}(?:is|are|was|were)\s+(?:already\s+)?"
    r"(?:included|attached|submitted|provided)\s+(?:with|in)\s+(?:this\s+)?submission"
    r"[^.。\n]{0,180}(?:platform[- ]specific\s+)?(?:search\s+)?(?:commands?|strings?|queries?)"
    r"[^.。\n]{0,100}(?:execution|run)\s+dates?|"
    r"(?:随稿提交|本次投稿已附|现已收录)[^。\n]{0,100}(?:补充材料|补充方法|补充表|附录)"
    r"[^。\n]{0,120}(?:检索式|检索策略|运行日期)"
)

SEARCH_CONTEXT_ANCHOR = (
    r"\b(?:literature|bibliographic)\s+search|"
    r"\bsearch\s+(?:strategy|strategies|terms?|keywords?|strings?|queries?|databases?)\b|"
    r"\b(?:database|databases|query|queries|keyword|keywords|eligibility|PRISMA)\b|"
    r"\b(?:records?|citations?|references?)\s+(?:were\s+)?(?:identified|screened|excluded)|"
    r"systematic\s+(?:literature\s+)?review|scoping\s+review|meta[- ]analysis|"
    r"检索|数据库|检索式|关键词|纳入标准|排除标准|文献筛选|系统综述|范围综述|荟萃分析"
)

SECONDARY_ROLE_PATTERNS = {
    "publisher_platforms": (
        r"(?:publisher(?:s|')?\s+(?:pages?|platforms?))\s+(?:were\s+|was\s+)?"
        r"(?:used|consulted|accessed)\s+(?:only\s+)?(?:for|to)\s+(?:full[- ]text\s+)?"
        r"(?:retriev|obtain|access|download)|"
        r"出版社(?:页面|平台)\s*(?:仅|只)?用于(?:获取|下载|查阅)全文|"
        r"full[- ]text\s+retrieval\s+(?:was\s+|is\s+)?(?:performed|conducted|done)\s+"
        r"(?:through|via|using)\s+publisher(?:s|')?\s+(?:pages?|platforms?)|"
        r"(?:used|利用|通过)[^.。\n]{0,80}(?:publisher(?:s|')?\s+(?:pages?|platforms?)|出版社(?:页面|平台))"
        r"[^.。\n]{0,80}(?:to\s+(?:identify|retrieve|access)|用于?(?:发现|获取|下载))|"
        r"(?:article\s+)?PDFs?\s+(?:were\s+|was\s+)?(?:obtained|retrieved|downloaded|accessed)"
        r"[^.。\n]{0,80}(?:on|from|through|via)\s+publisher(?:s|')?\s+(?:pages?|platforms?)|"
        r"publisher(?:s|')?\s+(?:pages?|platforms?)[^.。\n]{0,120}"
        r"(?:served|used)[^.。\n]{0,50}(?:download|retrieve|access)[^.。\n]{0,35}full[- ]texts?"
    ),
    "doi_landing_pages": (
        r"(?:DOI\s+(?:landing\s+)?pages?|DOI落地页)[^.。\n]{0,100}"
        r"(?:verif|confirm|check|metadata|publication\s+status|核验|验证|确认|元数据|发表状态)|"
        r"(?:metadata|publication\s+status)[^.。\n]{0,100}(?:verif|confirm|check)[^.。\n]{0,80}"
        r"DOI\s+(?:landing\s+)?pages?|"
        r"(?:used|利用|通过)[^.。\n]{0,80}(?:DOI\s+(?:landing\s+)?pages?|DOI落地页)"
        r"[^.。\n]{0,80}(?:to\s+(?:verify|confirm|check)|用于?(?:核验|确认|验证))|"
        r"(?:DOI\s+(?:landing\s+)?pages?|DOI落地页)[^.。\n]{0,100}"
        r"(?:served\s+to\s+)?(?:corroborat|cross[- ]check|authenticate)[^.。\n]{0,80}"
        r"(?:authors?|year|metadata|retraction|status)|"
        r"(?:DOI\s+(?:landing\s+)?pages?|DOI落地页)[^.。\n]{0,140}"
        r"(?:served|used)[^.。\n]{0,55}(?:verif|confirm|check|核验|确认|核对)[^.。\n]{0,70}"
        r"(?:authors?|dates?|year|metadata|corrections?|retractions?|publication\s+status|"
        r"作者|年份|元数据|更正|撤稿|发表状态)"
    ),
}

def read_docx(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        xml_parts = [archive.read("word/document.xml")]
        for optional in ("word/footnotes.xml", "word/endnotes.xml"):
            if optional in archive.namelist():
                xml_parts.append(archive.read(optional))
    paragraphs: list[str] = []
    for xml in xml_parts:
        root = ET.fromstring(xml)
        for paragraph in root.iter(W_NS + "p"):
            text = "".join(
                node.text or ""
                for node in paragraph.iter()
                if node.tag in {W_NS + "t", MATH_T}
            ).strip()
            if text:
                paragraphs.append(text)
    return "\n\n".join(paragraphs)


def read_text(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        return read_docx(path)
    if path.suffix.lower() not in {".txt", ".md", ".markdown"}:
        raise ValueError("supported inputs: .docx, .txt, .md, .markdown")
    return path.read_text(encoding="utf-8-sig")


def body_without_references(text: str) -> str:
    pattern = re.compile(
        r"(?im)^\s*(?:#{1,6}\s*)?(?:\d+(?:\.\d+)*[.)]?\s+)?"
        r"(?:references|bibliography|参考文献)\s*$"
    )
    matches = list(pattern.finditer(text))
    return text[: matches[-1].start()] if matches else text


def present(pattern: str, text: str, flags: int = re.IGNORECASE | re.DOTALL) -> bool:
    return re.search(pattern, text, flags) is not None


def count_paragraphs(pattern: str, text: str) -> int:
    return sum(
        1
        for paragraph in re.split(r"\n\s*\n", text)
        if present(pattern, paragraph)
    )


def repeated_boundary_function(text: str) -> bool:
    """Return true only when the same boundary function is repeated.

    Saying both "this is not systematic" and "examples are not exhaustive"
    answers two different questions and should not be collapsed into a style
    warning solely because they occur in separate paragraphs.
    """

    type_boundary = (
        r"systematic\s+(?:literature\s+)?review|系统综述|系统评价"
    )
    corpus_coverage_boundary = (
        r"comprehensive|exhaustive|coverage|census|corpus|"
        r"全面|穷尽|覆盖率|全部文献"
    )
    prevalence_boundary = (
        r"prevalence|occurrence|field[- ]wide\s+(?:rate|frequency)|"
        r"发生比例|发生率|领域比例"
    )
    boundary_items = [
        paragraph for paragraph in paragraphs(text) if present(COVERAGE_BOUNDARY, paragraph)
    ]
    type_items = [paragraph for paragraph in boundary_items if present(type_boundary, paragraph)]
    coverage_items = [
        paragraph
        for paragraph in boundary_items
        if present(corpus_coverage_boundary, paragraph)
    ]
    prevalence_items = [
        paragraph
        for paragraph in boundary_items
        if present(prevalence_boundary, paragraph)
    ]
    return (
        len(type_items) > 1
        or len(coverage_items) > 1
        or len(prevalence_items) > 1
    )


def paragraphs(text: str) -> list[str]:
    return [item.strip() for item in re.split(r"\n\s*\n", text) if item.strip()]


def sentence_units(text: str) -> list[str]:
    """Split prose enough to keep neighbouring scientific subjects separate.

    This is intentionally lighter than linguistic sentence parsing.  The
    uppercase look-ahead avoids splitting Ovid field tokens such as ``.mp.``
    before Boolean operators while still separating ordinary English prose.
    """

    units: list[str] = []
    for paragraph in paragraphs(text):
        units.extend(
            item.strip()
            for item in re.split(
                r"(?<=[。！？!?])\s*|(?<=\.)\s+(?=[A-Z][a-z])|"
                r"(?<=\.)\s+(?=DOI\b)",
                paragraph,
            )
            if item.strip()
        )
    return units


def unquoted_type_text(text: str) -> str:
    """Mask short quoted spans so cited titles do not declare this article's type."""

    return re.sub(
        r"“[^”\n]{0,400}”|‘[^’\n]{0,400}’|\"[^\"\n]{0,400}\"",
        " ",
        text,
    )


def search_context(text: str) -> str:
    """Return local paragraphs where the review's own search could be reported.

    A generic occurrence of ``deduplication`` or ``version`` is intentionally not
    an anchor: reviews often discuss candidate deduplication or software/model
    versions in their scientific body. One neighbouring paragraph on either side
    is retained so multi-paragraph Methods disclosures remain analyzable.
    """

    items = paragraphs(text)
    anchor_patterns = [SEARCH_CONTEXT_ANCHOR, KEYWORD_LABEL, SUPPLEMENT_SEARCH]
    anchor_patterns.extend(DATABASE_PATTERNS.values())
    anchor_patterns.extend(DISCOVERY_OR_VERIFICATION_PATTERNS.values())
    indices: set[int] = set()
    for index, paragraph in enumerate(items):
        if any(present(pattern, paragraph) for pattern in anchor_patterns):
            for offset in (-1, 0, 1):
                neighbour = index + offset
                if 0 <= neighbour < len(items):
                    indices.add(neighbour)
        if present(
            DISCOVERY_OR_VERIFICATION_PATTERNS["author_curated_collection"],
            paragraph,
        ):
            # Formation and entry rules for a personal library often occupy
            # two following paragraphs.  Keep the expansion source-anchored.
            for offset in (2, 3):
                neighbour = index + offset
                if 0 <= neighbour < len(items):
                    indices.add(neighbour)
    return "\n\n".join(items[index] for index in sorted(indices))


def self_declared(paragraph: str, article_type_pattern: str) -> bool:
    for match in re.finditer(article_type_pattern, paragraph, flags=re.IGNORECASE):
        prefix_start = max(0, match.start() - 140)
        prefix = paragraph[prefix_start : match.start()]
        negative = (
            r"\b(?:not|never|did\s+not|do\s+not|does\s+not|was\s+not|is\s+not|"
            r"rather\s+than|without)\b[^.。;；]{0,60}$|"
            r"(?:并未|并非|并不是|没有|未曾|不是|不属于|而非|不按|未按|未采用)[^。；]{0,40}$"
        )
        if present(negative, prefix):
            continue
        self_anchor = (
            r"\bthis\s+(?:review|study|analysis)\b[^.。;；]{0,60}$|"
            r"\bthis\s+(?:invited\s+)?(?:critical\s+)?$|"
            r"\bthis\s+(?:is|was)\s+(?:an?\s+)?$|"
            r"\bthe\s+present\s+(?:review|study|analysis)?[^.。;；]{0,40}$|"
            r"\bour\s+$|"
            r"\bour\s+(?:review|study|analysis)\b[^.。;；]{0,50}$|"
            r"\bwe\s+(?:conducted|performed|undertook|carried\s+out|report|present)\s+(?:an?\s+)?$|"
            r"(?:本文|本综述|本研究|本(?:结构化)?叙述性综述|本)[^。；]{0,40}$|"
            r"我们(?:开展|进行|采用|实施|报告)[^。；]{0,30}$"
        )
        if present(self_anchor, prefix):
            return True
    return False


def declared_review_type(text: str) -> str:
    clean = unquoted_type_text(text)
    declaration_patterns: list[tuple[str, str]] = [
        (
            "scoping",
            r"\bthis\s+scoping\s+review\b|"
            r"\bwe\s+(?:conducted|performed|undertook|present)\s+(?:an?\s+)?scoping\s+review\b|"
            r"\b(?:this|our|the\s+present|the\s+final)\s+(?:article|review|study)\s+"
            r"(?:is|was|constitutes)\s+(?:an?\s+)?scoping\s+review\b|"
            r"(?:本文|本综述|本研究)[^。；]{0,25}(?:为|是|采用|开展|进行)[^。；]{0,12}范围综述|"
            r"本范围综述",
        ),
        (
            "meta_analysis",
            r"\bthis\s+meta[- ]analysis\b|"
            r"\bwe\s+(?:conducted|performed|undertook|present)\s+(?:an?\s+)?meta[- ]analysis\b|"
            r"\b(?:this|our|the\s+present|the\s+final)\s+(?:article|review|study)\s+"
            r"(?:is|was|constitutes)\s+(?:an?\s+)?meta[- ]analysis\b|"
            r"(?:本文|本综述|本研究)[^。；]{0,25}(?:为|是|采用|开展|进行)[^。；]{0,12}荟萃分析|"
            r"本荟萃分析",
        ),
        (
            "systematic",
            r"\bthis\s+systematic\s+(?:literature\s+)?review\b|"
            r"\bwe\s+(?:(?:subsequently|ultimately|finally|then)\s+)?"
            r"(?:conducted|performed|undertook|carried\s+out|present)\s+"
            r"(?:an?\s+)?systematic\s+(?:literature\s+)?review\b|"
            r"\b(?:this|our|the\s+present|the\s+final)\s+(?:article|review|study)\s+"
            r"(?:is|was|constitutes)\s+(?:an?\s+)?systematic\s+(?:literature\s+)?review\b|"
            r"(?:本文|本综述|本研究)[^。；]{0,25}(?:为|是|采用|开展|进行)[^。；]{0,12}"
            r"(?:系统综述|系统评价)|本(?:系统综述|系统评价)|"
            r"我们(?:开展|进行|实施)[^。；]{0,12}(?:系统综述|系统评价)",
        ),
        (
            "structured_narrative",
            r"\bthis\s+structured\s+narrative\s+review\b|"
            r"\bwe\s+(?:conducted|performed|undertook|present)\s+(?:an?\s+)?"
            r"structured\s+narrative\s+review\b|"
            r"\b(?:this|our|the\s+present|the\s+final)\s+(?:article|review|study)\s+"
            r"(?:is|was|constitutes)\s+(?:an?\s+)?structured\s+narrative\s+review\b|"
            r"(?:本文|本综述|本研究)[^。；]{0,25}(?:为|是|采用|开展|进行)[^。；]{0,12}"
            r"结构化叙述性综述|本结构化叙述性综述",
        ),
        (
            "narrative",
            r"\bthis\s+narrative\s+(?:literature\s+)?review\b|"
            r"\bwe\s+(?:conducted|performed|undertook|present)\s+(?:an?\s+)?"
            r"narrative\s+(?:literature\s+)?review\b|"
            r"\b(?:this|our|the\s+present|the\s+final|final)\s+(?:article|review|study)\s+"
            r"(?:is|was|constitutes)\s+(?:an?\s+)?narrative\s+(?:literature\s+)?review\b|"
            r"(?:本文|本综述|本研究)[^。；]{0,25}(?:为|是|采用|开展|进行)[^。；]{0,12}"
            r"(?:结构化)?叙述性综述|本(?:结构化)?叙述性综述",
        ),
    ]
    candidates: list[tuple[int, str]] = []
    for review_type, pattern in declaration_patterns:
        for match in re.finditer(pattern, clean, flags=re.IGNORECASE):
            prefix = clean[max(0, match.start() - 80) : match.start()]
            matched_text = match.group(0)
            suffix = clean[match.end() : match.end() + 160]
            if present(
                r"\b(?:not|never|no)\b|(?:并未|并非|并不是|没有|未曾|不是|不属于|"
                r"未开展|未进行|未按|不按|未采用)",
                matched_text,
            ):
                continue
            if present(
                r"(?:cites?|discuss(?:es|ed)?|paper|article|study|title(?:d)?|guideline|checklist|"
                r"comment|remark|reviewer|editor|"
                r"consortium|named|called|label(?:led|ed)?)\s*$",
                prefix,
            ):
                continue
            if present(
                r"(?:[A-Za-z][A-Za-z'’.-]*\s+)?et\s+al\.\s+"
                r"(?:reported|described|presented|published)\s*$",
                prefix,
            ):
                continue
            if present(
                r"(?:registered\s+)?(?:outline|plan|protocol|label)[^.。;；]{0,80}"
                r"(?:withdrawn|abandoned|discarded|removed|superseded)|"
                r"(?:注册)?(?:方案|计划)[^。；]{0,60}(?:撤回|放弃|未实施|未执行|被取代)",
                suffix,
            ):
                continue
            if present(
                r"(?:planned|proposed|intended|considered|abandoned|discarded)\s+(?:as\s+)?$|"
                r"(?:not|never|no)\s+$|(?:原计划|曾计划|原拟|拟作为|放弃)[^。；]{0,20}$",
                prefix,
            ):
                continue
            candidates.append((match.start(), review_type))
    if candidates:
        # A later explicit statement such as "the final article is narrative"
        # resolves an earlier plan or superseded description.
        return max(candidates, key=lambda item: item[0])[1]
    negative_systematic = present(
        r"(?:not|did\s+not|do\s+not|does\s+not|was\s+not|is\s+not|rather\s+than)"
        r"[^.。;；]{0,60}systematic\s+(?:literature\s+)?review|"
        r"no\s+systematic\s+(?:literature\s+)?review\s+(?:was\s+)?"
        r"(?:conducted|performed|undertaken)|"
        r"(?:并未|并非|并不是|没有|未曾|不是|不属于|而非|不按)[^。；]{0,40}"
        r"(?:系统综述|系统评价)|非(?:系统综述|系统评价)|未按(?:系统综述|系统评价)",
        clean,
    )
    if negative_systematic:
        return "narrative"
    return "unspecified"


def keyword_inventory(text: str) -> bool:
    for paragraph in paragraphs(text):
        for match in re.finditer(KEYWORD_LABEL, paragraph, flags=re.IGNORECASE):
            tail = paragraph[match.end() : match.end() + 420]
            tail = re.split(r"[.。\n]", tail, maxsplit=1)[0]
            if len(re.findall(r"\s/\s|[;,；，、]", tail)) >= 3:
                return True
            if re.search(r"[“\"'][^”\"']+(?:\s/\s|[;；])[^”\"']+[”\"']", tail):
                return True
    return False


def executable_query_present(text: str) -> bool:
    """Detect database-shaped query syntax only inside a query-bearing sentence.

    Tokens such as ``TS`` and ``records`` are common scientific variables.  A
    database name elsewhere in the same paragraph is not enough to turn them
    into a literature query.
    """

    query_cue = (
        r"\b(?:search(?:ed|es|ing)?|query|queries|string|strings|strategy|strategies|"
        r"syntax|using|with)\b|(?:检索|查询|式为|检索式)"
    )
    database_union = "(?:" + "|".join(DATABASE_PATTERNS.values()) + ")"
    sentences = sentence_units(text)
    nonbibliographic_database = (
        r"\b(?:materials?|patient|clinical|assay|rheology|cell[- ]culture|instrument|"
        r"polymer|candidate)\s+database\b|"
        r"(?:材料|患者|临床|检测|仪器|候选)(?:数据)?库"
    )
    field_collision_definition = (
        r"\bwhere\s+(?:MH|TX|TS|TITLE-ABS-KEY)\s+(?:is|means|denotes)|"
        r"\b(?:MH|TX|TS|TITLE-ABS-KEY)\b[^.。;；]{0,100}"
        r"(?:material[- ]history|clinical\s+variable|composite\s+clinical|"
        r"transfection\s+exposure|thermal[- ]setting)|"
        r"\.(?:mp|tw|ti|ab)\.\s+(?:is|was|means?|meant|denotes?|denoted)"
        r"[^.。;；]{0,80}(?:torque|rheolog|instrument|assay)|"
        r"(?:字段|变量)[^。；]{0,50}(?:材料|患者|临床|转染|温度)"
    )
    query_continuation = (
        r"^(?:the\s+(?:database\s+)?(?:query|syntax|string)|"
        r"(?:the\s+)?(?:exact|full)\s+(?:query|string)|"
        r"TITLE-ABS-KEY|TS\s*=|\(|[A-Za-z0-9*\"']+\[(?:tiab|title/abstract|mesh))"
    )
    for index, sentence in enumerate(sentences):
        has_database = present(database_union, sentence)
        adjacent_database = False
        if index:
            adjacent_database = present(database_union, sentences[index - 1]) and present(
                query_continuation, sentence
            )
        has_context = present(query_cue, sentence) or (
            has_database and present(r"\b(?:used|specified|reported|ran)\b|式为", sentence)
        ) or adjacent_database
        if not has_context:
            continue
        for marker in re.finditer(EXACT_QUERY_MARKERS, sentence, flags=re.IGNORECASE):
            token = marker.group(0)
            if present(
                r"(?:not|never)\s+(?:an?\s+)?(?:bibliographic|literature|database)\s+"
                r"(?:search\s+)?(?:field|syntax|query|operator)|"
                r"(?:并非|不是|不属于)[^。；]{0,30}(?:文献|题录|数据库)(?:检索)?(?:字段|语法|检索式|算子)",
                sentence,
            ):
                continue
            if present(nonbibliographic_database, sentence) and present(
                field_collision_definition, sentence
            ):
                continue
            if not (
                has_database
                or adjacent_database
                or present(
                    r"\b(?:literature|bibliographic)\s+(?:search|query)|"
                    r"\b(?:database[- ]specific|exact|full)\s+(?:search\s+)?(?:query|string|syntax)",
                    sentence,
                )
            ):
                continue
            if re.fullmatch(r"(?i)N\d+", token) and not (
                has_database
                or present(
                    r"\b(?:search(?:ed|es|ing)?|query|queries|string|strings|strategy|"
                    r"strategies|syntax|proximity\s+operator)\b|(?:检索|查询|检索式)",
                    sentence,
                )
            ):
                continue
            if re.match(r"(?i)TS\s*=", token):
                rhs = sentence[marker.end() : marker.end() + 120]
                if re.match(
                    r"\s*[\[(（]?\s*[-+]?\d+(?:\.\d+)?\s*(?:°|degrees?|K\b|C\b)",
                    rhs,
                ):
                    continue
                if not present(r"[A-Za-z*\"'(].*(?:\bAND\b|\bOR\b|\bNOT\b|\*)|[\"'(]", rhs):
                    continue
            return True
    return False


def supplementary_search_status(text: str) -> str:
    if present(CURRENT_SUPPLEMENT, text):
        return "claimed_present"
    if present(PLANNED_SUPPLEMENT, text):
        return "planned_or_placeholder"
    if present(SUPPLEMENT_SEARCH, text):
        return "claimed_present"
    return "absent"


def search_cutoff_present(text: str) -> bool:
    """Bind a year or date boundary to literature-search context.

    Bare temporal wording such as ``outcomes were followed through 2025`` is
    not a search cutoff even when it sits beside a review Methods sentence.
    """

    database_union = "(?:" + "|".join(DATABASE_PATTERNS.values()) + ")"
    explicit_search_context = (
        r"\b(?:search(?:ed|es|ing)?|updated|literature\s+search|bibliographic\s+search|"
        r"search\s+(?:date|cutoff))\b|(?:检索|更新|截止|截至)"
    )
    bare_cutoff = (
        r"\b(?:through|until|up\s+to|as\s+of)\b[^.。\n]{0,70}(?:19|20)\d{2}|"
        r"(?:至|截至?)\s*(?:19|20)\d{2}"
    )
    for sentence in sentence_units(text):
        if not present(DATE_PATTERNS, sentence):
            continue
        if present(explicit_search_context, sentence):
            return True
        if present(database_union, sentence) and present(bare_cutoff, sentence):
            return True
    return False


def author_collection_boundary_present(text: str) -> bool:
    items = paragraphs(text)
    for index, paragraph in enumerate(items):
        if not present(DISCOVERY_OR_VERIFICATION_PATTERNS["author_curated_collection"], paragraph):
            continue
        # The provenance, date boundary and entry rule are often disclosed in
        # the immediately following sentences rather than repeated beside the
        # collection's name. Keep this window narrow and collection-anchored.
        paragraph = "\n".join(items[index : min(len(items), index + 4)])
        provenance = present(
            r"assembled|compiled|collected|formed|alerts?|subscriptions?|repositories?|archives?|"
            r"来源|汇集|形成|订阅|数据库|机构库|知识库",
            paragraph,
        )
        time_boundary = present(
            r"between\s+(?:19|20)\d{2}\s+and\s+(?:19|20)\d{2}|"
            r"from\s+(?:19|20)\d{2}\s+(?:to|through)\s+(?:19|20)\d{2}|"
            r"since\s+(?:19|20)\d{2}|(?:19|20)\d{2}\s*[—–-]\s*(?:19|20)\d{2}|"
            r"自\s*(?:19|20)\d{2}|(?:19|20)\d{2}年至(?:19|20)\d{2}年|时间范围|期间",
            paragraph,
        )
        entry_rule = present(
            r"eligibility|same\s+selection|entered|included|added|screened|source\s+was\s+logged|"
            r"additions?[^.。;；]{0,50}(?:meet|met|satisf(?:y|ied))[^.。;；]{0,30}"
            r"(?:identical|same)?\s*inclusion|"
            r"纳入|进入|筛选|同一选择|记录来源",
            paragraph,
        )
        if provenance and time_boundary and entry_rule:
            return True
    return False


def secondary_source_roles(text: str, secondary_sources: list[str]) -> dict[str, bool]:
    roles: dict[str, bool] = {}
    items = sentence_units(text)
    collective_mixed_roles = (
        "publisher_platforms" in secondary_sources
        and "doi_landing_pages" in secondary_sources
        and present(
            r"these\s+(?:resources|sources)[^.。]{0,140}"
            r"(?:(?:PDFs?|full[- ]texts?)[^.。]{0,100}"
            r"(?:metadata|corrections?|retractions?|status)|"
            r"(?:metadata|corrections?|retractions?|status)[^.。]{0,100}"
            r"(?:PDFs?|full[- ]texts?))",
            text,
        )
    )
    for source in secondary_sources:
        if collective_mixed_roles and source in {
            "publisher_platforms",
            "doi_landing_pages",
        }:
            roles[source] = False
            continue
        if source in SECONDARY_ROLE_PATTERNS:
            roles[source] = present(SECONDARY_ROLE_PATTERNS[source], text)
            if roles[source]:
                continue
            source_pattern = DISCOVERY_OR_VERIFICATION_PATTERNS[source]
            for index, sentence in enumerate(items[:-1]):
                if not present(source_pattern, sentence):
                    continue
                following = items[index + 1]
                explicit_one_sentence_link = present(
                    r"^(?:those|these)\s+(?:sites?|pages?|platforms?)\b|^they\b|"
                    r"^(?:前述|上述|这些)(?:平台|页面)",
                    following,
                )
                if source == "publisher_platforms" and explicit_one_sentence_link and present(
                    r"(?:suppl(?:y|ied)|provid(?:e|ed)|yield(?:ed)?|host(?:ed)?)"
                    r"[^.。]{0,80}(?:article\s+)?(?:PDFs?|full[- ]texts?)|"
                    r"(?:download|retriev|access|承担)[^.。]{0,80}(?:full[- ]texts?|全文)",
                    following,
                ):
                    roles[source] = True
                    break
                if source == "doi_landing_pages" and explicit_one_sentence_link and present(
                    r"(?:resolv|verif|confirm|check|corroborat|核验|确认|核对)[^.。]{0,100}"
                    r"(?:corrections?|dates?|years?|authors?|metadata|retractions?|status|"
                    r"更正|日期|年份|作者|元数据|撤稿|状态)",
                    following,
                ):
                    roles[source] = True
                    break
                # A bookkeeping sentence may intervene.  Accept a two-sentence
                # link only when the later sentence repeats the source noun;
                # bare ``they`` remains ambiguous when a competing plural noun
                # has appeared in between.
                if index + 2 >= len(items):
                    continue
                later = items[index + 2]
                if source == "publisher_platforms" and present(
                    r"^(?:those|these)\s+platforms?\b|^(?:前述|上述|这些)平台",
                    later,
                ) and present(
                    r"(?:suppl(?:y|ied)|provid(?:e|ed)|yield(?:ed)?|host(?:ed)?|"
                    r"download|retriev|access|承担)[^.。]{0,90}(?:article\s+)?"
                    r"(?:PDFs?|full[- ]texts?|全文)",
                    later,
                ):
                    roles[source] = True
                    break
                if source == "doi_landing_pages" and present(
                    r"^(?:those|these)(?:\s+landing)?\s+pages?\b|^(?:前述|上述|这些)页面",
                    later,
                ) and present(
                    r"(?:resolv|verif|confirm|check|corroborat|核验|确认|核对)[^.。]{0,110}"
                    r"(?:corrections?|dates?|years?|authors?|metadata|retractions?|status|"
                    r"更正|日期|年份|作者|元数据|撤稿|状态)",
                    later,
                ):
                    roles[source] = True
                    break
        elif source == "author_curated_collection":
            roles[source] = author_collection_boundary_present(text)
    return roles


def selection_features(text: str) -> dict[str, bool]:
    items = sentence_units(text)
    features: dict[str, bool] = {}
    domain_only = (
        r"imaging\s+dataset|microscopy|screen(?:ed|ing)?\s+(?:images?|micrographs?)|"
        r"fabrication\s+(?:pipeline|workflow)|candidate\s+deduplication|"
        r"molecular?\s+candidates?|(?:polymer\s+)?candidate\s+library|training\s+(?:data|dataset)|"
        r"electronic\s+(?:health|medical)\s+records?|patient\s+records?|cohort|clinicians?|"
        r"hospital\s+registry|clinical\s+(?:cohort|cases?)|case\s+records?|"
        r"tissue\s+(?:slice|section|slide)s?|specimen\s+barcodes?|pathologists?|"
        r"spectromet(?:er|ry)|instrument\s+records?|assay\s+preprocessing|outcome\s+modelling|"
        r"材料候选|候选库|显微图像|制备流程|患者记录|病例记录|临床队列|"
        r"电子病历|仪器记录|病例流程图|组织切片|标本条码|病理学家"
    )
    bibliographic_subject = (
        r"bibliographic\s+(?:search\s+)?(?:records?|citations?|references?|exports?)|"
        r"(?:literature|database\s+search|search)\s+(?:records?|exports?)|"
        r"(?:文献|题录)(?:检索)?(?:记录|导出)"
    )
    for name, pattern in SELECTION_PATTERNS.items():
        matched = False
        for index, sentence in enumerate(items):
            for _hit in re.finditer(pattern, sentence, flags=re.IGNORECASE | re.DOTALL):
                # Bind a selection signal to the sentence's scientific subject.
                # Patient records, images, candidates and instrument output are not
                # bibliographic records merely because they occur near review prose.
                discourse_context = sentence
                if index:
                    previous = items[index - 1]
                    explicit_coreference = present(
                        r"^(?:those|these|the|such)\s+records?\b|^they\b", sentence
                    )
                    implicit_record_pipeline = present(
                        domain_only, previous
                    ) and present(
                        r"^(?:duplicate\s+(?:records?|citations?|references?)|"
                        r"(?:records?|citations?|references?)\s+(?:were\s+)?deduplicat)",
                        sentence,
                    )
                    if explicit_coreference or implicit_record_pipeline:
                        discourse_context = previous + " " + sentence
                        if index > 1 and explicit_coreference:
                            discourse_context = items[index - 2] + " " + discourse_context
                if name in {"deduplication", "screening", "flow_accounting"} and present(
                    domain_only, discourse_context
                ):
                    positive_bibliographic = present(
                        bibliographic_subject, discourse_context
                    ) and not present(
                        r"(?:rather\s+than|not)\s+(?:the\s+)?(?:bibliographic\s+)?"
                        r"(?:citations?|records?|search\s+exports?)",
                        discourse_context,
                    )
                    if not positive_bibliographic:
                        continue
                matched = True
                break
            if matched:
                break
        features[name] = matched
    return features


def ordered_pattern_names(patterns: dict[str, str], text: str) -> list[str]:
    hits: list[tuple[int, int, str]] = []
    for order, (name, pattern) in enumerate(patterns.items()):
        match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
        if match is not None:
            hits.append((match.start(), order, name))
    return [name for _, _, name in sorted(hits)]


def build_report(path: Path, text: str) -> dict[str, Any]:
    body = body_without_references(text)
    context = search_context(body)
    review_type = declared_review_type(body)
    databases = ordered_pattern_names(DATABASE_PATTERNS, context)
    secondary_sources = ordered_pattern_names(DISCOVERY_OR_VERIFICATION_PATTERNS, context)
    source_roles = secondary_source_roles(context, secondary_sources)
    selection = selection_features(context)
    inventory = keyword_inventory(context)
    exact_query = executable_query_present(context)
    cutoff = search_cutoff_present(context)
    supplement_status = supplementary_search_status(context)
    supplement = supplement_status == "claimed_present"
    boundary_paragraphs = count_paragraphs(COVERAGE_BOUNDARY, body)

    diagnostics: list[dict[str, str]] = []
    if (
        review_type in {"structured_narrative", "narrative"}
        and inventory
        and not exact_query
        and not supplement
    ):
        diagnostics.append(
            {
                "code": "query_like_inventory_without_executable_query",
                "level": "revise",
                "reason": (
                    "The manuscript lists many search terms but does not provide a database-specific, "
                    "rerunnable query. This can look systematic without being reproducible."
                ),
                "action": (
                    "Keep the main text focused on sources, cutoff, purpose, and selection logic; either "
                    "place exact database-specific strings in a supplement or replace the inventory with "
                    "a concise description of the search concept blocks."
                ),
            }
        )
    unclear_secondary_roles = [
        source
        for source in ("publisher_platforms", "doi_landing_pages")
        if source in secondary_sources and not source_roles.get(source, False)
    ]
    if unclear_secondary_roles:
        diagnostics.append(
            {
                "code": "discovery_and_verification_sources_need_roles",
                "level": "check",
                "reason": (
                    "Publisher platforms and DOI landing pages do not describe one reproducible bibliographic index."
                ),
                "action": (
                    "Name the primary bibliographic databases separately and state whether publisher or DOI pages "
                    "were used for discovery, full-text retrieval, metadata verification, or publication-status checks."
                ),
            }
        )
    if (
        "author_curated_collection" in secondary_sources
        and not source_roles.get("author_curated_collection", False)
    ):
        diagnostics.append(
            {
                "code": "author_collection_boundary_needed",
                "level": "check",
                "reason": "An author-curated collection can add valuable sources but is not self-defining.",
                "action": (
                    "State how the collection was assembled, what period and source types it covers, and how records "
                    "from it entered the illustrative selection."
                ),
            }
        )
    if (
        supplement_status == "planned_or_placeholder"
        and review_type not in {"systematic", "scoping", "meta_analysis"}
    ):
        diagnostics.append(
            {
                "code": "planned_supplement_not_current_evidence",
                "level": "critical" if review_type in {"systematic", "scoping", "meta_analysis"} else "check",
                "reason": "A future or placeholder supplementary search record is not an existing rerunnable strategy.",
                "action": "Complete and attach the record before citing it; until then, treat the search strategy as missing.",
            }
        )
    if repeated_boundary_function(body):
        diagnostics.append(
            {
                "code": "repeated_non_systematic_disclaimer",
                "level": "revise",
                "reason": "The same coverage boundary is stated in more than one paragraph.",
                "action": "Retain one precise boundary sentence and use the recovered space for the review's selection logic.",
            }
        )

    systematic_types = {"systematic", "scoping", "meta_analysis"}
    missing_systematic: list[str] = []
    if review_type in systematic_types:
        requirements = {
            "named_database": bool(databases),
            "search_date_or_cutoff": cutoff,
            "executable_query_or_supplement": exact_query or supplement,
            "eligibility_criteria": selection["eligibility"],
            "deduplication": selection["deduplication"],
            "screening_process": selection["screening"],
            "flow_accounting": selection["flow_accounting"],
        }
        missing_systematic = [name for name, available in requirements.items() if not available]
        if missing_systematic:
            diagnostics.append(
                {
                    "code": "systematic_review_reporting_incomplete",
                    "level": "critical",
                    "reason": "The declared review type requires a reproducible selection record that is not fully reported.",
                    "action": "Complete the protocol and reporting record; do not solve this by weakening prose alone.",
                }
            )

    if review_type in {"structured_narrative", "narrative"}:
        if databases and cutoff and selection["selection_logic"] and boundary_paragraphs:
            disclosure_pattern = "transparent_narrative_scope"
        else:
            disclosure_pattern = "partial_narrative_scope"
    elif review_type in systematic_types:
        disclosure_pattern = (
            "systematic_record_structurally_complete" if not missing_systematic else "systematic_record_incomplete"
        )
    else:
        disclosure_pattern = "review_type_not_declared"

    return {
        "tool": "CNS Skills review search audit",
        "version": VERSION,
        "source": str(path.resolve()),
        "disclaimer": (
            "This diagnostic reports structural signals only. The label "
            "systematic_record_structurally_complete means only that the required textual signals were detected; "
            "it does not verify that a cited supplement exists, prove a query is rerunnable, authenticate the search "
            "or screening record, establish reproducibility or venue compliance, score review quality, or convert a "
            "narrative review into a systematic review. A zero strict-mode exit code is not an acceptance, "
            "authenticity, reproducibility, or reporting-compliance decision. This tool does not open cited "
            "supplements, execute database queries, inspect search exports, or validate deduplication and screening "
            "logs. Manual inspection of the real search materials and current venue instructions remains "
            "authoritative."
        ),
        "declared_review_type": review_type,
        "disclosure_pattern": disclosure_pattern,
        "evidence": {
            "named_databases": databases,
            "discovery_or_verification_sources": secondary_sources,
            "source_roles_explicit": source_roles,
            "search_context_paragraphs": len(paragraphs(context)),
            "search_date_or_cutoff": cutoff,
            "keyword_inventory": inventory,
            "executable_query_markers": exact_query,
            "supplementary_search_record": supplement,
            "supplementary_search_status": supplement_status,
            "selection": selection,
            "coverage_boundary_paragraphs": boundary_paragraphs,
        },
        "missing_systematic_elements": missing_systematic,
        "diagnostics": diagnostics,
    }


def shareable_report(report: dict[str, Any]) -> dict[str, Any]:
    output = dict(report)
    output["source"] = Path(str(report["source"])).name
    output["shareable_redaction"] = "The local path and manuscript text were not retained."
    return output


def render_text(report: dict[str, Any]) -> str:
    evidence = report["evidence"]
    lines = [
        f"CNS Skills review search audit v{report['version']}",
        f"Source: {report['source']}",
        f"Declared type: {report['declared_review_type']}",
        f"Disclosure pattern: {report['disclosure_pattern']}",
        "Named databases: " + (", ".join(evidence["named_databases"]) or "none detected"),
        f"Keyword inventory / executable query: {evidence['keyword_inventory']} / {evidence['executable_query_markers']}",
        f"Diagnostics: {len(report['diagnostics'])}",
    ]
    for item in report["diagnostics"]:
        lines.append(f"- [{item['level']}] {item['code']}: {item['action']}")
    lines.append(report["disclaimer"])
    return "\n".join(lines)


def same_path(left: Path, right: Path) -> bool:
    return str(left.resolve()).casefold() == str(right.resolve()).casefold()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument("input", type=Path, help="DOCX, Markdown, or text review manuscript")
    parser.add_argument("--json", type=Path, help="write a JSON report")
    parser.add_argument("--shareable", action="store_true", help="redact the local path")
    parser.add_argument(
        "--strict-systematic",
        action="store_true",
        help="return exit code 3 when a declared systematic/scoping/meta-analytic review lacks required structural signals",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.json and same_path(args.input, args.json):
        print("error: --json output cannot overwrite the input", file=sys.stderr)
        return 2
    try:
        report = build_report(args.input, read_text(args.input))
    except (OSError, ValueError, zipfile.BadZipFile, ET.ParseError) as error:
        print(f"review search audit failed: {error}", file=sys.stderr)
        return 2
    output = shareable_report(report) if args.shareable else report
    print(render_text(output))
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.strict_systematic and report["missing_systematic_elements"]:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
