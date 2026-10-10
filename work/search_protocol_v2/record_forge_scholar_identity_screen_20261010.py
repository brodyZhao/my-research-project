import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/图像鉴伪解释可靠性_重检_2026-10-05'
ID_QUERY='FORGE-ARXIV-ID-250315867-20261010'
CIT_QUERY='CIT-FORGE-TRUTHLENS-20261010'
EXACT_QUERY='FORGE-EXACT-TITLE-20261010'
SOURCE_ID='https://scholar.google.com/scholar?q=2503.15867&hl=zh-CN&as_sdt=0,5'
SOURCE_CIT='https://scholar.google.com/scholar?cites=5448038239159642453&as_sdt=2005&sciodt=0,5&hl=zh-CN'
items=[
('SFDM-ViCapsNet: using SSIM-guided frame selection and statistical fusion dynamic margin cropping to detect fake faces in videos','检测背景/排除','视频伪造检测方法，结果卡片未显示解释评价。','单纯检测身份，不纳入强相关候选。'),
('TruthLens: Visual Grounding for Universal DeepFake Reasoning','直接核心/复用FORGE身份','同一arXiv:2503.15867作品的旧标题版本；复用FORGE既有全文核读、83条参考题录筛查及优先身份，不重复计篇。','与FORGE同一作品；此处仅记Scholar别名结果位置。'),
('AIGI-Holmes: Towards Explainable and Generalizable AI-Generated Image Detection via Multimodal Large Language Models','直接强相关/复用既有身份','AI生成图像鉴伪并明确包含explainability；90/172均有既有身份，复用核读。','复用AIGI-Holmes既有身份与全文记录。'),
('Fine-grained DINO Tuning with Dual Supervision for Face Forgery Detection','检测背景/排除','脸部伪造检测，结果卡片没有解释可靠性终点。','只有检测证据不足以纳入本题解释可靠性。'),
('EvolveReason: Self-Evolving Reasoning Paradigm for Explainable Deepfake Facial Image Identification','直接强相关/复用候选','明确面向深伪人脸图像解释识别；候选90已有身份，沿现有全文待核状态推进。','复用EvolveReason身份，不重复建立候选。'),
('Memory-Anchored Multimodal Reasoning for Explainable Video Forensics','视频解释邻接/复用候选','解释型多模态视频取证，与图像直接核心分开；90已有身份。','复用既有视频邻接身份，不计图像直接核心。'),
('EXPDF: Adversarially Robust Spatiotemporal Deepfake Detection Using Temporal-Aware Attention Fusion And Evolutionary Hyperparameter Optimization','检测背景/排除','视频检测与时空鲁棒性，卡片未显示解释评估。','attention/鲁棒检测本身不构成解释可靠性证据。'),
('Evidence-Grounded Forensic Reasoning for Detecting and Grounding Multi-Modal Media Manipulation','直接核心/复用EFR身份','用户指定高相关作品，已在90/172核读；Scholar结果本轮复用已核身份。','复用EFR身份及已完成全文核读。'),
('VRAG-DFD: Verifiable Retrieval-Augmentation for MLLM-based Deepfake Detection','直接强相关/复用候选','可验证检索增强的深伪MLLM检测；90已有候选，按原文待核/已核状态复用。','复用VRAG-DFD候选身份。'),
('Além do Desempenho: Um Estudo da Confiabilidade de Detectores de Deepfakes','检测可靠性邻接','主题是检测器可靠性，但当前卡片未显示XAI或解释评价；作为测量邻接记录，不列解释强相关。','仅分类器可靠性，非解释可靠性。'),
('Explainable Deep Learning for Digital Image Forgery Detection: A Systematic and Critical Review','强相关综述/复用候选','直接聚焦图像伪造检测解释；90已有候选身份，题录重复发现不重复计篇。','复用既有综述身份，全文状态单独追踪。'),
('From Survey to Solution: Lightweight and Interpretable Multimodal Deepfake Detection Using CNNs and Grad-CAM','解释方法邻接/新候选','深伪检测中使用Grad-CAM的多模态框架；结果卡片未呈现faithfulness、人评或稳定性协议，保留为低优先方法邻接。','方法应用相关，但未见解释可靠性评价终点。'),
('PViT: A Hybrid Model for Deepfake Face Detection Using Patch Vision Transformers and Deep Learning','检测背景/排除','检测架构论文，结果卡片未显示解释评价。','无解释可靠性证据。'),
('DeepFake Face Detection Using SE-Enhanced 1D-CNN with Improved Calibration and Classification Performance','分类校准邻接','分类概率校准/性能是可靠性相邻维度，但未显示解释对象或解释效度。','单独分类校准不等同解释忠实性。'),
('Beyond Artifacts: Semantic Deepfake Detection and Digital Provenance Tracking with Multimodal Large Language Models','取证推理/溯源邻接，新候选待复核','多模态语义鉴伪与来源追踪方向相邻；卡片未见解释faithfulness终点，暂入邻接候选。','题名摘要级筛查，需读全文才可判断解释证据。'),
('Controlled Benchmarking of CNN Architectures for Fake Face Classification under Standardized Synthetic Conditions','检测基准背景/排除','标准化合成条件下分类器比较；未呈现解释评价。','检测基准不等于解释可靠性评价。'),
('MADL: Towards Dependable Image Forgery Detection Via Multi-Agent Forensic Reasoning','直接图像鉴伪/复用全文身份','图像伪造多智能体取证推理；90/172已有身份并完成核读，复用效度边界。','复用MADL身份和已完成全文核读。'),
('Explainable Image-Centric Forgery Detection: A Survey','强相关综述/复用候选','图像中心伪造检测解释综述；90已有身份，复用身份并待按既定计划核全文。','复用既有综述身份，不重复登记。'),
('TruthLens: Explainable DeepFake Detection for Face Manipulated and Fully Synthetic Data','直接核心/复用FORGE身份','同一arXiv:2503.15867历史题名/聚类记录，复用FORGE的172、T16及72身份。','同一作品的Scholar重复版本，不重复计篇。'),
('Towards Trustworthy AI: A Transformer-Driven Adaptive Framework for Robust Deepfake Detection in Digital Forensics','信任/鲁棒邻接/复用候选','已有90身份；题名涵盖深伪检测与鲁棒性，暂按邻接处理，不将trustworthy标题当作解释faithfulness证据。','复用候选身份；需全文检查是否存在解释指标。'),
('VIGIL: Part-Grounded Structured Reasoning for Generalizable Deepfake Detection','直接强相关/复用全文身份','部件级接地结构化深伪推理；90/172已有身份，复用全文边界。','复用VIGIL身份和已完成全文核读。'),
('Deepfake Face Detection and Adversarial Attack Defense Method Based on Multi-Feature Decision Fusion','检测/对抗防御背景','多特征融合检测与防御，标题未体现解释评估。','无解释可靠性终点。'),
('Photos, Charts and Video Must Explain Quickly','主题排除','通用视觉传播/说明章节，非取证检测解释研究。','非本题范围。'),
('Towards Trustworthy AI: A Transformer-Driven Adaptive Framework for Robust Deepfake Detection in Digital Forensics','信任/鲁棒邻接/重复版本','Scholar末页重复显示该条目，候选身份与位置观察应合并。','同一作品的重复检索结果，复用第20项身份。'),
('TruthLens: Explainable DeepFake Detection for Face Manipulated and Fully Synthetic Data','直接核心/复用FORGE身份/重复版本','Scholar第三页再次显示FORGE同一arXiv作品旧标题。','同一作品第三个标题变体，不重复计篇。'),
]
citations=[
('Evidence-Grounded Forensic Reasoning for Detecting and Grounding Multi-Modal Media Manipulation','直接核心/复用EFR身份','Scholar Cited by: TruthLens/FORGE明确显示该引用；EFR已全文核读并与FORGE引文链建立身份映射。','沿已存在EFR-CITEDBY-20261009及172身份复用，不重复审查。'),
('VIGIL: Part-Grounded Structured Reasoning for Generalizable Deepfake Detection','直接强相关/复用VIGIL身份','Scholar Cited by: TruthLens/FORGE明确显示该引用；90/172已有VIGIL身份。','复用已记录VIGIL全文核读，不重复计篇。'),
]

