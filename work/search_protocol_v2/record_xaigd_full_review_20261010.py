import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/图像鉴伪解释可靠性_重检_2026-10-05"
TITLE = "Unveiling Perceptual Artifacts: A Fine-Grained Benchmark for Interpretable AI-Generated Image Detection"
URL = "https://arxiv.org/html/2601.19430"


def read(name):
    with (OUT / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write(name, rows):
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


methods = (
    "arXiv:2601.19430v1, 2026-01-27, official HTML including appendices. X-AIGD contains paired real/fake images from 13 generators, "
    "7 artifact categories, and 18,202 pixel-level artifact instances across 3,035 valid annotated fake samples. Twelve annotators with higher "
    "education and foundational AIGI knowledge label artifacts in three relay rounds; later annotators inspect earlier labels and add missed regions, "
    "and annotations are retained rather than adjudicated to one canonical mask. Three independent annotators then rate confidence for every instance "
    "as 0, 0.5, or 1. Existing detectors' Grad-CAM, relevance maps, or sliding-patch heatmaps are binarized at 0.5 and compared to human masks using "
    "IoU and pixel precision/recall/F1. The paper tests perceptual artifact reliance, auxiliary artifact segmentation, and attention alignment against "
    "artifact masks; alignment is also compared with saliency, random, and benign masks, and repeated over 10 seeds."
)
evidence = (
    "The benchmark directly tests spatial agreement between model explanations and human-labeled visible artifacts. Existing detectors generally show "
    "weak agreement: for example, Category-Agnostic PAD IoU / pixel-F1 are 0.5 / 1.8 for CNNSpot, 0.4 / 0.8 for UnivFD, 0.5 / 0.9 for FatFormer, "
    "and 0.7 / 1.5 for DRCT-CLIP (reported as percentages in the table). Accuracy also does not significantly track the benchmark's perceptual-artifact "
    "ratio, and detected artifact masks need not correspond to the classifier's actual cues. Artifact-mask attention alignment improves both mask alignment "
    "and cross-dataset detection relative to no alignment and saliency/random/benign-mask controls; results average 10 seeds. This is evidence about "
    "visual grounding and a useful diagnostic of shortcut reliance, not a complete causal-faithfulness test."
)
limitations = (
    "The annotation workflow deliberately preserves disagreement and has no single adjudicated gold mask; the three-round relay means the three masks "
    "are not independent annotations. Confidence scoring by three additional independent raters provides instance-level certainty but the paper does not "
    "report an inter-rater reliability statistic. IoU/pixel overlap measures spatial agreement, not whether evidence is necessary/sufficient for the decision; "
    "attention alignment changes training and is not a deletion/insertion or counterfactual intervention on a fixed model. The artifact taxonomy captures "
    "human-perceptible synthetic-image defects, not every valid detector cue (e.g. low-level fingerprints), and image generation is limited to 13 generators. "
    "No natural-language explanation factuality/hallucination study, end-user comprehension, trust calibration, or appropriate-reliance experiment is reported. "
    "The authors explicitly list human alignment as future evaluation."
)
reviews = read("172_强相关核心及邻接论文原文解释可靠性效度核读.csv")
record = {
    "paper": TITLE,
    "verified_identity": "Yao Xiao et al.; arXiv:2601.19430v1, 2026-01-27; official arXiv HTML and appendices.",
    "relevance_class": "直接强相关：AI生成图像检测解释的像素级伪影接地基准；同时检验检测器是否真正使用人类可感知伪影作为判别线索。",
    "primary_source": URL,
    "scope_and_methods": methods,
    "observed_reliability_evidence": evidence,
    "limitations_and_construct_boundary": limitations,
    "screening_conclusion": "全文/附录已核。直接纳入图像鉴伪解释可靠性目录，归为视觉空间接地与线索依赖诊断证据；其掩码重叠与训练注意力对齐不足以单独证明因果忠实性或解释充分性。",
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
    "authors_year_venue": "Yao Xiao et al. — arXiv:2601.19430v1 (2026-01-27); ICLR 2026 proceedings record listed by authors",
    "preliminary_status": "官方arXiv全文/附录已核；直接强相关；像素级人工伪影标注、解释热图接地与artifact-reliance分析",
    "relevance_reason": "X-AIGD将检测解释热图与18,202个人工像素伪影实例直接比较，并测试准确率是否随人类可感知伪影变化；发现传统检测器解释空间重合弱且准确率不依赖显著伪影。",
    "discovery_query_id": "T05-F2-AIGEN-ATTR; priority rank 5 full-text review",
    "discovery_query": "AI-generated image interpretation and grounded artifact evaluation",
    "source_url": URL,
    "screen_basis": "官方arXiv全文§§3–6、Appendices A.3/A.5/B.3/D.3/E；核对12名标注者relay协议、三人独立置信度复核、热图重叠与10-seed注意力对齐实验。",
})
write("90_本轮新增强相关候选与引文复核.csv", candidates)

priority = read("72_V2已复核强相关优先清单.csv")
p = next(r for r in priority if r["title"].casefold().startswith(TITLE.casefold()))
p.update({
    "V2_relation": "直接强相关：18,202个人工伪影实例支持解释热图接地与检测线索依赖诊断；不测自然语言理由或适当依赖",
    "original_reading_scope": "arXiv官方全文§§3–6及Appendices A.3/A.5/B.3/D.3/E；数据标注协议、空间重叠与对照实验已核。",
    "limitations": limitations,
    "reassessment": "排名5的未核直接候选已完成全文/附录核读。保留强相关；其主要贡献是视觉空间接地与人工标注伪影基准。三轮relay标注无裁决且未报IAA；mask overlap不是因果充分性/必要性测试。",
})
write("72_V2已复核强相关优先清单.csv", priority)

report = OUT / "00_重检阶段报告_未完成.md"
section = f"""

---

# 2026-10-10续：X-AIGD像素级接地基准全文与附录核读

- arXiv:2601.19430v1全文/附录核读：X-AIGD有13个生成器、7类伪影、18,202个实例，分布于3,035个有效人工标注合成样本及配对真实图。12位标注者按三轮relay方式补充区域，保留全部掩码而不强行合并；另3名独立标注者逐实例给出0/0.5/1置信分。
- 作者将Grad-CAM、relevance map或滑窗热图阈值化后与人工mask比较IoU、像素precision/recall/F1；多个既有检测器的热图空间重合很低，并报告检测准确率不随PAR显著变化、分类线索与分割伪影不必相同。artifact-mask attention alignment相较无对齐及saliency/random/benign控制提高空间重合与跨数据集指标，报告10个随机种子。
- 效度边界：relay标注不是独立重复评审；三人置信度评分未配IAA。空间mask重合及改变训练目标不能替代固定模型上的必要/充分因果干预；没有自然语言claim事实性、用户信赖校准或适当依赖实验。作者将human alignment列为后续方向。已列直接强相关，避免将注意力对齐过度表述为faithfulness证明。
- 来源：{URL}。
"""
old = report.read_text(encoding="utf-8")
if "# 2026-10-10续：X-AIGD像素级接地基准全文与附录核读" not in old:
    report.write_text(old + section, encoding="utf-8")
