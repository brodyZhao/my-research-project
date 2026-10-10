import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/图像鉴伪解释可靠性_重检_2026-10-05"


def read(n):
    with (OUT / n).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write(n, rows):
    with (OUT / n).open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


reviews = read("172_强相关核心及邻接论文原文解释可靠性效度核读.csv")
records = [
    {
        "paper": "BusterX: MLLM-Powered AI-Generated Video Forgery Detection and Explanation",
        "verified_identity": "arXiv:2505.12620v8, 2026-06-15; official arXiv HTML.",
        "relevance_class": "视频取证解释可靠性强邻接：可迁移的专家评分、LLM裁判校准与grounding评测。",
        "primary_source": "https://arxiv.org/html/2505.12620",
        "scope_and_methods": "GenBuster-Bench仅在Wild track对正确预测样本评解释，Gemini 3 Flash按1–5评分：视觉grounding、推理深度/逻辑、事实准确与伪精确惩罚；解释与检测共享相同视频帧。另由5名有deepfake背景的专家按同维度评分；Gemini与人评分Spearman ρ=.64 (p<.01)。",
        "observed_reliability_evidence": "5名领域专家对BusterX rationale给出均分78.7；LLM裁判与专家评分秩相关ρ=.64。评分维度显式关注证据grounding、逻辑、幻觉与不可验证的精确声称，提供视频场景的直接人类解释质量证据和裁判校准证据。",
        "limitations_and_construct_boundary": "仅报告五位专家，未报告各自背景/样本数、盲评设计、专家间一致性或分数区间；只对正确预测的Wild样本评价，排除错误预测及真视频解释，造成条件选择。ρ=.64表示中等秩相关，不是裁判效度充分证明。视频任务属邻接证据；不测模型决策因果faithfulness或人类适当依赖。",
        "screening_conclusion": "RAIDX参考第74项直接相邻全文已核。对图像鉴伪研究可借鉴多维视觉grounding/幻觉惩罚和LLM-专家一致性设计；不可当作静态图像直接实证。",
        "review_date": "2026-10-10",
    },
    {
        "paper": "BusterX++: Towards Unified Cross-Modal AI-Generated Content Detection and Explanation with MLLM",
        "verified_identity": "arXiv:2507.14632v4; official arXiv HTML, current source crawled 2026-10-10.",
        "relevance_class": "图像/视频生成内容解释可靠性直接/邻接：专家成对偏好与视觉伪迹事实核查。",
        "primary_source": "https://arxiv.org/html/2507.14632",
        "scope_and_methods": "沿用90/rank89既有全文核读，官方§5.7确认100个生成媒体样本（50图、50视频），同一5名取证专家对匿名随机排序的BusterX++与GPT-5.2解释双盲成对比较；对100个正确预测为fake样本另作视觉伪迹是否真实存在的盲审。",
        "observed_reliability_evidence": "专家在evidence grounding/specificity/completeness等维度按3/5多数票，82%样本偏好BusterX++解释；在正确fake子集中，87/100多数票认定文中具体视觉伪迹确实存在。此为直接专家偏好和claim事实存在核验。",
        "limitations_and_construct_boundary": "样本混合图像/视频，非图像单独估计；偏好是相对GPT-5.2的成对选择，无绝对正确率刻度；5位评审也是基准筛选专家，未见IAA；87%只在模型正确判假的样本上验证，未覆盖错误解释、真样本、完整性或必要/充分性。未检验解释对人类决策的适当依赖或模型因果faithfulness。",
        "screening_conclusion": "已在90/rank89核读；本轮复用既有身份，补入统一172并关联RAIDX第75项，不重复计篇。该文有稀缺的claim级视觉存在性人评，属于当前最直接的可靠性证据之一，但条件和样本限制显著。",
        "review_date": "2026-10-10",
    },
]
by = {r["paper"].casefold(): r for r in reviews}
for r in records:
    key = r["paper"].casefold()
    if key in by:
        by[key].update(r)
    else:
        reviews.append(r)
        by[key] = r
assert len({r["paper"] for r in reviews}) == len(reviews)
write("172_强相关核心及邻接论文原文解释可靠性效度核读.csv", reviews)

refs = read("T02-F2-RAIDX_参考文献逐篇主题初筛_20261010.csv")
for no in ("74", "75"):
    r = next(r for r in refs if r["reference_no"] == no)
    r.update({
        "screen_decision": "直接/邻接候选：官方全文已核读，相关效度证据已录入172",
        "screen_reason": "BusterX/BusterX++含专家对生成解释的盲评；分别见5人评分/裁判相关和5人偏好/视觉事实审查。具体范围与构念边界见172。",
        "existing_candidate_or_review": "BusterX: new adjacent candidate 90 + 172; BusterX++: existing candidate 90 + rank 89 + consolidated review 172",
        "screen_basis": "RAIDX arXiv v1 References; official arXiv HTML v8/v4 full text, Sections 3.3/5.2/5.7 and relevant appendices; existing BusterX++ title/review reused.",
    })
