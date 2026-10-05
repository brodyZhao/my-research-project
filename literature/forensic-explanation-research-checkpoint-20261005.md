# 解释可靠性文献重检：2026-10-06阶段索引（沿用2026-10-05输出路径）

用户要求使用Google Scholar扩大重检，逐结果位置记录筛选，并排查强相关种子的引用链。旧337条目录遗漏EFR，不作为完整检索或继承验证状态。

本阶段仍未完成。已执行50条Scholar路线，48条观察到可见终页；正常范围8653个结果位置、遗留过滤15个位置，共8668条逐条日志。这些位置包含重复、无关和待判条目，不等于相关论文篇数；规则辅助初筛不冒充人工全文审读。候选目录6557条包含噪声，旧337条中191条在本轮主题/引用链已重新匹配。

用户完成验证后，GS030事实性6页59位置、GS020广义splicing83页827位置已到可见终页。后续完成可验证性31页304位置、概念瓶颈4页40位置、原型忠实性9页89位置、信任校准5页49位置、不确定性34页337位置、合成图像检测缺陷10页94位置、文档解释21页208位置及医学深伪6页52位置。GS045中文忠实性已记录310个位置，当前第33页已到可见终页，存在索引变动风险，实际末页/断点https://scholar.google.com/scholar?start=320&q=%E5%9B%BE%E5%83%8F%E9%89%B4%E4%BC%AA+%E8%A7%A3%E9%87%8A+%E5%BF%A0%E5%AE%9E%E6%80%A7&hl=zh-CN&as_sdt=0,5。估计数1680→272且出现非十步分页，不能当作完整索引覆盖。GS007原100页993位置已有两个年份分段补查，仍保留无年份与索引边界风险。

EFR全部56条参考文献逐条排查并取得原页/作者稿；非56篇全部全文质量评审。其当前被引用列表1条已查完。另11种子620参考位置已提取初筛，新加Beyond Accuracy 33条、Escalate 15条及中文SE-EffGNN 32条逐条初筛；未完成全部被引原文及核心前向链。

当前40篇原页复核核心文献按相关性排序，核查范围逐篇明确。本阶段新增Beyond Accuracy、CLIP Predictive Cues、Escalate、PIVOT、人机肖像校准、SEED、MIC与中文SE-EffGNN正式PDF。中文论文重点§2.3.2–2.3.4以AUC/ACC和内部可视化作评价，不能当独立解释忠实性验证；全部32参考另表。TV平滑度、概念相关性、检测准确率、模型裁判偏好及立场文章愿景均不能直接当作解释因果忠实性证明。

检索失败也保留：GS037弯撇号题名宽匹配已由GS038完整特征题名替代，首10位置不丢弃；Ramaswamy/Chockler论文实际题名含the，GS040近似精确短语零命中，GS041第2页及GS042正确完整题名成功确认。SSRN原稿Web403、正常浏览器停安全验证；仅人工Scholar复核，不冒充原稿已核验。SSRN按论文abstract_id去重，修正小词/题名版本重复。

2052条原页获取尝试保留成功、空响应与失败；成功浏览器核验不会覆盖之前失败的PDF尝试。完整原稿和页面文字只在work，outputs不再分发全文；Git仅跟踪索引与交接。

本地交付入口：

- [00_重检阶段报告_未完成.md](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/00_重检阶段报告_未完成.md)
- [12_原页复核核心文献_按相关性排序.md](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/12_原页复核核心文献_按相关性排序.md)
- [02_谷歌学术全部结果逐条筛选.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/02_谷歌学术全部结果逐条筛选.csv)
- [03_EFR全部56条参考文献逐篇排查.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/03_EFR全部56条参考文献逐篇排查.csv)
- [04_重检候选目录_暂按相关性排列.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/04_重检候选目录_暂按相关性排列.csv)
- [09_强相关种子620个参考文献位置初筛.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/09_强相关种子620个参考文献位置初筛.csv)
- [19_BeyondAccuracy全部33条参考文献初筛.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/19_BeyondAccuracy全部33条参考文献初筛.csv)
- [20_Escalate全部15条参考文献初筛.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/20_Escalate全部15条参考文献初筛.csv)
- [21_SEEffGNN全部32条参考文献初筛.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/21_SEEffGNN全部32条参考文献初筛.csv)
- [22_检索词覆盖审计_实际与未执行.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/22_检索词覆盖审计_实际与未执行.csv)
- [05_检索路线覆盖与终页核对.json](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/05_检索路线覆盖与终页核对.json)
- [17_文件与覆盖一致性检查.json](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/17_文件与覆盖一致性检查.json)

验证：逐位置与各引用表计数、EFR56证据SHA256、新种子33/15/32列表SHA256、CSV读回、页码连续、受限页非终页、身份ID唯一与核心排名连续通过；这些是文件/覆盖一致性检查，不证明召回率或零遗漏。检索脚本compileall及git diff --check另行执行。

仍须从GS050≤2015分段第2页验证断点继续，复核GS045/GS049索引变动、其他未执行术语、强相关核心前向/后向链、未取得原稿与版本核查。没有开始研究方案或模型实验。


GS049「图像鉴伪 解释 忠实性 [年份≥2016；GS045索引异常补查]」记录260个位置，当前第27页已到可见终页，存在索引变动风险。[实际断点/末页](https://scholar.google.com/scholar?start=260&q=%E5%9B%BE%E5%83%8F%E9%89%B4%E4%BC%AA+%E8%A7%A3%E9%87%8A+%E5%BF%A0%E5%AE%9E%E6%80%A7&hl=zh-CN&as_sdt=0,5&as_ylo=2016)。GS050「图像鉴伪 解释 忠实性 [年份≤2015；GS045索引异常补查]」记录10个位置，当前第2页需要用户手动完成Google人机验证，已发恢复提示。[实际断点/末页](https://scholar.google.com/scholar?start=10&q=%E5%9B%BE%E5%83%8F%E9%89%B4%E4%BC%AA+%E8%A7%A3%E9%87%8A+%E5%BF%A0%E5%AE%9E%E6%80%A7&hl=zh-CN&as_sdt=0,5&as_yhi=2015)。 GS045估计1680→272、GS049估计654→138，出现空尾页；互补年份不是总体年份排除。中文年份分段相对宽查询新增138个题名位置另见23号CSV，不当相关独立论文数量。

本轮另核DDL（TIFS2025方法，区别同缩写数据集）的保存出版社公开摘要与DOI题录；正文fidelity指标/公平扰动协议待核，IEEE刷新418保留。注册52个参考位置已逐条初筛，原稿完整性仍待核；40次被引DOI题录请求38成功/2失败保留，Crossref题录不当全文。Pinhasov论文新增方法复核：XAI图用于攻击检测、还测试保持图接近的攻击，主要攻击检测终点不充分证明原检测器解释因果忠实。

48条可见终页中，1条有显示上限风险、2条有索引变动风险；无这两类已观察风险的可见终页为45条。这不保证其他路线没有未观察到的遗漏。DDL缓存复核不算新获取，40次被引DOI题录另表，不混计原稿全文获取。

- [23_中文索引异常年份补查_新题名位置初筛.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/23_中文索引异常年份补查_新题名位置初筛.csv)
- [24_DDL注册参考52个位置初筛_原稿完整性待核.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/24_DDL注册参考52个位置初筛_原稿完整性待核.csv)
- [25_DDL被引DOI题录获取40次审计.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/25_DDL被引DOI题录获取40次审计.csv)
