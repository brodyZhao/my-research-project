#!/usr/bin/env python3
"""Screen all 17 Google Scholar citing records for Crum et al. (2023/2024).

The script preserves every citation position, matches identities against the
existing ledgers, and adds only the three new, full-text-reviewed adjacent
synthetic-face/saliency studies. It does not rescreen the earlier TQE snapshot.
"""
from __future__ import annotations

import csv
import re
import shutil
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/图像鉴伪解释可靠性_重检_2026-10-05"
MASTER = OUT / "74_V2完整分页逐位置初筛.csv"
CANDIDATES = OUT / "90_本轮新增强相关候选与引文复核.csv"
PRIORITY = OUT / "72_V2已复核强相关优先清单.csv"
REVIEWS = OUT / "172_强相关核心及邻接论文原文解释可靠性效度核读.csv"
ROUTES = OUT / "87_V2细查询子式实际试检状态.csv"
REPORT = OUT / "00_重检阶段报告_未完成.md"
SIDE = OUT / "T169_Crum_CitedBy17_逐位置筛查_20261011.csv"
DATE = "2026-10-11"
QID = "CIT-CRUM-CITEDBY-20261011"
QUERY = 'Google Scholar Cited by snapshot for "Explain To Me: Salience-Based Explainability for Synthetic Face Detection Models"'
CRUM_SCHOLAR = "https://scholar.google.com/scholar?cites=11606748264256168497&as_sdt=2005&sciodt=0,5&hl=en"
CRUM_SCHOLAR_P2 = CRUM_SCHOLAR + "&start=10"
CRUM = "Explain To Me: Salience-Based Explainability for Synthetic Face Detection Models"
CRUM_URL = "https://arxiv.org/html/2303.11969v2"

