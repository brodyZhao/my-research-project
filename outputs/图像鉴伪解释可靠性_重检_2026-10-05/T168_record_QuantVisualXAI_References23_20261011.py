#!/usr/bin/env python3
"""Screen the 23 references shown in IEEE Xplore for the SIBGRAPI 2025 XAI paper.

This script records every visible numbered bibliography position, deduplicates
against the existing literature ledgers, and adds only the newly discovered
Crum et al. identity. It preserves the source-access limitations for the seed.
"""
from __future__ import annotations
import csv, re, shutil, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/图像鉴伪解释可靠性_重检_2026-10-05"
MASTER = OUT / "74_V2完整分页逐位置初筛.csv"
CANDIDATES = OUT / "90_本轮新增强相关候选与引文复核.csv"
PRIORITY = OUT / "72_V2已复核强相关优先清单.csv"
REVIEWS = OUT / "172_强相关核心及邻接论文原文解释可靠性效度核读.csv"
ROUTES = OUT / "87_V2细查询子式实际试检状态.csv"
REPORT = OUT / "00_重检阶段报告_未完成.md"
SIDE = OUT / "T168_QuantVisualXAI_OfficialReferences23_逐位置筛查_20261011.csv"
DATE = "2026-10-11"
QID = "CIT-QUANTVISUALXAI-REFS-20261011"
SEED = "Quantitative Analysis of Visual XAI for Multiclass DeepFake Detection Based on CNN"
SEED_PDF = "https://sibgrapi.sid.inpe.br/col/sid.inpe.br/sibgrapi/2025/09.13.21.50/doc/santiago-128.pdf"
SEED_IEEE = "https://ieeexplore.ieee.org/document/11223365/references"
SEED_SCHOLAR = "https://scholar.google.com/scholar?cites=3230431899246326504&as_sdt=2005&sciodt=0,5&hl=en"
CRUM = "Explain To Me: Salience-Based Explainability for Synthetic Face Detection Models"
CRUM_ARXIV = "https://arxiv.org/html/2303.11969v2"
CRUM_DOI = "https://doi.org/10.1109/TAI.2023.3333310"
QUERY = f"Official IEEE Xplore references of {SEED}; numbered items [1]-[23], individually screened"

