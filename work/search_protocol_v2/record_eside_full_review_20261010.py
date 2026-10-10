import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/图像鉴伪解释可靠性_重检_2026-10-05"
TITLE = "Explainable Synthetic Image Detection Through Diffusion Timestep Ensembling"
URL = "https://ojs.aaai.org/index.php/AAAI/article/view/38060"
PDF = "https://ojs.aaai.org/index.php/AAAI/article/download/38060/42022"


def read(name):
    with (OUT / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write(name, rows):
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


methods = (
    "AAAI-26 official 9-page paper, Proceedings of AAAI 40(13), 10844-10852, DOI 10.1609/aaai.v40i13.38060. ESIDE combines DDIM intermediate-noise "
    "timestep classifiers for synthetic-image detection and adds a flaw-to-text explanation pipeline. GenExplain has 54,210 image/flaw/explanation groups "
    "across 14 flaw categories. GPT-4o first proposes labels for GenImage validation images; manual pruning removes 30.1%-67.4% of images categorized "
    "incorrectly in each subset. GPT-4o then generates phrase explanations, spaCy segments phrases, Faster R-CNN proposes image regions, and CLIP-based "
    "text-image cross-attention computes phrase-region similarity scores; top-k phrases are retained and re-refined for three iterations. Reported refinement "
    "measures include image-text similarity (sim@5/@10/overall) and lexical diversity/fluency proxies (TTR, entropy, perplexity)."
)
evidence = (
    "The paper directly identifies a substantial reliability problem in standalone MLLM flaw annotation: manual pruning rejects 30.1%-67.4% of initial "
    "GPT-4o image/category assignments as incorrect. It introduces a metric-guided grounding/refinement mechanism, and reports rising CLIP phrase-region "
    "similarity after refinement. This is a direct candidate for synthetic-image explanation quality and grounding; the rejection fraction is evidence about "
    "dataset label quality, while the similarity measure is an automated proxy rather than independent truth verification."
)
limitations = (
    "The paper gives no detailed human-pruning protocol, number or expertise of annotators, blinding, inter-rater agreement, or adjudication; therefore the "
    "30.1%-67.4% correction rate cannot be interpreted as a fully reproducible human hallucination estimate. Similarity is used both to select/refine phrases "
    "and as the reported explanation metric, creating a metric-alignment limitation; CLIP semantic similarity to detected regions does not establish that an "
    "artifact claim is true, causally relevant, necessary, or sufficient for the detector's decision. No pixel mask truth for explanation claims, human "
    "factuality review, explanation stability, deletion/insertion, model randomization, user comprehension, trust calibration, or appropriate reliance study is "
    "reported. The robustness experiments test detection accuracy under image perturbations, not explanation reliability."
)
reviews = read("172_强相关核心及邻接论文原文解释可靠性效度核读.csv")
record = {
    "paper": TITLE,
    "verified_identity": "Yixin Wu et al.; AAAI-26, Proceedings of AAAI 40(13), 10844-10852 (2026); DOI 10.1609/aaai.v40i13.38060; official AAAI full text.",
    "relevance_class": "直接强相关：合成图像检测解释生成、自动化接地/迭代修订和初始LLM标注错误筛查。",
    "primary_source": URL,
    "scope_and_methods": methods,
    "observed_reliability_evidence": evidence,
    "limitations_and_construct_boundary": limitations,
    "screening_conclusion": "AAAI正式全文已核，直接纳入；最有价值的可靠性发现是初始GPT-4o缺陷标签经人工筛除30.1%-67.4%错误，但人工协议未充分报告。迭代相似度改进不构成独立事实性或因果faithfulness验证。",
    "review_date": "2026-10-10",
}
existing = next((r for r in reviews if r["paper"].casefold() == TITLE.casefold()), None)
if existing:
    existing.update(record)
else:
    reviews.append(record)
assert len({r["paper"].casefold() for r in reviews}) == len(reviews)
write("172_强相关核心及邻接论文原文解释可靠性效度核读.csv", reviews)

candidates = read("90_本轮新增强相关候选与引文复核.csv")
c = next(r for r in candidates if r["title"].casefold().startswith(TITLE.casefold()))
c.update({
    "authors_year_venue": "Yixin Wu et al. — AAAI-26 (2026), 40(13), 10844-10852; DOI 10.1609/aaai.v40i13.38060",
    "preliminary_status": "AAAI官方全文已核；直接强相关；含自动phrase-region grounding/refinement，初始GPT-4o标签人工筛除率30.1%-67.4%",
    "relevance_reason": "GenExplain 54,210 image/flaw/explanation组，使用Faster R-CNN区域与CLIP text-image相似度做解释迭代；人工筛掉30.1%-67.4%错误初始类别，但修订指标仍是自动相似度代理。",
    "discovery_query_id": "T05-F2-AIGEN-ATTR; priority rank 9 full-text review",
    "discovery_query": "AI-generated image detection explanation and grounding reliability",
    "source_url": URL,
    "screen_basis": "AAAI正式全文§3.3–3.4、§4.3及官方PDF；核对GenExplain构建、人工筛除和解释修订指标，分开解释正确性与检测精度。",
})
write("90_本轮新增强相关候选与引文复核.csv", candidates)

priority = read("72_V2已复核强相关优先清单.csv")
p = next(r for r in priority if r["title"].casefold().startswith(TITLE.casefold()))
p.update({
    "V2_relation": "直接强相关：54,210组缺陷理由与CLIP phrase-region相似度修订；GPT-4o初始类别人工筛错率高但人评协议未报",
    "original_reading_scope": "AAAI官方全文§§3.3–3.4、4.2–4.3、实验表与数据构建；GenExplain标注和修订效度边界已核。",
    "limitations": limitations,
    "reassessment": "rank 9候选已完成AAAI正式全文核读。其人工筛除初始错分类比例是可用可靠性线索，但审核流程未报告；CLIP相似度经迭代优化不等同外部claim真值或因果忠实性。",
})
write("72_V2已复核强相关优先清单.csv", priority)

report = OUT / "00_重检阶段报告_未完成.md"
section = f"""

---

# 2026-10-10续：ESIDE/GenExplain正式全文核读

- ESIDE为AAAI-26正式论文。GenExplain包含54,210组图像/缺陷类别/理由，14类生成图缺陷。作者先用GPT-4o给GenImage验证图分类，经人工筛选删去各子集30.1%–67.4%的错误图像—缺陷标签，随后再生成文本理由。短语经过Faster R-CNN候选区域与CLIP text-image cross-attention评分，保留Top-K并迭代三轮修订。
- 该人工筛除率提示独立LLM flaw labeling存在较高错类风险；但论文未交代评审人数、专业背景、盲法、IAA和争议裁决，不能把比例表述成高质量人类幻觉率。迭代后提升的CLIP相似度是系统使用的自动代理指标，不是claim真值核验。没有解释因果faithfulness、充分/必要性、用户依赖或信任校准实验。
- 来源：AAAI官方记录{URL}；正式PDF {PDF}。
"""
old = report.read_text(encoding="utf-8")
if "# 2026-10-10续：ESIDE/GenExplain正式全文核读" not in old:
    report.write_text(old + section, encoding="utf-8")
