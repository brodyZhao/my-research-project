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


reviews = read("172_强相关核心及邻接论文原文解释可靠性效度核读.csv")
by_title = {r["paper"].casefold(): r for r in reviews}
entries = [
    {
        "paper": "ForgeryGPT: A Multimodal LLM for Interpretable Image Forgery Detection and Localization",
        "verified_identity": "arXiv:2410.10238; current author HTML title/version cross-checked at https://arxiv.org/html/2410.10238; cited by RAIDX under earlier title ‘ForgeryGPT: Multimodal Large Language Model For Explainable Image Forgery Detection and Localization’.",
        "relevance_class": "直接强相关：图像伪造解释文本评价及人类解释前后判断/信心变化。",
        "primary_source": "https://arxiv.org/html/2410.10238",
        "scope_and_methods": "§IV-E从IMD2020随机抽100张伪造图并人工复核参考描述；ROUGE-L、CSS、BLEU-4、SPICE比较解释文本。5名参与者在看解释前后判断同一批图像真假及信心变化。",
        "observed_reliability_evidence": "作者报告参与者基线正确认出74%伪造图；原先误判为真的图像中81%在看Forg­eryGPT解释后改判为假；对原已判断为假的图像，65%报告信心提高。参考文本匹配与人类判断影响提供相关证据。",
        "limitations_and_construct_boundary": "仅100张伪造图，5名参与者；无真实图、无解释关闭/替代解释对照，信心上升不等于适当依赖。未见独立逐claim事实核验、评分一致性或因果faithfulness测量。作者明确承认视觉证据含糊时有幻觉风险，并提出加强grounding为未来工作。",
        "screening_conclusion": "复用90、72既有全文与人类信心审查并补入统一172；强相关直接证据，但主要测说服/信心变化，不能解释为faithfulness或正确依赖。非本轮新发现。",
        "review_date": "2026-10-10",
    },
    {
        "paper": "Generating Attribution Reports for Manipulated Facial Images: A Dataset and Baseline",
        "verified_identity": "ACL 2026 Long Papers, 2026.acl-long.1405, pp. 30455–30473, DOI 10.18653/v1/2026.acl-long.1405; arXiv:2412.19685 earlier title ‘A Large-scale Interpretable Multi-modality Benchmark for Facial Image Forgery Localization’ is the same work/version lineage.",
        "relevance_class": "直接强相关：面部篡改区域+文字归因报告，并直接盲评解释faithfulness/helpfulness。",
        "primary_source": "https://aclanthology.org/2026.acl-long.1405/ ; https://aclanthology.org/2026.acl-long.1405.pdf",
        "scope_and_methods": "ACL正式版§4.1/Table 3：5名独立评审盲评100张随机测试图的模型文本，1–5分Faithfulness（识别伪造特征的准确性且不幻觉）和Helpfulness（能否帮助人工核验）；与SCA、LISA-7B、InstructBLIP比较。",
        "observed_reliability_evidence": "ForgeryTalker Faithfulness 4.3/5、Helpfulness 4.4/5；基线分别为SCA 2.3/3.1、LISA-7B 2.7/3.4、InstructBLIP 3.6/3.8。这里确有直接的人类解释事实质量判断，不只是自动caption相似分数。",
        "limitations_and_construct_boundary": "只5名评审和100张面部伪造图；未报告评分者背景/一致性、分数分布与区间或错误子类；盲法操作细节有限。Helpfulness评分不等于观察到的信任校准/适当依赖，且没有因果必要性/充分性干预。将旧题名与ACL正式版合并为一个作品，不重复计篇。",
        "screening_conclusion": "复用90、72中已核正式版的唯一记录，补入统一172并将RAIDX第38条标为已核；这是直接的人评解释faithfulness证据，需附上述小样本与报告完整性限制。",
        "review_date": "2026-10-10",
    },
]
for e in entries:
    key = e["paper"].casefold()
    if key in by_title:
        by_title[key].update(e)
    else:
        reviews.append(e)
        by_title[key] = e