# Position, citation as rendered in the IEEE references panel, canonical title,
# authors/year/venue, work URL, decision, and item-specific rationale.
REFS = [
(1,"R. Mubarak et al., A survey on the detection and impacts of deepfakes in visual, audio, and textual formats, IEEE Access 11, 144497–144529 (2023).","A survey on the detection and impacts of deepfakes in visual, audio, and textual formats","R. Mubarak et al.; IEEE Access 11 (2023)","https://ieeexplore.ieee.org/document/10365143","deepfake领域综述背景","综述视觉/音频/文本深伪的检测与影响；可追踪领域和术语，但不是解释效度原始实证。"),
(2,"D. L. R and B. B. Sujitha, Advancements in deepfake detection: A comprehensive review of AI-driven approaches, ICMLAS 2025, pp. 1007–1011.","Advancements in deepfake detection: A comprehensive review of AI-driven approaches","D. L. R, B. B. Sujitha; ICMLAS 2025","https://ieeexplore.ieee.org/document/10967658","深伪检测综述背景","检测方法综述；题录不显示解释可靠性或视觉XAI有效性实验。"),
(3,"N. Ur Rehman Ahmed et al., Visual deepfake detection: Review of techniques, tools, limitations, and future prospects, IEEE Access 13, 1923–1961 (2025).","Visual deepfake detection: Review of techniques, tools, limitations, and future prospects","N. Ur Rehman Ahmed et al.; IEEE Access 13 (2025)","https://ieeexplore.ieee.org/document/10816641","视觉深伪检测综述背景","视觉深伪检测综述，适合补领域地图；不是解释faithfulness的原始验证研究。"),
(4,"P. Ritter et al., Comparative analysis and evaluation of CNN models for deepfake detection, AiDAS 2023, pp. 250–255.","Comparative analysis and evaluation of CNN models for deepfake detection","P. Ritter, D. L. Anderies, A. Chowanda; AiDAS 2023","https://ieeexplore.ieee.org/document/10284611","检测器性能比较背景","比较深伪分类CNN，主要是预测性能和模型选择；不因标题中的evaluation就推断解释可靠性评价。"),
(5,"Y. Li et al., Celeb-DF: A Large-Scale Challenging Dataset for DeepFake Forensics, CVPR 2020, pp. 3204–3213.","Celeb-DF: A Large-Scale Challenging Dataset for DeepFake Forensics","Y. Li et al.; CVPR 2020","https://ieeexplore.ieee.org/document/9156368","深伪数据集背景","数据集/检测基准论文，不是解释质量验证。"),
(6,"K. Tsigos et al., Towards quantitative evaluation of explainable AI methods for deepfake detection, MAD ’24 (2024), pp. 37–45.","Towards quantitative evaluation of explainable AI methods for deepfake detection","K. Tsigos et al.; ACM MAD ’24 (2024); DOI 10.1145/3643491.3660292","https://doi.org/10.1145/3643491.3660292","核心直接相关；既有身份复用","直接评估深伪解释方法；已在T164/T165及172核读。本项只记录新论文参考边，不重读或重复计篇。"),
(7,"K. Jayakumar and N. Skandhakumar, A visually interpretable forensic deepfake detection tool using anchors, ICITR 2022, pp. 1–6.","A visually interpretable forensic deepfake detection tool using anchors","K. Jayakumar, N. Skandhakumar; ICITR 2022","https://ieeexplore.ieee.org/document/9993294","直接深伪解释系统；既有候选身份复用","在深伪视频检测器上使用Anchors并报告anchor-affinity/人工评价线索；90/72已有唯一候选记录。旧记录注明全文PDF尚未获得，本项不升级为全文核读。"),
(8,"B. Malolan et al., Explainable deep-fake detection using visual interpretability methods, ICICT 2020, pp. 289–293.","Explainable deep-fake detection using visual interpretability methods","B. Malolan, A. Parekh, F. Kazi; ICICT 2020","https://ieeexplore.ieee.org/document/9092227","早期深伪视觉解释方法；既有候选身份复用","早期视觉解释深伪检测工作；90已有唯一候选记录，TQE对其评价范围有引述。本轮只记录引文边，不重复计篇，也不声称本次读过被引文全文。"),
(9,"M. T. Hosain et al., Explainable AI approaches in deep learning: Advancements, applications and challenges, Computers and Electrical Engineering 117 (2024), 109246.","Explainable AI approaches in deep learning: Advancements, applications and challenges","M. T. Hosain et al.; Computers and Electrical Engineering 117 (2024)","https://doi.org/10.1016/j.compeleceng.2024.109246","通用XAI综述背景","广义深度学习XAI综述；与评价概念有关，但不专门研究鉴伪解释可靠性。"),
(10,"C. R. Crum et al., Explain to me: Salience-based explainability for synthetic face detection models, IEEE Transactions on Artificial Intelligence 5(6) (2024), pp. 2766–2778.",CRUM,"C. Crum, P. Tinsley, A. Boyd, J. Piland, C. Sweet, T. Kelley, K. Bowyer, A. Czajka; IEEE TAI 5(6) (2024); arXiv:2303.11969","https://arxiv.org/html/2303.11969v2","直接量化解释行为的强相关邻接；新身份全文已读","提出并测试五类Grad-CAM统计：saliency entropy、噪声响应、几何变换跟随、显著/非显著区域模糊后的预测/显著图变化、10次独立训练间显著图稳定性；比较普通交叉熵与使用人类显著性监督的CYBORG训练。它早于TQE预印本（2023 arXiv；2024期刊），但研究合成整脸真实性而非局部篡改取证。"),
(11,"T. Zhang, Deepfake generation and detection, a survey, Multimedia Tools and Applications 81(5) (2022), pp. 6259–6276.","Deepfake generation and detection, a survey","T. Zhang; Multimedia Tools and Applications 81(5) (2022)","https://doi.org/10.1007/s11042-021-11733-y","深伪领域综述背景","总结生成与检测技术；非解释质量或可靠性研究。"),
(12,"J. Thies et al., Face2Face: Real-time face capture and reenactment of RGB videos, Communications of the ACM 62(1) (2018), pp. 96–104.","Face2Face: Real-time face capture and reenactment of RGB videos","J. Thies et al.; Communications of the ACM 62(1) (2018)","https://doi.org/10.1145/3292039","面部操纵生成方法背景","面部重演/伪造生成技术出处；不涉及检测器解释。"),
(13,"H. Kim et al., Deep Video Portraits, ACM Transactions on Graphics 37(4) (2018).","Deep Video Portraits","H. Kim et al.; ACM Transactions on Graphics 37(4) (2018)","https://doi.org/10.1145/3197517.3201283","面部操纵生成方法背景","视频肖像合成方法出处；与解释可靠性无直接关系。"),
(14,"J. Thies, M. Zollhöfer, M. Nießner, Deferred neural rendering: Image synthesis using neural textures, ACM Transactions on Graphics 38(4) (2019).","Deferred neural rendering: Image synthesis using neural textures","J. Thies, M. Zollhöfer, M. Nießner; ACM TOG 38(4) (2019)","https://doi.org/10.1145/3306346.3323035","神经纹理操纵生成方法背景","引用的是伪造/重演数据生成技术，不是解释评价研究。"),
(15,"D. Chen et al., Face swapping: Realistic image synthesis based on facial landmarks alignment, Mathematical Problems in Engineering 2019, article 8902701.","Face swapping: Realistic image synthesis based on facial landmarks alignment","D. Chen et al.; Mathematical Problems in Engineering (2019)","https://doi.org/10.1155/2019/8902701","换脸生成方法背景","换脸生成方法/数据背景，不研究检测解释。"),
(16,"Deepfakes, https://github.com/Deepfakes/.","Deepfakes","Deepfakes project; software repository (not a paper)","https://github.com/Deepfakes/","非论文：软件项目","GitHub项目而非学术论文；作为生成工具来源保留书目位置，不纳入论文数量。"),
(17,"P. Isola et al., Image-to-Image Translation with Conditional Adversarial Networks, CVPR 2017, pp. 5967–5976.","Image-to-Image Translation with Conditional Adversarial Networks","P. Isola et al.; CVPR 2017","https://doi.org/10.1109/CVPR.2017.632","图像生成方法背景","Pix2Pix通用图像转换技术，非鉴伪解释评价研究。"),
(18,"R. Natsume et al., RSGAN: Face swapping and editing using face and hair representation in latent spaces, ACM SIGGRAPH 2018 Posters.","RSGAN: Face swapping and editing using face and hair representation in latent spaces","R. Natsume, T. Yatagawa, S. Morishima; SIGGRAPH 2018 Posters","https://doi.org/10.1145/3230744.3230818","换脸生成方法背景","人脸/头发潜在表示换脸生成方法，解释可靠性主题不见于题录。"),
(19,"Y. Nirkin et al., FSGANv2: Improved subject agnostic face swapping and reenactment, CVPR 2022.","FSGANv2: Improved subject agnostic face swapping and reenactment","Y. Nirkin, Y. Keller, T. Hassner; CVPR 2022","https://openaccess.thecvf.com/content/CVPR2022/html/Nirkin_FSGANv2_Improved_Subject_Agnostic_Face_Swapping_and_Reenactment_CVPR_2022_paper.html","换脸生成方法背景","身份无关换脸/重演方法；非XAI评价工作。"),
(20,"N. Mansoor and A. I. Iliev, Explainable AI for Deepfake Detection, Applied Sciences 15(2) (2025), article 725.","Explainable AI for Deepfake Detection","N. Mansoor, A. I. Iliev; Applied Sciences 15(2) (2025)","https://www.mdpi.com/2076-3417/15/2/725","直接深伪解释系统；既有全文核读身份复用","已在90/72/172核读：Network Dissection描述合成脸检测CNN内部概念；预测F1不是解释效度验证。本项仅补参考边。"),
(21,"A. Rössler et al., FaceForensics++: Learning to detect manipulated facial images, ICCV 2019.","FaceForensics++: Learning to detect manipulated facial images","A. Rössler et al.; ICCV 2019","https://openaccess.thecvf.com/content_ICCV_2019/html/Rossler_FaceForensics_Learning_to_Detect_Manipulated_Facial_Images_ICCV_2019_paper.html","深伪取证基准/数据集背景","提出检测数据集/基准，是本种子论文评估数据来源；不验证解释本身。"),
(22,"J. Xiang and G. Zhu, Joint face detection and facial expression recognition with MTCNN, ICISCE 2017, pp. 424–427.","Joint face detection and facial expression recognition with MTCNN","J. Xiang, G. Zhu; ICISCE 2017","https://ieeexplore.ieee.org/document/8110322","通用人脸预处理工具背景","人脸检测/表情识别预处理方法，不是伪造解释研究。"),
(23,"N. Kokhlikyan et al., Captum: A unified and generic model interpretability library for PyTorch, arXiv:2009.07896 (2020).","Captum: A unified and generic model interpretability library for PyTorch","N. Kokhlikyan et al.; arXiv:2009.07896 (2020)","https://arxiv.org/abs/2009.07896","XAI软件工具背景","解释算法软件库，不构成鉴伪解释可靠性验证论文。"),
]
assert len(REFS) == 23 and [x[0] for x in REFS] == list(range(1,24))