# Absolute rank, title, metadata as shown on Scholar, visible snippet, URL,
# decision, and a title/snippet-level screening reason for every position.
ITEMS = [
(1,"Second frcsyn-ongoing: Winning solutions and post-challenge analysis to improve face recognition with synthetic data","I. DeAndres-Tame, R. Tolosana, P. Melzi et al.; Information Fusion / Elsevier, 2025","Synthetic data is gaining popularity for face recognition amid privacy and real-data acquisition constraints.","https://www.sciencedirect.com/science/article/pii/S1566253525001721","合成数据人脸识别挑战赛分析；非鉴伪解释可靠性","研究合成训练数据对人脸识别性能的影响，不评估伪造检测器解释、证据定位或解释可靠性。"),
(2,"Frcsyn challenge at CVPR 2024: Face recognition challenge in the era of synthetic data","I. DeAndres-Tame, R. Tolosana, P. Melzi et al.; IEEE/CVF CVPR Workshops, 2024","Synthetic data is gaining increasing relevance for training machine learning models.","https://ieeexplore.ieee.org/abstract/document/10678240/","人脸识别挑战赛/合成数据背景","以合成脸增强人脸识别为主题，不是判断图像真伪的解释评价研究。"),
(3,"ECSPLAIN: Explainability Constrained-claSsifier for Pairing the detection and the Localization of moving Areas from SAR INterferograms","A. Bralet, A. M. Atto, J. Chanussot; IEEE TGRS, 2025","Detecting slope instabilities on synthetic aperture radar interferograms using deep learning presents challenges.","https://ieeexplore.ieee.org/abstract/document/11108247/","遥感运动区域检测/定位的解释方法；领域不匹配","题名中的explainability与detection/localization看似相近，但对象是SAR干涉图中的地表运动，不是图像伪造或媒体篡改。"),
(4,"Assessment of human emotional reactions to visual stimuli deep-dreamed by artificial neural networks","A. Marczak-Czajka, T. Redgrave, M. Mitcheff et al.; Frontiers in Psychology, 2024","Studies emotional reactions to visual stimuli synthesized by artificial neural networks.","https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2024.1509392/full","合成视觉刺激的人类情绪研究；非鉴伪解释可靠性","研究人对deep-dream图像的情绪反应，不涉及真实性判定、解释证据或检测器依赖。"),
(5,"AutoSIGHT: Automatic Eye Tracking-based System for Immediate Grading of Human experTise","B. Dowling, J. Probcin, A. Czajka; IEEE VL/HCC, 2025; arXiv:2508.01015","Uses eye-tracking features to classify human expertise while participants solve iris presentation-attack detection tasks.","https://arxiv.org/abs/2508.01015","人类专长评估/人机配对邻接；无解释评价","通过眼动评估操作者在iris PAD中的专长，可作人机分工背景；本文不提供模型解释，也不测解释对恰当依赖的影响。"),
(6,"MENTOR: Human perception-guided pretraining for increased generalization","C. R. Crum, A. Czajka; arXiv:2310.19545v3, 2025","Uses a saliency-predicting autoencoder before classifier fine-tuning; tests iris PAD, synthetic-face detection and chest-X-ray anomalies.","https://arxiv.org/html/2310.19545","强相关邻接：合成脸检测的人类显著性预训练与显著图统计；新增全文核读","在synthetic-face detection中用人工显著性进行无类别预训练，并定量报告CAM熵；该终点是显著图紧致度代理，不能证明其忠实反映分类因果或真实篡改证据。"),
(7,"Taking training seriously: Human guidance and management-based regulation of artificial intelligence","C. R. Crum, C. Coglianese; IEEE conference, 2024; arXiv:2402.08466","Discusses governance and regulatory approaches to human guidance and management of AI.","https://arxiv.org/abs/2402.08466","AI治理/人类指导制度背景","治理与监管分析，不是图像取证/XAI可靠性的技术或用户实证研究。"),
(8,"Saliency-guided training for fingerprint presentation attack detection","S. Webster, A. Czajka; IEEE IJCB, 2025; arXiv:2505.02176v2","Uses 800 human-annotated fingerprint saliency maps and tests generalization on LivDet-2021.","https://arxiv.org/abs/2505.02176","生物识别PAD显著性训练方法邻接；无解释可靠性验证","研究指纹呈现攻击检测的人工显著性引导训练与准确率/泛化，不是数字图像篡改鉴伪解释；保留为边界邻接，不列核心候选。"),
(9,"Grains of saliency: Optimizing saliency-based training of biometric attack detection models","C. R. Crum, S. Webster, A. Czajka; IEEE IJCB, 2024; arXiv:2405.00650","Studies saliency granularity and sources for iris PAD and synthetic-face detection across multiple CNNs.","https://arxiv.org/html/2405.00650","强相关邻接：合成脸检测的人类显著性训练与跨域泛化；新增全文核读","含synthetic-face detection；比较人工/仿人模型/分割显著图的粒度对泛化影响。只报告分类AUROC，不验证输出解释对独立真值、模型因果机制或用户依赖的正确性。"),
(10,"Is There Evidence of Gender Bias in Iris Presentation Attack Detection Approaches?","M. Mitcheff, S. K. Khan, P. J. Flynn et al.; IEEE Identity Science, 2026","Investigates gender-specific differences in iris PAD accuracy.","https://ieeexplore.ieee.org/abstract/document/11614531/","虹膜PAD公平性；非解释可靠性","研究生物属性分组下PAD准确率差异，题录不显示解释方法或解释有效性评估。"),
(11,"Lightweight vision transformer architectures and comparative analysis of multi-head classifiers with integrated gradients for red chilli powder adulteration detection","B. Büyükarıkan; Journal of Food Measurement and Characterization, 2026","Uses integrated gradients in image-based red-chilli adulteration detection.","https://link.springer.com/article/10.1007/s11694-026-04797-7","食品掺假视觉检测XAI；不属图像伪造/鉴伪","虽使用Integrated Gradients，但任务是食品掺假分类，题录和摘要未涉及图像真实性或解释可靠性。"),
(12,"Almost Right: Making First-Layer Kernels Nearly Orthogonal Improves Model Generalization","C. R. Crum, A. Czajka; arXiv:2504.16362, 2025","Proposes nearly orthogonal first-layer CNN kernels to improve generalization.","https://arxiv.org/abs/2504.16362","通用CNN泛化方法；非XAI或鉴伪","研究卷積核正交化和模型泛化，不涉及合成图像检测解释或解释评价。"),
(13,"SAGE: Saliency-Guided Contrastive Embeddings","C. R. Crum, C. Sweet, A. Czajka; arXiv:2511.12744v2, 2025","Tests iris PAD, chest-X-ray anomalies and synthetic-face detection; includes a flipped-saliency sanity check.","https://arxiv.org/html/2511.12744","强相关邻接：合成脸检测的显著图反转sanity check；新增全文核读","在synthetic-face detection上做saliency-guided training，并反转显著图检查性能变化；Face AUROC约0.587降至0.577，提供有限的输入干预证据，但不是独立局部真值、解释忠实性基准或人类依赖评估。"),
(14,"AI-Aided Design for Industrial Manufacturing: Generating Synthetic Image Datasets to Train 3D Object Reconstruction Neural Networks","F. Manuri, F. De Pace, I. Piparo et al.; IET Collaborative Intelligent Manufacturing, 2025","Generates synthetic image datasets for industrial 3D object reconstruction.","https://ietresearch.onlinelibrary.wiley.com/doi/abs/10.1049/cim2.70039","制造业合成训练数据；非图像鉴伪XAI","synthetic images用于3D重建训练，不是判断图像真伪或解释可靠性。"),
(15,"Quantitative Analysis of Visual XAI for Multiclass DeepFake Detection Based on CNN","L. S. de Araújo, F. L. Seixas, A. L. e Souza et al.; SIBGRAPI 2025; DOI 10.1109/SIBGRAPI67909.2025.11223365","Compares visual XAI methods for multiclass deepfake detection.","https://ieeexplore.ieee.org/document/11223365","强相关直接评估；既有身份复用","直接评估深伪视觉解释；已在T168及172核对。此处只记录Crum→该论文引文边，不重复计篇或复核全文。"),
(16,"Integrating Human-Perceptual Priors Into Deep Learning","C. R. Crum; ProQuest dissertation/book, 2025","Dissertation/book on human-perceptual priors in deep learning.","https://search.proquest.com/openview/4ad67e622343664ed5a9214f8a6e4722/1?pq-origsite=gscholar&cbl=18750&diss=y","学位论文/综合性方法背景；既有题名身份复用","既有74账本已记录该ProQuest学位论文题名；不是新增独立期刊/会议论文，当前引文卡未提供可用于核查的独立解释可靠性实证。"),
(17,"Prioritizing face editing models using fuzzy hierarchical analysis","M. Afsharpour, A. Bahrololom; Fuzzy Systems and its Applications, 2025","Uses evidence-based fuzzy analytic hierarchy process to prioritize adversarial face-editing models.","http://jfsa.fuzzy.ir/article_242186.html?lang=en","人脸编辑生成模型排序；非检测解释","对象是编辑/生成模型选择，不判断给定图像是否伪造，也不评价检测模型的解释。"),
]
assert len(ITEMS) == 17 and [x[0] for x in ITEMS] == list(range(1, 18))

