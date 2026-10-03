# 图像鉴伪解释可靠性文献检索：2026-10-04

分支：`codex/forensic-explanation-literature`。实际使用Google Scholar，26条路线、66页、636个含重复的可见列表位置。主表251条（题名与作者核验240条），扩展候选86条。包含方法基础、综述和边界研究；没有证明零遗漏或完成逐篇全文系统综述。

完整本地交付位于`outputs/图像鉴伪解释可靠性文献检索_2026-10-04/`，该目录依仓库规则被Git忽略，不随push上传。包含详细报告、主表CSV、候选清单、已核验BibTeX、Scholar页次日志和核验审计。生成及核验脚本在本地`work/literature_search_20261004/`，同样不上传。

## 首要阅读入口

- [An adversarial attack approach for eXplainable AI evaluation on deepfake detection models](https://doi.org/10.1016/j.cose.2023.103684)：直接检验鉴伪解释评估：常见插入/删除干预可能产生额外伪造线索；提出更贴合鉴伪任务的对抗式评估。2023预印本、2024正式卷期。
- [Towards Quantitative Evaluation of Explainable AI Methods for Deepfake Detection](https://doi.org/10.1145/3643491.3660292)：直接定量比较深度伪造解释方法；对解释所选区域施加攻击并观察检测变化。方法排名仅适用于论文的检测器、数据与干预设定。
- [Improving the Perturbation-Based Explanation of Deepfake Detectors Through the Use of Adversarially-Generated Samples](https://doi.org/10.1109/wacvw65960.2025.00080)：用对抗生成样本改进扰动式鉴伪解释；与2024定量评估论文相关，但属于独立方法论文。
- [Explaining AI-Image Detection: What the Heatmap Actually Shows](https://arxiv.org/abs/2607.29581)：直接讨论AI图像检测显著图的实际含义；优先复核原文。
- [Explainable Artificial Intelligence for Deepfake Detection: Pipeline, Open Source and Comparisons](https://onlinelibrary.wiley.com/doi/10.1111/exsy.70222)：比较16种解释方法，考察正确性、完整性与连续性等多个维度；结果依赖检测器、数据及评价设置。
- [JECA^2: Judgment-Explanation Consistent Adversarial Attack against Forensic Vision-Language Models](https://arxiv.org/abs/2605.28609)：针对取证视觉语言模型的判断与解释一致攻击，直接关联解释被操控的可靠性。
- [Unveiling Perceptual Artifacts: A Fine-Grained Benchmark for Interpretable AI-Generated Image Detection](https://openreview.net/forum?id=Tk8ujiOgHM)：X-AIGD提供分层感知伪影与像素标注，用于解释对齐；与人工区域对齐不能单独证明因果依赖。
- [Defake-o3: From Speculative Rationales to Verifiable Evidence for Explainable AIGI Detection](https://arxiv.org/abs/2608.16259)：GroundFake提供经人工核验的局部伪影证据，使用证据验证器奖励优化推理；与可验证解释训练高度相关，仍需独立干预验证因果忠实性。
- [EditSleuth: A Dataset of Grounded Reasoning Chains for Image-Edit Forensics](https://arxiv.org/abs/2605.08695)：图像编辑取证的接地推理链数据集，直接关联证据可追踪性。
- [SNIPPET: A Framework for Subjective Evaluation of Visual Explanations Applied to DeepFake Detection](https://doi.org/10.1145/3665248)：主观视觉解释评价框架，包含深度伪造任务。用户或专家评价不能单独证明模型因果忠实性。
- [TriDF: Evaluating Perception, Detection, and Hallucination for Interpretable DeepFake Detection](https://openaccess.thecvf.com/content/CVPR2026/html/Jiang-Lin_TriDF_Evaluating_Perception_Detection_and_Hallucination_for_Interpretable_DeepFake_Detection_CVPR_2026_paper.html)：分开评价感知、检测与解释幻觉；包含图像、视频和音频，应提取视觉子任务。
- [Faithfulness Under the Distribution: A New Look at Attribution Evaluation](https://proceedings.iclr.cc/paper_files/paper/2026/hash/409fcc9d24b549969b8b9be68b56a7be-Abstract-Conference.html)：FUD用扩散重建缓解像素删除的分布外偏移，评价归因忠实性；一般视觉分类实证，迁移到鉴伪须验证重建是否改变伪造标签。
- [Truthful or Fabricated? Using Causal Attribution to Mitigate Reward Hacking in Explanations](https://proceedings.iclr.cc/paper_files/paper/2026/hash/d4b892df8bec8e13925f57649fbae039-Abstract-Conference.html)：语言模型解释与偏好优化中的奖励投机研究，使用因果归因评价/改进解释；不是视觉鉴伪实证，可迁移其评价和奖励设计思路。

## 已翻至终页的具体路线

- Gowrisankar与Thing核心评估论文的可见引用链：5页45个位置。
- Tsigos等定量评估论文的可见引用链：5页49个位置。
- `"image forgery" "faithfulness"`：8页76个位置，终页无下一页。
- `"AI-generated image" "explanation" "faithfulness"`：10页94个位置，终页无下一页。

多数宽查询只访问1–5页。未完成所有种子的前后向引用追踪，也没有穷尽中文数据库、学位论文或全部PDF。上述四个终页记录不能扩展为整个领域检索完成。

## 必须保持的区分

人工伪影标注对齐、用户觉得解释合理、模型裁判高分、分类准确率，以及解释对决策的因果忠实性属于不同证据。JPEG工具保证有管线和计算假设。FUD是一般归因评价；Truthful or Fabricated与DEPO是可迁移语言/医学方法，不能写成已有鉴伪实证。
