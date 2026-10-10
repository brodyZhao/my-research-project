import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/图像鉴伪解释可靠性_重检_2026-10-05"
TITLE = "Towards General Visual-Linguistic Face Forgery Detection"
URL = "https://openaccess.thecvf.com/content/CVPR2025/html/Sun_Towards_General_Visual-Linguistic_Face_Forgery_Detection_CVPR_2025_paper.html"
ARXIV = "https://arxiv.org/html/2502.20698"


def read(name):
    with (OUT / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write(name, rows):
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


methods = (
    "CVPR 2025 final paper; official CVF page and author arXiv HTML (arXiv:2502.20698) checked. Face Forgery Text Generator (FFTG) makes raw "
    "annotations from paired real/fake frames: absolute pixel difference yields a forgery map; facial landmarks divide mouth/nose/eyes/face regions; "
    "handcrafted color, blur, SSIM, texture, and boundary criteria identify region/type; GPT-4o-mini then refines text using the paired images, raw "
    "annotation and derivation, task instructions, and schema. The study compares human DD-VQA, direct GPT-4o-mini, and FFTG annotations. For MLLM "
    "outputs, explanation quality is evaluated by checking whether region terms match the known forgery-mask areas."
)
evidence = (
    "Using forgery masks as region ground truth, annotation region-identification precision/recall/F1 are 89.48/57.12/64.96 for FFTG, versus "
    "62.46/51.52/52.06 for DD-VQA and 61.27/44.00/47.18 for direct GPT-4o-mini. For the fine-tuned MLLM explanation outputs, region-term "
    "precision/recall are 88.07/55.30 for FFTG supervision, versus 62.94/53.62 for DD-VQA supervision and 58.26/41.85 for direct GPT-4o-mini "
    "supervision. This is direct region-grounding and annotation-hallucination evidence for face forgery images/frames."
)
limitations = (
    "The explanation metric checks whether a named facial region (mouth/nose/eyes/face) matches a manipulation mask using exact terms or synonyms; "
    "it does not verify the specific artifact claim, whether the rationale captures all relevant evidence, or whether the classifier causally relies on it. "
    "FFTG's reference depends on paired original/manipulated images and pixel-difference-derived masks, then hand-coded thresholds and GPT-4o-mini; the "
    "pipeline is therefore strongest for paired face manipulations and its error profile may not transfer to unpaired or general image tampering. The paper "
    "reports neither independent human claim verification/IAA for the generated explanations nor deletion/insertion, counterfactual necessity/sufficiency, "
    "user comprehension, appropriate reliance, or trust calibration. The human DD-VQA baseline is a competing annotation source, not a blinded reliability "
    "study of the final model explanations."
)
reviews = read("172_强相关核心及邻接论文原文解释可靠性效度核读.csv")
record = {
    "paper": TITLE,
    "verified_identity": "Ke Sun et al.; Proceedings of CVPR 2025, pp. 19576-19586; official CVF record and arXiv:2502.20698.",
    "relevance_class": "直接强相关（面部图像/视频帧伪造邻域）：自然语言解释的mask区域接地及标注幻觉评测。",
    "primary_source": URL,
    "scope_and_methods": methods,
    "observed_reliability_evidence": evidence,
    "limitations_and_construct_boundary": limitations,
    "screening_conclusion": "官方CVPR全文已核，直接纳入面部图像伪造解释可靠性目录；支持区域指称接地和降低越区幻觉的结论，不扩张为artifact claim真实性、决策因果faithfulness或用户适当依赖证据。",
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
c = next(r for r in candidates if r["title"].casefold() == TITLE.casefold())
c.update({
    "authors_year_venue": "Ke Sun et al. — CVPR 2025, 19576-19586; arXiv:2502.20698",
    "preliminary_status": "CVPR 2025官方全文/附录已核；直接强相关（面部图像/视频帧）；报告mask区域grounding指标",
    "relevance_reason": "FFTG以原始/伪造帧mask为视觉证据，比较人工、GPT-4o-mini、FFTG自然语言解释的伪造区域指认；最终MLLM解释区域precision/recall为88.07/55.30，但尚非claim级或因果faithfulness评测。",
    "discovery_query_id": "T05-F2-AIGEN-ATTR; priority rank 7 full-text review; X-AIGD REF045",
    "discovery_query": "AIGI/image forgery解释接地检索及X-AIGD引文链",
    "source_url": URL,
    "screen_basis": "CVF官方CVPR 2025页面、arXiv官方HTML §§3/5及附录C/D；区分区域提及检索指标与claim事实性/因果解释效度。",
})
write("90_本轮新增强相关候选与引文复核.csv", candidates)

priority = read("72_V2已复核强相关优先清单.csv")
p = next(r for r in priority if r["title"].casefold() == TITLE.casefold())
p.update({
    "V2_relation": "直接强相关（面部伪造）：mask-grounded区域提及与标注幻觉指标；无claim-level、因果或用户依赖测试",
    "original_reading_scope": "CVPR 2025官方全文及arXiv HTML §§3–5、Appendix C/D；生成标注、解释指标与数据边界已核。",
    "limitations": limitations,
    "reassessment": "rank 7未完成记录现已全文核读。保留直接相关，限定为面部图像/视频帧的自然语言伪造区域接地。表中88.07/55.30仅表示region precision/recall，不是完整解释真实性或faithfulness。",
})
write("72_V2已复核强相关优先清单.csv", priority)

report = OUT / "00_重检阶段报告_未完成.md"
section = f"""

---

# 2026-10-10续：VL-FFD/FFTG区域解释接地全文核读

- CVPR 2025正式论文《Towards General Visual-Linguistic Face Forgery Detection》通过CVF官方页及arXiv全文核对。FFTG利用已配对真/伪帧差分mask、面部区域与手工伪造类型线索生成初始证据，再以GPT-4o-mini润色解释。
- 以已知mask区域为真值，标注的region precision/recall/F1为89.48/57.12/64.96（DD-VQA人标62.46/51.52/52.06；直出GPT-4o-mini 61.27/44.00/47.18）。用该标注训练的MLLM解释region precision/recall为88.07/55.30（DD-VQA训练62.94/53.62；GPT直出训练58.26/41.85）。这属于区域指称grounding，不是claim artifact事实准确或决策因果faithfulness。
- 效度边界：指标只抽取mouth/nose/eyes/face区域名与mask重合，依赖成对原图和伪造mask；无独立人评最终输出、IAA、充分/必要干预或适当依赖测试。人工DD-VQA是参照标注方案，并非模型用户研究。面部视频帧伪造与通用静态图像篡改需分层解释。
- 来源：{URL}；{ARXIV}。
"""
old = report.read_text(encoding="utf-8")
if "# 2026-10-10续：VL-FFD/FFTG区域解释接地全文核读" not in old:
    report.write_text(old + section, encoding="utf-8")
