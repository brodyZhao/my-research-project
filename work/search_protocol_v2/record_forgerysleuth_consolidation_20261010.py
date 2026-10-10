import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/图像鉴伪解释可靠性_重检_2026-10-05"
TITLE = "ForgerySleuth: Empowering Multimodal Large Language Models for Image Manipulation Detection"
ARXIV = "https://arxiv.org/html/2411.19466"
NEURIPS = "https://proceedings.neurips.cc/paper_files/paper/2025/file/e0e25d425450b6fc8e34380de71b3aee-Paper-Conference.pdf"


def read_csv(name):
    with (OUT / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(name, rows):
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


# Integrate the earlier official NeurIPS review with the later complete arXiv HTML audit.
reviews = read_csv("172_强相关核心及邻接论文原文解释可靠性效度核读.csv")
existing = [r for r in reviews if r["paper"].casefold() == TITLE.casefold()]
record = {
    "paper": TITLE,
    "verified_identity": "NeurIPS 2025; arXiv:2411.19466v2 (2025-12-29); official conference paper and official arXiv full text agree on identity.",
    "relevance_class": "直接强相关：图像篡改分析解释，并实测人类对解释正确性、相关性和细节的评分。",
    "primary_source": f"{ARXIV} ; {NEURIPS}",
    "scope_and_methods": "ForgeryAnalysis-Eval含618个样本（全ForgeryAnalysis共2,370条）；GPT-4按正确性/相关性/细节以1–10分评估并给理由，报告重复两次的平均分；另有14名志愿者，每人随机评30个样本。人工结果表按QWen2/GPT-4o/本文分别含139/134/147个样本，报告召回及正确性、相关性、细节、总分。评测还报告与参考文本的STS语义相似度。",
    "observed_reliability_evidence": "存在直接的人类解释质量评价：人工表中本文召回91.2%、正确性9.48、相关性9.53、细节9.61、总分9.44；GPT-4自动评分表中本文对应9.10/9.60/9.89/9.45。专家交叉修订参考分析文本，支持参考标签的内容审校；模型输出的质量另由志愿者评分。",
    "limitations_and_construct_boundary": "14名志愿者的专业背景、样本分配/重叠及评分者间一致性未报告；不能从14×30推断420个独立样本。GPT-4评估可能偏差或幻觉，作者明确承认；STS只反映语义相似，作者将幻觉量化列为未来工作。该研究是claim内容正确性/相关性/细节的人评证据，但没有删除/插入、必要性/充分性、模型决策因果归因或适当依赖实验。不能把人工评解释质量等同于机制性faithfulness。",
    "screening_conclusion": "已完成官方全文与NeurIPS补充材料核读；强相关，列入核心优先文献。证据强度：有直接人评，但评审设计报告不足；用于解释内容质量/grounding，不足以证明因果faithfulness或用户适当依赖。此条整合既有153记录，非新增独立发现。",
    "review_date": "2026-10-10",
}
if existing:
    assert len(existing) == 1
    existing[0].update(record)
else:
    reviews.append(record)
assert len({r["paper"] for r in reviews}) == len(reviews)
write_csv("172_强相关核心及邻接论文原文解释可靠性效度核读.csv", reviews)

candidates = read_csv("90_本轮新增强相关候选与引文复核.csv")
matches = [r for r in candidates if r["title"].casefold() == TITLE.casefold()]
assert len(matches) == 1
matches[0].update({
    "preliminary_status": "强相关核心；官方全文核读已完成（复用153既有身份记录）",
    "relevance_reason": "图像篡改解释的正确性、线索相关性和细节有14名志愿者及GPT-4评估；核读显示有人评证据，但评审一致性/专业背景缺报，且未做因果faithfulness/适当依赖测试。",
    "source_url": ARXIV,
    "screen_basis": "Google Scholar候选复用；NeurIPS正式论文与arXiv v2全文、补充D.3/E.2核对；详见172及既有153。",
})
write_csv("90_本轮新增强相关候选与引文复核.csv", candidates)

rank = read_csv("72_V2已复核强相关优先清单.csv")
ranks = [r for r in rank if r["title"].casefold() == TITLE.casefold()]
assert len(ranks) == 1
ranks[0].update({
    "V2_relation": "图像篡改解释内容质量：人评正确性/相关性/细节 + GPT-4评估",
    "original_reading_scope": "官方arXiv全文§5.3、附录A.3/A.4、D.3、E.2及NeurIPS正式论文核读；14名志愿者各评30个随机样本，另由GPT-4评1–10分，辅以STS。",
    "limitations": "人评专业性、样本分配与评分一致性未报告；GPT-4和STS效度有限，作者承认且提出量化幻觉为未来工作；不含因果faithfulness或适当依赖。",
    "reassessment": "复用153既有记录；本次将完整官方arXiv全文边界并入172。保留rank 25，不重复计篇。",
})
write_csv("72_V2已复核强相关优先清单.csv", rank)

refs = read_csv("T02-F2-RAIDX_参考文献逐篇主题初筛_20261010.csv")
ref = [r for r in refs if r["reference_no"] == "63"]
assert len(ref) == 1
ref[0].update({
    "author_year_as_printed": "Sun et al. 2024 (arXiv preprint; NeurIPS 2025 proceedings)",
    "screen_decision": "直接/邻接候选：官方全文已核读，复用既有153并统一登记172",
    "screen_reason": "图像篡改分析解释含志愿者对模型输出的直接质量评分，并以GPT-4/STS补充；评测效度边界见172。",
    "existing_candidate_or_review": "90 candidate + 153 original review + 172 consolidated full-text review; do not duplicate",
    "screen_basis": "RAIDX arXiv v1 References title; identity/year cross-checked against official NeurIPS 2025 proceedings and arXiv v2 full text; complete paper and supplement read.",
})
write_csv("T02-F2-RAIDX_参考文献逐篇主题初筛_20261010.csv", refs)

report = OUT / "00_重检阶段报告_未完成.md"
with report.open("a", encoding="utf-8") as f:
    f.write("\n\n---\n\n# 2026-10-10 ForgerySleuth既有核读记录整合与效度补核\n\n")
    f.write("- RAIDX参考文献第63项此前已有NeurIPS补充材料D.3核读记录（153）及优先rank 25；本轮发现统一总表172遗漏该记录，因此复用既有身份并补入，不作为新发现或重复论文。\n")
    f.write("- 对照官方arXiv v2全文§5.3、附录A.3/A.4、D.3、E.2及NeurIPS正式版：ForgeryAnalysis-Eval为618条、整个ForgeryAnalysis为2,370条；14名志愿者每人评30个随机样本。报告人工对正确性/相关性/细节的1–10分与召回，且GPT-4另行评分、STS作文本相似度指标。该设计提供直接的人类解释质量证据。\n")
    f.write("- 效度界限：论文未充分报告志愿者专业背景、分配/重叠与评分一致性；不能据14×30声称420独立样本。作者承认GPT-4可能偏差/幻觉、STS仅测语义相似，并将幻觉量化列为未来方向。人评解释内容质量不等于因果faithfulness；没有模型决策干预或适当依赖实验。90/72/172和RAIDX refs第63项已统一。\n")

handoff = ROOT / "HANDOFF.md"
old = handoff.read_text(encoding="utf-8")
section = """# 2026-10-10 ForgerySleuth引文核读统一入账\n\n- 沿RAIDX第63条参考引文复核发现ForgerySleuth早有NeurIPS补充材料评测证据（153、rank 25），但未并入统一原文效度核读总表172。本次复用既有审读并与官方arXiv v2全文§5.3、附录A.3/A.4、D.3、E.2交叉核验，向172补入一条，保持标题去重；90和72更新为全文已核，RAIDX引用表修正待核状态及正式出版年。\n- 论文有直接人评：14名志愿者各评30个随机样本；解释正确性、相关性、细节和召回均有记录，GPT-4与STS作补充评估。志愿者专业背景、分配/重叠及IAA未报告；GPT-4/STS局限由作者承认，幻觉量化列为未来工作。它支持解释内容质量评估，但不是因果faithfulness或适当依赖证据。\n- 本轮变更文件：172、90、72、`T02-F2-RAIDX_参考文献逐篇主题初筛_20261010.csv`、阶段报告、`HANDOFF.md`及本次核读脚本。测试：待运行package checkpoint、compileall、CSV唯一性断言、CRLF-aware diff check及ZIP哈希/CRC。\n- 全局文献重检仍未完成；继续RAIDX直接/邻接引文的全文审核，并复用既有paper ID与原文记录。\n\n"""
if not old.startswith(section):
    handoff.write_text(section + old, encoding="utf-8")