r = next(r for r in refs if r["reference_no"] == "58")
r.update({
    "topic_class": "synthetic-image detection and generator-source attribution",
    "screen_decision": "主题邻接/不纳入解释可靠性直接候选",
    "screen_reason": "全文研究判别图像是真实还是文本到图像生成，并将生成图像分类到源生成模型；此处attribution是来源模型归因，不是模型为何判假的解释，也没有解释生成、解释忠实度或人类解释评价。",
    "existing_candidate_or_review": "title-level screen plus official conference paper audit; do not count as an explanation-reliability study",
    "screen_basis": "Official ACM CCS 2023 paper PDF author-hosted at https://yangzhangalmo.github.io/papers/CCS23-DEFAKE.pdf; title and abstract checked against arXiv:2210.06998.",
})
write("T02-F2-RAIDX_参考文献逐篇主题初筛_20261010.csv", refs)

candidates = read("90_本轮新增强相关候选与引文复核.csv")
if not any(r["title"].startswith("BusterX: MLLM-Powered") for r in candidates):
    candidates.append({
        "title": "BusterX: MLLM-Powered AI-Generated Video Forgery Detection and Explanation",
        "authors_year_venue": "H Wen et al. — arXiv:2505.12620v8 (2026-06-15)",
        "preliminary_status": "强视频邻接；五位深伪专家人评解释，LLM裁判与专家相关ρ=.64",
        "relevance_reason": "正确预测Wild视频解释由Gemini按grounding/逻辑/事实性评分，并与5位专家评分校准；专家均值78.7，Spearman ρ=.64。仅视频；只评正确预测样本，缺专家间一致性/因果faithfulness/适当依赖。",
        "discovery_query_id": "T02-F2-RAIDX-REFS-74",
        "discovery_query": "RAIDX references item 74: BusterX",
        "source_url": "https://arxiv.org/html/2505.12620",
        "screen_basis": "Official arXiv v8 full text §§3.3, 5.1–5.2; retained as adjacent video evidence, not an image-only core paper.",
    })
write("90_本轮新增强相关候选与引文复核.csv", candidates)

report = OUT / "00_重检阶段报告_未完成.md"
with report.open("a", encoding="utf-8") as f:
    f.write("\n\n---\n\n# 2026-10-10 RAIDX视频/跨模态引文核读与DE-FAKE构念排除\n\n")
    f.write("- RAIDX第74条BusterX（arXiv v8）是视频解释邻接：Gemini按视觉grounding、推理逻辑、事实准确/伪精确惩罚对正确预测Wild样本打分；5名深伪专家评分均值78.7，与Gemini秩相关ρ=.64。样本数/IAA/盲评报告不足且按正确预测选择，不能作图像直接证据。新入90/172。\n")
    f.write("- 第75条BusterX++已在90/rank89全文核过，复用后补入172：5名专家盲评100个图视频混合样本，对BusterX++解释相对GPT-5.2有82%多数票偏好；100个正确fake样本中，87%多数票认为理由所述伪迹确实存在。此为直接grounding事实证据，但存在小评审组、未报IAA、选择正确预测及无适当依赖测试等限制。\n")
    f.write("- 第58条DE-FAKE全文构念核查后排除直接解释可靠性：attribution指追溯图像来源生成模型，并非说明检测决策理由；不把题名相似误判为强相关。\n")

handoff = ROOT / "HANDOFF.md"
old = handoff.read_text(encoding="utf-8")
section = """# 2026-10-10 RAIDX视频/跨模态引文筛查\n\n- 第74项BusterX全文核读后新增为视频邻接候选90/172：Wild track解释由Gemini依grounding/逻辑/事实性评估，另有5位深伪专家评分；专家均分78.7，与Gemini秩相关ρ=.64。只对正确预测视频评价，专家间一致性、评审规模和盲法不足，不等同图像直接faithfulness证据。\n- 第75项BusterX++此前已在90/rank89核读；官方v4核后复用身份补进172：5位评审对100个图视频混合样本相对GPT-5.2盲评，82%多数票偏好；另对100个正确fake样本核视觉伪迹，87%被多数专家确认。未报IAA，且排除失败预测；不测适当依赖。\n- 第58项DE-FAKE全文概念核查后定为源生成模型归因，不是理由解释，降为主题邻接/不纳入直接候选。更新RAIDX refs、90与172；总体检索未完成。\n\n"""
if not old.startswith(section):
    handoff.write_text(section + old, encoding="utf-8")

