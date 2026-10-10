import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/图像鉴伪解释可靠性_重检_2026-10-05"
QUERY_ID = "CIT-SIDE-VLM-REFS-20261010"
TITLE = "Explainability-Guided Deepfake Detection for High-Fidelity Facial Edits"
SOURCE = "https://link.springer.com/chapter/10.1007/978-3-032-31663-9_33"
refs = [
    ("Easier painting than thinking: can text-to-image models set the stage, but not direct the play?", "泛化方法邻接", "讨论文本到图像模型能力，非取证解释或伪造解释可靠性。"),
    ("SAiW: Source-Attributable Invisible Watermarking for Proactive Deepfake Defense", "取证溯源邻接", "水印溯源/主动防御，与解释可靠性不同构念。"),
    ("Analyzing and improving the image quality of StyleGAN", "生成模型背景", "StyleGAN图像质量分析，非深伪解释可靠性。"),
    ("Can ChatGPT detect DeepFakes? A study of using multimodal large language models for media forensics", "直接/邻接核心；复用候选身份", "评估MLLM媒体取证检测和视觉语言推理；已在90按同一作品身份登记，不重复计数，需沿其既有全文状态复用。"),
    ("SHIELD: A benchmark study on zero-shot detection of AI-Edited images with vision language models", "直接鉴伪邻接；复用候选身份", "AI编辑图像VLM检测基准，需核查是否含解释可靠性终点；已在90登记，复用身份、不重复建候选。"),
    ("MesoNet: a compact facial video forgery detection network", "检测方法背景", "面部视频伪造检测基线，不含解释可靠性终点。"),
    ("EfficientNet-based deepfake detection: a robust approach for real and fake media classification", "检测方法背景", "分类器/检测鲁棒性背景；摘要题名未见解释或grounding评价。"),
    ("Right for the right reasons: training differentiable models by constraining their explanations", "解释可靠性方法学邻接", "解释对齐训练的基础方法，可为CAM-mask对齐效度分析提供方法参照；不是取证专用研究。"),
    ("VisFIS: visual feature importance supervision with right-for-the-right-reason objectives", "解释可靠性方法学邻接", "视觉重要性监督与right-for-right-reasons目标，直接方法学邻接；非深伪应用。"),
    ("IndicSideFace: a dataset for advancing deepfake detection on side-face perspectives of Indian subjects", "高保真/侧脸数据邻接", "侧脸视角鉴伪数据，支持该领域数据背景；本题解释可靠性尚需另证。"),
    ("Securing AI-Generated media: rethinking deepfake vulnerabilities in side-face perspectives", "威胁/数据场景邻接", "侧脸深伪威胁与漏洞背景；不是解释评价研究。"),
    ("Gemini 2.5: pushing the frontier with advanced reasoning, multimodality, long context, and next generation agentic capabilities", "通用模型背景", "通用VLM模型报告，不是取证解释评估。"),
    ("Blind/Referenceless image spatial quality evaluator", "图像质量方法背景", "传统无参考图像质量指标，与鉴伪解释效度不同。"),
    ("GANs trained by a two time-scale update rule converge to a local Nash equilibrium", "生成模型理论背景", "GAN训练理论，不涉及鉴伪解释。"),
    ("OpenAI GPT-5 System Card", "通用模型安全/能力背景", "系统卡，不是图像鉴伪解释实证。"),
    ("A new era of intelligence with Gemini 3", "通用模型背景", "模型产品/能力背景，非解释可靠性研究。"),
    ("Grok 4.1 model card", "通用模型背景", "通用模型卡，非媒体取证解释评估。"),
    ("SynthID-Image: Image Watermarking at Internet Scale", "来源溯源邻接", "生成图像水印/来源检测，非事后解释faithfulness。"),
    ("DeepFake Detection (DFDC) Solution", "数据/实现背景", "挑战赛检测实现方案，题名未显示解释终点。"),
    ("Multi-attentional deepfake detection", "检测方法背景", "深伪检测注意力结构；注意力本身不构成可靠解释验证。"),
    ("Capsule-Forensics: using capsule networks to detect forged images and videos", "取证检测背景", "伪造图像/视频检测方法背景，未见解释可靠性终点。"),
]


def read(name):
    with (OUT / name).open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write(name, rows):
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
        w.writeheader()
        w.writerows(rows)


rows = []
for i, (ref_title, decision, reason) in enumerate(refs, 1):
    rows.append({
        "reference_position": i,
        "citing_paper": TITLE,
        "reference_title": ref_title,
        "screen_decision": decision,
        "screen_reason": reason,
        "identity_reuse": "复用90候选身份" if "复用候选" in decision else "按题名初筛；需全文审核的直接邻接项单独标记",
        "source": SOURCE,
    })
