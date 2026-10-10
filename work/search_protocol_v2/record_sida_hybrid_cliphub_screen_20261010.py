import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/图像鉴伪解释可靠性_重检_2026-10-05'
TITLE='A Hybrid CLIP-Diffusion Architecture for Transparent Deepfake Detection and Explainability Evaluation'

def read(name):
    with (OUT/name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def write(name, rows):
    with (OUT/name).open('w', encoding='utf-8-sig', newline='') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader(); w.writerows(rows)

candidates=read('90_本轮新增强相关候选与引文复核.csv')
row=next(r for r in candidates if r['title']==TITLE)
row['authors_year_venue']='Andreas Specker, Manjunatha Veerappa, Thomas Golda, Nadia Burkart, Dominik Alveen, Anna Wilhelm; CVPR 2026 SAFE Workshop, pp. 467–476'
row['preliminary_status']='直接强相关核心候选；题录和机构项目摘要已核；完整论文效度待取得全文'
row['relevance_reason']='图像深伪检测与解释评估直接命题；高度相关，优先全文核查faithfulness/解释评价指标、基准和人评协议。'
row['source_url']='https://www.safeworkshop.org/cvpr-2026/ ; https://www.iosb.fraunhofer.de/en/projects-and-products/realorrender-deepfake-detection-explainable-ai.html ; CVF PDF link currently listed by Scholar but returns 404: https://openaccess.thecvf.com/content/CVPR2026W/SAFE/papers/Specker_A_Hybrid_CLIP-Diffusion_Architecture_for_Transparent_Deepfake_Detection_and_Explainability_Evaluation_CVPRW_2026_paper.pdf'
row['screen_basis']='SIDA Cited-by位置225/225已在74逐条登记；SAFE Workshop页面核实作者、会议与页码，Fraunhofer IOSB项目页只支持系统采用attribution/segment-based解释及其自述评估。未取得论文正文；不把项目介绍当成论文实验结果。'
write('90_本轮新增强相关候选与引文复核.csv',candidates)

priority=read('72_V2已复核强相关优先清单.csv')
if not any(r['title']==TITLE for r in priority):
    priority.append({
      'rank':'11.5','title':TITLE,
      'url':'https://openaccess.thecvf.com/content/CVPR2026W/SAFE/papers/Specker_A_Hybrid_CLIP-Diffusion_Architecture_for_Transparent_Deepfake_Detection_and_Explainability_Evaluation_CVPRW_2026_paper.pdf',
      'V2_relation':'图像深伪检测解释评价直接核心；来自SIDA前向引用链。',
      'original_reading_scope':'SAFE Workshop元数据和Fraunhofer IOSB项目说明已核；Scholar所示CVF PDF链接当前404，未能读取论文全文。',
      'limitations':'项目宣传页不提供解释评价协议、faithfulness操作化或论文实验细节；不能据此判定为已证实的faithfulness研究。',
      'reassessment':'高优先全文待核，暂排在rank 11 DDL之后、早期Anchors工具之前；必须取得CVPRW论文正文后再判断其解释可靠性证据。'
    })
    priority.sort(key=lambda r: float(r['rank']))
write('72_V2已复核强相关优先清单.csv',priority)
