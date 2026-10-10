import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/图像鉴伪解释可靠性_重检_2026-10-05"
TITLE = "Specialist-Generalist Fusion with Outcome-Supervised Rationales for Deepfake Detection"
URL = "https://arxiv.org/html/2605.31192v2"


def read(name):
    with (OUT / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write(name, rows):
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


methods = (
    "arXiv v2 official HTML, 2026-08-24. Specialist forensic features and Qwen2.5-VL vision features jointly feed the classifier. "
    "Outcome-supervised rationale RL uses only binary label correctness and output-format reward, with no target explanation annotations. "
    "Rationales are optional at inference; authors state quantitative detection tests run without rationales. The user study compares "
    "10 model descriptions with 10 DD-VQA human-annotated descriptions, shown in randomized order to each of three computer-vision experts; "
    "each rates whether the described artifact exists on a 1–5 scale. Model mean 3.57 (SD 1.10), DD-VQA 3.83 (SD 0.99). Appendix bootstrap "
    "resamples ratings one million times and reports 0.988 probability of the model mean lying within one smaller SD of the reference mean. "
    "Separately, Gemini checks 40 annotated images for overlap-based hallucination (7.5%); a further 20-explanation Gemini image-match check "
    "marks 95.7% of claimed artifacts image-supported, including two partial hallucinations that also contain another supported artifact. "
    "A causal-grounding intervention masks cited artifact boxes versus matched non-cited face regions on 50 correctly classified samples; cited-region "
    "masking produces 45% larger error (geometric average)."
)
limitations = (
    "Three computer-vision experts provide direct artifact-existence judgments; the user study is small (20 descriptions per expert, 60 rating events), "
    "and the paper reports no inter-rater reliability or detailed expertise profile. The same 20 stimulus descriptions may be reused across raters; "
    "resampling responses does not establish generalization to new images or annotators. The study explicitly selects correctly classified cases, so it "
    "does not assess explanation reliability when the detector is wrong, nor appropriate user reliance. The Gemini 7.5% overlap rule and 95.7% claim-support "
    "estimate are model-judged, not independent human fact checking; a rationale can contain at least one supported artifact and still omit or misstate others. "
    "The cited-region masking test is direct causal evidence of local decision relevance, but covers only 50 correctly classified examples, uses an "
    "occlusion intervention that can itself perturb image statistics, and does not test sufficiency/restoration or behavior on errors. Binary-label reward can "
    "improve detection without requiring faithful reasoning; authors' output-order control explicitly allows hallucinated explanations. No parameter-randomization, "
    "insertion test, or human decision-reliance experiment is reported."
)
reviews = read("172_强相关核心及邻接论文原文解释可靠性效度核读.csv")
record = {
    "paper": TITLE,
    "verified_identity": "Benedikt Hopf, Zongwei Wu, Radu Timofte; arXiv:2605.31192v2, 2026-08-24; official arXiv HTML.",
    "relevance_class": "直接强相关：深伪检测的结果监督视觉理由，含专家对视觉伪迹存在性的人工评审及claim级LLM辅助核查。",
    "primary_source": URL,
    "scope_and_methods": methods,
    "observed_reliability_evidence": "三名计算机视觉领域专家分别评价随机顺序的10条本模型解释与10条DD-VQA人工解释，按伪迹是否存在打1–5分；模型3.57±1.10、DD-VQA 3.83±0.99。40张图用Gemini做参考描述重合型hallucination筛查（作者报告7.5%）；另20条解释的Gemini图像匹配/claim核查报告95.7% claim被标为图像支持。另在50个正确分类样本比较理由引用伪迹框遮挡与匹配未引用人脸区域遮挡，前者造成45%更大的错误增幅（几何平均），属于有限规模的因果区域接地证据。",
    "limitations_and_construct_boundary": limitations,
    "screening_conclusion": "直接强相关全文已核，兼有专家对具体伪迹存在性的评分和50样本 cited-region masking 对 matched-region control 的决策敏感性测试，属于有限的解释质量及因果接地实证。评审/样本小且仅取正确预测；LLM claim比例非独立人评；遮挡证据不等同充分性/完整因果faithfulness，亦无适当依赖结论。",
    "review_date": "2026-10-10",
}
if any(r["paper"].casefold() == TITLE.casefold() for r in reviews):
    next(r for r in reviews if r["paper"].casefold() == TITLE.casefold()).update(record)
else:
    reviews.append(record)
assert len({r["paper"].casefold() for r in reviews}) == len(reviews)
write("172_强相关核心及邻接论文原文解释可靠性效度核读.csv", reviews)

candidates = read("90_本轮新增强相关候选与引文复核.csv")
c = next(r for r in candidates if r["title"].casefold().startswith(TITLE.casefold()))
c.update({
    "preliminary_status": "arXiv v2全文/附录已核；直接强相关；3名CV专家评分及50样本cited-region遮挡对照，有限因果接地实证",
    "relevance_reason": "§4/Appendix D：3名计算机视觉专家对模型/DD-VQA各10条解释随机顺序评分，3.57±1.10 vs 3.83±0.99；只评正确判决。§4.3另在50个正确样本对比理由引用伪迹区域遮挡与匹配未引用区域遮挡，前者使分类错误增幅高45%，是有限的因果接地证据。Gemini 95.7% claim支持率只来自20条解释，不是人类独立核验。",
    "discovery_query_id": "T02-F3-S1-DEEPFAKE-EVAL; rank 4 full-text review",
    "discovery_query": "深伪检测解释专家评分与claim support",
    "source_url": URL,
    "screen_basis": "arXiv v2官方HTML §§3.3, 4.2, 4.3及Appendix D/F；独立复核用户评审、claim hallucination检查与解释训练奖励边界。",
})
write("90_本轮新增强相关候选与引文复核.csv", candidates)

priority = read("72_V2已复核强相关优先清单.csv")
p = next(r for r in priority if r["title"].casefold() == TITLE.casefold())
p.update({
    "V2_relation": "直接强相关；三位CV专家评分及50样本遮挡对照提供有限因果接地证据；无适当依赖/充分性评测",
    "original_reading_scope": "arXiv v2官方全文 §§3.3/4.2–4.3、Appendices D/F。",
    "limitations": limitations,
    "reassessment": "原rank4候选已完成附录全文核读。保留直接强相关；人类评分聚焦伪迹存在，且50例引用区/匹配区遮挡对照支持局部决策相关性；仍需保留小样本、仅正确预测、遮挡副作用、缺充分性/适当依赖等边界。Gemini claim判断需与人评严格分开。",
})
write("72_V2已复核强相关优先清单.csv", priority)

report = OUT / "00_重检阶段报告_未完成.md"
section = """\n\n---\n\n# 2026-10-10续：Outcome-Supervised Rationales专家评审全文核读\n\n- arXiv:2605.31192v2全文及Appendix D/F已核。三名计算机视觉专家每人评模型和DD-VQA各10条随机顺序解释，按描述伪迹是否实际存在打1–5分；模型3.57±1.10、DD-VQA 3.83±0.99。作者仅选最终判决正确的图；未报IAA。\n- 另有40图Gemini重合型幻觉筛查（7.5%）及20解释Gemini claim图像支持评分（95.7%），属于模型裁判，不当作人类真值。50个正确判决样本的理由区域遮挡vs匹配未引用区域遮挡使错误增幅高45%，是有限的局部因果接地证据；样本条件化、遮挡副作用及无充分性测试限制了结论。没有用户适当依赖实验。\n- 来源：https://arxiv.org/html/2605.31192v2。\n"""
existing = report.read_text(encoding="utf-8")
if "# 2026-10-10续：Outcome-Supervised Rationales专家评审全文核读" not in existing:
    report.write_text(existing + section, encoding="utf-8")