def read(name):
    with (OUT/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(name,rows):
    with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\r\n' if name.startswith(('74_','87_')) else '\n')
        w.writeheader();w.writerows(rows)

# Query screening ledger: every visible result position, including duplicate versions.
main=read('74_V2完整分页逐位置初筛.csv')
assert not any(r['query_id'] in (ID_QUERY,CIT_QUERY) for r in main)
for i,(title,decision,reason,identity) in enumerate(items,1):
    start=((i-1)//10)*10;pos=((i-1)%10)+1
    main.append({'result_id':f'V2E-{ID_QUERY}-{i:03d}','query_id':ID_QUERY,'requested_query':'FORGE/TruthLens citing and identity search via arXiv ID 2503.15867','actual_query':'Google Scholar query 2503.15867','page_start':str(start),'position_on_page':str(pos),'result_position':str(i),'title':title,'metadata':'Google Scholar result card; metadata limited to visible citation snippet','url':SOURCE_ID,'screen_decision':decision,'screen_reason':reason,'screen_basis':identity,'source_page_url':SOURCE_ID if start==0 else SOURCE_ID+f'&start={start}','captured_at':'2026-10-10'})
for i,(title,decision,reason,identity) in enumerate(citations,1):
    main.append({'result_id':f'V2E-{CIT_QUERY}-{i:03d}','query_id':CIT_QUERY,'requested_query':'Google Scholar Cited by: TruthLens/FORGE arXiv:2503.15867','actual_query':'cites=5448038239159642453','page_start':'0','position_on_page':str(i),'result_position':str(i),'title':title,'metadata':'Google Scholar Cited by result card','url':SOURCE_CIT,'screen_decision':decision,'screen_reason':reason,'screen_basis':identity,'source_page_url':SOURCE_CIT,'captured_at':'2026-10-10'})
write('74_V2完整分页逐位置初筛.csv',main)

# Detailed one-row-per-position citation/title screen.
for name,rows,headers in [
 ('T22_FORGE_arXiv身份号Scholar_25条逐位置题录筛查_20261010.csv',items,['result_position','page_start','position_on_page','scholar_title','screen_decision','screen_reason','identity_reuse']),
 ('T23_FORGE_TruthLens被引作品_2条逐项筛查_20261010.csv',citations,['result_position','citing_title','screen_decision','screen_reason','identity_reuse'])]:
    path=OUT/name
    if name.startswith('T22'):
        data=[{'result_position':i,'page_start':((i-1)//10)*10,'position_on_page':((i-1)%10)+1,'scholar_title':a,'screen_decision':b,'screen_reason':c,'identity_reuse':d} for i,(a,b,c,d) in enumerate(rows,1)]
    else:data=[{'result_position':i,'citing_title':a,'screen_decision':b,'screen_reason':c,'identity_reuse':d} for i,(a,b,c,d) in enumerate(rows,1)]
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=headers,lineterminator='\n');w.writeheader();w.writerows(data)

routes=read('87_V2细查询子式实际试检状态.csv')
assert not any(r['query_id'] in (EXACT_QUERY,ID_QUERY,CIT_QUERY) for r in routes)
routes += [
 {'query_id':EXACT_QUERY,'parent_id':'FORGE-TRUTHLENS-SEED','query':'"FORGE: Forensic Reasoning with Grounded Evidence"','actual_trials':'Exact title search performed after CAPTCHA; Scholar returned no matching article under current title.','valid_pages':'1','valid_positions':'0','visible_terminal':'True','coverage_complete':'True','blank_page_conflict_offsets':'','estimate_min':'0','estimate_max':'0','missing_offsets':'current-title indexing absent; use arXiv identifier/title history','status':'精确现题名无命中；同一作品以旧题TruthLens编目，转arXiv ID检索。','source_url':'https://scholar.google.com/scholar?q=%22FORGE%3A+Forensic+Reasoning+with+Grounded+Evidence%22&hl=zh-CN&as_sdt=0,5','next_url':SOURCE_ID,'coverage_claim':'只说明该精确字符串未命中，不说明作品未被收录。'},
 {'query_id':ID_QUERY,'parent_id':'FORGE-TRUTHLENS-SEED','query':'2503.15867','actual_trials':'Google Scholar pages start=0,10,20; 10+10+5 result cards. Title/abstract snippets screened at every position.','valid_pages':'3','valid_positions':'25','visible_terminal':'True','coverage_complete':'True','blank_page_conflict_offsets':'','estimate_min':'25','estimate_max':'25','missing_offsets':'arXiv ID search is a Scholar query snapshot, not a complete citing-paper set; full text pending for new neighbors.','status':'arXiv ID query 25/25 visible positions screened; multiple historical TruthLens titles merged to FORGE identity; existing works reuse 90/172 identities; see T22.','source_url':SOURCE_ID,'next_url':'','coverage_claim':'该Scholar查询的可见25个结果位置闭合题录筛查；不等同于FORGE全部前向引用。'},
 {'query_id':CIT_QUERY,'parent_id':'FORGE-TRUTHLENS-SEED','query':'Google Scholar Cited by: TruthLens/FORGE arXiv:2503.15867','actual_trials':'Cited-by page cites=5448038239159642453; one page, two result cards.','valid_pages':'1','valid_positions':'2','visible_terminal':'True','coverage_complete':'True','blank_page_conflict_offsets':'','estimate_min':'2','estimate_max':'2','missing_offsets':'This is Scholar Cited-by snapshot; author/title-version cluster may differ.','status':'Scholar Cited by returned 2 works: EFR and VIGIL; both identities already full-text screened and reused; see T23.','source_url':SOURCE_CIT,'next_url':'','coverage_claim':'该FORGE/TruthLens Scholar引文聚类快照可见2/2项筛查完成；不代表版本聚类之外的所有引文。'}]
write('87_V2细查询子式实际试检状态.csv',routes)

# Add only genuinely new adjacent works; append discovery provenance to known identities.
candidates=read('90_本轮新增强相关候选与引文复核.csv')
known_updates={
 'AIGI-Holmes: Towards Explainable and Generalizable AI-Generated Image Detection via Multimodal Large Language Models',
 'EvolveReason: Self-Evolving Reasoning Paradigm for Explainable Deepfake Facial Image Identification',
 'Memory-Anchored Multimodal Reasoning for Explainable Video Forensics',
 'Evidence-Grounded Forensic Reasoning for Detecting and Grounding Multi-Modal Media Manipulation',
 'VRAG-DFD: Verifiable Retrieval-Augmentation for MLLM-Based Deepfake Detection',
 'Explainable Deep Learning for Digital Image Forgery Detection: A Systematic and Critical Review',
 'MADL: Towards Dependable Image Forgery Detection Via Multi-Agent Forensic Reasoning',
 'Explainable Image-Centric Forgery Detection: A Survey',
 'Towards Trustworthy AI: A Transformer-Driven Adaptive Framework for Robust Deepfake Detection in Digital Forensics',
 'VIGIL: Part-Grounded Structured Reasoning for Generalizable Deepfake Detection',
 'FORGE: Forensic Reasoning with Grounded Evidence (earlier cited as TruthLens: Visual Grounding for Universal DeepFake Reasoning)',
}
for r in candidates:
 if r['title'] in known_updates:
  if ID_QUERY not in r['discovery_query_id']:r['discovery_query_id'] += ';'+ID_QUERY
  if r['title'].startswith('FORGE:') and CIT_QUERY not in r['discovery_query_id']:r['discovery_query_id'] += ';'+CIT_QUERY
new=[
 {'title':'From Survey to Solution: Lightweight and Interpretable Multimodal Deepfake Detection Using CNNs and Grad-CAM','authors_year_venue':'M. S. M. Mane, S. Y. Raut, M. P. Bharati; 2026 international conference; metadata pending publisher verification','preliminary_status':'低优先解释方法邻接；全文待核','relevance_reason':'多模态深伪检测采用Grad-CAM；当前题录/摘要未显示faithfulness、人评或稳定性评价，不能列作直接可靠性实证。','discovery_query_id':ID_QUERY,'discovery_query':'Google Scholar arXiv identity search: 2503.15867, page start=10','source_url':'https://ieeexplore.ieee.org/abstract/document/11484573/','screen_basis':'Scholar题录摘要位置12；逐条筛查见T22；暂存方法邻接身份，需原文核查。'},
 {'title':'Beyond Artifacts: Semantic Deepfake Detection and Digital Provenance Tracking with Multimodal Large Language Models','authors_year_venue':'J. J. Sara, S. Rizvi, T. J. Tasfi et al.; 2025 international conference; metadata pending verification','preliminary_status':'取证推理/来源溯源邻接候选；全文待核','relevance_reason':'多模态语义鉴伪与来源追踪场景相关；题录卡片未显示解释效度指标，暂不作为解释faithfulness核心。','discovery_query_id':ID_QUERY,'discovery_query':'Google Scholar arXiv identity search: 2503.15867, page start=0','source_url':'https://ieeexplore.ieee.org/abstract/document/11490141/','screen_basis':'Scholar题录摘要位置15；逐条筛查见T22；当前为引文检索中题录级邻接候选。'},
]
for item in new:
 if not any(r['title'].casefold()==item['title'].casefold() for r in candidates):candidates.append(item)
write('90_本轮新增强相关候选与引文复核.csv',candidates)

# Append a concise report section once.
report=OUT/'00_重检阶段报告_未完成.md'
section='''\n\n---\n\n# 2026-10-10 FORGE/TruthLens Scholar身份与前向引文筛查\n\n- 精确现题名`FORGE: Forensic Reasoning with Grounded Evidence`在Google Scholar返回零结果；这只是字符串未命中。改用同一作品arXiv ID `2503.15867`，三页（start=0/10/20）25个可见位置逐项筛查，逐位置决策及身份复用见`T22_FORGE_arXiv身份号Scholar_25条逐位置题录筛查_20261010.csv`。Scholar仍将该作品显示为多个旧题名TruthLens，全部映射回既有FORGE身份，不增加篇数。\n- 该ID检索中的AIGI-Holmes、EvolveReason、EFR、VRAG-DFD、VIGIL、MADL、Explainable Image-Centric Forgery Detection综述等已有90/172身份逐一复用；从题录新识别的Grad-CAM多模态检测、语义鉴伪/来源追踪两项仅列低优先邻接候选，尚未将其当作faithfulness证据。检测器校准/一般可靠性结果与解释可靠性分开。\n- 随后跟进FORGE/TruthLens自身Scholar Cited by聚类（cites=5448038239159642453），可见2项：EFR和VIGIL，两者均已完成全文核读；逐项记录见`T23_FORGE_TruthLens被引作品_2条逐项筛查_20261010.csv`，无新增独立作品。该聚类快照不表示所有版本/数据库引文穷尽。\n'''
old=report.read_text(encoding='utf-8')
if 'FORGE/TruthLens Scholar身份与前向引文筛查' not in old:report.write_text(old+section,encoding='utf-8')
