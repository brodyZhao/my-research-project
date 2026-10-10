import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/图像鉴伪解释可靠性_重检_2026-10-05"
TITLE = "Locate-Then-Examine: Grounded Region Reasoning Improves Detection of AI-Generated Images"
URL = "https://openaccess.thecvf.com/content/CVPR2026/papers/Ji_Locate-Then-Examine_Grounded_Region_Reasoning_Improves_Detection_of_AI-Generated_Images_CVPR_2026_paper.pdf"


def read(name):
    with (OUT / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write(name, rows):
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


methods = (
    "CVF官方CVPR 2026 11页全文。TRACE含10,000张真实图与10,000张AI生成图；GPT-4o生成真伪解释，"
    "Qwen2.5-VL将解释定位为框。每图两次生成解释并以语义一致性过滤；两次定位框IoU过阈值才保留，"
    "另滤除过大框/主体框。测试解释BLEU/ROUGE对齐这些模型生成参考，定位用IoU。User Study以GPT-5、"
    "Gemini 2.5 Pro和8位有AI生成艺术经验的人评解释1–5分，聚焦accuracy/completeness。每位评审随机评300条，"
    "TRACE、LTE-7B、LTE-32B各100条；同一评审不重复看同一图，单条独立评价。错误最终判决的回复排除。"
)
limits = (
    "8位有AI生成艺术经验的人类评分是直接的人类解释质量证据；表3中人评分为TRACE 3.75、LTE-7B 3.10、"
    "LTE-32B 3.68（1–5）。但只纳入最终判决正确的解释，不能反映错误判决时的解释可靠性或整体系统可靠性；"
    "评审看到图像标签，且任务是单条解释评分，不是用户实际依赖决策。正文未报告评审间一致性/分数区间。"
    "TRACE解释由GPT-4o生成，框由Qwen2.5-VL生成，过滤依靠同类模型重复采样/一致性规则而非人工真值审计；"
    "因此BLEU/ROUGE和框IoU只衡量对模型构造的参考/区域的对齐，不能单独证明视觉claim正确或因果faithfulness。"
    "未见参数随机化、删除插入、反事实干预或appropriately-reliance实验。"
)
reviews = read("172_强相关核心及邻接论文原文解释可靠性效度核读.csv")
record = {
    "paper": TITLE,
    "verified_identity": "Yikun Ji, Yan Hong, Bowen Deng, Jun Lan, Huijia Zhu, Weiqiang Wang, Liqing Zhang, Jianfu Zhang; CVPR 2026; official CVF open-access paper.",
    "relevance_class": "静态AI生成图像鉴伪解释的直接强相关研究；具有8名领域邻接专家的解释质量评分和区域接地评测。",
    "primary_source": URL,
    "scope_and_methods": methods,
    "observed_reliability_evidence": "8位有AI生成艺术经验的人类评审以1–5分评价解释的accuracy/completeness；每位300条，三组各100条随机样本，同一评审不重复看同图，独立评估。人评均分：TRACE 3.75、LTE-7B 3.10、LTE-32B 3.68。另有GPT-5/Gemini 2.5 Pro评分与区域IoU/文本相似度自动指标。",
    "limitations_and_construct_boundary": limits,
    "screening_conclusion": "直接纳入强相关。它提供较稀缺的解释质量专家人评及区域接地证据，但数据参考由模型自动生成并用模型内重复一致性过滤；正确判决条件化和无IAA/适当依赖/因果faithfulness限制必须随结论保留。",
    "review_date": "2026-10-10",
}
if any(r["paper"].casefold() == TITLE.casefold() for r in reviews):
    row = next(r for r in reviews if r["paper"].casefold() == TITLE.casefold())
    row.update(record)
else:
    reviews.append(record)
assert len({r["paper"].casefold() for r in reviews}) == len(reviews)
write("172_强相关核心及邻接论文原文解释可靠性效度核读.csv", reviews)

candidates = read("90_本轮新增强相关候选与引文复核.csv")
c = next(r for r in candidates if r["title"].casefold() == TITLE.casefold())
c.update({
    "preliminary_status": "官方全文已核；直接强相关；8位有AI生成艺术经验评审打分，测试仅含判决正确样本",
    "relevance_reason": "TRACE以GPT-4o生成解释、Qwen2.5-VL生成框，并以重复生成的一致性规则过滤；另有8位艺术经验评审对正确判决样本解释按accuracy/completeness评分。具有人评及定位数据，但模型造参考和正确样本筛选会限制效度。",
    "screen_basis": "CVF官方CVPR 2026 PDF全文，§3.2、§4.5、Table 1/Table 3及附录/参考表；11页官方开放版。",
})
write("90_本轮新增强相关候选与引文复核.csv", candidates)

priority = read("72_V2已复核强相关优先清单.csv")
p = next(r for r in priority if r["title"].casefold() == TITLE.casefold())
p.update({
    "V2_relation": "直接强相关；静态生成图鉴伪解释评价含区域接地与8位艺术经验评审；无因果faithfulness/适当依赖",
    "original_reading_scope": "CVF官方11页全文；§3.2数据和质控、§4.5人评、Tables 1/3及Conclusion。",
    "limitations": limits,
    "reassessment": "rank2原有候选现已完成全文核读。保留直接强相关排序；其人评比纯LLM judge强，但只评正确输出，且解释/区域参考由GPT-4o、Qwen2.5-VL自动构建并过滤。",
})
write("72_V2已复核强相关优先清单.csv", priority)

report = OUT / "00_重检阶段报告_未完成.md"
section = """\n\n---\n\n# 2026-10-10续：Locate-Then-Examine全文核读\n\n- CVF官方CVPR 2026全文已核读，升级候选90/优先72/效度172。TRACE含20,000张真假图；解释由GPT-4o生成、框由Qwen2.5-VL接地，并通过重复生成的一致性阈值过滤。解释评分含BLEU/ROUGE参考对齐及IoU定位。\n- 人评直接证据：8位有AI生成艺术经验者各独立评分300条解释（TRACE、LTE-7B、LTE-32B各100）；同一评审不重复看同一图；重点评accuracy/completeness，均分3.75/3.10/3.68（满分5）。仅纳入最终判决正确回答，且正文未报IAA/区间；解释及框参考为模型生成/过滤，故不能据此宣称claim真值已独立验证。未测试适当依赖或因果faithfulness。\n- 全文来源：https://openaccess.thecvf.com/content/CVPR2026/papers/Ji_Locate-Then-Examine_Grounded_Region_Reasoning_Improves_Detection_of_AI-Generated_Images_CVPR_2026_paper.pdf。强相关参考文献已按位置逐条筛查并关联既有身份。\n"""
existing = report.read_text(encoding="utf-8")
if "# 2026-10-10续：Locate-Then-Examine全文核读" not in existing:
    with report.open("a", encoding="utf-8") as f:
        f.write(section)
