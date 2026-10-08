# 图像鉴伪解释可靠性：V2.1检索方案（2026-10-08）

本方案替代无统一优先级的旧扩词翻页流程。研究问题：图像/含图像的媒体真实性鉴别中，解释所述证据是否真实、是否对应模型判决、是否稳定，以及能否帮助人类正确使用鉴伪工具。覆盖传统篡改、整幅生成、局部编辑、人脸伪造；文档、医学和遥感作为扩展任务。纯音频、纯文本假新闻、一般医疗诊断、生成质量审美不计直接相关；视觉/多模态鉴伪中的解释评价可以纳入。不限级别和文献类型；预印本、学位论文与正式论文分别标注；全文不可得保留待核，不作无关排除。

## 检索的逻辑

任务T、解释E、可靠性R分开建词表，不能把deepfake作为必需条件，也不能把T AND E AND R作为唯一入口。15任务族分别执行；同族OR，族间隐式AND。无NOT，避免误删跨任务论文。107式为15任务族×7检索分支加2方法补充，不代表全体可能词组合，也不保证数据库覆盖全领域。

T：image forgery/tampering、image manipulation/editing、splicing/compositing、copy-move、AI-generated image、synthetic/generated image、GAN-generated、diffusion-generated、image forensics/authenticity、media/multimedia forensics、deepfake/face forgery/facial manipulation、inpainting/retouching、document image/forgery、medical image/CT volume、satellite/remote sensing image。

E：explanation、explainable、interpretability、interpretable、attribution、saliency、rationale、reasoning。别名还需由原稿和引文迭代；XAI、CAM/Grad-CAM、LIME、SHAP、attention、concept bottleneck、prototype及自然语言解释作为方法追查词，不能因没写explanation排除。

F1：明确解释忠实性/保真/可靠性短语。F2：接地、幻觉、证据一致性。F3：人类评价、正确依赖、信任校准、解释稳定性。F4：合理性检查、参数随机化、对抗评测、删除/插入。F5：因果忠实、证据充分/必要、解释完整性、捷径依赖。B1：T AND E AND 鉴伪任务动作，不强制R；B2：T AND R AND 鉴伪任务动作，不强制E。另补量化解释质量与信号域批评，避免词表围绕新MLLM文献过拟合。

## 可行性验证与修正

所有107式已在实际Google Scholar UI输入并保存首页语法、估计规模、题名、来源、下一页和时间。页面实际query须与请求相同；一次读到旧查询的记录无效，已重测并保留错误。初始宽词式2.82万、synthetic宽式3.03万不作为细查入口；医学/遥感/GAN的混入据实际题录增加任务/视觉限定。但限定后仍可能是参考文献命中，必须从摘要/正文筛。

8个自选已知锚点回检通过：EFR、2022 BMVC量化评价、2024对抗量化评价、Gowrisankar解释评测效度、Beyond Accuracy、SNIPPET、空间域解释批评、HexMIL。原105式首页没回检到BMVC和空间域批评，补2方法分支才检出，保留这次真实漏检诊断。8/8不是总体召回率；其他未知文献仍可能遗漏。107式的首页语法/规模测试通过，不等于107式所有分页或领域穷尽完成。每个试检位置都在69，规则初筛与人工原稿核查明确区分。

## 执行顺序与显示上限

先F1/F5等最小规模细检索，随后F2/F3/F4；各组内先有明确评价终点和少量结果的路线。再B1/B2宽检索，最后反向参考、前向引用和版本。≥900估计结果的裸查询不直接翻100页当穷尽；先拆同族别名、解释子词与发表年份，逐子查询再次测规模，仍过大则细分年份。标题限定查询可作先行高精度补查，但不得替代全文关键词查询。原查询及失败、空尾页、索引数变化均保留；真实末页无Next才记可见结束，受阻/未加载不算零命中。

每位置记录请求式、实际式、页码/位置、标题/作者年/URL、筛选理由和证据范围。逐篇筛选先题名摘要，再相关原稿；检测准确率/泛化/定位IoU、热图外观/跨方法一致性、因果忠实、解释事实接地、人类依赖效用各自标注，不能混为一个可靠性指标。同行评审与年份不作为主题相关性的替代。强相关分两类：直接讨论或评价解释可靠性；为该问题提供核心解释/证据机制。仅报告准确率、展示热图的论文不自动成为直接可靠性证据。

## 时间范围

“2024才出现”不成立。Baldassarre等2022-10-07预印本、BMVC2022接收声明已经明确提出解释量化评价；Gowrisankar等2023-12-08预印本质疑删除/插入协议，2024出版。更早2013 Fontani是取证工具可靠性/证据融合基础，不直接当现代XAI忠实性实验。上述说明至少2022已存在直接研究，不是断言2022是领域第一篇。初查不设年份下限，现代直接研究与更早历史探索分开：较早年份优先定向评价词及参考链，避免大量无关老文献翻页；不能以2024新兴MLLM子方向替代整个选题起点。

来源：[BMVC2022作者预印本](https://arxiv.org/abs/2210.03683)、[2023解释评测效度预印本](https://arxiv.org/abs/2312.06627)、[2013机构记录](https://iris.polito.it/handle/11583/2506327)。

## 旧目录重审与交付

旧82篇全部进入68重审队列，旧55标签不继承为V2最终计数。本轮先按已有原页证据复评8篇的主题与评价边界（72），没有冒称重新全文读完82篇。其余74篇和英文候选继续按本协议筛；已有原文与逐位置日志保留，不删除证据。最终交付相关性排序、每篇评价对象与指标/证据等级、版本去重、完整筛选日志及覆盖缺口。任何一批完成只报该批状态，不能把检索量当完成度。

首批执行：T12-F1两位置、T13-F1六位置、T03-F1七位置、T04-F1十一位置，共26位置，完整可见分页/逐位置题录初筛见73。MDPI拼接解释候选原页Web429，未记正文取得。原105式第一轮与补方法试验不是完备性证明，48式估计≥900必须拆分再执行。

交付文件：

- [67_检索方案V2_完整查询矩阵.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/67_检索方案V2_完整查询矩阵.csv)
- [68_既有82篇核心_V2逐篇重审队列.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/68_既有82篇核心_V2逐篇重审队列.csv)
- [69_V2试检全部结果位置初筛.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/69_V2试检全部结果位置初筛.csv)
- [70_V2检索式验证与锚点回检.json](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/70_V2检索式验证与锚点回检.json)
- [72_V2已复核强相关优先清单.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/72_V2已复核强相关优先清单.csv)
- [73_V2首批细检索全部26位置筛选.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/73_V2首批细检索全部26位置筛选.csv)
