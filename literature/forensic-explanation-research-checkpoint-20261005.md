# 解释可靠性文献重检：2026-10-07阶段索引

用户要求Google Scholar扩大重检、逐结果位置记录筛选、排查EFR与强相关引用链。英文优先，中文低相关不计入相关阅读目录，已有日志保留。旧337条遗漏EFR，不继承旧验证或作为完整目录。

重检仍未完成。现有69条无异常过滤的Scholar路线，66条观察到可见终页；正常范围10819位置，另保留25个遗留引文过滤位置，共10844条日志。位置含重复/无关/待核，不当相关论文数量。候选7763条含噪声，旧目录本轮重匹配207条。

人工原页核查核心64篇，英文63篇（其中1篇通用迁移基础另标），每篇注明摘要/选定正文核查范围，非全部全文质量审评。EFR按相关性列首；相关性排序不等于证据质量排名。英文待人工候选333条、可迁移方法候选223条，不计已核相关论文。

33术语族已有代表性直接主题查询，不能当整体召回率或穷尽全部词组合。GS051篡改忠实性261位置、GS052元评估18、GS053人类评价415、GS054对抗攻击327、GS055用户信任140、GS058信任校准136到可见终页。GS054/55估计大幅变动，GS056≤2025和GS057≥2026补查170/140位置仍有索引风险，不把无Next等同无遗漏。

GS050中文≤2015第2页已恢复，20位置保留；依用户指示降低后续宽中文噪声翻页优先级，不作查完。用户确认后核GS070，实际仍显示Google人机验证，单次重新加载后也未显示结果；已请求看到结果后恢复，其他位置不变。GS037弯撇号题名歧义用GS038替代；GS040缺the的近似题名零命中用GS041/42纠正。GS060缩写查询出现遗留引文参数，异常位置保留，以无过滤GS061完整SNIPPET题名替代；前向GS062另记录。

EFR56参考位置已逐条排查并获取原页或公开作者稿，非全部全文质量评审。其他11种子620，Beyond33、Escalate15、SE-EffGNN32、DDL注册52、SGEVL15、FKG90、EAI141、Mansoor24、SNIPPET66、Cooper50参考位置初筛另表。不是这些数相加等于独立相关论文；全部被引原稿未读完。DDL52为注册列表，原稿完整性待核。前向EFR1、对抗解释评价GS05946、SNIPPET GS06212位置已到可见终页。

Wiley安全验证已恢复：核EAI正式五作者题录、公开摘要、全部141公开参考；正文仍需订阅，没有声称全文指标已核。XPlainVerse公开50页作者PDF与SNIPPET30页含封面接受稿正常TLS取得，正文指标/人类协议已读。XPlainVerse人工重叠集为10例而非100；Entity/Evidence为文本参考匹配，不是因果忠实。SNIPPET人工重合/偏好亦非模型因果真值。Cooper公开查看器7页已读，预设建议不是真实鉴伪模型。

新增ForenX/FakeXplained/AIFo/ForgeryGPT/AIGI-Holmes/鉴伪RewardBench原稿评价范围核查。RewardBench98.3%人工一致率为明确胜者子集，完整四分类68%；分类指标不混用。ForgeryGPT5人全伪图前后判断不当错误依赖校准。文字合理性、IoU、模型裁判/偏好与代理共识均不自动当因果忠实。ForenX部分提示检测大幅下降保留；强相关引用链未全部补齐。新核Look Before You Judge方法/指标/限制及完整38参考位置（39表）；其CHAIR/Hal包含空解释/漏检惩罚、分类表外主张丢弃，不能作纯解释幻觉率。DFP-Net官方接受列表题录已核，全文协议待核。ForenX前向6、RewardBench前向1位置已查。

英文解释裁判GS067估计622→213，仅190实际位置后空尾页；互补GS068≥2026到201、GS069≤2025到90位置，全部保留索引变动风险。37表记录相对宽查询的新题名位置，不当新增独立相关论文。英文检索没有总体年份排除。SSRN6811534题录/摘要已恢复并核2作者、2026-05-22、DOI与41页注记，公开关联41参考初筛见38；PDF下载未返回文件、浏览入口回题录、Web403，正文仍待核。Google Scholar GS070当前仍需人机验证；用户确认后一次重载仍无论文结果，不能记零命中或终页。

2116条原页/主DOI题录获取尝试记录成功/空/失败；不等于唯一原稿数量，DDL被引40次题录另表。完整网页和原稿仅work，输出为题录/筛选/哈希；Git仅索引和交接。

当前未决路线：GS007, GS037, GS045, GS049, GS050, GS054, GS055, GS056, GS057, GS067, GS068, GS069, GS070。显示上限风险：GS007；索引变动风险：GS045, GS049, GS054, GS055, GS056, GS057, GS067, GS068, GS069。完整候选原稿、强相关前后向链与版本归并继续核查；没有开始研究方案/模型实验。

本地交付入口：

- [00_重检阶段报告_未完成.md](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/00_重检阶段报告_未完成.md)
- [27_英文原页复核核心_按相关性排序.md](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/27_英文原页复核核心_按相关性排序.md)
- [02_谷歌学术全部结果逐条筛选.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/02_谷歌学术全部结果逐条筛选.csv)
- [03_EFR全部56条参考文献逐篇排查.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/03_EFR全部56条参考文献逐篇排查.csv)
- [04_重检候选目录_暂按相关性排列.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/04_重检候选目录_暂按相关性排列.csv)
- [22_检索词覆盖审计_实际与未执行.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/22_检索词覆盖审计_实际与未执行.csv)
- [29_英文解释可靠性候选_待人工复核.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/29_英文解释可靠性候选_待人工复核.csv)
- [35_SNIPPET全部66条参考文献初筛.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/35_SNIPPET全部66条参考文献初筛.csv)
- [36_Cooper全部50个参考位置初筛.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/36_Cooper全部50个参考位置初筛.csv)
- [37_英文索引异常年份补查_新题名位置审计.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/37_英文索引异常年份补查_新题名位置审计.csv)
- [38_SSRN空间域解释公开关联41参考位置_原稿完整性待核.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/38_SSRN空间域解释公开关联41参考位置_原稿完整性待核.csv)
- [39_LookBeforeYouJudge全部38条参考文献初筛.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/39_LookBeforeYouJudge全部38条参考文献初筛.csv)
- [05_检索路线覆盖与终页核对.json](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/05_检索路线覆盖与终页核对.json)
- [17_文件与覆盖一致性检查.json](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/17_文件与覆盖一致性检查.json)

验证：逐位置ID/理由、EFR56证据SHA、各参考表计数与SHA、CSV读回、核心连续排序、过滤/验证非正常终页通过。修复压缩日志同页引用即时缓存，现导出零解析失败；原始观察均保留。这些检查不证明零遗漏。ZIP与compileall在阶段保存时另核。