MASTER_FIELDS = ["result_id","query_id","requested_query","actual_query","page_start","position_on_page","result_position","title","metadata","url","screen_decision","screen_reason","screen_basis","source_page_url","captured_at"]
def read(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader=csv.DictReader(f); return list(reader.fieldnames), list(reader)
def write(path, fields, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w=csv.DictWriter(f, fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
def norm(s):
    return " ".join(re.findall(r"[a-z0-9]+", unicodedata.normalize("NFKD", str(s)).casefold()))
def exact_hits(title, ledgers):
    target=norm(title); result=[]
    for name, rows, key in ledgers:
        hits=[r for r in rows if norm(r.get(key,"")) == target]
        if hits: result.append(f"{name}: {len(hits)} exact normalized-title match(es)")
    return "; ".join(result) or "no exact normalized-title match in prior ledgers"

mf, master = read(MASTER)
cf, candidates = read(CANDIDATES)
pf, priorities = read(PRIORITY)
vf, reviews = read(REVIEWS)
rf, routes = read(ROUTES)
assert mf == MASTER_FIELDS

side_rows=[]
main_rows=[]
ledgers=[("74", master, "title"),("90", candidates, "title"),("72", priorities, "title"),("172", reviews, "paper")]
for n, shown, title, meta, url, decision, reason in REFS:
    hits=exact_hits(title,ledgers)
    if n == 10:
        identity=("新论文身份：作者/主题与本账中Crum的2025年学位论文相近，但题名、DOI、版本和研究问题不同；不可合并。ArXiv v2全文身份已核。")
    elif n == 6:
        identity="既有TQE唯一作品身份复用；已在T164/T165/172核查，不重读。"
    elif n in (7,8):
        identity="既有直接深伪XAI候选身份复用；只补本引文边。已有原稿可得性/效度边界照旧，不升级全文状态。"
    elif n == 20:
        identity="既有Mansoor & Iliev唯一作品身份复用；172已有全文/效度记录，不重复计篇。"
    elif n == 16:
        identity="非论文网页/软件项目；只保留引用位置，不进入论文身份计数。"
    else:
        identity="题名/题录逐项对账；作为背景/方法/数据/工具位置记录，不新增解释可靠性候选。"
    evidence=("arXiv官方HTML全文v2，2026-10-11访问；方法、实验环境、指标定义、结果与局限均核读。"
              if n == 10 else "IEEE Xplore官方References列表逐项题名/元数据筛选；不是对该被引作品的全文核读。")
    side_rows.append({"reference_position":str(n),"cited_title":title,"citation_as_shown":shown,
      "cited_work_url":url,"screening_decision":decision,"individual_reason":reason,
      "identity_handling":identity,"prior_ledger_hits":hits,"evidence_scope":evidence,
      "primary_bibliography_source":SEED_IEEE,"screened_at":DATE})
    main_rows.append({"result_id":f"V2E-{QID}-{n:03d}","query_id":QID,
      "requested_query":QUERY,"actual_query":f"IEEE Xplore references item [{n}]",
      "page_start":"reference list","position_on_page":str(n),"result_position":str(n),
      "title":title,"metadata":meta,"url":url,"screen_decision":decision,
      "screen_reason":reason,
      "screen_basis":"IEEE Xplore official bibliography, numbered item-by-item; title/venue screened and exact normalized-title identity checked against 74/90/72/172.",
      "source_page_url":SEED_IEEE,"captured_at":DATE})

side_fields=["reference_position","cited_title","citation_as_shown","cited_work_url","screening_decision","individual_reason","identity_handling","prior_ledger_hits","evidence_scope","primary_bibliography_source","screened_at"]
if SIDE.exists():
    sf, old=read(SIDE); assert sf==side_fields
    by_pos={r["reference_position"]:r for r in old}
    for r in side_rows: by_pos[r["reference_position"]]=r
    side_rows=[by_pos[k] for k in sorted(by_pos,key=int)]
write(SIDE,side_fields,side_rows)

seen_ids={r["result_id"] for r in master}
new_main=[r for r in main_rows if r["result_id"] not in seen_ids]
if new_main:
    with MASTER.open("a",encoding="utf-8-sig",newline="") as f:
        csv.DictWriter(f,fieldnames=mf,extrasaction="ignore").writerows(new_main)

# Add only the genuinely new Crum work; do not conflate it with Crum's thesis.
crum_meta="Colton R. Crum, Patrick Tinsley, Aidan Boyd, Jacob Piland, Christopher Sweet, Timothy Kelley, Kevin Bowyer, Adam Czajka; IEEE Transactions on Artificial Intelligence 5(6), 2766–2778 (2024); DOI 10.1109/TAI.2023.3333310; arXiv:2303.11969v2 (2023)"
crum_reason=("在synthetic-face真实性检测任务中系统比较解释/显著图行为，含噪声与几何变换响应、显著区/非显著区模糊、跨随机种子稳定性，和本题的视觉伪造解释可靠性直接相邻。"
"但全脸StyleGAN生成检测不是局部图像篡改取证；稳定/扰动响应与解释忠实、篡改区域ground truth和用户恰当依赖仍是不同构念。")
crum_candidate={"title":CRUM,"authors_year_venue":crum_meta,
 "preliminary_status":"强相关邻接核心；arXiv官方HTML全文核读；方法、指标和迁移边界已记录",
 "relevance_reason":crum_reason,"discovery_query_id":QID,
 "discovery_query":QUERY,"source_url":CRUM_ARXIV,
 "screen_basis":"由SIBGRAPI 2025 XAI评估论文IEEE官方参考[10]反向发现；arXiv官方HTML v2全文核对身份和实证终点。"}
if not any(norm(r["title"])==norm(CRUM) for r in candidates): candidates.append(crum_candidate)
else:
    for r in candidates:
        if norm(r["title"])==norm(CRUM): r.update(crum_candidate)
write(CANDIDATES,cf,candidates)

crum_priority={"rank":"36.875","title":CRUM,"url":CRUM_ARXIV,
 "V2_relation":"直接量化synthetic-face detector视觉解释行为的强相关邻接；方法上接近解释稳定性/扰动可靠性，但不是局部篡改定位研究。",
 "original_reading_scope":"arXiv官方HTML全文v2核读。任务：FFHQ真实脸与StyleGAN/2/2-ADA/3合成脸检测；DenseNet121/ResNet50、Grad-CAM，对照交叉熵与CYBORG人类显著性引导训练。核查五类指标定义、实验表和讨论。",
 "limitations":"五项指标涵盖热图熵、噪声响应、几何变换跟随、显著/非显著区域模糊响应、10次独立训练稳定性；CYBORG把人工显著性用于训练，但本论文未做独立用户评价。全脸合成标签无局部篡改区域真值；指标可表征内部行为/稳定性，不能单独建立因果faithfulness或法证证据充分性。",
 "reassessment":"将其纳入2023–24合成脸解释量化评估的重要前史/方法邻接；对图像鉴伪可靠性问题有方法迁移价值，结论标记为相邻而非同任务直接证据。"}
if not any(norm(r["title"])==norm(CRUM) for r in priorities): priorities.append(crum_priority)
else:
    for r in priorities:
        if norm(r["title"])==norm(CRUM): r.update(crum_priority)
def rank_key(row):
    try:return float(row["rank"])
    except (ValueError,TypeError):return 1e9
priorities.sort(key=rank_key); write(PRIORITY,pf,priorities)

# Revise the seed's status from abstract-only to partial primary-source text access.
for r in candidates:
    if norm(r["title"])==norm(SEED):
        r["preliminary_status"]="直接定量解释质量评估核心候选；官方IEEE摘要/参考表及会议PDF可索引正文片段已核；完整PDF下载端点超时，全文细节仍标部分可核"
        r["relevance_reason"]=("在FaceForensics++上比较Grad-CAM、SmoothGrad、Integrated Gradients、Input×Gradient与Saliency，并报告熵、噪声响应、几何变换和AOS指标。已核片段显示AOS把显著区删除后测预测变化，却称为functional sufficiency；该操作更接近必要性/删除敏感性，不能单独证明解释可靠。")
        r["screen_basis"]="T164 Google Scholar Cited-by position 33; IEEE Xplore official abstract/references; official SIBGRAPI PDF search-indexed body excerpts for AOS and Tables I/III/IV. Direct PDF endpoint timed out; not marked as full binary/full text retrieved."
write(CANDIDATES,cf,candidates)

# Refine existing priority entry for the seed; preserve its rank and title.
for r in priorities:
    if norm(r["title"])==norm(SEED):
        r["original_reading_scope"]="IEEE Xplore official abstract and complete visible references [1]-[23]; official SIBGRAPI proceedings PDF indexed body excerpts checked for AOS definition, experimental detector accuracies and Tables III–IV. Full publisher PDF fetch timed out on 2026-10-11, so this is partial text audit rather than complete binary retrieval."
        r["limitations"]="AOS is described as sufficiency but removes the most salient regions and measures prediction change, which operationally resembles necessity/comprehensiveness. The available text does not establish independent manipulated-region truth or human appropriate-reliance testing. The official IEEE list ends at [23]; ResearchGate secondary metadata says 25 references, a source-count discrepancy retained for audit."
        r["reassessment"]="Keep as a direct core evaluation paper and a particularly important comparison with TQE/Crum; distinguish metric proxies and deletion sensitivity from causal faithfulness and forensic evidence validity. Do not claim complete full-text review until publisher PDF is accessible."
write(PRIORITY,pf,priorities)

crum_review={"paper":CRUM,"verified_identity":"Colton R. Crum et al.; IEEE Transactions on Artificial Intelligence 5(6), 2766–2778 (2024); DOI 10.1109/TAI.2023.3333310; arXiv:2303.11969v2 (submitted 2023-03-21, revised 2023-03-27)",
 "relevance_class":"强相关邻接：synthetic-face detection的定量saliency/XAI行为评价；非局部操纵取证",
 "primary_source":CRUM_ARXIV,
 "scope_and_methods":"arXiv官方HTML全文核读。使用10,000张FFHQ真脸和四种StyleGAN生成脸；评价子集为4,000真/4,000假。DenseNet121、ResNet50的Grad-CAM，对照交叉熵与CYBORG人类显著性监督训练。定义五类汇总指标：S_entropy、S_noise（盐椒噪声下SSIM）、S_resilience（平移/翻转/90度旋转并逆变换对齐）、S_focus（模糊显著区与非显著区后看AUROC和热图变化）、S_stability（每个架构/训练配置十个独立seed的热图SSIM）。",
 "observed_reliability_evidence":"实证报告不同模型/训练方案在显著图集中度、输入噪声反应、几何变换跟随、显著/背景模糊反应和跨seed稳定性上的差异；人类显著性监督模型总体表现出更高跨seed一致性。作者把这些定位为可扩展的模型行为解释指标。",
 "limitations_and_construct_boundary":"任务是整脸合成/真实分类，不是局部篡改定位或拼接检测。CYBORG的人类标注参与训练监督；本文没有独立用户评价，也未以独立篡改区域真值验证解释正确性。S_focus以模型自身显著图选区并再看模型性能/新显著图变化，存在自参照性；熵/稳定/几何一致性是行为质量代理，不等同因果忠实或足够法证证据。噪声/变换类型由作者说明为示例，需按任务适配。",
 "screening_conclusion":"纳入图像真实性XAI量化评价的重要前史/强方法邻接。对本题可迁移的是稳定性、输入扰动和受控删除测试设计；不能把其人类引导训练或高saliency稳定性误写为用户信任校准或局部篡改证据真值。",
 "review_date":DATE}
if not any(norm(r["paper"])==norm(CRUM) for r in reviews): reviews.append(crum_review)
else:
    for r in reviews:
        if norm(r["paper"])==norm(CRUM): r.update(crum_review)

seed_review={"paper":SEED,
 "verified_identity":"Leandro Santiago de Araújo et al.; 2025 38th SIBGRAPI Conference on Graphics, Patterns and Images; IEEE DOI 10.1109/SIBGRAPI67909.2025.11223365; conference 30 Sep–3 Oct 2025",
 "relevance_class":"核心直接候选；原文证据部分核对，完整PDF不可得",
 "primary_source":SEED_PDF,
 "scope_and_methods":"IEEE Xplore官方摘要及References [1]-[23]已直接核对；官方会议PDF索引片段包含AOS定义及实验表。FaceForensics++多类面部操纵；比较ResNet50、EfficientNetB7、InceptionV3、ConvNeXt上的Grad-CAM、SmoothGrad、Integrated Gradients、Input×Gradient、Saliency；报告显著图熵、噪声响应、几何变换resilience、SLIC segmentation AOS，并将指标输入Random Forest区分类别。完整PDF端点访问超时，因此操作细节仍是部分核对。",
 "observed_reliability_evidence":"官方索引正文显示AOS把最显著区删除后量化预测改变；Table I的检测准确率约91%–94%，Tables III–IV给不同解释器统计量及基于这些量的RF分类率。这些证明作者提出了定量行为/判别代理，不代表解释已通过独立法证证据验证。",
 "limitations_and_construct_boundary":"作者将AOS解释为functional sufficiency，但实际删除已高亮特征后测输出下降，构念更接近necessity/comprehensiveness或deletion sensitivity；经典sufficiency应检验仅保留被解释特征时能否维持输出。当前可访问原文内容未显示独立伪造区域mask/专家真值或人类适当依赖评估；仅有预测准确率不能验证解释正确性。已读的是官方摘要、引用列表与索引正文片段，不能声称已取得完整PDF/阅读全文。IEEE Xplore显示[1]-[23]共23个编号；ResearchGate元数据显示References 25，主来源计数差异保留。",
 "screening_conclusion":"高优先级直接候选；论文真正贡献是鉴伪场景下视觉XAI指标的应用和比较。采用时必须区分稳定性/扰动敏感/模型预测差异与grounded causal faithfulness，且将AOS操作化作为待检验构念问题。完整全文核查仍待出版社PDF可访问。",
 "review_date":DATE}
if not any(norm(r["paper"])==norm(SEED) for r in reviews): reviews.append(seed_review)
else:
    for r in reviews:
        if norm(r["paper"])==norm(SEED): r.update(seed_review)
write(REVIEWS,vf,reviews)

route={"query_id":QID,"parent_id":"CIT-TQE-CITEDBY-20261011",
 "query":QUERY,
 "actual_trials":"IEEE Xplore official reference panel for article 11223365, positions [1]-[23]; full numbered list transcribed and each title/topic screened. Cross-matched normalized title against 74/90/72/172. The TQE Cited-by snapshot itself was already 49/49 and was not rescreened.",
 "valid_pages":"1 official bibliography panel","valid_positions":"23","visible_terminal":"True","coverage_complete":"True",
 "blank_page_conflict_offsets":"","estimate_min":"23","estimate_max":"23",
 "missing_offsets":"None among the IEEE Xplore numbered entries [1]-[23]. ResearchGate secondary metadata displays 25 references, but both the official IEEE panel and indexed official SIBGRAPI PDF text show numbered references ending at [23]; retain discrepancy without inventing [24]-[25].",
 "status":"All 23 numbered references exposed by the primary IEEE source were individually screened. Five directly relevant deepfake-XAI items were identity-matched: TQE, Anchors, Malolan, Crum, Mansoor/Iliev. The first, second, third, and fifth use existing identities where appropriate; only Crum et al. is newly added as a distinct full-text reviewed adjacent study. Generic detector/dataset/generator/method sources and one GitHub software citation are separately classified. Seed paper body was only partially available through official indexed excerpts; its full PDF remains unverified.",
 "source_url":SEED_IEEE,"next_url":"",
 "coverage_claim":"Closed only for the 23 numbered references displayed by IEEE Xplore and corroborated in the official PDF index. Does not mean the cited papers were all read in full, that the 2-item ResearchGate metadata discrepancy is authoritatively explained, or that the field/citation graph is exhaustive."}
route_by_id={r["query_id"]:r for r in routes}; route_by_id[QID]=route
write(ROUTES,rf,list(route_by_id.values()))

with REPORT.open(encoding="utf-8") as f: report=f.read()
heading="## 2026-10-11续：TQE被引候选QuantVisualXAI参考链与Crum方法核读（T168）"
if heading not in report:
    section=f"""

{heading}

- TQE Google Scholar精确题名页仍显示Cited by 49；T164侧表/主账已有49/49，按用户的去重要求本轮只确认现有记录，不重复重筛。沿其中位置33的《{SEED}》扩展引用链。
- IEEE Xplore官方References面板列[1]–[23]，逐条筛查记于`T168_QuantVisualXAI_OfficialReferences23_逐位置筛查_20261011.csv`、主账74及路线87。23个位置完整，分类涵盖5篇直接/邻接深伪XAI、综述/检测数据/生成方法/工具；直接作品按90/72/172身份复用。ResearchGate二手页面显示25条references，与IEEE和可索引官方会议PDF止于[23]不同，保留为元数据差异，不凭空补两条。
- 新增并全文核读《{CRUM}》（arXiv 2023，IEEE TAI 2024）。它是2024年TQE之前的重要合成脸XAI量化前史，提出saliency entropy、noise response、geometric resilience、salience-guided degradation及跨十个seed的稳定性。人工显著图进入CYBORG训练，但不是独立用户解释评测；研究为整脸StyleGAN真实性检测，不是局部篡改区域法证。完整效度边界记于172。
- 种子论文《{SEED}》的IEEE摘要和[1]–[23]参考表已直接核；官方会议PDF索引还提供AOS定义与Tables I/III/IV片段。种子PDF端点本轮超时，未取得完整二进制，172中按“部分原文证据”标注，不冒称全文审读。可访问文本把AOS叫作sufficiency，但实现是删去显著区后看预测变化，更接近necessity/deletion sensitivity；未见独立篡改区域真值或恰当依赖证据。
- 累计账本更新后计数：74主账{len(master)+len(new_main)}条位置；90候选{len(candidates)}个唯一题名；72优先表{len(priorities)}项；172效度记录{len(reviews)}项；87路线{len(route_by_id)}条。统计单位不同，不能解释为强相关独立论文数或检索全量。TQE本身被引位置不重复增行。
- 验证：T168侧表23/23连续、理由非空；主账23个新ID唯一；TQE旧49条未增行；候选/优先/效度身份唯一；打包脚本校验ZIP成员、CRC及源文件哈希。下一步优先继续新核读的Crum前向引用及Anchors/Malolan的缺失全文检查，但只筛未见身份/未闭合页，不再刷TQE 49条或本次23条书目。
"""
    report += section
    REPORT.write_text(report,encoding="utf-8")

# Put an executable audit copy in the deliverables so the input ledger can be rebuilt.
shutil.copy2(Path(__file__), OUT / "T168_record_QuantVisualXAI_References23_20261011.py")

assert len(side_rows)==23 and [int(r["reference_position"]) for r in side_rows]==list(range(1,24))
assert all(r["individual_reason"].strip() for r in side_rows)
assert len({r["result_id"] for r in main_rows})==23
assert sum(1 for r in candidates if norm(r["title"])==norm(CRUM))==1
assert sum(1 for r in priorities if norm(r["title"])==norm(CRUM))==1
assert sum(1 for r in reviews if norm(r["paper"])==norm(CRUM))==1
assert sum(1 for r in reviews if norm(r["paper"])==norm(SEED))==1
print(f"T168 refs screened={len(side_rows)}; new master rows={len(new_main)}; 90={len(candidates)}; 72={len(priorities)}; 172={len(reviews)}; 87={len(route_by_id)}")
