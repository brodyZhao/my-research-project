import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/图像鉴伪解释可靠性_重检_2026-10-05"


def read(name):
    with (OUT / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write(name, rows):
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


title = "ForenDeX: Unlocking Forensic Insights for Explainable AI-Generated Image Detection"
url = "https://openaccess.thecvf.com/content/CVPR2026F/papers/Tan_ForenDeX_Unlocking_Forensic_Insights_for_Explainable_AI-Generated_Image_Detection_CVPRF_2026_paper.pdf"
summary = (
    "CVPR 2026 Findings官方PDF全文与补充表格核读。ForgReason由2,215张Midjourney合成图构成，"
    "人工框出不合理区域并写说明，随后GPT-4 Vision将框/人工说明汇总为最终解释，主要用作训练数据。"
    "推理输出评价：ChatGPT-4o对Midjourney/Flux样本的生成解释和上述人工参考按comprehensiveness、"
    "relevance、similarity、reasonableness打分，三次运行取均值；Table 3列出四项与平均分。另有用户研究："
    "100张真实风格图、20名用户、5点量表，对ForenDeX与LLaVA-FT匿名随机顺序解释评价accuracy、"
    "relevance、reasonableness、completeness及总体评价。"
)
limitations = (
    "用户研究提供盲序的人类感知质量比较，是直接解释质量/可理解性证据；但正文未报告用户专业背景、"
    "评审间一致性、置信区间/显著性检验或可复用的评分rubric，也没有把accuracy分数与独立claim级真值核验对齐。"
    "2,215条人工标注是训练监督而非独立测试评审；GPT-4o评分的reference来自人工框注再经GPT-4V改写/摘要，"
    "similarity并非事实正确性或因果faithfulness。没有删除/插入、参数随机化、反事实证据干预或人类适当依赖实验。"
)
reviews = read("172_强相关核心及邻接论文原文解释可靠性效度核读.csv")
row = next((r for r in reviews if r["paper"].casefold() == title.casefold()), None)
new = {
    "paper": title,
    "verified_identity": "Chuangchuang Tan, Jinglu Wang, Xiang Ming, Renshuai Tao, Yunchao Wei, Yao Zhao, Yan Lu; CVPR 2026 Findings; CVF Open Access version (10-page PDF).",
    "relevance_class": "直接强相关：静态AI生成图像鉴伪解释，兼有盲序用户质量评审；可靠性维度偏感知正确/相关/合理/完整，不是因果faithfulness或适当依赖实证。",
    "primary_source": url,
    "scope_and_methods": summary,
    "observed_reliability_evidence": "20名用户对100张Midjourney/Flux真实风格图的ForenDeX与LLaVA-FT解释作匿名随机顺序比较，按accuracy、relevance、reasonableness、completeness、overall五维以满分5分打分；作者报告ForenDeX各维更优。另有GPT-4o对参考解释的四维自动评价，三次取平均；该自动评价是辅助而非独立的人类真实性核验。",
    "limitations_and_construct_boundary": limitations,
    "screening_conclusion": "纳入直接强相关文献，并标为直接解释质量人评、因果faithfulness证据不足。20用户盲序对照是本领域有用的用户评审先例，但缺评审可靠性统计与独立事实真值；不能把训练注释、GPT参考相似度或LLM裁判分数等同于解释忠实。",
    "review_date": "2026-10-10",
}
if row:
    row.update(new)
else:
    reviews.append(new)
assert len({r["paper"].casefold() for r in reviews}) == len(reviews)
write("172_强相关核心及邻接论文原文解释可靠性效度核读.csv", reviews)

candidates = read("90_本轮新增强相关候选与引文复核.csv")
c = next(r for r in candidates if r["title"].casefold() == title.casefold())
c.update({
    "preliminary_status": "官方全文已核：直接强相关静态图像解释质量研究，含20用户/100图盲序评价；缺独立claim真值与因果faithfulness",
    "relevance_reason": "完整原稿确认ForgReason训练数据由2,215张Midjourney图的人工区域框注/文字说明再经GPT-4V汇总而成；独立用户研究由20人对100张图上的ForenDeX/LLaVA-FT解释匿名随机顺序评分，五维accuracy/relevance/reasonableness/completeness/overall。自动GPT-4o参考评分另列，不当作专家事实核验。",
    "screen_basis": "CVF官方CVPR 2026 Findings PDF全文（10页），§3.2.2、§4.2、Table 3、Figure 5及结论；从Chrome PDF下载后本地文本提取核读。",
})
write("90_本轮新增强相关候选与引文复核.csv", candidates)

priority = read("72_V2已复核强相关优先清单.csv")
p = next(r for r in priority if r["title"].casefold() == title.casefold())
p.update({
    "V2_relation": "直接强相关：静态图像鉴伪解释质量研究，20用户对100图进行盲序质量评分；未测因果faithfulness/适当依赖",
    "original_reading_scope": "CVF官方CVPR 2026 Findings 10页全文核读；§3.2.2、§4.2、Table 3、Figure 5。",
    "limitations": limitations,
    "reassessment": "由题录待读升级为直接强相关全文核读。区分2,215条人工训练注释、GPT-4o参考式自动指标和20用户独立盲序质量评价；不把相似度/LLM judge解释为faithfulness。最终排名需与所有直接核心研究统一复核。",
})
write("72_V2已复核强相关优先清单.csv", priority)

report = OUT / "00_重检阶段报告_未完成.md"
with report.open("a", encoding="utf-8") as f:
    f.write("\n\n---\n\n# 2026-10-10续：ForenDeX官方全文与用户评审核读\n\n")
    f.write("- 已通过Chrome读取CVF官方10页PDF全文，完成候选90、优先清单72和效度表172的身份去重更新。该文是直接静态图像鉴伪解释研究，纳入强相关。\n")
    f.write("- 可靠性证据：20名用户盲序比较100张Midjourney/Flux图上的ForenDeX与LLaVA-FT解释，按accuracy/relevance/reasonableness/completeness/overall五维、5分制评分。该证据属于解释感知质量/可理解性；正文没有报告用户专业背景、IAA、评分区间/显著性检验或独立claim真值校准。\n")
    f.write("- 2,215张人工框注并带说明的图经GPT-4V整理为训练解释参考；GPT-4o对生成解释与该参考计算comprehensiveness/relevance/similarity/reasonableness，三次均值。明确区分训练监督、LLM评估和独立用户研究；相似度/LLM评分不等于因果faithfulness。论文没有适当依赖或决策因果干预实验。\n")
    f.write("- 主要来源：CVF官方全文PDF，https://openaccess.thecvf.com/content/CVPR2026F/papers/Tan_ForenDeX_Unlocking_Forensic_Insights_for_Explainable_AI-Generated_Image_Detection_CVPRF_2026_paper.pdf。强相关引用逐篇排查另开侧表；既有SIDA、SHIELD等引用身份按已存在筛查记录复用。\n")

print(f"updated ForenDeX review; 172={len(reviews)}, 90={len(candidates)}, 72={len(priority)}")