assert len({r["paper"] for r in reviews}) == len(reviews)
write("172_强相关核心及邻接论文原文解释可靠性效度核读.csv", reviews)

refs = read("T02-F2-RAIDX_参考文献逐篇主题初筛_20261010.csv")
for no, exact, existing in [
    ("38", "A Large-scale Interpretable Multi-modality Benchmark for Facial Image Forgery Localization", "Generating Attribution Reports for Manipulated Facial Images: A Dataset and Baseline; existing 90/72 review merged to 172"),
    ("42", "ForgeryGPT: Multimodal Large Language Model For Explainable Image Forgery Detection and Localization", "ForgeryGPT: A Multimodal LLM for Interpretable Image Forgery Detection and Localization; existing 90/72 review merged to 172"),
]:
    rows = [r for r in refs if r["reference_no"] == no]
    assert len(rows) == 1 and rows[0]["title_as_printed"] == exact
    rows[0].update({
        "screen_decision": "直接/邻接候选：官方全文已核读，复用既有唯一候选并登记172",
        "screen_reason": "已核原文发现直接解释质量或人类评价证据；精确测量及效度边界见172/90/72。",
        "existing_candidate_or_review": existing,
        "screen_basis": "RAIDX arXiv v1 References title; version/identity matched to official arXiv and/or ACL full text; reuse existing candidate/rank review and consolidate into 172; do not duplicate.",
    })
write("T02-F2-RAIDX_参考文献逐篇主题初筛_20261010.csv", refs)

report = OUT / "00_重检阶段报告_未完成.md"
with report.open("a", encoding="utf-8") as f:
    f.write("\n\n---\n\n# 2026-10-10 RAIDX直接引文：ForgeryGPT与ForgeryTalker版本/效度合并\n\n")
    f.write("- ForgeryGPT不是新发现：复用候选90/rank31既有全文与人类说服审查，并补入统一总表172；arXiv官方§IV-E确认100张伪造图、5人前后判断，81%原先误判真的图在看解释后改判，65%已判为假的图信心提高。结论是有说服/信心影响证据；单一伪造条件与极小评审组无法支持适当依赖，作者承认幻觉风险。\n")
    f.write("- RAIDX第38项的2024题名版本与ACL 2026正式版合并为同一Lian等人的ForgeryTalker论文（ACL 2026 Long Papers）。官方正式版报告5名独立盲评者、100张测试图，Faithfulness 4.3/5、Helpfulness 4.4/5，直接属于人工解释质量评价；但未报告评分者一致性、分布/区间，且helpfulness不能替代实际适当依赖。统一入账172，并修正RAIDX参考表的核读状态。\n")

handoff = ROOT / "HANDOFF.md"
old = handoff.read_text(encoding="utf-8")
section = """# 2026-10-10 RAIDX引文后续：ForgeryGPT与ForgeryTalker版本核对\n\n- RAIDX第42条ForgeryGPT原已在90/rank31完成全文/人类信心变化审查，本轮复用旧记录、核对官方arXiv全文§IV-E/V并纳入统一172，未新增计篇。只测100张伪造图、5人前后判断；误判改判/置信增强说明解释有说服影响，无法证明适当依赖；作者承认幻觉风险。\n- 第38条2024旧题名与ACL 2026论文《Generating Attribution Reports for Manipulated Facial Images: A Dataset and Baseline》确认为同一版本链。正式ACL论文报告5名盲评者、100样本及Faithfulness 4.3/5和Helpfulness 4.4/5，属直接解释质量人评；评分者一致性/分布与适当依赖仍缺证。修正RAIDX引文状态并补进172。\n- 本轮修改文件：172、RAIDX 82条参考筛查表、阶段报告、`HANDOFF.md`和核读脚本。后续需重建归档、运行编译/唯一性断言、diff与ZIP校验，再提交推送。总体重检仍未完成。\n\n"""
if not old.startswith(section):
    handoff.write_text(section + old, encoding="utf-8")