table = OUT / "T21_SIDE-VLM_21条出版商参考文献逐位置筛查_20261010.csv"
with table.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\r\n")
    w.writeheader()
    w.writerows(rows)

main = read("74_V2完整分页逐位置初筛.csv")
assert not any(r["query_id"] == QUERY_ID for r in main)
for i, ref in enumerate(refs, 1):
    ref_title, decision, reason = ref
    main.append({
        "result_id": f"V2E-{QUERY_ID}-{i:04d}",
        "query_id": QUERY_ID,
        "requested_query": f"Publisher references of {TITLE}",
        "actual_query": "Springer official reference list; reference title/topic screen",
        "page_start": "0",
        "position_on_page": str(i),
        "result_position": str(i),
        "title": ref_title,
        "metadata": f"Springer publisher reference [{i}]",
        "url": SOURCE,
        "screen_decision": decision,
        "screen_reason": reason,
        "screen_basis": "Publisher-visible reference title and topic screening; do not treat as full-text review.",
        "source_page_url": SOURCE,
        "captured_at": "2026-10-10",
    })
write("74_V2完整分页逐位置初筛.csv", main)

routes = read("87_V2细查询子式实际试检状态.csv")
assert not any(r["query_id"] == QUERY_ID for r in routes)
routes.append({
    "query_id": QUERY_ID,
    "parent_id": "ICPR-2026-SIDE-VLM",
    "query": f"Publisher references of {TITLE}",
    "actual_trials": "Springer official chapter references [1]-[21], each title and topic screened; no full-text access to citing chapter.",
    "valid_pages": "1",
    "valid_positions": str(len(refs)),
    "visible_terminal": "True",
    "coverage_complete": "True",
    "blank_page_conflict_offsets": "",
    "estimate_min": str(len(refs)),
    "estimate_max": str(len(refs)),
    "missing_offsets": "citing chapter full text inaccessible; abstract claims await full-text verification",
    "status": "Springer可见21条参考文献位置已逐项主题初筛，见T21；Can ChatGPT Detect DeepFakes与SHIELD既有候选身份复用。全文章节受订阅限制，摘要内容未当作已核实实验。",
    "source_url": SOURCE,
    "next_url": "",
    "coverage_claim": "仅publisher当前列出的21个参考位置闭合题名筛查；不表示21篇均全文审核或该文摘要主张已验证。",
})
write("87_V2细查询子式实际试检状态.csv", routes)

candidates = read("90_本轮新增强相关候选与引文复核.csv")
c = next(r for r in candidates if r["title"].casefold() == TITLE.casefold())
c["discovery_query_id"] = f"{c['discovery_query_id']};{QUERY_ID}"
c["screen_basis"] += " Springer官方页面公开参考表21/21逐项初筛见T21；全文不可访问，未把摘要宣称当作原文实证。"
write("90_本轮新增强相关候选与引文复核.csv", candidates)

priority = read("72_V2已复核强相关优先清单.csv")
p = next(r for r in priority if r["title"].casefold() == TITLE.casefold())
p["original_reading_scope"] = "Springer官方摘要、正式书目信息及出版商可见21条参考位置已核；全文受订阅限制，实验效度待全文。"
p["reassessment"] = "保持rank 10和高优先全文待核。摘要与方法主题高度相关但只有出版商摘要可见；21条参考题录已筛并复用旧身份，不能将摘要中的解释faithfulness结论写成已验证证据。"
write("72_V2已复核强相关优先清单.csv", priority)

report = OUT / "00_重检阶段报告_未完成.md"
section = f"""

---

# 2026-10-10续：Side-VLM出版商摘要和21条参考筛查（全文待核）

- Springer正式页面确认ICPR 2026论文《Explainability-Guided Deepfake Detection for High-Fidelity Facial Edits》，2026-08-03 online，DOI 10.1007/978-3-032-31663-9_33。摘要报告Side-VLM侧脸/多视角高保真编辑数据、像素级mask和CAM-mask对齐，并声称解释faithfulness与扰动鲁棒性提升；章节全文受Springer订阅限制。本次只记题录与摘要，不将摘要指标结论作为已核全文实证。
- Springer列出的21个参考位置逐项筛查，见`T21_SIDE-VLM_21条出版商参考文献逐位置筛查_20261010.csv`；Can ChatGPT Detect DeepFakes和SHIELD与90既有身份复用，不重复计篇。Right-for-the-right-reasons、VisFIS为方法学邻接，其余区分数据/检测/生成/水印背景。
- 当前等待该章节全文可用后再核mask指标、稳定性定义、CAM解释充分/必要边界。来源：{SOURCE}。
"""
old = report.read_text(encoding="utf-8")
if "# 2026-10-10续：Side-VLM出版商摘要和21条参考筛查（全文待核）" not in old:
    report.write_text(old + section, encoding="utf-8")