MASTER_FIELDS = ["result_id","query_id","requested_query","actual_query","page_start","position_on_page","result_position","title","metadata","url","screen_decision","screen_reason","screen_basis","source_page_url","captured_at"]
SIDE_FIELDS = ["result_position","page_start","position_on_page","title","scholar_metadata","visible_snippet","work_url","screening_decision","individual_reason","identity_handling","prior_ledger_hits","evidence_scope","source_page_url","screened_at"]

def read(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        r=csv.DictReader(f)
        return list(r.fieldnames), list(r)

def write(path: Path, fields, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w=csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader(); w.writerows(rows)

def norm(s):
    return " ".join(re.findall(r"[a-z0-9]+", unicodedata.normalize("NFKD", str(s)).casefold()))

mf, master = read(MASTER)
cf, candidates = read(CANDIDATES)
pf, priorities = read(PRIORITY)
vf, reviews = read(REVIEWS)
rf, routes = read(ROUTES)
assert mf == MASTER_FIELDS
ledgers = [("74",master,"title"),("90",candidates,"title"),("72",priorities,"title"),("172",reviews,"paper")]

def exact_hits(title):
    target=norm(title); found=[]
    for name, rows, key in ledgers:
        count=sum(1 for r in rows if norm(r.get(key,""))==target)
        if count: found.append(f"{name}: {count} exact normalized-title match(es)")
    return "; ".join(found) or "no exact normalized-title match in 74/90/72/172"

side=[]; main=[]
for rank,title,meta,snippet,url,decision,reason in ITEMS:
    start="0" if rank<=10 else "10"
    pos=str(rank if rank<=10 else rank-10)
    prior=exact_hits(title)
    if rank==15:
        identity="Exact normalized title already exists as T168/TQE-Cited-by position 33 in 74, and in 90/72/172; reuse it and add only this new citation edge."
        evidence="Google Scholar citing-result card; cited work itself was previously screened through the official IEEE/source record and is not re-read here."
    elif rank==16 and prior.startswith("74:"):
        identity="Exact dissertation title already occurs in 74; preserve the title identity and avoid counting it as a new article."
        evidence="Google Scholar citing-result card; previous 74 query record exists, but this citation card alone does not establish new full-text evidence."
    elif rank in (6,9,13):
        identity="No exact title identity found in 74/90/72/172; new distinct preprint/article identity, full text checked at official arXiv HTML."
        evidence="Google Scholar Cited by result card plus official arXiv HTML full text; abstract, task, methods, reliability/evaluation endpoint, results and construct boundaries checked."
    else:
        identity="Title and visible bibliographic metadata screened as a distinct citing item; no strong candidate addition; citation-list record retained."
        evidence="Google Scholar Cited by result card title, visible metadata/snippet and linked record; no full-text claim made unless separately noted."
    source=CRUM_SCHOLAR if rank<=10 else CRUM_SCHOLAR_P2
    side.append({"result_position":str(rank),"page_start":start,"position_on_page":pos,"title":title,
      "scholar_metadata":meta,"visible_snippet":snippet,"work_url":url,"screening_decision":decision,
      "individual_reason":reason,"identity_handling":identity,"prior_ledger_hits":prior,
      "evidence_scope":evidence,"source_page_url":source,"screened_at":DATE})
    main.append({"result_id":f"V2E-{QID}-{rank:03d}","query_id":QID,"requested_query":QUERY,
      "actual_query":f"Cited by cluster 11606748264256168497; page start={start}","page_start":start,
      "position_on_page":pos,"result_position":str(rank),"title":title,"metadata":meta,"url":url,
      "screen_decision":decision,"screen_reason":reason,
      "screen_basis":"Google Scholar Cited by card screened by title, visible metadata/snippet, and linked primary record where the result was a plausible in-scope candidate; identity cross-matched to 74/90/72/172.",
      "source_page_url":source,"captured_at":DATE})

if SIDE.exists():
    sf, old=read(SIDE); assert sf==SIDE_FIELDS
    by={r["result_position"]:r for r in side}
    # Preserve the original pre-addition identity match snapshot on reruns.
    # Recomputing it after appending the papers would falsely mark each as a
    # prior hit against its own T169 record.
    for r in old: by[r["result_position"]]=r
    side=[by[k] for k in sorted(by,key=int)]
write(SIDE,SIDE_FIELDS,side)

seen={r["result_id"] for r in master}
new_main=[r for r in main if r["result_id"] not in seen]
if new_main:
    with MASTER.open("a",encoding="utf-8-sig",newline="") as f:
        csv.DictWriter(f,fieldnames=mf,extrasaction="ignore").writerows(new_main)

NEW = [
 {"title":"MENTOR: Human Perception-Guided Pretraining for Increased Generalization",
  "authors_year_venue":"Colton R. Crum, Adam Czajka; arXiv:2310.19545 (v1 2023; v3 2025)",
  "preliminary_status":"强相关邻接；synthetic-face detection与模型saliency统计；arXiv官方HTML全文核读",
  "relevance_reason":"在iris PAD、合成脸检测、胸部X光异常三个open-set任务上，以人工显著图预测预训练CNN，再微调分类器；还报告测试CAM的salience entropy。Face任务直接涉及真实/StyleGAN脸识别，且用363名标注者的真实/假判断支持训练。",
  "discovery_query_id":QID,"discovery_query":QUERY,"source_url":"https://arxiv.org/html/2310.19545",
  "screen_basis":"Google Scholar Cited by 17 position 6; official arXiv v3 HTML full text, including datasets, results and §6.2 quantitative saliency analysis. Method adjacency, not a direct forensic-explanation faithfulness test."},
 {"title":"Grains of Saliency: Optimizing Saliency-based Training of Biometric Attack Detection Models",
  "authors_year_venue":"Colton R. Crum, Samuel Webster, Adam Czajka; IEEE IJCB 2024; arXiv:2405.00650",
  "preliminary_status":"强相关邻接；合成脸真实性检测的saliency training与泛化；arXiv官方HTML全文核读",
  "relevance_reason":"在iris PAD与synthetic-face detection上比较人工、仿人saliency模型及分割来源的BOI/AOI/FOI粒度，并用多架构、多seed AUROC评估open-set泛化。合成人脸任务使其与图像真实性解释研究直接相邻；它检验的是训练收益而非解释的独立正确性。",
  "discovery_query_id":QID,"discovery_query":QUERY,"source_url":"https://arxiv.org/html/2405.00650",
  "screen_basis":"Google Scholar Cited by 17 position 9; official arXiv HTML full text, including three tasks, training/evaluation, results and all 46 numbered references."},
 {"title":"SAGE: Saliency-Guided Contrastive Embeddings",
  "authors_year_venue":"Colton R. Crum, Christopher Sweet, Adam Czajka; arXiv:2511.12744v2 (2025)",
  "preliminary_status":"强相关邻接；包含合成脸检测显著图反转sanity check；arXiv官方HTML全文核读",
  "relevance_reason":"在iris PAD、胸部X光和synthetic-face detection上用人类saliency指导logit/embedding训练；通过反转saliency map作sanity check。合成脸任务ResNet50 AUROC为0.587，反转后0.577；这提供有限的干预性机制线索，但不是独立伪造区域GT、faithfulness gold standard或用户解释评估。",
  "discovery_query_id":QID,"discovery_query":QUERY,"source_url":"https://arxiv.org/html/2511.12744",
  "screen_basis":"Google Scholar Cited by 17 position 13; official arXiv v2 HTML full text, including methods, three tasks, full flipped-map sanity check, results and limitations."}
]
for item in NEW:
    existing=next((r for r in candidates if norm(r["title"])==norm(item["title"])),None)
    if existing: existing.update(item)
    else: candidates.append(item)
write(CANDIDATES,cf,candidates)

PRIORITIES = [
 {"rank":"37.00","title":"SAGE: Saliency-Guided Contrastive Embeddings","url":"https://arxiv.org/html/2511.12744",
  "V2_relation":"强方法邻接：synthetic-face detection中用人类显著性指导训练，并对反转saliency做sanity check；不是直接法证XAI评测。",
  "original_reading_scope":"arXiv官方HTML v2全文；Iris PAD、chest X-ray、synthetic face detection三任务；比较SAGE/CYBORG/MENTOR等方法；核对开集AUROC、多架构结果、反转saliency表与讨论。",
  "limitations":"合成脸ResNet50 AUROC 0.587，反转saliency后0.577，差异较小；实验关注训练有效性而非给定测试图解释faithfulness，没有独立篡改区域真值、解释标注者评审或恰当依赖测试。不能把该反转sanity check写成完整忠实性证明。",
  "reassessment":"作为最贴近解释可靠性技术验证的合成脸方法邻接纳入：其反转图sanity-check可迁移为机制测试，但幅度小且端点是分类AUC，仍需独立GT/删除插入等验证。"},
 {"rank":"37.125","title":"MENTOR: Human Perception-Guided Pretraining for Increased Generalization","url":"https://arxiv.org/html/2310.19545",
  "V2_relation":"强方法邻接：人类显著性预训练用于open-set synthetic-face detection，并对测试CAM报告entropy。",
  "original_reading_scope":"arXiv官方HTML v3全文；iris PAD、合成脸、胸片三个任务；人工saliency autoencoder预训练+分类微调；十次seed评估、结果、CAM qualitative/entropy analysis及局限。",
  "limitations":" synthetic-face分类数据只用765个训练样本和20,000验证样本；主结果是AUROC而非解释faithfulness。§6.2只报告CAM salience entropy，并明确缺乏可用于检验model/human salience efficacy的额外人工GT；entropy不能说明模型真正依赖这些区域。",
  "reassessment":"作为2023年合成脸XAI/人类感知训练邻接加入。它包含真实解释质量代理和清楚的效度限制，适合构念比较，不等于独立法证解释正确性。"},
 {"rank":"37.25","title":"Grains of Saliency: Optimizing Saliency-based Training of Biometric Attack Detection Models","url":"https://arxiv.org/html/2405.00650",
  "V2_relation":"强方法邻接：比较合成脸检测中人类salience来源与粒度对跨seed泛化的影响。",
  "original_reading_scope":"arXiv官方HTML全文；iris PAD和合成脸两个身份相关任务；人类/仿人模型/分割来源与BOI/AOI/FOI粒度；三种CNN；多次独立运行AUROC、结果与全46条参考文献。",
  "limitations":"synthetic-face任务的各saliency训练结果受架构影响且方差较大；只评价分类泛化，没有测量测试解释是否对齐独立GT、是否忠实反映模型因果机制或是否帮助用户正确决策。",
  "reassessment":"纳入解释训练机制与一般化之间的邻接证据；不归为解释可靠性直接实验。可为数据域差异、saliency标签粒度及人工标注成本提供背景。"}
]
for item in PRIORITIES:
    existing=next((r for r in priorities if norm(r["title"])==norm(item["title"])),None)
    if existing: existing.update(item)
    else: priorities.append(item)
priorities.sort(key=lambda r: float(r["rank"]) if re.fullmatch(r"\d+(?:\.\d+)?",r["rank"]) else 1e9)
write(PRIORITY,pf,priorities)

REVIEW_ROWS = [
 {"paper":"MENTOR: Human Perception-Guided Pretraining for Increased Generalization",
  "verified_identity":"Colton R. Crum and Adam Czajka; arXiv:2310.19545 (submitted 2023-10-30; v3 2025-04-26)",
  "relevance_class":"强方法邻接：synthetic-face detection人工saliency预训练和CAM熵分析；非直接局部取证faithfulness验证",
  "primary_source":"https://arxiv.org/html/2310.19545",
  "scope_and_methods":"全文核读。两阶段MENTOR先以autoencoder在无类别标签下预测人工显著图，再移除decoder并微调分类器；任务为iris PAD、synthetic-face detection和chest X-ray；10个随机seed测AUROC。Face任务使用363名Amazon Mechanical Turk参与者提供的real/fake判断及支持区域标注；训练样本765张（379 real/386 fake），20,000张验证样本。对比Cross-entropy、CYBORG、UNET+Gaze及不同backbone。",
  "observed_reliability_evidence":"作者报告预测CAM的定性图例与test CAM salience entropy；将entropy作为显著图紧致/聚焦的粗代理，并把分析定位为synthetic-face explainability toolkit的一部分。其主实验展示saliency-guided pretraining与分类泛化，不是test explanation的独立真值判定。",
  "limitations_and_construct_boundary":"§6.2说明因时间限制仅计算S_entropy；作者承认已使用所有可用human saliency作训练，缺少额外数据以测model saliency与human saliency的效能差异。Entropy只量化紧致性，不能检验解释对模型决策的因果忠实性/局部篡改mask正确性；无用户解释效用或适当依赖实验。Face训练/验证规模及GAN数据域也限制外推。",
  "screening_conclusion":"强方法邻接，纳入2023起synthetic-face explainability研究脉络。重要的是它明确显示‘saliency训练泛化’与‘saliency解释是否正确’是不同终点；保留作者的entropy代理并标明缺少独立human-ground-truth校验。","review_date":DATE},
 {"paper":"Grains of Saliency: Optimizing Saliency-based Training of Biometric Attack Detection Models",
  "verified_identity":"Colton R. Crum, Samuel Webster, Adam Czajka; IEEE International Joint Conference on Biometrics (IJCB), 2024; arXiv:2405.00650",
  "relevance_class":"强方法邻接：synthetic-face detection人类显著图训练与开集泛化；不是解释输出评价",
  "primary_source":"https://arxiv.org/html/2405.00650",
  "scope_and_methods":"全文核读。研究iris PAD与合成脸检测；比较人工subjects、模仿人类显著性的autoencoder、领域分割模型，以及Boundary/Area/Features of Interest三档salience granularity；ResNet50、DenseNet121、Inception-V3；iris测试AUC跨3次、合成脸跨5次独立训练。合成脸测试集7,000张（1,000 real、6,000 StyleGAN系列合成脸）。",
  "observed_reliability_evidence":"测量saliency来源与粒度对开集检测泛化的效应。synthetic-face结果显示不同架构的最优粒度不同、方差偏宽；这提示人类saliency监督在伪造检测中的效益并不稳定。",
  "limitations_and_construct_boundary":"所有主要结果是分类AUROC，不是模型解释与测试图像独立ground truth的对齐、必要/充分证据或模型参数随机化测试；human saliency被用作训练引导而非独立评价基准。只覆盖合成脸与生物PAD，不代表局部图像拼接/修补。",
  "screening_conclusion":"强方法邻接；能支持人类显著监督、标签粒度、架构和跨训练seed的对比设计，不可将分类提升写作解释faithfulness或取证正确性。","review_date":DATE},
 {"paper":"SAGE: Saliency-Guided Contrastive Embeddings",
  "verified_identity":"Colton R. Crum, Christopher Sweet, Adam Czajka; arXiv:2511.12744v2 (submitted 2025-11-16; revised 2025-12-05)",
  "relevance_class":"强方法邻接：synthetic-face detection上的显著图引导训练与反转图sanity check",
  "primary_source":"https://arxiv.org/html/2511.12744",
  "scope_and_methods":"全文核读。SAGE以saliency-preserving/degrading模糊增强、logit分布对齐和embedding triplet loss结合人类显著图；任务包含iris PAD、chest X-ray异常与synthetic-face detection；比较CYBORG、UNet+Gaze、Gaze-GNN、MENTOR等；5次独立训练，报告AUROC。附saliency-map反转sanity check。",
  "observed_reliability_evidence":"Synthetic-face ResNet50 AUROC：SAGE 0.587±0.060；将人类saliency map反转后0.577±0.037（差0.010）。该干预能有限检查训练收益是否对指定saliency输入敏感；其他任务的差异更大，任务效应不一致。",
  "limitations_and_construct_boundary":"研究目标是saliency-guided training的性能/机制，不是解释质量benchmark。合成脸结果较低且反转差异小，不能证明解释是正确/忠实；无真实篡改区域mask、独立证据真值、删除插入评测或用户适当依赖研究。作者把人工标注质量作为留待未来工作的问题。",
  "screening_conclusion":"纳入合成脸解释脉络中少见的saliency反转sanity-check方法；审慎视为低幅度机制证据，不能等同完整faithfulness验证。","review_date":DATE},
]
for item in REVIEW_ROWS:
    existing=next((r for r in reviews if norm(r["paper"])==norm(item["paper"])),None)
    if existing: existing.update(item)
    else: reviews.append(item)
write(REVIEWS,vf,reviews)

route={"query_id":QID,"parent_id":"CIT-QUANTVISUALXAI-REFS-20261011","query":QUERY,
 "actual_trials":"Google Scholar Cited by cluster 11606748264256168497: page 1 start=0 (10 cards) and page 2 start=10 (7 cards); all 17 title/snippet/metadata positions screened and exact identity matched against 74/90/72/172. Plausible synthetic-face/saliency results were checked against official arXiv HTML. Existing QuantVisualXAI identity reused; three distinct adjacent papers (MENTOR, Grains of Saliency, SAGE) added and full-text screened.",
 "valid_pages":"2","valid_positions":"17","visible_terminal":"True","coverage_complete":"True","blank_page_conflict_offsets":"","estimate_min":"17","estimate_max":"17",
 "missing_offsets":"None within the displayed 17-result Scholar Cited-by snapshot. Scholar citation counts are snapshot-dependent; this closes the captured list only.",
 "status":"All 17 displayed citing positions individually screened. 1 direct Quantitative Analysis identity reused, 3 new strong-method-adjacent synthetic-face/saliency studies added (MENTOR, Grains of Saliency, SAGE); remaining 13 retained with itemized reasons as outside direct scope or method/background boundary. Full texts were read only for the three plausible adjacent candidates. No new direct evaluation of local image-forgery explanation faithfulness discovered in this snapshot.",
 "source_url":CRUM_SCHOLAR,"next_url":CRUM_SCHOLAR_P2,
 "coverage_claim":"Complete for this captured Google Scholar Cited-by 17 snapshot at 2026-10-11, not the entire citing literature or field. Counts are not guaranteed stable over time; title-level screening is not full-text review for the other 14 positions."}
route_by={r["query_id"]:r for r in routes}; route_by[QID]=route
write(ROUTES,rf,list(route_by.values()))

with REPORT.open(encoding="utf-8") as f: report=f.read()
heading="## 2026-10-11续：Crum《Explain To Me》前向引文17条逐项筛查（T169）"
if heading not in report:
    report += f"""

{heading}

- Google Scholar《{CRUM}》记录显示Cited by 17；第一页10条、第二页7条均已逐条筛选，日志为`T169_Crum_CitedBy17_逐位置筛查_20261011.csv`，主位置账74增加17个独立引文边，路线87记录本快照。此前TQE Cited by 49及T168参考文献23项均未重筛。
- 位置15《Quantitative Analysis of Visual XAI for Multiclass DeepFake Detection Based on CNN》是既有T168/TQE链候选，身份复用不重复计篇；位置16的Crum博士论文/图书题名在74已有精确记录。
- 新增全文核读三篇强方法邻接研究：MENTOR（synthetic-face detection的人类saliency预训练，附CAM熵代理）、Grains of Saliency（合成脸检测saliency来源/粒度与开集泛化）、SAGE（含saliency反转sanity check）。三篇均不属于局部图像篡改解释的直接faithfulness验证；其具体端点和限制写入90/72/172。
- 其余14个位置均留有逐篇筛选理由。直接法证XAI可靠性/忠实性新论文：0；直接相关身份复用：1；新增强方法邻接：3。页内标题/摘要筛选不冒充其它论文的全文审读。
- 当前账本计数：74主账{len(master)+len(new_main)}条位置；90候选{len(candidates)}个唯一题名；72优先表{len(priorities)}项；172全文/效度记录{len(reviews)}项；87路线{len(route_by)}条。统计单位不同，不能解释为强相关独立论文总数。
- 验证：T169侧表17/17连续、理由非空；主账17个ID唯一；既有QuantVisual身份唯一；新增MENTOR/Grains/SAGE各在90/72/172唯一；全表result_id唯一。
- 下一步：优先从MENTOR/Grains/SAGE的原始参考文献中筛查尚未处理的合成脸解释/显著性评估研究，如CYBORG、Human-aided saliency maps、Model Focus和Teaching AI to Teach；仅处理新身份与缺失引文位置，不回扫已核论文。
"""
    REPORT.write_text(report,encoding="utf-8")

shutil.copy2(Path(__file__),OUT/"T169_record_CrumCitedBy17_20261011.py")

assert len(side)==17 and [int(r["result_position"]) for r in side]==list(range(1,18))
assert all(r["individual_reason"].strip() for r in side)
assert len(new_main) in (0,17)
assert len({r["result_id"] for r in master+new_main})==len(master)+len(new_main)
for title in ("MENTOR: Human Perception-Guided Pretraining for Increased Generalization", "Grains of Saliency: Optimizing Saliency-based Training of Biometric Attack Detection Models", "SAGE: Saliency-Guided Contrastive Embeddings"):
    assert sum(norm(r["title"])==norm(title) for r in candidates)==1
    assert sum(norm(r["title"])==norm(title) for r in priorities)==1
    assert sum(norm(r["paper"])==norm(title) for r in reviews)==1
assert sum(norm(r["title"])==norm(ITEMS[14][1]) for r in candidates)==1
print(f"T169 screened={len(side)}; new master rows={len(new_main)}; new candidates=3; 74={len(master)+len(new_main)}; 90={len(candidates)}; 72={len(priorities)}; 172={len(reviews)}; 87={len(route_by)}")
