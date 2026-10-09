# 2026-10-09 T11-F2-S2 扩展分页续查（第32页验证阻断，仍未完成）

- 仓库 `brodyZhao/my-research-project`；分支 `codex/forensic-explanation-literature`；上次已推送检查点commit `e8acb06 docs: record Scholar search checkpoint`，本轮完成后会更新交接并推送。只更新忽略目录下检索记录与handoff，不改业务源码；用户原有两个未跟踪文件保持未修改、未暂存。
- Google Scholar路线 `T11-F2-S2` 查询式：`(deepfake OR "face forgery" OR "facial manipulation") (explanation OR explainable OR interpretability OR interpretable OR attribution OR saliency OR rationale OR reasoning) (hallucination)`。恢复后核第30页`start=290`正常，继续第31页`start=300`并逐项筛录位置301–310；点击第32页后`start=310`被Google异常流量页拦截，未把阻断页当空结果/末页。当前等待用户恢复；恢复后从`start=310`续查。
- 全局逐位置主表`74_V2完整分页逐位置初筛.csv`现21,222个位置观察，result_id唯一、筛选理由齐全；`90_本轮新增强相关候选与引文复核.csv`296条候选观察；`72_V2已复核强相关优先清单.csv`159个有序条目（临时序列，非最终统一相关性排序）。这些数都不是独立论文数或最终纳入数。第31页的FakeScope、Show Me the Work等是目录已有论文，明确标记复用旧核查，不重复阅读全文；新增《The age of synthetic realities》已核作者arXiv HTML §7.1.3：明确陈述深伪图像检测不够可解释、需提供理由，属于早期领域缺口背景/引文枢纽；没有解释忠实性或人因依赖测量。其紧邻引用[241][242]是检测/泛化论文，不应误认作解释可靠性证据。
- 第31页还排除了通用元宇宙、指纹识别威胁、音频深伪、影响策略、远程脉搏、GeoAI、CLIP检索幻觉及纯检测模型，理由均逐条记录在`145_T11-F2-S2_deepfake_hallucination_第31页逐位置筛选.csv`。该宽式仍高噪声；Scholar估算约4,790不代表有效文献数或覆盖完备。全局`complete=false`，多个主题子式/引用链及去重全文筛选仍未完成，不承诺零遗漏。
- 输出目录中检索账本被`.gitignore`忽略，不会因push HANDOFF而自动入Git；阶段ZIP须同步更新，用户可从本地`outputs/`查看。`83`审计已记当前受阻断点，`87`路线表记第31页310位置和下一步start=310。
- 建议下一步：用户恢复后继续`start=310`；每页先用题名去重旧目录，只对新强相关候选做原稿/引文审查；阶段性复建压缩包、做唯一ID/空理由/状态一致性和CRC校验；再交接并推送。
# 2026-10-09 Scholar恢复复核与EFR效度边界续查（仍未完成）

- 仓库 `brodyZhao/my-research-project`；分支 `codex/forensic-explanation-literature`；交接前HEAD `51d420204813d30f52b9366722b27827184417d8`。输出日志在忽略目录 `outputs/图像鉴伪解释可靠性_重检_2026-10-05/`，阶段归档 `outputs/图像鉴伪解释可靠性_重检阶段结果_2026-10-09.zip`。
- 用户回复“已恢复”后，Google Scholar V109（含 `evaluation` 的宽式）start=460正常显示第47页、估计约20,900条。沿页面可见“下一页”到start=470时，Google再显示异常流量/验证页；新断点已写入83审计及87路线表。没有将受限页记作空结果。V110（不含evaluation的宽式）start=720仍是另一个受限断点，本轮没有证据证明解除。全局可见逐位置账仍20,375条，唯一文献数未据此估算，审计 `complete=false`。
- 新一轮一手全文复核进一步细化EFR(arXiv:2608.08009v1 / ACM MM 2026)：§3.2.2说明50K训练理由由已知GT的MLLM生成，经规则、独立MLLM审核和标记样本人工检查；§3.3.1以坐标/文本范围重叠和内部一致性为可验证奖励；§4.4只在正确预测的被篡改样本上报告NLI entailment、redundancy、ROUGE-L和Distinct指标。它是本题强相关的证据接地/一致性方法论文；这些结果不能单独证明自然场景解释事实准确、解释因果忠实，也没有报告用户解释判断或人因信赖校准。详细原文记录已在现有90/72条目中；原文来源 https://arxiv.org/html/2608.08009 。沿EFR引文链追溯TriDF (arXiv:2512.10652v3)并补读全文：50+标注者、每个fake样本至少3人多数表决；用人工伪迹标签评估解释Cover/CHAIR/Hal/F0.5。但自由文本映射仍由外部LLM执行，漏判fake直接使CHAIR=1，需注意映射可靠性及检测/解释构念混合；已更新72/90/100。原文 https://arxiv.org/html/2512.10652v3 。
- 当前整理文件计数：72优先候选78行（暂定相关性次序，尚需全目录统一重排）；90新增候选与引文复核215行；100全文/效度边界复核17篇；102 So-Fake参考位置9条；103 ForgeryGPT参考文献位置1–61连续、逐项标题/引用语境筛查（不是61篇全部全文核读）。
- 本次无源代码改动。阶段ZIP已重建，336个成员CRC校验通过；关键CSV计数/连续性、V109未完成状态与全局complete=false断言通过；`python3 -m compileall -q work/search_protocol_v2`和`git diff --check`通过。提交时只暂存HANDOFF，不触碰原有两个未跟踪用户文件。远端origin已配置，按仓库规则推送交接提交。
- 未完成：Scholar V109 start=470、V110 start=720及其他未跑/受限拆分；最终全候选去重与统一排序；EFR和其他种子论文的前向/后向引文原稿复核；严禁称“一个不漏”或宣称领域穷尽。待用户恢复V109后从start=470续页；独立可做的原稿核查可并行继续。

# 2026-10-09 So-Fake 引文链全文复核续查（仍未完成）

- 仓库 `brodyZhao/my-research-project`；分支 `codex/forensic-explanation-literature`；阶段开始时HEAD `2128384`，首次交接提交 `e9cd79c2301ede0771c1d989eb12468851e8db31`；本轮交接再提交后以 `git rev-parse HEAD` 为最终HEAD。本轮不改业务源码；原有两个未跟踪文件保持原样且未暂存。检索记录位于忽略目录 `outputs/图像鉴伪解释可靠性_重检_2026-10-05/`，交付快照重建于 `outputs/图像鉴伪解释可靠性_重检阶段结果_2026-10-09.zip`。
- 用户回复“已恢复”后，可见 IAB Scholar 标签为 V109 主题式第47页（start=460），显示约20,900结果且有正常的十条题录和分页；该路线在既有日志中已到start=990并直接核过start=1000空页，本轮不重复记位置。Chrome扩展标签清单中 V110宽式start=720此前仍为reCAPTCHA；本轮辅助权限初始化两次未完成，不能重新读取该标签，也不能将V109已恢复解释为V110已恢复。83审计已区分两条路线；如果用户后续恢复的是V110，应先独立核start=720再续。
- 沿So-Fake v5参考表逐条继续全文核验：Common Sense Reasoning for Deepfake Detection（arXiv:2402.00126）全文确认2,968图、14,782问答、每图3人标注及至少2人一致的真假标签；答案生成主要用BLEU/CIDEr/ROUGE/METEOR/SPICE。尚无独立生成理由事实性盲评/决策干预，不能由检测和文本相似度推出faithfulness。与A Hitchhiker’s Guide (arXiv:2410.00485)分开记录。FFAA(arXiv:2408.10072)全文核查：ACC/AUC/sACC主要衡量检测跨域表现/稳定性，没有独立解释忠实性终点。FakeScope(arXiv:2503.24267)全文确认30位受训专家参与证据类别标注、每图双标后取交集、50假+50真人工解释示例及6位标注者对100图进行2AFC偏好（ACoTI 99.17%）；作者明确声明rationale为post-hoc、不代表真实因果决策依据，提示亦输入GT标签/人类证据类别。偏好不是视觉claim支持率或因果faithfulness。ForgeryGPT(arXiv:2410.10238v4)全文补核§IV-E：100张伪造图、5人看解释前后评真假与信心；原先误判真的图中81%看后改判假、已判假的样本信心增加65%。仅假样本且无无解释/真样本条件，直接支持“说服影响”候选，不证明appropriate reliance或解释faithfulness。
- `102_SoFake解释相关引文逐条初筛.csv`现仍9个reference位置，更新三篇逐条全文筛查结果，并更正ForgeryGPT错误arXiv编号为2410.10238（官方arXiv题录v1 2024-10-14、v4 2026-04-07）；其IEEE正式页机器人验证，卷期页不猜填；FakeShield一手源改为arXiv。`100_V110新候选全文核读与效度边界.csv`现14篇全文记录。`90_本轮新增强相关候选与引文复核.csv`214条候选观察，更新FakeScope、FFAA和Specialist-Generalist证据。`72_V2已复核强相关优先清单.csv`增补Specialist-Generalist和FakeScope两个候选，ForgeryGPT重排到暂定第14位，现77行；`103_ForgeryGPT全部61条参考文献逐条初筛.csv`按原稿参考位置1–61逐项标题/引用语境初筛，其中相关方法/通用幻觉评估来源和数据集已分层，尚非全部被引全文核验；排名仍是增补中的暂定相关性顺序，尚未按所有候选统一重排，不能作为最终排序。
- 本轮未增加Google Scholar逐位置数；主位置总账仍20,375行，独立文献数仍未从位置估算。全局 `complete=false`；剩余工作包括V110分页（720起点待验证）、宽子查询待试、去重/版本映射、所有优先强相关论文全文边界统一复核、EFR及其他种子双向递归引用链。不能承诺“一个不漏”。
- 验证：`work/search_protocol_v2` 可运行编译；阶段ZIP重建含335个成员，`ZipFile.testzip()`通过；本轮后应重建ZIP并复跑CSV连续性/关键字段校验、`python3 -m compileall -q work/search_protocol_v2`与`git diff --check`。本轮没有代码或模型改动，不需tensor/推理测试。
- 建议 ChatGPT Web 下一步：V110若已由用户恢复，先确认宽式start=720正常页并逐位置筛；若仍受限，沿FakeScope的FakeBench/FakeClue等引文链追查解释证据支持/评测终点，同时开始全表按“任务匹配/解释事实性/决策忠实度/人因依赖”四类统一重排。

# 2026-10-09 图像鉴伪解释可靠性重检续查（未完成）

- 仓库 `brodyZhao/my-research-project`；分支 `codex/forensic-explanation-literature`；本阶段检索检查点提交 `cd413b9`；当前HEAD还包含随后提交的HANDOFF哈希记录。工作区原有两个未跟踪文件 `faithfulness_pilot_EXPERIMENT_LOG_2026-09-27.md` 和 `literature/forensic-explanation-relevance-20261004.md` 未改动、未暂存。
- 继续检查用户所给 `"image forgery" "human evaluation" explanation` 断点：此前记录覆盖活动可见位置1–106；本轮复核start=80/90/100与start=106空页，未发现新题录，末页仍Next禁用。Google Chrome实际当前标签是Google Scholar异常流量/验证页（不是正常结果页），没有将其记成零结果或完成；本阶段转向可读的一手论文页面继续核对。
- 原先总账 `74_V2完整分页逐位置初筛.csv` 现有18,656条位置观察，result_id唯一且筛选理由无空值；这些不是独立文献数。重算审计 `83`：107主路线，59条记录到可见末页；主路线13,941位置，149个拆分计划条目/路线当前交叉命中4,625位置、其中68可见末页且55标记覆盖完成；82条ForensicChat前向引用位置；另有90条不属于当前主/细分计划的题名或引用补充记录。全局 `complete=false`，去重、未试检拆分路线、全文和递归引文仍未结束。计数口径区分已写入83审计文件。
- 更新PRPO原稿核验 `137_PRPO原稿解释可靠性与人评效度复核.csv`：确认ICML 2026正式出版（PMLR 306:92466–92496）；作者v3有8名评审、每人5张图、CAC/EGIA/RQ/CC/CU五项评分。该人评能支撑解释质量/证据接地，但评审间一致性未报告，不能推成因果忠实性测试。PRPO的CLIP图文相似奖励与段落/最终判决多数一致奖励是代理构念；稀疏伪影多数票失败局限已记录。
- PRPO的76条参考文献均已在 `142_PRPO全部76条参考文献逐条题录筛选.csv` 按题名/引用上下文逐条初筛；其中直接解释可靠性相关的核心小组见 `138_PRPO强相关引文逐篇初筛.csv`（6项）：X²-DFD、FFAA、SIDA、FakeBench、FakeShield、Common Sense Reasoning for Deep Fake Detection。逐项确认题名身份，区分全文核读与摘要待核；X²-DFD的PRPO引用年份与NeurIPS官方出版年份冲突，保留为待解版本元数据问题，未猜填预印本链接。
- `139_X2-DFD原稿与人评效度复核.csv`记录NeurIPS 2025 / arXiv v4 §4.3评价与人评维度：检测能力、解释合理性、细节程度；补充材料检索片段报告15名参与者和100个样本，OpenReview直开验证页受阻，故样本分配等完整细节待核。`141_FakeBench原文解释评价构念复核.csv`记录其人参与线索描述标注，而模型评价主要由文本指标/GPT辅助完成；论文中的“causal investigation”是双向问答任务，不是删除/插入等证据干预测试。`140_EFR原文空间接地与可靠性边界复核.csv`确认EFR ACM MM 2026 DOI，并记录50K条件生成样本、坐标/文本接地奖励与标注筛选边界；原有56条EFR参考文献初筛表仍在。
- FakeBench引文回溯新增三条早期/标注可靠性线索，记录在 `143_FakeBench引文发现的早期解释与标注可靠性论文.csv`；其中CVPR 2025 Face Forgery Text Generator论文指出人类和MLLM描述都可能幻觉，使用伪造mask约束线索生成。候选与引文表 `90_本轮新增强相关候选与引文复核.csv`现有133条候选观察/题录记录（未按所有预印本/版本完全去重）；PRPO、X²-DFD、EFR等已写入构念分层，新增FFAA/SIDA。专表137–141与改动的90字段均核对CSV结构；Scholar页位置观察未因引用核读而重复计数。原始页继续在`work/search_protocol_v2/execution_pages.json`与既有拆分计划。
- 阶段交付快照：`outputs/图像鉴伪解释可靠性_重检阶段结果_2026-10-09.zip`已按151个输出文件重建，CRC与每个成员字节比对通过；正文不承诺零遗漏。验证命令：`python3 -m compileall -q work/search_protocol_v2`、`git diff --check`；74主账唯一键和理由非空、PRPO参考位置1–76连续、候选表133条、151个ZIP成员逐字节校验均通过。无业务代码或模型实验改动。
- 遗留：Google Scholar Chrome当前受自动流量验证影响；PRPO全部参考文献尚未逐篇完成，仅先核与解释可靠性直接相关引文；EFR引用前后向链、候选版本合并、宽查询拆分和剩余主/子路线均未完成。下一步若Scholar恢复，从断点/待执行子式续分页；与此同时沿PRPO/X²-DFD/FakeBench/EFR高相关引文做原稿检查，并维护位置日志。ChatGPT Web优先复核137–143中“人评质量、人工标注、证据接地、因果faithfulness”四种构念分层。

# 2026-10-09 Google Scholar 生成图像解释人评分支续检（未完成）

- 仓库 `brodyZhao/my-research-project`；分支 `codex/forensic-explanation-literature`；本阶段起点 commit `985c7b7672036f38245b2367d276e9bf9f5d3f30`。工作区保留两个既有未跟踪文件，未改动、未暂存。检索表和原始页在忽略目录 `outputs/`、`work/`。
- 按任务术语OR项拆分继续 `T06-F3-S1-AUTH`。父式约2,830；`"synthetic image" ... ("human evaluation") ...` 子式约621，已逐条记录首页10项，未分页。平行 `"generated image" ...` 子式约2,510；已读start=0/10/20共30项。该分支过宽，保持未完成，并加入解释词OR四分支 `E1`–`E4` 待试检；不得将部分页面描述为完整覆盖。
- 为优先检验直接图像伪造语境，另跑两条明确标作高精度交叉检索（不是父式逻辑等价替代）：`"generated image" explanation "human evaluation" "image forgery"`，估数52→42，start=0/10/20/30/40逐条记录位置1–42，Next禁用并直接查start=42空；`"synthetic image" explanation "human evaluation" "image forgery"`，估数36→26，逐条记录位置1–26，Next禁用并直接查start=26空。只代表Scholar当时的窄式可见索引闭合，不能外推为领域穷尽。
- 累计筛选表 `74_V2完整分页逐位置初筛.csv` 目前18,549个结果位置观察，result_id唯一、每行均有筛选理由；它们不是18,549篇独立文献。子式状态表有143条，细查询累计位置数按该表当前值为4,275；全局审计仍 `complete=false`，独立文献去重、原稿终点核验、强相关引文链和其他待试检子式都未完成。此前累计值与细状态表重新汇总有差异，本阶段以表内明细重新计算并在83审计记录校正，不将其解释为新召回下降。
- 新逐条专表：`126_T06-F3-S1-AUTH-GENERATED_生成图解释人评逐位置筛选.csv`（宽式前30个位置，部分）；`127_T06-F3-S1-AUTH-GENERATED-EXPLAIN-FORGERY_精确式逐位置筛选.csv`（42个位置）；`128_T06-F3-S1-AUTH-SYNTH-EXPLAIN-FORGERY_逐位置筛选.csv`（26个位置）。新检索线索包括XPlainVerse、ForgeryGPT、HierForge、Agentic Tool-Augmented Reasoning、FACT、ForensicZoom、X2-DFD、So-fake、From Masks to Pixels and Meaning、OmniVL-Guard、GenShield、MedForge、Toward Generalizable Forgery Detection and Reasoning等；目录已有重复版本时按题名合并。筛选记录严格区分解释质量/证据真实性、检测准确率人评、生成图质量人评和异常严重度评价。
- 原始页与拆分计划在 `work/search_protocol_v2/execution_pages.json`、`fine_split_queries.json`；路线状态和计数在87/83表。已重建 `outputs/图像鉴伪解释可靠性_重检阶段结果_2026-10-09.zip`，137个成员、15,628,331字节，CRC和每个ZIP成员逐字节比对通过。修复重复追加的90条相同观察后，74主日志18,549行且result_id唯一、筛选理由非空；126/127/128专表分别30/42/26行且理由非空。`python3 -m compileall -q work/search_protocol_v2` 与 `git diff --check` 均通过。无业务代码或模型修改，无模型实验测试。
- 后续从E1–E4实际试检继续；如果仍然过宽，沿解释概念或取证背景递归拆分，并保留OR覆盖关系。随后继续精确查询、其他未试检分支、EFR及强相关候选的逐篇参考/被引链、版本去重与原稿核查。ChatGPT Web优先抽查42/26页终端边界、候选人评构念分层，以及审计计数从旧汇总重算的口径。当前Scholar标签保留在合成图精确交叉检索末页边界。

## 2026-10-09 图像伪造解释人评检索续检（未完成；断点 start=70）

- 仓库 `brodyZhao/my-research-project`；分支 `codex/forensic-explanation-literature`；本轮起点commit `4571c4aa6d3a3df5f0a7cc35248aaf0ed3952d8d`，交接提交后以Git HEAD为准。仅修改HANDOFF为tracked变更；检索明细写入忽略目录 `outputs/` 和 `work/`。用户两个未跟踪文件保留且未暂存。
- 继续T06-F2-S2精确短语子式 `("AI-generated image" OR "synthetic image") ("hallucinated explanation" OR "explanation faithfulness") (forensic OR detection)`：记录第2页位置11–13；Scholar总数约13，直接查start=20为空且Next禁用。当前子式可见索引位置1–13连续，87状态标作该路线可见索引完成，不等于主题穷尽。
- 执行之前待跑的 `T02-F3-IMAGEFORGERY-HUMAN`：`"image forgery" "human evaluation" explanation`。旧74主日志其实已有该式270个页面位置观察（20种不同偏移），覆盖结果位置1–106且有重叠；旧87状态曾误标“未试检”，本轮已修正为历史+本轮刷新两阶段。Scholar估算约117，start=30降114、start=40回115，显示索引估数动态；本轮start=0至70按10步分页重查，连续覆盖位置1–79（第8页显示9条），未到末页。最新Scholar估算116；下一步从start=80继续。不能仅以估算115就认定12页/末页，必须逐页观察并核对偏移/Next状态。
- 每页逐条记录在 `74_V2完整分页逐位置初筛.csv` 和专表 `123_T02-F3-IMAGEFORGERY-HUMAN_图像伪造人评细式逐位置筛选.csv`；page0–70共79条。强相关新增/确认线索包含ForgeryGPT版本、XPlainVerse、Toward Generalizable Forgery Detection and Reasoning、So-fake、Agentic Tool-Augmented Reasoning、HierForge、ForgeReason、ForensicZoom、Rethinking VLMs、Evidence Fusion、From Masks to Pixels and Meaning、OMNI-fake、GenShield、FACT、Veritas、OmniVL-Guard、PRPO、IDRetracor等。候选表按论文题名去重；部分ResearchSquare / Scholar结果URL仍需确认稳定来源和版本关系。
- 筛选严格区分图像/视频伪造解释、解释质量人评、检测准确率人评、图像质量人评、通用多模态推理。人评解释有用/连贯不能直接算faithfulness；候选中仅摘要声称测hallucination或证据对齐的须全文核实指标、样本、标注协议、真值与干预测试。相邻视频、医学、化学、新闻分类及版本记录均标注边界/排除理由。
- 更新raw `work/search_protocol_v2/execution_pages.json`、`fine_split_queries.json`、87路线状态、83计数及90候选表。经修正审计：74全日志18,385个结果位置（非独立论文）；细查询子式136条、其中位置4,528；52条子式标记当前可见索引已核完；全局 `complete=false`，受阻观察21。保留任何大查询拆分、索引漂移、原稿/引用链待核事项，不声称完整穷尽。
- 新阶段ZIP `outputs/图像鉴伪解释可靠性_重检阶段结果_2026-10-09.zip` 重建后以本轮最终校验值为准。验证：`python3 -m compileall -q work/search_protocol_v2`、`git diff --check`；检查CSV主ID唯一、无空筛选理由、T02本轮路线位置1–79齐全；ZIP CRC与每个成员和源文件逐字节比对。无业务源码/模型代码修改，无模型运行测试。
- 后续只继续文献检索及候选全文/版本/引文核查；先从当前Scholar `start=80`继续T02-F3精确人评式，并记录动态估数、分页缺口和每条排除理由。全局主题检索仍未完成，不进入研究方案/实验阶段。建议ChatGPT Web优先复核123专表与90候选中“人评解释质量≠解释忠实性”的分层，以及ResearchSquare来源/论文版本映射。

## 2026-10-09 T01-F2图像伪造解释忠实性路线续检（本查询可见索引完成；全任务未完成）

- 仓库 `brodyZhao/my-research-project`；分支 `codex/forensic-explanation-literature`；本轮起点commit `39671f790c716192182d373769875cf95ffa8bc3`，本交接提交后以Git HEAD为准。仅修改本交接；检索CSV/原始页面/ZIP在本机 `outputs/`、`work/` 忽略目录。用户两个未跟踪文件继续保留且未暂存。
- 按用户恢复指示继续Scholar查询 `T01-F2-IMAGE-FORENSIC-RELIABILITY`：`(“image forgery” OR “image tampering” OR “image splicing” OR “copy-move forgery”) × (“explanation faithfulness” OR “explanation fidelity” OR “sanity check” OR “parameter randomization”)`。Scholar估计数在186–198间波动；标准分页start=150后跳到167，已直接查start=160补足，再查start=170/176/180确认可见结果序列。start=180显示约186条、第19页、Next禁用。结果位置1–186无缺号，206条页面观察含20条跨偏移重复；这只证明本查询当前Scholar可见索引连续，不是主题召回率/零遗漏保证。
- 逐条观察写入 `74_V2完整分页逐位置初筛.csv` 及专表 `114_T01-F2-IMAGE-FORENSIC-RELIABILITY逐位置筛选.csv`；该专表206行、186个不同位置。对分页尾端的技术、医学、图书/版本、视频和非视觉研究逐项记录排除/背景理由。页17邻近候选 SalArt-VQA 已加入90候选表，状态仍为待全文核验；不计作直接忠实性证据。候选90共87行，含已有候选，不等于87篇核心文献。
- 更新87子式状态：本路线21个页面/偏移观察，206观察位置、186个连续唯一位置，标记“该查询可见索引完成”；此前150→167偏移异常由160核对。更新83审计：74共18203观察位置、细查询4346观察位置、63条子路线曾见末页、50条子路线当前标记覆盖完成；全局 `complete=false`，去重和强相关原稿筛选仍未完成。结果数均是观察位置/子路线统计，不是独立论文数。
- 下一待执行细式 `T02-F2-S1`（图像操纵 × 解释术语 × grounding）首页估计约14,200条，过宽，不能顺页当作可完成覆盖；按矩阵方法递归拆词并先试规模。之后还有大量未执行细式、异常索引回检、强相关全文与递归引文链。用户最初提出的全面重检未完成，不得称“一个文献都没漏”或进入研究方案下一步。
- 交付快照 `outputs/图像鉴伪解释可靠性_重检阶段结果_2026-10-09.zip` 已从当前输出目录重建：124文件，15,485,202字节；CRC/testzip与ZIP中每个文件逐字节匹配通过。验证命令：`python3 -m compileall -q work/search_protocol_v2`、`git diff --check`通过；74/114 result_id唯一且筛选理由非空；114独立位置连续为1–186。
- 后续建议：从14,200条的T02-F2-S1做递归细分和实际规模试检；检索正常时保留分页与偏移复核日志；再完成其他未试细式、大查询拆分、候选原稿评价终点核查和引文前后向追踪。ChatGPT Web可优先复核本次start=160/167/170/176/180的重复映射和T02-F2-S1拆分逻辑。没有修改模型代码，无模型/实验测试事项。

## 2026-10-08 遥感恢复、剩余小F4与细查询拆分（整体未完成）

- 仓库 `brodyZhao/my-research-project`；分支 `codex/forensic-explanation-literature`；索引最新commit `0e0bddc9eae05c879f31633e52413477f279b257` 已推送；交接另提交推送，最终hash见Git HEAD。仅检索协议/HANDOFF tracked修改，work/outputs本机；两用户未跟踪文件不改/不提交。
- 本轮用户确认遥感恢复，T15-F4到可见末页765位置；T09-F4到末页797位置；T01-F4正常680位置后start680空尾页，总数从约805降538。主路线59可见结束（15 F1/15 F5/11 F3/8 F2/10 F4），其中T12-F2/T08-F4/T01-F4三条索引大幅波动需拆词回检，不当覆盖充分。48父路线未全分页。主查询13941位置，附加题名/版本/前向28，74合13969，非独立论文数；22优先/61旧待审仍未变化。
- 新split_fine_queries.py生成85矩阵：16大细父式+3索引异常父式，19父/83子。可靠性OR逐词分配，任务、解释、其他限定保留；86逻辑并集等价，非语义完整性或总体召回保证。83子式需实际试检，若仍≥900更细拆分；当前只有首子T01-F4-S1尝试且受自动查询限制，未取得有效规模/题录（87），不能当零命中。其余82未试检。不重跑split脚本直接覆写85实际状态。
- 最新真实阻塞 tab1 是T01-F4-S1首页（image forgery/image tampering × explanation/attribution/saliency × sanity checks），没有验证码控件，readV2保存自动查询限制。用户需手动恢复当前页；下一轮正常后 `readV2('T01-F4-S1',fineSplitPlan.find(x=>x.query_id==='T01-F4-S1').query)` 先保存，再按实际规模决定完整分页。旧遥感第14页已恢复，不再向用户要恢复旧页。
- CUA持久新增 fineSplitPlan（读取fine_split_queries.json）、beginFineSplit(id)（goto已定义子式->readV2并打印首页），continueFineV2可直接用子ID（从execution_pages同ID找最后页，不依赖v2Plan）。不重置v2Executed。beginFineSplit首式被限流，不要重试循环。主体publisher目前子式若有正常页面会写入74，但主107覆盖统计不会算入子式；后续需增加独立子式覆盖统计/87状态，不能把子式当ForensicChat附加28。当前子式全0有效，因此主/附加计数未受影响。
- 实际检索仍是Codex IAB tab1。前一用户询问无痕，曾误开桌面Chrome无痕窗口，已承认；IAB能力仅visibility/viewport不能切无痕。用户随后明确恢复并继续IAB检索，未迁移桌面Chrome，不关闭用户窗口。
- 测试 `python3 -m compileall -q work/search_protocol_v2`、`git diff --check`通过；74 13969 ID唯一/理由非空；75 107路线、59可见结束无offset缺页、3大变化风险；85 83唯一子ID/19父逻辑并集验证通过。90文件ZIP14811073字节，CRC和逐文件字节一致通过，非零遗漏保证。输出目录/ZIP同前；新的85/86/87为逻辑矩阵/验证/实际状态。
- 后续先完成索引风险回检与大细子查询，再B1/B2大宽查询拆分、61旧核心和其他候选原稿、递归引文/版本。WorldScientific原稿安全验证未决保持。建议ChatGPT Web检查85–87没有把逻辑等价当检索完成，审核三条空尾页异常，重检未收尾前不做实验。

## 2026-10-08 从拼接第2页恢复：新增四条扰动评价路线（整体未完成）

- 仓库 `brodyZhao/my-research-project`；分支 `codex/forensic-explanation-literature`；本阶段最新索引commit `290c8dde397af44158f51536db138ab895b0db41` 已推送，交接另提交推送；最终commit以Git HEAD为准。主要tracked修改仅检索协议及HANDOFF；两用户未跟踪文件未改/未提交。
- 当前有效统计取代下方旧52条/9431：107父路线56到可见末页（F1 15/F5 15/F3 11/F2 8/F4 7），主查询11829结果位置，附加28位置，74总11857位置；不是独立论文数。新增T03-F4 466、T13-F4 500、T07-F4 569、T10-F4 743；T15-F4取得第1–13页130位置。优先22及旧61待重审未变化，原稿并未本轮新全读。
- 最新真正阻塞是tab1 T15-F4第14页start130自动查询限制，没有验证码控件；已AX核实。T03-F4旧阻塞已恢复并完成47页，不再让用户恢复旧页。下一轮恢复当前页面后先 `readV2('T15-F4',v2Plan.find(x=>x.query_id==='T15-F4').query)` 保存恢复观察，再 `continueFineV2('T15-F4',8)`；不能直接从受阻末尾空next判结束。不要重置v2Executed或重复finish完成路线。
- 51父查询未全分页；56可见结束中2条T12-F2/T08-F4索引波动风险仍需拆词回检，不当覆盖充分。48大父查询仍待拆分。小F4还T09-F4/T01-F4；后续拆异常/大F分支，然后B1/B2和候选/引文原稿/版本。整体检索未完，禁止进入实验下一阶段。
- 输出74/75/83已由publish_execution_round.py刷新；原始execution_pages.json全保留。本轮正常与受阻观察共历史7次受阻，不把受阻当零结果。旧prototype脚本会覆写后续资料，继续使用当前publisher。
- 测试 `python3 -m compileall -q work/search_protocol_v2`、`git diff --check`通过；74全部11857 ID唯一/理由非空；75 107路线、56末页offset连续；87文件ZIP14550250字节CRC及逐文件字节一致通过。不保证零遗漏。路径与上一交接同，work/outputs仅本机。
- 建议ChatGPT Web优先检查本次四条路线是否可见连续分页，75的索引风险与51待执行状态，不要把56/107当召回率。用户恢复Scholar后继续遥感第14页；WorldScientific原稿安全验证旧未决仍保留。

## 2026-10-08 V2细检索续检与原稿核查（整体未完成，当前学术受阻）

- 仓库 `brodyZhao/my-research-project`；分支 `codex/forensic-explanation-literature`；本阶段索引最新commit `7bdaecfb77492ffbaba324ad959ee23e4ee92d75` 已推送；本交接随后单独提交推送，最终HEAD以Git为准。用户两个未跟踪文件未改/未提交。work/outputs仅本机保留。
- 用户本轮恢复Scholar后逐断点继续。107父查询中52条到可见末页：F1全部15、F5全部15、F3 11、F2 8、F4 3。主查询9431位置，ForensicChat附加28位置（题名1/版本3/前向24），74共9459位置；不是独立论文数，不把1125试检再加为新增。75有107路线实际页数、偏移缺口、末页、估计数范围和风险。52中T12-F2/T08-F4大幅索引变化须拆词回检，故可见末页不当覆盖充分；55父路线未全分页，48大查询仍需拆分。
- 最新真实阻塞：tab1 T03-F4第2页start10自动查询限制，无验证码控件；已核AX，首页10位置保存。不要对用户刚回复恢复的旧T10-F2再索取恢复。T10-F2已恢复并到第62页616位置。下一轮先复核当前页，正常后 `readV2('T03-F4', v2Plan.find(x=>x.query_id==='T03-F4').query)` 保存恢复页，再 continueFineV2；不能从末尾受阻观察的空next判断完成。用户须手动恢复，未自动验证/绕过限制。
- 原稿：ForensicChat2509.25502作者v1指定方法/解释实验/AppendixE.3；800均假图，错误判决评分惩罚耦合；没有已核视觉干预因果协议。Counterfactual Tests2609.06704为SNLI-VE/AOKVQA迁移方法，不计直接鉴伪；编辑/识别误差与单模型重建控制边界见78。HexMIL2608.05101升级§2–5/表1–5：前向注意力、热图门控/平滑/阈值、切片结节坐标标签；架构均值池化消融不等于固定模型解释随机化；补充待核（81）。ATAR2609.39066升级§3.1/3.2/4.3/4.4.1：200图裁判、50图3人，ATAR独有额外热图裁判输入不对称；原页列MM2026 DOI，正式对应待核（84）。没有新实验或设计工作。
- 新参考题录全部位置初筛：ForensicChat65（76）、视觉反事实48（77）、HexMIL48（80），共161；不是161被引全文已核。ForensicChat前向24已取全、逐题名人工初筛82；3版本不计3论文。既有EFR56及其他参考旧日志保留。72优先22条（旧21重审+新ForensicChat），68旧82尚61待重审；机制相关与直接评价分开，全文范围受限如实注明。
- 原始观察 `work/search_protocol_v2/execution_pages.json`；scripts publish_execution_round.py新增CAPTCHA/自动查询/请求不符排除、有效页offset去重、连续性、索引变化风险；空阻塞不当零。pilot_records.json留原始115次试检。不要把 v2Executed 清空/重复finish已结束路线。CUA持久v2Scholar/tab1、v2Primary/tab3；恢复文档后复用。不要重跑publish_protocol/refine_protocol/finish_first_batch/add_primary_round/reassess_twelve，会重置部分新记录。执行publisher保留ATAR新增22。
- 测试：`python3 -m compileall -q work/search_protocol_v2`、`git diff --check`通过；74全部9459 ID唯一/理由非空；75全部107路线、52可见结束的offset连续；65/48/48参考、24前向数量与连续性检查通过。87文件ZIP14258440字节，CRC及每文件字节一致通过。文件一致性不能证明零遗漏。交付目录 `outputs/图像鉴伪解释可靠性_重检_2026-10-05/`；ZIP `outputs/图像鉴伪解释可靠性_重检阶段结果_2026-10-05.zip`。
- 遗留：当前Scholar限流；WorldScientific DOI10.1142/S0218001426400343仍安全验证待核，未当不存在。T12-F2 start750尾页估计由约750降525并空，取得750位置；T08-F4首页估计241尾页82/92，实际100位置；需拆解释子词回检。剩余F4小路线/大路线拆分/B1B2，候选正文、版本、递归引文未完。
- 建议ChatGPT Web首先检查75索引异常与74初筛范围；52可见结束不是完成率/召回率，22也不全部是独立忠实性实证。继续本协议细到宽，禁止在重检未收尾前进入模型实验/研究方案。

## 2026-10-08 用户要求重建检索逻辑：V2.1取代旧流程（整体仍未完成）

- 仓库 `brodyZhao/my-research-project`；当前分支 `codex/forensic-explanation-literature`；最新方案commit `059d502` 已推送，交接随后另commit/push，最终hash见HEAD。主要tracked文件 literature/forensic-explanation-search-protocol-v2-20261008.md 和旧阶段索引开头的撤销继承提示；outputs/work忽略，两用户未跟踪文件不改动。
- 用户明确先拟全面可行检索式并自查、然后细先宽后、给强相关并重查旧目录。已完成范围重建与实际首页试检：15任务族×7分支=105式，额外2量化质量/空间频域补充，共107式；115次观察（含复测/首批重复）、114有效、1次加载读到旧query排除并重试，1125有效首页结果位置，非独立论文数。全部原始DOM可见观测保存在work/search_protocol_v2/pilot_records.json，由cua控制浏览器并本地保存；并非猜测/编造检索命中。67查询矩阵、69每位置规则初筛、70验证。48式估计≥900，必须拆别名/解释子词/年份后再次试检，不能裸查到100页当全覆盖。
- 试检真修正：初始宽词式估计28200和synthetic宽式30300不作细入口；GAN/扩散加视觉，inpainting/document/medical/satellite加forgery/tampering/fake/authenticity/forensics；仍有参考引用/其他任务噪声，不声称100%精准。8锚点：首页回检EFR、BeyondAccuracy、Gowrisankar、Tsigos、SNIPPET、HexMIL；2022 BMVC和SSRN空间域批评原105式首页未现，补2方法分支后出现。这是自选8锚点测试而非整体召回率；所有107式语法/规模试跑不等于全部分页查完或零遗漏。
- 时间：arxiv2210.03683原页2022-10-07、BMVC2022接收确认；2312.06627原页2023-12-08。故不能从2024截断，至少2022已有直接解释评价，不宣称2022领域第一篇。2013 Fontani是工具可靠性/证据融合历史基础，不能充当现代XAI因果忠实实验。现代主线与更早定向历史/引用链分开，无总体年份排除。
- 冻结V2后首批细查完整可见26位置：T12-F1=2、T13-F1=6、T03-F1=7（复用已完全取得的首页避免重复翻），T04-F1两页11（真实Next至末页），完整位置/理由73CSV。新MDPI15/8/525拼接替代解释原页Web429，只有题录候选，不能报全文已核。其余路线继续按67实际规模/状态执行，首批完结不等于整体完成。
- 旧82全部入68队列，旧55 strong标签不继承V2最终数。先按已有原页证据重审8篇主题/终点/限制：EFR、Gowrisankar、Tsigos、BMVC、BeyondAccuracy、SNIPPET、SSRN空间域、ECS，72CSV；明确没有重新全文读完82篇，其他74待审。高相关与可靠性证据强弱分开，展示热图/检测准确率/跨方法一致性不自动当因果忠实。旧15,380日志是历史主体；V2试检另存，不把1125重复位置直接相加为独立论文。
- 文献继续用ARS inline bibliography角色规则，但用户不限级别/年份/全文可得性、细先宽后指令优先，未派subagents。新scripts refine_protocol.py/publish_protocol.py/finish_first_batch.py在work/search_protocol_v2。publish重写67/68/71，之后finish_first_batch加首批状态和tracked索引；重复finish会再次prepend旧索引提示，避免无理由重复。旧pipeline重刷会覆盖旧index，不应取代新的V2权威方案。
- 检查：python3 -m compileall -q work/search_protocol_v2、git diff --check、CSV107/82/8/26读回计数、8锚点真实命中、26ID唯一且末页无Next通过。76文件ZIP13,069,078字节，CRC/每文件内容相同通过；不是零遗漏证明。
- 浏览器绑定browser2当前tab1（旧tab5已不存在），copy-move细式第2页末页已markHandoff，无年份/cites过滤。当前会话helpers protocolPilot/concisePilot从UI填写每式、只首屏保存；有时input返回旧query，正常footer也不足，必须对actual==requested，已有无效观测保留。后续先取得真实当前tab，不用旧tab5变量。
- 下一步：继续67中小规模F1/F5到末页并逐篇原稿筛选，48大式先细分再试检；按68重审其余74篇及旧352英文候选/252迁移方法候选。不要回到deepfake主导、结果数量代完成度或原样跑所有巨大宽式。不进入方案/实验。建议ChatGPT Web先查71的选题边界、107矩阵的必查/补漏逻辑、70锚点测试限制，以及72八篇是否把主题相关性与证据质量分开。

## 2026-10-08 文献重检进度汇报与年份细分续检（仍未完成）

- 仓库 `brodyZhao/my-research-project`；分支 `codex/forensic-explanation-literature`；最新阶段索引commit `e35d7aa` 已推送。交接随后单独提交并推送，最终hash见Git HEAD。仅索引与HANDOFF入Git；两个用户未跟踪文件保持原样。
- 用户最新要求先汇报检索式、强相关数量、引用追查和剩余工作；完整本地汇报为 outputs/图像鉴伪解释可靠性_重检_2026-10-05/66_文献重检进度汇报_2026-10-08.md，附全部101有效范围路线原式。当前15,380日志=15,355正常+25遗留过滤；核心82（tier1强相关55、tier2紧密26、tier3通用1），英文81中文1；352英文候选及252迁移候选待人工边界判定，非全部相关篇数。99路线可见终页，87无既定两风险；14待结案含已分段的宽查询、GS037更正题名和低优先级中文GS050，不说14条全未检索。
- GS096恢复后已987位置至第100页空尾页，估计1,030保留显示上限风险。更细分GS097≤2024共38页377位置、GS098仅2025共65结果页644位置均终页；GS098第59页自动查询限制用户恢复后续到末页。已有GS095≥2026共740终页。四补查相对GS094新增1,200题名位置/770规范化题名，不当新增独立相关论文。60/61记录差集，65连续性核验三条本轮路线无缺页。一次20页批次超时核重置，420–600逐页重读；曾丢失800压缩payload已重读该页。export解析审计保留1条历史不完整，不能说零解析失败；各页原始证据覆盖完整。压缩marker直接拼接会吞下一marker字母，export已插换行修复。读取自己JSONL只用LF split，PDF含U+2028。
- Guo ICLR2026 The Value of Information in Human-AI Decision-Making官方32页PDF正常TLS获取2,069,381字节，focused_primary_GuoILIV2026记录SHA。选定§3/4/5/6.2/7、Appendix H已读；新的421名US Prolific六组解释实验为Ames房价任务，不是深伪解释干预。深伪重分析Groh2022的5,524人及7视频级特征，Brier信息价值非检测准确率/因果忠实；互补性人为构造、SHAP基础缺陷未解决。全部83参考按首行x108/悬挂118从11–16页提取并逐题录初筛62CSV，标题句段抽取可能遇姓名缩写，完整raw_citation保留；被引全文未全核。其他种子引用2052+EFR56=2108位置，不当独立相关文章。
- GS099正式题名相近结果1；展开全部GS100共22；GS101前向26；GS102全部版本3（不计三篇）。52位置人工题录初筛63与主日志匹配；人工专题位置累计628=400+98+78+52，其他日志仍规则辅助初筛。作者目录网页转ziyangguo.com，旧题名列ICLR2026并直链33页作者稿；与arxiv2502.06152/官方32页有较强映射，仍未逐版确认或合并NeurIPS2024，64保留边界。Web原稿ref turn153view0，arxiv154、作者目录155、作者稿156。
- 本轮scripts add_guo_information.py/finish_reliance_round.py/write_progress_report.py，加enrich_guoiliv与checkpoint83计数。完整pipeline依次export→build_research→enrich_catalog→build_checkpoint→build_term_coverage→build_english_focus→build_english_partition_audit→refresh_phase_index。最后write_progress_report补66与索引段落；若重新refresh会覆盖最后补段，需再运行报告脚本。不要单跑enrich已stripped public master；勿重跑旧add_*重置后来阅读范围。
- 验证：pipeline主ID/理由/原证据SHA检查通过；Guo83连续参考/SHA及52人工位置↔主日志通过，65有结果；python3 -m compileall -q work/literature_research_20261005与git diff --check通过。69文件ZIP重新打包12,930,956字节，CRC和每文件字节一致通过。这里只证文件一致性，不证零遗漏或重检完成。
- 浏览器当前用户只保留tab5，GS102三版本页面，无年份过滤。最后状态无需再恢复第59页；下步继续英文候选352及强相关引用链/原稿/版本。33术语族代表查询不等于穷尽全部组合，仍需补对抗解释/裁判索引风险，精确版本核查、正文未取得条目处理。按用户要求只做重检，未经重检收尾不进入研究方案/实验。建议ChatGPT Web先检查66汇报的计数/强相关定义是否清晰，重点看62–65证据边界与05未决原因。

# Project Handoff

## 2026-10-07 专业工作流与过度依赖扩词续检（仍未完成）

- 仓库 `brodyZhao/my-research-project`，分支 `codex/forensic-explanation-literature`；阶段索引commit `f3c9197b8e29ac30dc437964408c2b0f776249e7` 已推送，交接随后单独提交/推送，最终commit见Git HEAD。只索引/HANDOFF入Git，work/outputs及两个用户未跟踪文件不改动、不提交。
- 用户两次“已完成”均实际复核：GS089恢复正常1结果终页；GS096较早年份补查reCAPTCHA恢复后连续记录21页210位置，第22页start210现在为Scholar“automated queries/can’t process”限制，无验证复选框。此为新的自动查询阻挡，不把刚才验证码完成当解除全部限流，不刷新循环/自动解验证。最后实际AX/DOM已核，非零命中/非终页。当前没有再次要求用户点不存在的验证复选框。
- GS090情报分析员精确题名1，GS091前向10到终页；GS092 Dungeons题名4页35，GS093前向4页33到终页。全部78位置人工题录初筛59CSV，背景/重复/非英文/不足题名保留实际位置，不当78篇独立相关论文。修复build_research对明确中文`[前向引用]`标签的识别：此前只认Cited by导致GS091/93误记遗留过滤，人工表校验报KeyError，没有交付失败状态。修正后78与02理由一致；原三条遗留过滤25位置仍保留，没有把意外cites全部放行。
- GS094扩词 `"deepfake" ("explanation" OR "explainable") ("overreliance" OR "over-reliance" OR "appropriate reliance")` 100页995实际位置，估计1810→1800，明显显示上限，未宣称穷尽。GS095≥2026从实际年份菜单切换，74页740位置终页，估计743→740，无已观察到的显示上限/大幅索引风险。GS096≤2025通过实际高级搜索设置，必须把完整布尔式放全部字词、至少一个字词清空，防菜单自动拆散OR组；恢复页面query核与原式一致，估计1040→1030。当前210位置，不记查完。60/61差集321新题名位置/321规范化题名，相对原995，包含噪声，不当新增独立相关论文，与主日志理由一致；较早段未完整、无年份条目仍可能遗漏。
- Wu情报分析员作者项目公开PDF普通TLS取得36页9,958,396字节，SHA1d67ea4b8c09c5f2f7ffe1eb8f7588b678bd423d9666335b79829e1a7aa42e71。4作者 Y. Kelly Wu/Saniat Javid Sohrawardi/Candice R. Gerstner/Matthew Wright；稿上CHI2025 DOI10.1145/3706598.3713711。所读36页稿有提交标记，正式26分页仅二级提示，ACM浏览器直页安全验证、旧Web403保留，未核正式全文。§3/4.4/5.3/8：30从业者需求（不是全为分析员）、11人本体评价不合并人数；28 analytics，本体界面固定在模糊搜索之后，主要Likert/报告帮助与定性反馈，不当随机解释忠实性或错误建议下依赖校准。文本受欢迎，热图/频域/噪声图较难解释，比较基线/工具提示有实际意义。作者稿完整93参考57CSV，二级RG73不能当完整数，被引原稿未全核。提取时行号与分页奇偶位置不同，最终按LF/完整数字加空白边界清理，保留跨行DOI和226等真实页码，连续1–93及源SHA核。
- Dungeons & Deepfakes DOI10.1145/3613904.3641973新增核心范围为ACM搜索返回公开摘要/题录：4作者、2024-05-11、CHI776:1–17，24名美国记者，涉及不可靠工具过度依赖；Web直开403，全文/全部引用尚未核。作者nviable项目页有扩展跨国34和训练19学生等研究，不能直接作为本篇24人协议，也有表19+15+10与total34不一致，不从案例页继承人数或效果。RIT机构仓储博士论文12387公开题录/摘要已核，Saniat Javid Sohrawardi、2025-12、PhD；下载链接13509 Web失败/普通TLScurl403，不是PDF成功。论文包含记者解释需求/美国孟加拉情境/平台，有CHI研究重叠，单列文献但不重复计样本/效应；正文引用待核。
- Zhou arxiv2508.01906 v1 2025-08-03，5作者 Yingfan Zhou/Ester Chen/Manasa Pisipati/Aiping Xiong/Sarah Rajtmajer；摘要题名Risk Perception、HTML Perceived Risk不统一。PSU机构题录列正式PACMHCI9(7)CSCW407、DOI10.1145/3757588，作者/题名高度匹配，v1 DOI仍XXXX模板，没有直接版本映射，正式稿全文未核。读作者HTML §3/4/6：400招募/390有效，美国Prolific，风险组间、FPR描述组内且两轮顺序随机；无实际检测器。告知3%/30%FPR，但两轮均每四项1TP/1TN/1FP/1FN，实际错误结构相同，不把描述当真性能；风险操纵检验未显著，信任差异d0.09、中介路径不成立。依赖/合规不是解释忠实性，未随机操纵像素/文本解释。全部59参考初筛58CSV含1993/1994自动化基础，不因年代排除；所读预印本与正式身份疑点保留。
- 实际原始1424页面/13534行，1423有效Scholar页面观察、1导航异常4行排除；主日志13530=13505正常+25遗留过滤。95有效范围路线、92可见终页/81无既定两类观察风险，14未决包含原12、GS094显示上限及GS096访问阻挡。新增2025实际位置（GS0891+GS0901+GS09110+GS09235+GS09333+GS094995+GS095740+GS096210），非相关篇数。显示上限GS007/94，9旧索引风险仍保留。核心81/英文80（含1迁移基础）/中文1；英文待核352、迁移方法248，候选9417含噪声，旧337本轮重匹配224。EFR56另计；其他种子参考1969=1817+93+59，非独立相关篇数/全原稿核验。原页获取尝试2147成功与历史失败并存；本轮46补充Web返回另记16，不混Scholar。原输出与索引全部重新生成，64件ZIP 11,845,232字节。
- 全流水线export→build→enrich→checkpoint→term→English→partition→index成功；refresh_phase_index现自动运行build_reliance_partition_audit并读61动态差集，避免静态321数字遗留。检查引用57的93/58的59连续位置、每条理由/源SHA，59全部78人工题录与02、60全部321差集与02一致，EFR首位/81核心、25遗留位置一致；ZIP CRC/testzip及每文件字节一致，compileall -q work/literature_research_20261005和git diff --check通过。无模型/实验。JSONL读取曾因PDF中的Unicode分行符被splitlines当行界报错；改为只按LF分割真正JSONL记录，恢复零导出失败，原会话未修改。失败中间包未交付。
- 浏览器2继续复用：tab5 activeScholarTab为GS096 start210自动查询限制断点，含as_yhi=2025；正常恢复后先读该第22页，再往下，后续不限年主题必须清年份。tab8 continuedPrimary为arxivHTML2508.01906v1；tab6旧OpenReview挑战。currentRead仍只直接识别gs_captcha_f，Google/sorry的captcha-form需DOM/AX确认；build_research已有验证redirect脱敏投影，不把失败当导航/零结果。后半段浏览器观察使用SCHOLAR_GZIP_B64，export支持解压原始完整每页，refs缓存也核；不要把Base64输出当遗漏未读行，也不要声称它们全部人工全文审评。旧emitResearchBatch闭包仍被旧walker捕获，单独重赋值不改变其行为；本轮后半分页采用当前cell的显式goto→AX→currentRead→gzip循环，保留全部位置。
- 新脚本add_human_workflow_round.py/add_zhou_dependence.py/screen_workflow_positions.py/build_reliance_partition_audit.py以及enrich/checkpoint接57/58，索引接59/60/61。不重跑旧add_*重置后来证据阅读范围；新脚本按需改，历史状态不要继承。下一步只继续重检：GS096恢复后分页与如触上限的更细年份补查；352英文候选、强相关引用链原稿/版本；Guo ICLR2026 The Value of Information in Human-AI Decision-Making与2502.06152/NeurIPS2024身份、VRAG-DFD、职业工具/新闻研究、2011前身与高相关非英文捷克用户论文仍待核。不能把所有位置rule初筛当人工全文已读，不进入方案/实验，不宣称重检完成或零遗漏。

## 2026-10-07 原型解释、跨数据集一致性与早期证据融合续检（仍未完成）

- 仓库 `brodyZhao/my-research-project`，分支 `codex/forensic-explanation-literature`；阶段索引commit `f5d8e13771ba58d5cec090456d5dc005550ae7d2` 已推送，交接随后单独提交/推送，最终commit见Git HEAD。只索引/HANDOFF入Git，论文原文、work/outputs和两个用户未跟踪文件不提交、不改动。
- 原断点ExplaNET IEEE10542403参考页已正常加载20条，不是上一工具输出截断意味着网站失败。公开摘要/介绍首段核原型训练及Grad-CAM，4作者、DOI10.1109/TBIOM.2024.3407650、在线2024-05-30/期号2024-10、6(4):486–497；正文要求登录，不确认原型干预、因果忠实性、人类信任实验。全部20公开引用逐条初筛53CSV；SupCon/ICCVW被引用未标workshop的题录问题与ProtoExplorer2023预印本链接2024正式DOI保留。
- IET用户恢复后已核 From pixels to proof，Anita Khadka/Carsten Maple，DOI10.1049/icp.2025.2976，CADE2025、2025(22):138–144；在线2025-09-18/期号2025-10-01分开。PDF实际按钮回带download=true摘要页、订阅拒绝；无全文/公开参考，不作零参考结论。原先安全验证阻挡已更新，历史Web403仍保留；从题录待核升级为公开摘要核心，tier2，摘要不足以证明解释可靠性。
- GS087 SupCon题名1，GS088前向10页98位置到可见终页；全部98人工题录筛选54CSV与主日志一致，含重复/无关/不足题名，不称98篇相关文献。GS089 ECS精确题名查询触发“请进行人机身份验证”，显示1结果但没有可读条目，记录0已读位置/非零命中/非终页。已异步请用户手动恢复，当前尚无新回复；不能自动解验证或刷新绕过。新增99实际位置，原始1216页/11509行，4非Scholar排除；主日志11505=11480正常+25遗留过滤。88有效范围路线、85可见终页/75无既定两类观察风险，13未决包含原12与GS089。
- SupCon官方CVF PDF正常TLS下载11页1,614,480字节、SHA c1280868e77ee6113f254c97929cf5b392e80659fbb3f4268a6e285f4db5359d。Ying Xu/Kiran Raja/Marius Pedersen，WACVW2022 XAI4B:379–389，DOI .00044由IEEE被引正式记录核，非WACV主会。选定4/5/6、图4/5热图与UMAP及评价限制已读：定性投影/热图比较后融合，不当独立忠实性验证；FaceSwap TOSC47.55/融合49.77等泛化失败保留。全部71参考按列提取，连续位置及源SHA核，52CSV初筛；6/7同题疑似重复、引用55通用可视化评价不等于本研究实际量化忠实性。不要无依据叫热图Grad-CAM。
- GS088第85位置再次检出已有核心ECS，原页Research Square rs-10864099/v1正常，四作者 Adedayo Ayomide Adeniran/Adetayo Olaniyi Adeniran/Abiodun Ojo/Thomas Oluwaseun Onih；2026-09-21预印本未期刊同行评审。正常TLS取得33页607,706字节，SHA ab04e01c8588a5911aab9cb58dda2856044bb60e40752d498e54069606e79026。§3.5–3.6/4/5/7.1选定原稿升级，不新增独立核心计数。ECS是同图同检测器Grad-CAM与++的top15% IoU/SSIM等权组合，聚合仅正确分类图；跨域分布差异不比较不同图热图，单初始化SD非多种子。不能证明错误线索依赖或因果忠实。§4.1保留未编辑drop-path参数备注，测试视频数量措辞不清，26引用的24 SupCon写154–164/.00020错误，已保留原始错误并用正式379–389/.00044匹配。全部26位置55CSV；Ajayi参考刊名身份未核，不自动断言虚假。手稿图2借自Tsigos，不能当本实验展示。此文高度相关但证据质量限制保留。
- 2013 Fontani作者PDF此前默认沙箱DNS/TLS失败，本次正常TLS扩展权限下载成功32页4,534,612字节，SHA50d0c26bf013c617f665d7cea3a8147ba37d6d5bc7d0efbc51d25e36c540a948。IEEE Cite This核正式TIFS8(4):593–607，2013-04，DOI10.1109/TIFS.2013.2248727及5作者。作者稿2013-02-27 DRAFT，页眉2007为模板，非最终15页期刊排版。核II/III、IV-B、V：工具可靠性折扣、疑问质量、痕迹兼容、证据独立性/重复计权/归一化冲突消失；检测ROC/可靠性扰动非现代解释忠实性。正文20次与图7标10次不一致，草稿未解析[?]且缺bibliography。IEEE公开19参考逐条初筛56CSV，不能当作者稿引用完整性；其中1976 Shafer书链接2008 IEEE记录，保留身份疑点，不以该DOI自动合并。早期1967理论等不因年代排除。
- 核心77/英文76（含1通用迁移基础）/中文1，英文待核345、迁移方法238；候选8386含噪声，旧337本轮重匹配222。ECS旧title身份review升级为DOI后去重复当前review，仍1独立核心。EFR56另计；其他种子参考1817=1681+71+20+26+19，不当独立相关篇数或全被引全文已读。原页尝试2139含成功与历史失败；新27补充Web结果另表16，不混Scholar。公开输出59件，ZIP 10,335,051字节；CRC/testzip与每文件逐字节一致。
- 全流水线 export→build→enrich→checkpoint→term→English→partition→index成功；引用52/53/55/56位置连续、每条理由/原列表SHA，54的98人工题录理由与02一致，旧400人工记录仍核。compileall -q work/literature_research_20261005、git diff --check通过；EFR首位、核心77排序连续断言通过，无模型代码/实验。一次新筛选脚本把原list当dict失败，未写出中间成果，改为result_id索引后重新生成验证；未交付失败状态。这些一致性检查不证明零遗漏。
- 浏览器2复用：tab5 activeScholarTab为GS089验证断点；tab8 continuedPrimary为Fontani6470675/references，Cite This弹窗打开，正式题录已读。tab6 englishPrimary旧OpenReview挑战仍保留；无需为读正式FakeXplain要求用户处理。当前helpers绑定5；恢复后先核实际结果并记录GS089，再继续主题查询。Scholar引文查询后必须经真实首页清除cites；不要重选浏览器。
- 新脚本 add_prototype_round.py/add_ecs_reading.py/add_fontani_restored.py与screen_supcon_forward.py只针对本阶段证据；旧add_continue_round.py不可全跑，会重置后来阅读范围。新add_prototype_round也不要在ECS升级后无理由再跑，其三review可保留但旧摘要身份审计注意去重。下一步继续GS089恢复、英文345候选/强相关前后向链，CHI情报分析员工具原稿、Sparse/ConvNext原型、捷克热图用户论文两位置高相关不因语言排除；2011前身、版本链、索引风险未闭环。不得进入方案/实验，不得宣称全面检索完成或零遗漏。

## 2026-10-07 可核验/完整性扩词与JPEG、用户信任原页重检（仍未完成）

- 仓库 `brodyZhao/my-research-project`，分支 `codex/forensic-explanation-literature`；阶段索引commit `1c7c0d9756fb0838a47f7d9210b8e5730afdd7db`，随后单独提交/推送本交接，最终commit见Git HEAD。保留用户两个未跟踪文件，work/outputs与原稿不入Git。上一阶段交接候选7945为抄录错误，按该阶段工具结果应为7976；本阶段使用实际生成计数8266，不继承旧数字。
- GS080 Dual JPEG题名4、GS081前向3、GS082 Trusting题名1；GS083英文可核验解释25页241位置（估计249→241）、GS084解释完整性16页159位置（估计162→169→159）均到可见终页。GS085 IET题名1、GS086前向2位置已记。共新增411位置，仍不当411篇独立相关论文。原始1204页/11410行，4非Scholar行排除；主日志11406位置=11381正常+25遗留过滤；85正常路线、83可见终页/73无既定两类观察风险。原12未决（显示上限/9索引风险/替代歧义/降低宽中文优先级）保留，没有宣称穷尽。
- GS083/84全部400位置增加人工题录筛选51CSV，63保留直接/强邻域候选、177方法/背景、160排除直接目录；理由与主日志400个位置一致，仍不是全文排除。许多Academia题名为医学/历史/哲学但摘录反复带同一取证句，保留索引/串页疑点，不仅凭摘录关键词纳入。build_research新增 `manual_position_screening.json`逐result_id覆盖初筛；其他路线原始自动初筛不伪称全部人工已读。
- JPEG arxiv2408.17106 v1首发2024-08-30、v2 2025-04-07，3作者核；原稿IV/VI/VII算法、评价限制已读。已知JPEG流程且充分搜索的不兼容证明可作为可核验依据；有限搜索未求解块也判假时不能套零误报保证。实验为块级且可翻转预测，受控小图/QF条件；完全兼容拼接和强重压缩边界保留。完整27参考（含软件资源14）逐位置初筛46CSV，未全核被引原稿。
- Trusting the Detector IEEE11558887已在浏览器正常恢复：Lucas Kopp/Alina Lytovchenko/Robin Cohen，DOI10.1109/ICDEW71238.2026.00011；会议2026-05-04–08与入库2026-06-16分别标明。原摘要明确标签/热图/文本/混合四条件、Likert/Friedman及主观信任接受度，正文需登录，样本N/错误建议设计未核。展开公开参考时初始Getting results/另一个“not available”不能当无参考，等加载后View More全部30条已展开并初筛47；二级RG29非权威计数。升级核心但范围仅公开摘要/介绍首段/参考，不当全文人类信任校准。
- OmniVL-Guard Pro arxiv2605.16962，2026-05-16 v1、列明10作者；核3/4/5与附录E/F的工具轨迹、Checker0/0.5/1协议，多MLLM一致判分蒸馏且仅对正确答案施过程惩罚。实际在线工具记录可审计，不等于因果忠实性验证；分类/定位改善不替代理由可靠性终点。完整32参考逐位置初筛50，已补全，本轮add_continue_round再跑会重置basis，勿覆盖后续32引用范围。
- ForenAgent正式Springer章节 Code-in-the-Loop Forensics，DOI10.1007/978-3-032-37592-6_12，2026-09-14、ECCV LNCS17023:203–221，13作者核。GS083 Google Books错误作者不覆盖正式题录；只公开摘要，订阅正文未取得，过程奖励/评价细节待核；公开65注册参考逐条初筛49（8产品/软件/系统卡资源），原PDF参考完整性待核。35传统重采样2005等早期方法不因年代排除。
- FakeXplain从GS083实际结果获得ICLR2026正式页及22页PDF，不依赖OpenReview才能读正式稿。48CSV保存其与2506.07045高度疑似版本关系：数据/模型/8772例相同，题名/作者顺序及Hong Yan/Yan Hong拼写不同；arxiv只有v1且未映射正式发表，作者GitHub为空库无ID映射。暂不计新增独立核心、不自动合并，也不把新正式稿偏好结果当因果忠实。OpenReview tab6原挑战仍未回复，当前不要求用户为读原文处理该验证。
- IET From pixels to proof原页Web403，浏览器tab8持续“正在进行安全验证”，尚无正文；已异步请求用户检查恢复后回复“IET已恢复”，当前无回复。高相关待核保持manual_result优先，不因会议级别或访问失败排除。Scholar正常，本次不自动处理挑战/刷新循环/付费/联系作者。12个补充Web搜索结果另计16，不混进Scholar位置。原页记录2131，成功与失败均保留，不当独立原稿数。
- 核心73/英文72（含通用迁移基础1）/中文1，英文待核346、方法231；候选8266含噪声，旧337本轮重匹配211。EFR全部56另计，其他种子引用位置1681=1527+27+30+65+32，非独立相关论文总数或全部被引全文核验。输出54件；ZIP testzip及每文件逐字节比较通过（10,185,257字节），所有引用表ID/理由/源SHA、400人工筛选主日志一致、核心/EFR首位断言通过；`python3 -m compileall -q work/literature_research_20261005`、`git diff --check`通过。修复ForenAgent参考解析中同一工具文本行拼接的L编号，最终65连续位置；一次脚本变量注入碰撞导致集成未执行，已改用独立ns/明确base并完整重建，不交付失败中间计数。无模型代码修改/实验，不需tensor/模型测试。
- 浏览器2 Scholar tab5 `activeScholarTab`在GS086前向末页，继续主题查询必须先经真实学术首页清除cites。tab6 OpenReview旧挑战；tab8 `continuedPrimary`为IET安全页面。保留断点，不重选浏览器；当前helpers绑定5有效。完整流水线 export→build→enrich→checkpoint→term→English→partition→index；新引用JSON已接入enrich/checkpoint，表48/51也在索引列出。
- 下一步只继续重检：IET实际恢复后核原稿；继续英文346候选、FakeXplain版本/正式稿引用链、ForenDeX版本、早期2013融合原文与强相关前后向链。400位置分类不代表全部11406人工全文筛过；这些文件一致性检查不证明零遗漏。不要进入方案/实验，也不要把阶段包叫最终穷尽检索。

## 2026-10-07 GS070实际恢复与英文机制/证据引用链重检（仍未完成）

- 仓库 `brodyZhao/my-research-project`；当前分支 `codex/forensic-explanation-literature`。本阶段最新索引commit `f05b343f1d8fce902ba7d6235588f57f1c29ce3a`，交接随后单独提交/推送，最终commit见Git HEAD。只索引与HANDOFF入Git；两个用户未跟踪文件不修改，原稿与输出留本地。
- 用户“结果已显示”后实际核GS070为正常1条SSRN6811534结果，无Next；没有可见被引按钮，不推出全球零引用。GS071由实见Related articles链接逐页10页100推荐位置，非引用/主题穷尽。GS072 ForenDeX citation-only1、GS073前向1；引用论文Foundation ref49称CVPR2026:6592–6601，原稿身份未核，不能据同七作者与ForenX归并，42CSV保留疑点。
- GS074早期Dempster–Shafer2013题录1、GS075全部12版本位置2页到终页，版本非12独立论文；GS076 watchful forensic analyst多线索融合14位置2页到终页。Siena作者PDF curl正常TLS exit35、另urllib默认证书验证EOF失败，未取得PDF，不关闭证书校验。GS077 ESIDE精确题名1、GS078前向13位置2页、GS079 EvoGuard精确7位置均到可见终页。
- 新增原稿人工阅读：Defake-o3 arxiv2608.16259，选定证据生成/评价/附录，70参考逐位置初筛（43）；Agentic Forensics 2609.24359，适用家族仲裁而非理由因果依赖，31参考（40）；Foundation Mechanisms 2608.12155，频段干预/反演样本选择边界，64参考（41）。完整引用列表不等于所有被引正文已读。Agentic列明作者6，不按arxiv自动文字错算9；原引用旧ForgeryGPT题录不覆盖已核v4。
- ESIDE正式AAAI40(13):10844–10852，DOI10.1609/aaai.v40i13.38060，2026-03-14，10作者；正式9页PDF直指扩展arxiv2503.06201确认身份，选定解释模块/评价核读，49参考位置逐条初筛（44）。图文短语相似度/文本质量不证明检测决策忠实，人工剔除错误伪迹标签不等于全解释独立人工评审。shell PDF下载DNS失败，Web正式PDF章节已返回，未声称本地PDF下载成功。EvoGuard原稿3.2–3.4/4.1–4.4与讨论核读，工具共同失效可误导推理；奖励真假/格式/分析长度不证明理由忠实，完整96参考位置已逐条初筛见45，被引原稿仍待核。
- Scholar当前健康，无Google验证待办。OpenReview FakeXplain实际跳转 `https://openreview.net/challenge?redirect=%2Fforum%3Fid%3DUcpTOa8OnG`，显示浏览器验证；已异步请求人工恢复，尚未回复；与已核FakeXplained版本关系未核。不自动解挑战或登录，不连刷。没有进入方案/模型实验。
- 导出1158原始页、10999原始行，4非Scholar行排除；公开日志10995位置（正常10970+遗留过滤25），78正常路线，76可见终页/66无已观察风险。12未决路线保留；显示上限GS007、9索引变动路线不作穷尽，宽中文GS050依用户指示降低优先级。33词族有代表查询，不是整体召回率。核心69，英文68（含迁移基础1）、中文1；英文待核345，方法224。候选7945含噪声、旧目录重匹配208；EFR56参考另计，其他已初筛1527位置，不当独立相关篇数。原页/主DOI获取尝试2124，含失败，不当唯一稿数。
- 全流水线export→build→enrich→checkpoint→term→English→partition→index成功；0解析失败；新增31/64/70/49/96位置连续、理由、源SHA和CSV读回通过，核心69/EFR首位及GS070恢复断言通过。`python3 -m compileall -q work/literature_research_20261005`、`git diff --check`通过；48件ZIP testzip和逐文件字节比较通过（9,774,593字节）。只文献数据，无模型运行测试。
- 浏览器2原标签1/2/3中途消失，listTabs空后在同浏览器建新页；参考原稿tab7已完成96位置提取，可关闭；当前Scholar tab5 `activeScholarTab`/`resumedScholar`，OpenReview tab6 `englishPrimary`。旧helpers闭包捕获tab1，赋值不足以恢复；已同cell重建 `currentRead`、`searchResearchRoute`、`walkResearchPages`绑定tab5。新页正常；无须重选浏览器。继续新查询须经实际学术首页清除遗留cites/cluster/year过滤。记录读取选定正文，不取隐藏浏览器状态。
- ChatGPT Web下一步只继续重检：OpenReview人工恢复后核FakeXplain版本；EvoGuard全部96参考已初筛，被引原稿及英文345候选与其他强相关前后向链/早期融合原文待核。公共目录仍明确未完成；不可因增加条目或文件检查通过而称零遗漏。新增scripts `add_evidence_round.py` 重跑会重置部分阅读范围（Defake已补70引用），不要无理由覆盖；先全流水线重建再脱敏，不单独enrich去snippet后的公共master。

## 2026-10-07 学术恢复回复后核对仍受阻，继续原稿与38参考审计（未完成）

- 仓库 `brodyZhao/my-research-project`，分支 `codex/forensic-explanation-literature`；索引提交 `2842e5268b0547cbec156733e2f8d076a655fee8` 已推送。交接随后单独提交/推送，最终commit见Git HEAD。两个用户未跟踪文件不修改，原稿/work/outputs不入Git。
- 用户回复“学术已恢复”，但实际Scholar标签1仍显示“请进行人机身份验证”及未勾选reCAPTCHA，footer=false/rows0。确认只有一个Scholar标签后，在用户确认恢复的基础上仅重新加载一次，仍captcha=true、无论文结果。两个新观察已导出（同URL最新记录替换，独立页/位置数不增加）。已异步请用户看到结果后回复“结果已显示”，本次尚无进一步回复。不自动完成验证、不连续刷新、不能把计数1当已取得题名/零命中/终页。
- 在等待期间继续核原稿：Look Before You Judge，arXiv2609.35536，首发2026-09-28，11名作者已核。作者HTML方法/实验、附录A/B指标及限制人工阅读；区域注意力对比是提议机制，作者明确非决策因果归因。外部LLM将解释映射预定义伪迹分类，分类表外主张被丢弃；空映射或伪图判真也记最大CHAIR/Hal惩罚，故Hal不等于纯已输出幻觉率。伪迹分数仅假样本，ACC全部真假；白盒/高频/细节保留限制明确。纳入强相关核心，完整38参考逐条初筛39CSV，Qwen3.5博客23作为资源不当独立论文。
- DFP-Net用IAPR保存的IJCB2023官方接受列表确认题名与4作者Fatima Khalid/Ali Javed/Khalid Mahmood Malik/Aun Irtaza，纳入方法核心但范围仅官方题录；DOI原页/注册API失败，全文未取得，原型是否进入分类路径/干预/独立用户实验未知。相邻TOC的Korshunov等不误当本篇作者。未继承二级综述描述为已核实验。Union-Saliency作者公开稿网页工具失败，正常TLS curl20秒握手失败(exit35)，不关闭证书验证；其攻击对象与直接解释相关性继续待正文，不从搜索摘录作确定排除。
- 本轮补充Web104–109各返回结果保留16初筛；4个Web原页/题录失败与Union正常TLS失败另计15审计，新人工来源2条。当前原页/主题录尝试2116，核心64/英文63（含通用迁移基础1）/中文1；英文待核333、迁移方法223；候选7763含噪声，旧337重匹配207。其他参考位置1217=原1179+Look38，EFR56另计，非独立相关篇数或被引全文全已核。Scholar正常路线69、10844位置、66可见终页/56无已观察风险、GS070当前阻挡/13未决均不变。没有开始方案/模型实验。
- 全流水线export→build→enrich→checkpoint→term→English→partition→index成功；零解析失败，64核心/EFR首位/Look惩罚条款和DFP官方列表范围断言通过，GS070当前非终页/rows0、38参考SHA与CSV读回通过。python3 -m compileall -q work/literature_research_20261005、git diff --check通过；42件ZIP testzip及逐字节比较通过（9,551,734字节）。无模型代码修改/推理，不需模型测试。输出42件保持未完成。
- 浏览器2，标签1 resumedScholar仍GS070验证码；标签2 englishPrimary已用于Look作者HTML并核38参考，源页可继续参考链；旧Drive下载标签3前次挂起未处理，不当文件成功。两有效标签继续markHandoff。用户真正恢复后先核结果再读引用入口/版本；不再等待已恢复的SSRN题录，SSRN正文仍缺。继续未核英文原稿/强相关前后向链；保留来源范围，不因核心数量增大宣称重检完成或零遗漏。

## 2026-10-07 SSRN恢复核查与新的Scholar验证断点（重检未完成）

- 仓库 `brodyZhao/my-research-project`，分支 `codex/forensic-explanation-literature`；索引提交 `c9830a42e31410a705125ef23c5b867b2f2d26bf` 已推送。此交接随后单独提交/推送，最终提交见 Git HEAD。用户两个未跟踪文件保留；仅索引/HANDOFF入Git，原稿/网页/outputs留本地。
- 用户回复“SSRN已恢复”后实际核到SSR​​N6811534正常原页：Addressing the Shortcomings of Spatial-Domain Tools in Explaining Synthetic Image Detection Models；Aditi Ramaswamy、Hana Chockler；Posted2026-05-22、41页、DOI10.2139/ssrn.6811534。题录明确预印本，未核期刊出版。原摘要直接质疑空间后验可视化是否含真假分类决策信息，高度相关，升级为原页复核核心第6；没有把摘要批评推广为所有XAI无效。
- 展开所有公开关联41参考位置，38CSV逐条初筛；这是SSRN关联题录列表，非已取得原稿参考表完整性核验。5 Cochran1977与32 Rosenthal1991没有题名，保留身份待核，不猜题名或加入论文计数；37题名截断待核。部分作者字段混入会议编辑者，保留原串并注明。现在EFR56另计，其他参考位置1179（原1138+41），非独立相关篇数/被引全文全部已读。
- 原页下载控件名称为“PDF iconDownload This Paper”（DOM无空格）；正常下载等待20秒无文件，浏览器公开PDF入口新临时标签实际回题录，Web同一公开PDF URL403；Downloads定向查所见文件名未找到。不能记为全文已下载/方法已核；题录成功与PDF失败分别保存，正文实验、空间/频域度量和统计协议仍待核。本次无新SSRN验证码；不要再等待SSRN恢复。
- Google Scholar新GS070完整题名查询真正显示“请进行人机身份验证”，footer=false、rows0，虽然摘要计数显示1；captcha=true，非零命中/终页。已异步请用户完成Google验证回复“学术已恢复”，当前尚无恢复回复。Scholar标签1 resumedScholar保留当前GS070挑战，实际URL不含年份/cites过滤；SSRN原页标签2 englishPrimary正常。临时SSRN PDF标签4已关闭，旧Drive下载标签3取句柄超时未能显式关闭，未再标handoff；不要据下载页存在宣称PDF成功。两有效标签已markHandoff。
- 当前70原始route编号、69正常范围路线；1136原始观察排除误导航1后1135Scholar观察；10844逐位置日志不变=10819正常+25过滤。66可见终页、56无已观察分页/索引风险，13未决（含GS070当前阻挡）。核心62篇，英文61含迁移基础1/中文1，英文待核335、迁移候选221；候选7743含噪声，旧337本轮重匹配206。2109原页/主题录尝试历史记录不覆盖。27英文排序、38参考表、00/14/30/索引与ZIP已更新，仍标未完成，未进入方案/实验阶段。
- 来源选择修复：enrich此前按文件名最后覆盖同URL，导致已恢复SSRN在04主目录仍显示历史安全阻挡。现在优先人工明确证据，再选成功题录；所有历史失败仍留15审计。旧阅读evidence_path可能指原始文本而非JSON对象，初次加载失败后已修复按raw_path匹配/仅有效JSON记录读取，兼容旧记录。修复后全流水线成功，SSR​​N当前恢复状态与历史阻挡同时保留的回归断言通过，62核心/EFR首位/GS070非终页/41参考SHA与CSV读回通过。python3 -m compileall -q work/literature_research_20261005、git diff --check通过；41件ZIP testzip及逐字节比较通过（9,527,213字节）。无模型修改，无模型运行测试。
- 下一步只继续重检：用户恢复Google后先核GS070正常结果，记录题名版本/实际引用入口，再继续原稿与强相关引用链。SSR​​N正文没有取得，不要重跑旧新增脚本覆盖后来升级的阅读范围。流水线顺序仍export→build_research→enrich→build_checkpoint→build_term_coverage→build_english_focus→build_english_partition_audit→refresh_phase_index；输出公开主表去snippet后不能单独enrich。当前安全验证来自Google，与已恢复SSR​​N区分。

## 2026-10-07 英文优先扩词、评价器与人类实验核查（重检未完成）

- 仓库 `brodyZhao/my-research-project`；分支 `codex/forensic-explanation-literature`；最新阶段索引提交 `f6f61b22e7c9c203193dc0a132136f58d0350823` 已正常推送。交接随后另行提交/推送，最终交接提交见 Git HEAD。仅跟踪检索索引和本交接，用户两个未跟踪文件不动，work/outputs 原稿不上传。
- 用户已恢复中文GS050第2页，并明确英文最重要、低相关中文可不计入。GS050恢复10行，累计20位置；降低后续宽中文噪声分页优先级，不记查完。33术语族均已有代表性直接查询，非整体召回率或全部词组合穷尽。新完成GS051篡改忠实性261、GS052元评估18、GS053人类评价415、GS054对抗攻击327、GS055用户信任140、GS058信任校准136实际位置。GS054估计631→327，GS055883→160/空尾页；互补GS056≤2025到170、GS057≥2026到140，仍保留索引风险。
- 新增GS067合成图像解释裁判22页190位置，估计622→213且3空尾页；GS068≥2026到21页201位置，GS069≤2025到10页90位置且估计210→36空尾页。三者仍索引风险，年份补查非总体时间排除。37CSV分别记录GS054补查32、GS067补查102个新题名位置（后者99规范化题名），包含噪声/重复/版本，非新增相关论文数量。GS059对抗解释评价前向46、GS062 SNIPPET前向12、GS064 ForenX前向6、GS066 RewardBench前向1到可见终页。GS060缩写查询首10行遗留cites，单独SCOPED保留，由GS061完整题名无过滤1行替代。
- 当前69原始route编号、68正常范围路线；1135原始页面观察，误导航1页排除后1134 Scholar观察；10819正常位置+25遗留过滤位置=10844逐条日志。66可见终页，其中GS007显示上限、9条索引变动；56条无这两类已观察风险，不当索引召回率。12条未决见05。候选7724含噪声、旧337本轮重匹配205。2107条原页/主题录获取尝试、另DDL被引40题录请求，缓存人工阅读不混计新获取。
- 人工原页核心61篇，英文60（含Danry通用文本信任迁移1篇另标）、相关中文1。新增21篇有逐篇摘要/选定正文核查范围，EFR仍列首；英文待人工候选336、迁移方法220，均非已核相关论文。27英文排序、28中文不计入记录、29英文待核、30计数、33方法候选已生成。中文473暂不计目录、4待核，日志保留，不声称逐篇全文排除。
- 用户此次完成的是Wiley EAI DOI10.1111/exsy.70222安全验证：核5作者、首次2026-02-04/期号2026-03-01、公开摘要16方法/Co12的7属性及141参考。Read full text实际订阅拒绝，指标正文未读；32CSV141位置初筛。另新增SGEVL15、FKG90、Mansoor24、SNIPPET66、Cooper50参考审计，与原752参考位置合计1138，非独立相关篇数；EFR56另计。SNIPPET38缺明确题名、Mansoor6/7版本同题、EAI70/71重复TCAV及132 DF40卷号错误线索保留待核。
- XPlainVerse公开PDF正常TLS下载50页20,506,923字节，SHA74e6f13dc0db507701f5ef56041065319cb9d4b802aaa53001bd25b35500017b；§3.2/4/5/B/I已读。Entity/Evidence用Qwen3.5-4B对解释文本与参考匹配，不直接对图像或模型因果路径验证；12标注者/2000图，重叠10例5人，0.5/0.44非kappa，纠正初步100例误读。SNIPPET公开接受稿30页含封面17,191,714字节SHAba288b721a337bde8b5abaa8606ac12839e33d4e005fa291d22ded090e3d54db；§4–8已读，161人/1542票/562用户标注，§8为70合成标注；SIM/CC人类重合不当模型因果真值，只允许正确辨假者标注与矩形污染等限制保留。
- Cooper DOI10.1145/3706599.3719870通过作者Huw Jarvis主页公开Drive查看器读全部7页，下载事件未返回，不声称本地PDF成功。最终285人、建议算法约75%正确/实测72.76%，不是训练鉴伪模型；无独立无AI组，未操纵解释。整体人机67.86%不超过算法，信任关联不当随机信任因果效应；50参考位置36CSV，区别二级网站47参考估计。BMVC2025 Visual Saliency原稿14页§3–4已读，题名fidelity为数据逼真度/训练检测性能，非解释忠实性；参考链待补。
- 新增ForenX、FakeXplained、AIFo、ForgeryGPT、AIGI-Holmes、XAIGID-RewardBench原稿评价核查。ForenX20人100图、GPT裁判三次重复，附录v3/v4检测下降保留。FakeXplained1525为去中立票非人数，宽容质量阈值与人工对齐非因果真值。AIFo充分性由代理定性判断、记忆50错例恢复非整体增益。ForgeryGPT采用v4七作者，与旧引用六作者/题名差异待版本归并；5人100全伪图、信心只保持/增高不当依赖校准。AIGI-Holmes CVF官方检索题录ICCV2025 18746–18758确认，原页403保留，正文读arXivv2。RewardBench四类人类一致68%，98.3%为明确胜者条件子集；88.76%同样二类子集，四类模型最佳68.92%，不能混作整体可靠率。上述新强相关完整参考链仍待補，不把正文读过等同全部引用闭环。
- 目前Scholar没有人机阻挡。另SSRN6811534最高优先级原页持续停“正在进行安全验证”，正常浏览器重查仍未恢复；已异步请用户手动检查，尚无新恢复回复。Wiley恢复不等于SSRN恢复，不刷新挑战/自动完成验证；失败证据脱敏存focused_primary_SSRNvalidation20261007.json。浏览器2，Scholar标签1 resumedScholar当前GS069末页含as_yhi=2025，后续不限年检索必须移除年份chip或经实际首页；标签2 englishPrimary当前SSRN挑战，留给用户。两个标签markHandoff保留，后续恢复需先核正常正文，不能据“已完成”盲记成功。
- 修复export_scholar_log同页压缩引用：逐行解析后立即写缓存，以前5个缺引用解析错误及批次后页已重新导出，原始观察保留，当前零解析失败。enrich新增各引用链/原稿证据；build_checkpoint更新索引风险（非空尾页估计大幅下降也标）、英文范围、计数、SHA与输出脱敏；Cooper引用跨行DOI须严格10.x/suffix匹配，避免截断身份。不要仅enrich公开已去snippet目录：export→build_research→enrich→build_checkpoint→build_term_coverage→build_english_focus→build_english_partition_audit→refresh_phase_index。旧add_early_methods/add_downloaded_primary会重置后来升级的阅读范围，切勿无理由重跑覆盖Cooper/XPlainVerse。
- 验证：全流水线成功；10844位置ID唯一/理由、EFR56 SHA、引用表620/33/15/32/52/15/90/141/24/66/50行与源SHA、CSV读回、页码连续、过滤/验证非终页、61核心连续排名、EFR首位/新论文存在断言通过。40件输出ZIP testzip及逐字节比较通过（9,508,904字节）；python3 -m compileall -q work/literature_research_20261005、git diff --check通过。这些是文件/覆盖一致性检查，不证明零遗漏；没有模型代码修改/训练/推理，所以没有模型测试。
- ChatGPT Web下一步只继续重检，不进入方案/实验：用户恢复SSRN后核其原稿，继续英文高相关候选、已取原稿未读部分、强相关前后向参考链和版本归并。GS067补查新强相关标题如Locate-Then-Examine、Defake-o3、SalArt-VQA、agentic forensics需原稿筛选；旧核心Mandela-Bench/VIGIL已核摘要，不能当本轮新发现独立篇数。本次未执行新基础设计。阶段输出含“未完成”状态，不应交付为最终穷尽目录。

## 2026-10-06 中文年份补查与DDL注册参考审计（重检未完成）

- 仓库`brodyZhao/my-research-project`；分支`codex/forensic-explanation-literature`；最新索引提交`1fa5bdf68be0e06789b1df2ce0ed458961659c46`已成功推送。之前GitHub:443 TLS连接失败现已恢复；本次正常push从远端c75ade7推进到1fa5bdf，包含此前待推送提交，没有关闭TLS校验。本交接随后单独提交并推送，最终交接提交见Git HEAD。
- 用户完成GS045第8页验证后继续：共31个有结果页面310位置，再观察两个空尾页且末页无Next。其估计1680→915/440/272，分页出现非十步链接，不当索引穷尽。GS049“图像鉴伪 解释 忠实性”≥2016互补段26个有结果页面260位置，空第27页估计138（之前654/393），也独立标索引变动风险。GS050≤2015首10位置已保存，第2页start=10实际Google reCAPTCHA及“进行人机身份验证”复选框；已通过异步问题请用户手动完成，当前没有恢复回复。不能处理为零结果/终页。互补年份不是总体年份排除。23CSV差集138个新题名位置，含噪声/重复，不是138篇新增相关文献。
- 当前50路线、899原始页面观察（1误导航页排除）、898Scholar观察；8653正常范围+15遗留cites过滤=8668逐位置日志。48路线可见终页，45无两类已观察风险；GS007显示边界、GS045/49索引变动、GS037错误弯撇号已由GS038替代但原始宽匹配未到末页、GS050当前受阻共5条未决。22表33术语族29直接主题查询，4族未直接检索，不当整体召回率。未进入研究方案/模型实验。
- 新核DDL: Effective and Comprehensible Interpretation Framework for Diverse Deepfake Detectors，DOI10.1109/TIFS.2025.3553803，Zekun Sun/Na Ruan/Jianhua Li，TIFS20:3601–3615、2025（注册只有年份，具体日期待核）。读取既有出版社HTML公开摘要元标签，不当全文；启发式/分割/解析、图像/频域/视频检测器与fidelity声明高度相关，但具体指标/扰动基线仍待核。区别同缩写DDL数据集。本次IEEE刷新418失败保留；Crossref主DOI题录成功，以certifi正常TLS校验获取，无关闭证书校验；不使用注册提供的出版社staging相似性检查链接。
- DDL出版方注册52个参考位置全部逐条初筛，24CSV，非原稿全部参考/所有被引全文核验。40个有DOI记录题录请求38成功、2失败（3号DataCite arXiv DOI向Crossref查询404；22号CORE DOI请求429）保留25CSV；3号另由arXiv原页确认VAE，22号二级DOI映射+CVF官方检索题录匹配CORE，CVF原页403，映射/正文仍待核。3个GitHub/解析资源位置不当论文，仍在52行审计中保留；49个论文位置加入候选引用链。原稿参考列表是否比注册列表更多仍待核，不引用二级网站“57参考”作已核数量。
- Pinhasov等XAI-Based Detection of Adversarial Attacks on Deepfake Detectors，arXiv2403.02955，首发2024-03-05/v2 2024-08-18，5位作者题录已核；正文§3.4–3.5/4和表3–4人工读取，解释图用于攻击检测，去图基线及保持图接近的攻击与解释敏感性相关，主要检测终点不能证明解释因果忠实。作者TMLR2024注记与HTML生成页眉2026不混作首发；正式 venue 独立核验待补。
- 原页复核核心40条，EFR仍排序首位；DDL第15、Pinhasov第29，排序按相关性，不代表证据质量或全文全部读完。候选6557含噪声/待判，旧337本轮重匹配191。EFR56原页逐条排查保留；11种子620+Beyond33+Escalate15+中文GNN32+DDL注册52=其他752个参考位置初筛，非752篇独立相关论文或被引全文都读完。
- 2052条候选原页/主DOI题录获取尝试记录成功/空响应/失败；DDL被引40次注册题录请求单独审计，缓存人工阅读记录不混计新获取。新Web查询结果逐块保存/16单独初筛，不充当Scholar位置。原稿/完整网页留在work，输出以题录、理由、证据哈希交付，不分发完整文章。当前outputs28件及ZIP已刷新；Git仅跟踪索引/HANDOFF，保留用户两个未跟踪文件。
- 代码修正：readResearchPage/walkResearchPages必须检查footer，即使header-only已有摘要计数也不记终页；GS045第10页短暂加载未完已重读补齐，导出最新完整记录。build_research估计支持“获得/找到”，新增index_instability_risk与明确非穷尽解释；enrich加入DDL引用链/人工证据URL，过滤资源不作论文；build_checkpoint检查52注册位置和40请求及所有逐位置ID；refresh_phase_index正确记录GS049/50和新断点。不要仅enrich已经去掉snippet的public master，应export→build_research→enrich→build_checkpoint→build_term_coverage→refresh_phase_index。
- 验证：export899/8672原始观察零解析错误；build/enrich/checkpoint/term/index成功；8668位置ID唯一/理由非空、EFR56 SHA、620/337/40 CSV读回、33/15/32/52引用行与源SHA、DDL38/40元数据成功、页码连续、验证非终页、核心连续排序、EFR首位和两个新核心唯一通过；06/08验证参数脱敏断言通过。28件ZIP testzip和逐字节比较通过（7794702字节）。python3 -m compileall -q work/literature_research_20261005、git diff --check通过；这些是文件/覆盖一致性验证，不证明零遗漏。没有模型修改/推理，故无模型测试。
- ChatGPT Web下一步只继续重检：先等用户完成当前GS050第2页验证，核对正常页面后再捕获，沿实际Next继续；不要重新刷新当前挑战/自动完成CAPTCHA。剩余4个直接主题术语族为image manipulation、人类评价/用户信任、adversarial explanation/intervention、meta-evaluation，仍需执行；核心前向链/后向被引原稿/版本继续核。用户强制重检完成才能下一阶段。当前CUA浏览器2、Scholar标签1（provider browser-use:ec71204e-6c3c-46e0-8c6e-64343f4534fd），resumedScholar；已markHandoff保留，临时源页无须再下载。新运行时已重建readResearchPage/walkResearchPages/emitResearchBatch与引用缓存，walk返回最后page对象，searchResearchRoute未重建；压缩引用仅包含新运行时已输出观察，导出读取本对话既有session还原全量。若运行时再重置按文档重建，不读取隐藏浏览器状态。

## 2026-10-05 中文正式稿核查与Scholar第8页验证断点（未完成）

- 仓库`brodyZhao/my-research-project`；分支`codex/forensic-explanation-literature`；最新索引提交`c75ade77ec063860c1b492983a5d633d0c125537`已推送。本交接随后单独提交，最终交接提交见Git HEAD。审批已正常恢复；交接提交f92b85c两次推送因GitHub:443 TLS连接错误失败，远端最后确认c75ade77ec063860c1b492983a5d633d0c125537。本地文件/提交完整，未关闭TLS校验或更改remote。
- GS046“深度伪造/自解释”4个结果、GS047明确“图像篡改/忠实性”零命中、GS048“图像鉴伪/可解释”1个结果均到可见终页；零命中仅当前短语边界，不证明没有相关中文论文。返回GS045宽中文查询第8页start=70时，于21:23观察Google reCAPTCHA及“进行人机身份验证”复选框；已请用户手动完成，当前尚无恢复回复。前7页70位置已保留；待恢复继续第8页，不当零命中/终页。Scholar标签2须保留。未开始下一研究/实验阶段。
- 期刊正式稿“面向深度伪造检测的高效自解释图神经网络”下载成功，本地原稿`work/literature_research_20261005/raw/SE_EffGNN_official_v2.pdf`、提取文本同目录上一级。PDF9页，§2.3.2–2.3.4及结束语人工核对；解释主要为内部特征/距离/注意力top30可视化，敏感性与消融以检测AUC/ACC评价，未见独立解释忠实性协议。采期刊正式题录6作者、43(4):1229–1237、优先2025-09-25/正式2026-04-05；PDF字体人名缺字不擅自改写。全部32条参考按列提取且逐条初筛，21CSV；被引原文未全部取得。下载事件设置40秒工具超时，但后台实际返回约7071秒；已取得文件，后续不要重下载，避免重复长阻塞。
- 当前48路线、844原始页面观察（1误导航页排除）、843Scholar观察；8143正常范围+15异常过滤=8158逐位置日志。46路线可见终页、45无显示上限风险。原稿复核核心38条；SSRN6811534只人工Scholar复核，不混计核心原稿核验。候选6164包含噪声与待判，不是相关论文数量。原页获取尝试2044条（含同URL不同尝试）。EFR56原页排查保留；11种子620+Beyond33+Escalate15+中文GNN32=其他700参考位置初筛，非700独立相关论文/原稿全部读完。
- 新增22号术语覆盖审计：33术语族中29族有实际直接主题查询，剩余4族没有直接查询；不冒充整体召回率或全部词组合覆盖。48路线含题名、版本、前向引文入口，须与主题查询区别。GS007显示边界、GS037错误弯撇号查询已替换但原始记录保留、GS045当前受阻均公开说明。
- 本地输出25件及ZIP已刷新；00/12/13/14/17/21/22一致。build_research/enrich_catalog/build_checkpoint/build_term_coverage运行成功；导出零解析错误；EFR56证据SHA、8158/620/337/38 CSV计数、33/15/32新增引用表理由与SHA、页码连续、验证阻挡非终页、ID及核心排名连续均通过。额外断言EFR列首、中文GNN存在、06/08不含本次网络地址/验证码挑战参数；25件ZIP testzip与逐字节一致通过。`python3 -m compileall -q work/literature_research_20261005`通过；`git diff --check`提交前核对。无模型代码/训练/推理，故没有模型测试。
- 本轮仅跟踪阶段索引与HANDOFF，保留用户未跟踪实验日志和旧排序索引；work/outputs/Downloads原稿不提交。ChatGPT Web下一步只继续重检：用户完成验证后先核对第8页当前正常状态，readResearchPage重新捕获GS045，再跟实际Next继续。已取得原稿与失败证据无需重复取得；继续核心引用链、剩余术语/原稿与版本核查。22表未执行项应据实际路线规划，不据候选缺席声称新颖性。当前CUA浏览器2，标签2 resumedScholar为Google验证页，标签3 primaryIEEE现在为中文期刊原页；临时原稿标签可关闭，Scholar标记handoff保留。

## 2026-10-05 19:18重检继续：45条路线与新增原稿证据（仍未完成）

- 仓库：`brodyZhao/my-research-project`；分支：`codex/forensic-explanation-literature`；最新检索索引提交`246deb49c63ddc09807b2af36b1f15e4c74029df`已推送origin。本交接随后单独提交，最终交接提交见Git HEAD。此前审批额度限制已经通过正常审批恢复；没有绕过审批，也没有上传原稿/work/outputs。
- 用户18:15确认人机验证完成后，GS030第4页正常，查完6页59位置；GS020查完83页827位置。本阶段新增完成GS031/32 Beyond Accuracy题名/版本，GS033可验证性31页304位置、GS034概念瓶颈4页40位置、GS035原型忠实性9页89位置、GS036信任校准5页49位置、GS038 Escalate完整特征题名、GS039图像篡改解释不确定性34页337位置、GS041检测缺陷10页94位置、GS042正确SSRN完整题名、GS043文档解释21页208位置、GS044医学深伪6页52位置。GS045中文忠实性目前7页70位置，已观察下一页start=70；估计1680条须警惕分页上限，不能当作70条穷尽。
- 当前快照45路线；840原始页面观察，剔除1误导航页后839个Scholar观察；正常范围8138位置+遗留cites过滤15位置=8153逐条日志。43路线到可见终页、42无显示上限风险。GS007仍有边界风险；GS037弯撇号产生7.21万宽匹配，首10条保留，已由GS038完整特征题名1条替代，不能假称该错误查询到末页。GS040近似题名漏the零命中，GS041第2页找回实际题名“Addressing the Shortcomings…”且GS042成功。当前Scholar访问正常，无受阻路线，但整体重检未完成。
- 原页复核核心表37条：新增Beyond Accuracy（IEEE题录/全文I–VII）、CLIP Predictive Cues（arXiv方法、稳定性实验/附录）、Escalate（完整立场正文）、PIVOT（方法/实验/未来方向）、人机肖像校准、SEED、MIC（后3者当前原页摘要）。每篇明确证据范围与局限：TV平滑≠因果忠实；CLIP概念分类器≠原检测器解释；Escalate无框架实证；PIVOT仍由LLM判定且可执行数值验证是未来工作；肖像calibration摘要重点判准偏差，不等同ECE。EFR56原页与逐条排查保留，其他11种子620位置初筛外另新增Beyond33/Escalate15逐条参考初筛，19/20CSV；并非全部被引原文已读。
- SSRN6811534已人工Scholar复核为强相关待原稿条目，不加入“原页已复核核心”计数；Web原页403、正常浏览器标签3仍安全验证。失败PDF尝试及随后成功IEEE浏览器全文证据分别保留。现2043原页获取尝试（允许同URL不同获取尝试），1223HTML身份未审、615失败、62PDF待提取、135空响应、8份单独人工复核证据；成功不覆盖失败。候选目录6141含噪声/待判，非6141篇相关论文；旧337本轮匹配189，旧验证不继承。
- work脚本新增SSRN abstract_id身份键，防止题名小词差异分成两篇；Scholar结果人工复核与原稿人工复核分开排序。新主题清除cluster/cites/年份过滤；跨页底部守卫继续保留。build_checkpoint动态GS020/30状态和人工核心计数，19/20的33/15行与原始证据SHA256断言；获取器保留不同尝试。输出23件与ZIP已刷新，07/06/08原文/验证令牌脱敏逻辑保留。
- 验证：export零解析错误；build_research→enrich_catalog→build_checkpoint成功；EFR56 ID/理由/SHA、620/337/8153/37计数CSV读回、33/15新增参考理由及SHA、页码连续、受阻非终页、ID唯一/排名连续通过；23件ZIP testzip与逐字节比较通过；`python3 -m compileall -q work/literature_research_20261005`、`git diff --check`通过。仅检索文档，没有模型/数据流程修改，故无模型测试。保留用户未跟踪实验日志和旧排序索引。
- 下一步只继续重检，禁止先做研究方案或实验：从GS045已观察start=70继续；补剩余术语/核心前向链和相关后向原稿，保留限制与待核。CUA浏览器2、Scholar标签2 resumedScholar；原稿临时标签3 primaryIEEE现为SSRN安全页。readResearchPage外层有空DOM TypeError重读，walk闭包应绑定最新版reader；walk返回最后page对象而非数组。重建顺序export→build_research→enrich_catalog→build_checkpoint，然后ZIP/索引/HANDOFF刷新。当前阶段索引不得误读为最终结果。

## 2026-10-05 18:15继续：事实性路线恢复，Git交接提交待完成

- 仓库：`brodyZhao/my-research-project`；分支：`codex/forensic-explanation-literature`；最新已确认提交/推送为`2e9cc80dd86b83122084a610962c42dec216856e`。上一轮HANDOFF提交未执行：自动审批报告额度限制、无法完成审批（不是不安全判定），提示17:57可重试。没有绕过审批；本地交接与后续索引修改已保留，待正常审批恢复后提交。
- 用户要求继续后，18:09 GS030第3页正常补录10条；转第4页跳Google reCAPTCHA。已明确观察复选框并请用户手动完成，用户18:15回复已完成；第4页恢复正常，随后查完第5/6页，实际可见终页为第6页共59个结果位置。继续GS020广义splicing路线，当前已至第6页60个位置，下一页start=60；仍未进入研究方案或实验阶段。
- 处理Google验证重定向：作为失败的Scholar请求保留请求URL和脱敏重定向页，去除网络地址/挑战参数，不能当零结果或终页。work保留本地诊断；交付的06/08不会转发验证令牌/网络地址或导航异常全文。当前新查询/页面尚在继续，计数、ZIP和最终提交须在本阶段末再次刷新。


## 2026-10-05 再次恢复后的扩词与年份分段补查（仍未完成）

- 仓库：`brodyZhao/my-research-project`；分支：`codex/forensic-explanation-literature`；本轮检索索引最新提交：`2e9cc80dd86b83122084a610962c42dec216856e`，已推送origin。本段交接随后单独提交，最终交接提交见Git HEAD。只推进检索、逐位置筛选及检索内的原稿核验，未开始研究方案或实验阶段。
- 用户确认恢复后，GS022图像拼接2页11个位置与GS010反事实81页807个位置查到可见终页。为GS007第100页显示边界补查GS023（≤2025）55页548个位置与GS024（≥2026）56页552个位置，两段均到可见终页，126个原查询未显示的题名位置另存18号CSV；不是126篇新增相关独立论文，无年份条目及索引穷尽性仍有边界风险。
- 扩词完成GS025深度伪造/解释/fidelity共35页350个位置、GS026 forgery/explanation fidelity共4页33个位置、GS027删除/插入23页224个位置、GS028参数随机化7个位置、GS029健全性检查3页29个位置。GS030生成图像解释事实性已存前2页20个位置，第3页在2026-10-05 15:22上海时间再次返回automated queries限制，无验证码；已请用户手动确认恢复，当前无恢复回复。实际断点：`https://scholar.google.com/scholar?start=20&q=%22AI-generated+image%22+%22explanation%22+%22factuality%22&hl=zh-CN&as_sdt=0,5`。GS020原断点start=20仍待继续，其首20条含DocShield等文档取证线索，不能因splicing歧义把它整体当无关撤销。
- 当前30条路线；原始621页面观察，剔除1个误导航页面后620个Scholar观察；正常范围6034位置、异常cites过滤15位置另存，日志合计6049，比本轮开始4078新增1971。28路线到可见终页，27条无分页边界风险；未决GS007（边界）、GS020（分页）、GS030（当前限制）。规则辅助初筛和待判不冒充全文人工复核；拼接候选4570包含噪声，不代表4570篇相关论文。旧337中183条在本轮主题/引文链已有匹配，旧验证不继承。EFR56及11种子620参考位置的证据保留。
- 本轮新增人工原页复核DocShield（arXiv题录/完整摘要）及Quantifying Explainability with Multi-Scale Gaussian Mixture Models（作者PDF摘要、§4–7），核心表从28到30。GMM说明FF++、7检测器、4解释方法及XMGD分布相似度；不把相似性或与模型指标排序对应写成因果忠实性证明，正式日期仍待核。DocShield文档篡改、跨线索推理、RealText-V1专家解释直接相关，摘要检测提升不等于独立解释忠实性验证。DDL解释框架与DDL数据集不同，不能按缩写合并；其余新增强相关原页核验仍未完成。
- 本轮批量公开原页获取会话40589已结束；共2035个URL尝试（含单独GMM作者稿）：1223个HTML身份待核、62个PDF待提取、134空响应、615失败，1份GMM PDF已提取人工复核。HTTP成功不等于身份确认。新线索包括MIC arXiv2609.33441、GMM作者稿、DDL方法、Anchors2022、Memory-Anchored2508.14581、人类信任/AIES作者题名版本等；逐篇/引用链仍待补。
- 修改：work中export_scholar_log.py支持完整行/字段无损重复引用，零解析错误；build_research.py补fidelity/factuality/randomization/concept/prototype初筛用语并明确共现不等于解释可靠性；新增页面底部加载守卫。GS027第17页一度部分加载、最后一题名不完整且无下一页，已重读补齐并恢复真实下一页，未计为终页。build_checkpoint.py动态核心计数、当前受阻状态、18号分段差集；enrich_catalog.py并入单独作者PDF证据。原文只在work，本地outputs21件及ZIP已刷新；Git只跟踪索引与交接，保留用户未跟踪实验日志和旧排序索引。
- 验证：导出621观察零解析错误；build_checkpoint的EFR56条ID/理由/SHA256、CSV读回、页码连续、受限非终页、稳定ID/核心排名连续通过；另独立断言6049位置均有理由与依据、GS027为224条且不留不完整题名、核心30条EFR列首、DocShield/GMM均存在、分段差集126条、ZIP21件testzip及逐文件字节比较通过。`python3 -m compileall -q work/literature_research_20261005`及`git diff --check`通过。没有模型代码修改或模型测试。
- ChatGPT Web下一步：只继续重检。Scholar恢复后从GS030第3页实际断点继续，再完成GS020与尚未执行的同义词（证据可验证性、concept/prototype、人类信任与校准、医学/文档/中文等）及核心前向/后向链，核验未审原稿与版本。重建顺序export → build_research → enrich_catalog → build_checkpoint，最后刷新ZIP。CUA当前浏览器2、标签2，resumedScholar绑定；新函数应重新绑定避免闭包仍引用旧定义。readResearchPage包含页面底部守卫，searchResearchRoute使用expectNavigation，walkResearchPages须在新定义后重新绑定；空文档读页错误须先观察当前页再捕获，不能再次提交并丢失结果。不要把当前目录缺席用作新颖性依据，不声称重检完成。


## 2026-10-05 Scholar恢复后的续查与新限制

- 仓库：`brodyZhao/my-research-project`；分支：`codex/forensic-explanation-literature`；本轮日志、索引与普通入口限制核查最新提交为`846c90ff3a419920ac9f13284ca16dec10e79c70`，已推送origin；本交接随后单独提交，最终提交以Git HEAD为准。用户确认已恢复后，直接核对现有标签2正常显示GS021的10个结果；重新绑定全部采集函数至该标签，没有依赖已失效的旧标签1。
- 本轮只推进重检、逐条日志和覆盖状态，没有开始后续研究分析、方案设计或模型实验。GS021不可辨识性10条、GS015可靠性26页254个位置、GS009稳定性63页627个位置已到可见终页。GS007解释幻觉到第100页993个位置不再给下一页，但页面仍估计1130条，明确标注可能显示上限，须分段补查，不能记作所有索引结果穷尽。GS010反事实前61页610个位置已捕获，第62页在2026-10-05 13:39上海时间再次返回自动查询限制，无验证码；已请用户恢复，GS010断点为start=610；当前可见页为GS022限制页。随后从普通Scholar首页实际提交GS022（image splicing / explanation / faithfulness）也被同一限制拒绝，确认不仅深分页受阻；无验证码，无结果，不当作零命中。当前共22条路线；GS020及其余扩词/核心引用链仍待继续。
- 原始累计420页面观察，排除1个误导航页面后419个Scholar观察（含异常过滤和受阻页面）；有效范围4063个结果位置，异常过滤15个另存，日志合计4078条，比上阶段新增2064个位置。原始导出零解析错误；新增紧凑JSON格式仅压缩重复字段，恢复逐行所有题名/URL/题录/摘要线索/被引用链接，未省略结果位置。自有脚本显示的terminal元信息在限制页曾为true，但路线判定依据实际错误正文，受阻始终记false；不能把该元信息当成终页证据。
- 当前拼接候选3869条包含大量无关、背景与待判，不代表3869篇相关论文。旧337条有169条在本轮主题或种子链已有匹配；旧验证标签仍不继承。人工原页复核核心仍28条；没有把本轮新发现写成已读原文。EFR56条与其他11种子620个参考位置的原排查/初筛保留。
- 修改文件：本地work中的export_scholar_log.py增加紧凑日志和自有custom_tool_call_output读取；build_research.py增加预估计数、实际结果页、受阻观察与分页风险；build_checkpoint.py动态反映当前覆盖风险与受阻；对应outputs日志/候选/计数/状态与ZIP刷新；跟踪索引与前一版本HANDOFF已提交推送；本段补记提交状态。公开交付只保存题录/哈希/摘要短摘与筛选理由，不上传论文全文。用户未跟踪实验日志、旧排序索引保持未暂存。
- 验证：export_scholar_log零解析错误；build_checkpoint的EFR56条ID/理由/文件SHA256、CSV读回计数、页码连续、限流非终页、身份键生成稳定ID唯一/核心排序连续全部通过；compileall和git diff --check通过；ZIP testzip及逐文件字节比较通过。无模型代码修改，无模型测试。
- ChatGPT Web下一步：仅继续检索；Scholar恢复后重试实际断点GS010 start=610，再完成GS020；GS007必须补充分段检索而不能只按无下一页验收。扩展术语与强相关引文链仍未完成。采集使用activeScholar、readResearchPage、walkResearchPages，重建日志按export → build_research → enrich_catalog → build_checkpoint顺序。不要依据现有目录缺席作新颖性结论，不宣称重检完成。

## 2026-10-05 重新打开Google Scholar后仍受限

- 仓库：`brodyZhao/my-research-project`；分支：`codex/forensic-explanation-literature`；当前最新提交：`e2ce436e1c00eeeb20cf52b1d49b7ae26f31a3fe`。
- 用户最新约束：重新打开Google Scholar，完成重检后才允许推进下一步工作。已在可见新标签页重新打开不限语言的Scholar首页并实际提交GS021检索；2026-10-05 13:00上海时间仍返回automated queries限制，无验证码，无可筛选结果。没有推进下一阶段分析、追加非Scholar检索或宣称重检完成。
- 当前新标签页保留为恢复断点；旧采集函数引用的旧标签已失效，恢复后须将所有采集/分页函数重新绑定至当前实际标签。新标签页限流状态已通过直接DOM观察记录，不能写成零命中或终页。
- 已异步请求用户手动检查正常搜索是否恢复；未取得恢复证据前，不继续依赖Scholar的分页与扩词。没有修改旧结果数量或排序，未运行模型/代码测试；本次仅浏览器只读恢复尝试及本段状态交接，交接尚未提交。

## 2026-10-05 文献重检阶段交付（Scholar限流，未完成）

- 仓库：`brodyZhao/my-research-project`；继续分支：`codex/forensic-explanation-literature`；阶段索引最新commit：`ea4506f8935d5bee0ed0cb4d30991668209141d8`，已push origin。本交接随后另作提交；最终交接提交以Git HEAD为准。先前自动审批超时不再阻挡本轮指定索引提交。
- 用户明确要求扩大Google Scholar检索、所有结果逐条筛选日志、EFR等核心种子参考文献逐篇排查，旧目录不得再视为完整。用户回复已完成人机验证后，EFR当前被引用1条已查完；累计21路线、209个有效Scholar页面观察，其中含2个遗留cites过滤页和1个限流页。正常范围1999个结果位置，异常过滤15个位置另存，共2014条日志；15路线已观察到可见终页，6条未完成。GS007到40页仍有下一页；GS009/010/015/020未至终页；GS021在提交时返回automated queries限制，隔十分钟再提交仍受限，没显示验证码。已异步请用户手动检查是否恢复，未收到恢复回复。不得记限流为终页，亦不得声称整体重检完成。
- 本轮成果：EFR全部56条参考文献有逐条筛选理由及出版/预印本原页或作者公开稿，非56篇全部全文质量评审；REF016原页403改核作者11页ViKI PDF，REF025压缩响应与解压证据哈希分别保存。EFR有题名/作者版本变化的条目已记录，不把TruthLens/FORGE、FakeReasoning/Toward Generalizable等同ID版本当成独立新论文。另11种子公开HTML共620个参考位置提取初筛、保留未决条目，并未完成全部被引论文原页核验。旧337条全部对照，152条在本轮主题/引文链已有匹配，185条仅旧目录补回待审；旧验证标记不继承。
- 已人工复核28篇核心原页摘要，部分进一步核查方法/实验/局限；EFR列首，另有TriDF、Why Fake、Heatmap、DeepfakeJudge、JECA²、Gowrisankar/Tsigos系列、CDTS、不可辨识性、Mandela-Bench、ATAR、LaP、EditSleuth、REVEAL等。记录了因果忠实性/证据事实性/热图一致性/人工偏好不同终点及关键局限，例如ATAR评审额外只收到ATAR工具热图，DeepfakeJudge正文最高性能主张与Table4不一致，LaP格式率不等于文字忠实性，Heatmap方法结论依赖检测器和替换协议。当前2261条拼接候选包括噪声、背景和未决，不能当作2261篇相关文献。
- 交付在本地 `outputs/图像鉴伪解释可靠性_重检_2026-10-05/`：00阶段状态、01矩阵方案、02全部逐位置初筛、03EFR56条、04暂排序候选、05路线覆盖、06页记录、07EFR元数据/文件哈希、08导航异常、09种子620位置、10旧337条对照、11拼接计数、12/13核心28篇排序、14阶段计数、15原页获取尝试、16补充Web初筛、17一致性检查。ZIP为`outputs/图像鉴伪解释可靠性_重检阶段结果_2026-10-05.zip`，明确阶段交付未完成。原始网页/PDF与中间脚本在`work/literature_research_20261005/`，不上传论文全文；outputs/work按仓库规则忽略。跟踪新增索引`literature/forensic-explanation-research-checkpoint-20261005.md`已提交推送，HANDOFF本段待提交。用户未跟踪实验日志及前一任务排序索引仍保留不暂存。
- 检查：`python3 -m compileall -q work/literature_research_20261005`、`python3 work/literature_research_20261005/build_checkpoint.py`、`git diff --check`通过；EFR56条ID/理由/本地文件及SHA256相符，CSV读回计数、页码连续、限流非终页、稳定ID/核心排名唯一通过；ZIP testzip和逐文件字节比较通过。1176个候选URL获取尝试：711 HTML响应身份待核、31 PDF尚未提取、113空响应、321失败。获取成功不等于身份/结论已核验。无模型代码修改，无模型tensor/device或推理测试。
- 继续条件与ChatGPT Web下一步：待用户确认Scholar正常搜索恢复，从日志05的实际下一页继续GS007/009/010/015/020，重启GS021并落实尚未执行的扩词矩阵；核验其余核心论文全文及全部强相关引文链，人工复审规则初筛噪声、候选版本去重与未取得摘要的条目。每次重建按export_scholar_log → build_research → enrich_catalog → build_checkpoint顺序；最后一个脚本将交付JSON压缩为元数据/哈希，原始摘要全文仍在work证据中。不要把当前28篇核心表当最终全集，不依据缺席作无先行工作结论。

## 2026-10-05 EFR遗漏后的检索流程追溯

- 仓库：`brodyZhao/my-research-project`；分支：`codex/forensic-explanation-literature`；最新commit仍为`23c90379582c81317a604b291c64a55a87d8d89e`。保留此前HANDOFF、排序索引及用户实验日志的未提交状态。
- 用户质疑高度相关的EFR遗漏及检索准确率。本轮复核原检索日志、原报告和题录审计：26条Scholar路线仅4条明确至终页，其余22条无终页确认；没有专门覆盖证据接地/取证推理/多模态篡改用语的Scholar检索路线；完整前向引用链只有2条，没有完成全部核心文献双向追踪。原报告虽说明局限，仍未达到用户要求的全面检索标准。
- 责任判断：检索覆盖与停止/验收标准不足。现有页次级日志缺少全部结果的逐条筛选理由，不能准确定位EFR在发现、阅读或纳入哪个环节掉落；没有证据归因于Google索引延迟。一次遗漏不能量化总体准确率/召回率；240条题名作者核验也不能当作检索准确率。
- 本地新增`outputs/检索覆盖缺口审计_2026-10-05.md`；本段更新交接。原337条目录和ZIP未改，EFR仍未补入，重检仍未执行；目录仅可作初步候选集合，不能支撑查新完整性或“没有先行工作”。
- 验证：Python读回日志并汇总26路线/66页/636重复位置/4终页，核对审计主表251、候选86、核验240、待核11；rg检索工作原始JSON/TXT/PY无EFR题名、arXiv ID或首作者命中；`git diff --check`。没有源码或模型修改，无模型测试。
- 遗留：补同义表达和宽查询页次、核心分支双向引用、近期期刊会议/预印本，再维护逐条发现与筛选依据、回检和停止标准。本轮只是纠错审计，不能称已修复检索覆盖。此前Git自动审批两次超时的未提交/未推送状态保持；本轮未重试Git写操作。建议ChatGPT Web优先检查这一审计，并避免依据原目录缺席作新颖性结论。

## 2026-10-05 EFR论文是否收录核查

- 仓库：`brodyZhao/my-research-project`；分支：`codex/forensic-explanation-literature`；当前最新commit仍为 `23c90379582c81317a604b291c64a55a87d8d89e`。此前排序索引及HANDOFF尚未提交，保留其未提交修改，不覆盖用户文件。
- 用户仅询问 `Evidence-Grounded Forensic Reasoning for Detecting and Grounding Multi-Modal Media Manipulation` 是否在原目录。核查结果：原337条目录没有该论文，题名、arXiv编号 `2608.08009` 及作者 `Yichun Yeh` 均无匹配，确认是此前检索遗漏。原R115为TSAD（DOI `10.1145/3805622.3810582`，作者Wenzheng Liu等），不能用相似的题名后半段认作EFR的版本。
- 原始来源：`https://arxiv.org/abs/2608.08009`，作者Yichun Yeh、Yiheng Li、Xiaobo Hu、Zhen Lei、Yang Yang；2026-08-08首发；作者在Comments注明accepted by ACM MM 2026。摘要讨论解释与预测位置断开、锚定验证推理链、可验证证据-结论一致性奖励和多任务优势路由。基于摘要判断与解释可靠性高度相关，但坐标一致性不能自动认定因果忠实性。
- 主要修改仅本段核查交接；没有改原337条目录、排序名次、CSV/BibTeX或ZIP，也没有把确认论文存在写成已补录目录。测试为本地rg核查（准确题名/arXiv ID/作者均无命中）及原R115记录对照、arXiv原始页面核验、`git diff --check`；无源码或模型测试。
- 遗留/建议下一步：若继续补全目录，应为EFR分配新的稳定编号，补原始作者/版本元数据，纳入直接相关优先档并同步所有表、BibTeX、排序和计数；当前未执行这一补录阶段。此前Git写操作的自动审核两次超时阻塞仍记录在下方；本轮不将尚未同步的文件说成远端已更新。ChatGPT Web优先检查EFR与TSAD身份及其证据一致性/因果忠实性边界。

## 2026-10-04 已有文献按相关性排序

- 仓库：`brodyZhao/my-research-project`；继续分支：`codex/forensic-explanation-literature`；远端：`https://github.com/brodyZhao/my-research-project.git`。当前最新commit为此前检索交接提交 `23c90379582c81317a604b291c64a55a87d8d89e`，本轮排序尚未提交；自动权限审核超时阻塞情况见下文。
- 用户要求将已有检索文献按相关性排列。本轮不追加检索，保留全部337条记录（主表251条、候选86条）及原R/K编号，按“图像鉴伪的解释是否可信”作主题判断；未按年份、会议级别或引用量排名，也不将相关性当作论文质量或结论可靠性等级。
- 排序分6档：直接解释评价及证据验证27条；证据接地基准、受约束解释与反事实66条；可迁移评测基础和专题综述38条；普通解释方法及人类使用103条；检测/定位/置信度/取证背景与候选101条；纯音频2条。档内前列为人工整理的阅读顺序，其他条目按已有子主题顺序稳定排列；未赋造精确分数。题录待核和扩展候选保留暂定相关性标记。
- 本地新增交付位于 `outputs/图像鉴伪解释可靠性文献检索_2026-10-04/`：`09_文献按相关性排列.md`（含前20篇和完整337条排序理由）、`10_主表251篇_按相关性排序.csv`、`11_全部337条_按相关性排序.csv`、`12_相关性排序依据与记录.json`、`13_排序一致性检查.json`、`14_已核验题录_按相关性排序.bib`。完整ZIP已更新为14件文件；原01–08文件字节不变。BibTeX仍只有240条已核验主表记录，只重排文本顺序，引用键和字段未改。
- 跟踪/待跟踪修改：本段HANDOFF，以及新增未跟踪 `literature/forensic-explanation-relevance-20261004.md`（排序标准和前27篇索引）。脚本在本地 `work/literature_search_20261004/rank_relevance.py`；outputs/work按现有.gitignore不上传。未修改模型代码，未覆盖用户未跟踪的 `faithfulness_pilot_EXPERIMENT_LOG_2026-09-27.md`。
- 验证：`python3 work/literature_search_20261004/rank_relevance.py` 通过337条ID集合不变、原题录全部字段不变、总序号/主表序号连续、档次有序、CSV读回数量、原8文件SHA-256不变、240条BibTeX字段/引用键不变，以及14件ZIP testzip和逐字节一致检查。`python3 -m py_compile work/literature_search_20261004/rank_relevance.py` 与 `git diff --check` 通过。仅文献整理，无模型tensor/device或推理测试。
- 提交/推送阻塞：尝试 `git add literature/forensic-explanation-relevance-20261004.md` 时，自动权限审核没有在截止时间前完成，工具拒绝执行；依工具允许重试一次后再次同样超时。暂存未执行，因此本轮commit和push均未执行。超时本身不是动作不安全的判定；所有本地排序交付已完成。不要把本轮索引/HANDOFF误认为已在远端。
- 遗留：排序基于既有题录和已整理内容，未完成所有文献的全文审读；原检索未穷尽的页次/来源、11条主表题录待核和候选筛选缺口保持不变。下一步可在权限审核恢复后仅暂存上述本轮文件、检查diff、提交并push同一任务分支；ChatGPT Web先检查前列文献是否分别覆盖干预有效性、解释攻击、证据事实性与主观解释评价，不将这些维度统称因果忠实性。

## 2026-10-04 图像鉴伪解释可靠性文献检索

- 仓库：`brodyZhao/my-research-project`；分支：`codex/forensic-explanation-literature`；目标远端：`https://github.com/brodyZhao/my-research-project.git`。本任务从唯一现有远端默认分支 `codex/setup-github-workflow` 创建任务分支（仓库无 main/master）；开始时 HEAD 为 `28589e46502a981cf90d14d7f774adf29e24ed70`。本交接提交前最新 commit（资料索引提交）为 `64556d0d4a2de36b85a0b8eb2c693cff14b06e4c`，交接提交后以分支 HEAD 为准。
- 用户要求不设年份/级别限制、使用 Google Scholar 尽可能全面检索图像鉴伪可解释性的可靠性相关研究。用户完成 Scholar 人机验证后继续访问；本次记录26条检索/引用路线、66页、636个含重复的可见列表位置。已翻至终页的路线：Gowrisankar与Thing评估论文前向引用5页45个位置、Tsigos等定量评估论文前向引用5页49个位置、`"image forgery" "faithfulness"` 8页76个位置、`"AI-generated image" "explanation" "faithfulness"` 10页94个位置。多数宽查询未翻完，不能声称整个领域已穷尽或保证零遗漏。
- 本地交付：`outputs/图像鉴伪解释可靠性文献检索_2026-10-04/` 的详细Markdown报告、分类主表CSV、扩展候选CSV/Markdown、已核验BibTeX、Scholar页次JSON、题录核验审计JSON及一致性检查JSON，共8件；另有 `outputs/图像鉴伪解释可靠性文献检索_2026-10-04.zip`。分类主表251条、扩展候选86条，合计337条去重记录；主表240条核对题名与作者、11条待核。数量含综述、方法基础和边界研究，不是337篇直接可靠性实证。BibTeX只含240条已核验题录，统一简化为@misc，投稿前仍须补正式类型/卷期/版本年份。
- 主要修改：跟踪文件 `literature/forensic-explanation-search-20261004.md` 和本段交接；检索中间记录/核验脚本在 `work/literature_search_20261004/`。outputs与work按原有.gitignore不提交或push；ChatGPT Web只能通过Git看到简短索引和交接，无法直接读取完整本地交付件。未触碰用户未跟踪的 `faithfulness_pilot_EXPERIMENT_LOG_2026-09-27.md`，未改模型代码、未运行推理或训练。
- 核验来源：Scholar发现，arXiv/CVF/ACL/会议官网及出版社页面核对；Crossref只用于题录。作者综述目录读取152条，Crossref144条通过、7条题名差异、1条获取失败；目录自己的6,837/189数字不冒充本次检索数量。题名及年份版本差异、待核作者、模型裁判/主观评价与因果忠实性边界均在报告中注明。FUD是一般归因评价，Truthful or Fabricated是语言解释奖励投机研究，DEPO是医学视觉语言偏好优化，不能写成鉴伪实证。
- 验证：`python3 work/literature_search_20261004/build_catalog.py` 完成并通过内置唯一ID/DOI格式/作者完整性/别名清理/年份断言；`python3 -m compileall -q work/literature_search_20261004` 通过。另用Python读回CSV/BibTeX/报告/ZIP，确认251主表、86候选、240引用条目及报告ID一致，BibTeX括号平衡，ZIP testzip通过且8件逐字节一致；`git diff --check` 和已暂存索引检查通过。由于仅文献检索与文档生成，无模型tensor/device测试。
- 遗留：宽检索其余页次、所有种子的双向引文追踪、中文数据库/学位论文检索和逐篇全文质量评价尚未完成；保留11条题录待核及86条候选，不将它们当作完整审读文献。当前浏览器保留在已到终页的生成图像解释忠实性查询；CAPTCHA已解决，不是当前阻塞。没有证明检索饱和。
- 建议 ChatGPT Web 下一步：先检查索引中的扰动评估、热图对照、JECA²联合解释攻击、X-AIGD与Defake-o3证据验证路线；区分接地、主观可信与因果忠实性，再核对本项目局部干预研究与这些先行工作的重叠。若继续全文系统综述，应取得本地完整清单，补逐篇实验与证据编码、版本关系及未遍历来源。

## 2026-09-29 A 会公开数据与检测器可获取性审计

- 仓库：`brodyZhao/my-research-project`；分支：`codex/setup-github-workflow`；远端：`https://github.com/brodyZhao/my-research-project.git`；任务开始时最新 commit：`6b54aebaf10f0c1da8c2be85645d4dcf2f37cf02`。
- 用户要求核查现成 A 会图像鉴伪数据集与同时输出真假判断、解释、定位的检测器能否取得，判断是否必须自建数据集。本次只查公开会议论文、作者代码/模型卡、Hugging Face 数据卡与文件树；未下载权重/数据、未连接远程 GPU、未运行推理。
- 交付：`outputs/A会公开数据集与鉴伪检测器可获取性审计_2026-09-29.md`（outputs 被 `.gitignore` 忽略，故为本地交付件，不提交到 Git）。审计结论：可以避免从零构建大型原始数据集；FakeShield ICLR 2025 是当前最容易取得的冻结三输出系统，SIDA CVPR 2025 有公开模型与 SID-Set（但 explanation checkpoint 模型卡要求独立验证检测/定位），Omni-Fake CVPR 2026 数据与代码已公开但当前仓库未见训练好的 adapter，X-AIGD 的真实图需重建且无模型权重，FakeXplain 论文链接仓库当前为空且作者后续数据下载端点未能从本环境确认。
- 关键边界：有真假两类只够普通分类评测；若要把假图某块恢复为“对应原始真图”内容，必须确认 source ID 映射与像素配准。当前没有确认到这种可直接使用的一对一公开配对清单。使用区域删除/修复干预时则不一定需要 source-paired donor。FakeShield checkpoint 约 44.2 GB、其 DTE-FDM 约 27.3 GB；vGPU-32GB 的实际推理显存余量未验证。报告逐个附会议官方论文页、作者仓库和数据/模型卡链接。
- 主要修改文件：仅本段交接记录；未触碰用户未跟踪文件 `faithfulness_pilot_EXPERIMENT_LOG_2026-09-27.md`。`README.md` 在仓库中缺失。
- 验证：在线核对 ICLR/CVPR 正式主会论文页面及相关作者资源；`git diff --check` 已通过。无源码、模型或数据流程测试，因为本阶段没有运行代码/模型。
- 遗留：在远程主机上确认 SID-Set test Google Drive 可达、检查 FakeShield/SID-Set 的分割和数据文件清单；核实 FakeShield eval 是否避开训练样本及是否存在可审计 source-pair/配准键；再对 FakeShield 做单样本显存 smoke test 后决定是否启动小规模 pilot。建议 ChatGPT Web 下一步审阅资源选择与“像素配对替换 vs. 区域删除/修复”边界。

## 2026-09-29 下午组会汇报稿

- 仓库：`brodyZhao/my-research-project`；分支：`codex/setup-github-workflow`；远端：`https://github.com/brodyZhao/my-research-project.git`；本任务开始时最新 commit：`09dabd6e5b83dff50b3df8febba0d00d91ae9b79`。
- 用户要求生成今天下午可汇报的两周进展，突出实验选择和修正过程、读文献的启发、收获、导师问题及下一步。稿件已写入 Obsidian：`/Users/zhaomengchen/Documents/Obsidian Vault/文献阅读笔记/2026.9.14-2026.9.30/组会汇报_2026.9.29_下午版.md`；工作区副本 `outputs/组会汇报_2026.9.29_下午版.md`。
- 稿件沿时间线解释首轮选择 SynthScars/Qwen3-VL（人工伪迹 mask、同一模型输出理由/区域；4B 未缓存，临时用 8B）、80 张全假样本的 Gate 0 错误与 blur GT 反向、SynthScars 面积/重绘剂量和数据抽取排错、FF++ held-out 双向替换、X-AIGD × FakeVLM 中模板解释复现，并写入 8 篇论文逐篇启发、SIDA 候选准备状态、导师讨论问题、下一步和 90 秒口头稿。明确区分观察与因果结论，不把尚未运行的 SIDA 准备冒充模型结果。
- 验证：使用 Obsidian helper 写入实际 vault；Obsidian Markdown 与工作区副本字节一致；8 篇文献笔记路径均存在，2 个本地嵌图也在同文件夹且嵌入名称一致；稿件 12 个主章节；`git diff --check` 通过。未追加模型推理/训练。
- 遗留：主因果假设仍未决；当前模板化观察限 FakeVLM 的冻结 X-AIGD 子集及提示。下一步请导师确定研究主线（解释可靠性基准或解释决策因果依赖），并优先打通 SIDA 独立 test/GPU、人工接地审阅与局部干预阳性对照。

## 2026-09-29 X-AIGD 结果与鉴伪解释基准选题澄清

- 仓库：`brodyZhao/my-research-project`；分支：`codex/setup-github-workflow`；本次答疑开始时最新 commit：`911797610aaba77ce4de7dbc4823961733f82c6f`，本段提交后以仓库 `HEAD` 为准。
- 用户询问 X-AIGD 是否为真假判断与伪迹定位基准、是否可扩展为“真假判断＋伪迹定位＋文字解释”的可靠评测基准，以及 X-AIGD 论文主要结果。本次核对 `work/x_aigd/paper.pdf` / `paper.txt`、现有逐篇笔记和 ICLR 官方论文页；未修改实验源码或 Obsidian 组会稿。
- 源论文事实：X-AIGD 定义 AJ 与 PAD 两项任务；收集 4,000 真图及 13 生成器各 4,000 假图（52,000 假图），最终取得 3,035 张有效详细标注假图；3 层、7 类伪迹，像素级区域与类别。表 2：DRCT-ConvB AJ balanced accuracy 82.5%、归因图与伪迹 mask IoU 9.0%；AJ-only 为 89.3%，PAD-only IoU 27.2%，多任务 AJ 89.1%、PAD IoU 27.3%。附录表 13：同一多任务模型分类 Grad-CAM IoU 4.8%，AJ-only 分类归因 IoU 8.8%。表 4：伪迹区域注意力对齐使 Synthbuster 的 F1 55.9→63.2、X-AIGD F1 84.3→87.4；不能概括为所有数据集准确率均提高。附录 C.2 已定性指出 FakeVLM 模板化解释，表 10 报告 FakeVLM 真类 43.7%、假类 98.9%、平均 71.3%；与本项目不同冻结子集的 0.868 BA 不直接对比。
- 研究判断：单独把文字解释加到 AJ/PAD 后面与 X-AIGD、FakeXplain、LEGION 重叠较大；有潜力的新增基准应明确测文字的图像特异性、事实正确性、空间接地和经有效反事实检验的决策一致性，并分别报告不可评测率。X-AIGD 作者关于“较少依赖可见伪迹”的依据主要是归因图、任务对照与训练对齐，不是对原模型的直接局部因果干预；本项目当前 169/208 模板重复是单模型/子集观察，不能宣称首次发现或领域普遍性。X-AIGD 真/假为语义配对，不是可逐像素局部修复配对。
- 核验：查阅本地官方 PDF 提取文本中 §3.1–3.3、表 2/4、附录 C.2、D.3；用网页再次核对 ICLR 官方摘要和 FakeXplain 官方摘要。只进行文献答疑，没有运行模型或代码测试；`git diff --check` 通过。遗留：若正式立项，需进一步做系统文献查新、跨模型/数据集样本和盲审标注，先验证局部干预阳性对照。建议 ChatGPT Web 优先审阅基准的新颖性边界及最小可行标注协议。

## 2026-09-29 近两周研究组会汇报写入 Obsidian

- 仓库：`brodyZhao/my-research-project`；分支：`codex/setup-github-workflow`；远端：`https://github.com/brodyZhao/my-research-project.git`；交接撰写前最新 commit：`47627659f48190ee5eb22583df1c64928666a97a`，本次交接提交后以仓库 `HEAD` 为准。
- 用户要求把近两周全部研究进展、八篇相关论文和现有实验结果合成一份可用于 2026-09-30 组会的报告，保存在 Obsidian。已写入 `/Users/zhaomengchen/Documents/Obsidian Vault/文献阅读笔记/2026.9.14-2026.9.30/组会汇报_2026.9.14-2026.9.30.md`，同目录有两张结果图。工作区备份在 `outputs/组会汇报_2026.9.14-2026.9.30.md`，图表与可复核分析在 `work/group_meeting_20260929/`；这两个目录按仓库约定被 Git 忽略，Obsidian 原稿是用户交付件。
- 汇报组织为：问题定义、两周时间线与工作量、八篇 CCF-A 会议论文、9/19 单类能力门修正、9/27 面积/配对/掩膜诊断、9/28 FF++ held-out 双向替换、9/29 X-AIGD × FakeVLM 主实验、结论边界、下一步和导师问答。另附 90 秒照读版。主实验 208 fake + 109 real，AUROC 0.939、balanced accuracy 0.868；原生解释 169/208 重复泛化措辞、11/208 可自动定位；追问后 18/208 可定位，同类别接地 0/18；最终 856 个变体与 208 个 no-op 复核完整。报告明确局部模糊阳性对照失败、n=8 只是探索性，不能宣布因果错位或进入 DPO/EPO 训练。
- 主要修改文件：跟踪文件 `HANDOFF.md`；交付文件见上述 Obsidian Markdown 和两张 PNG；本地可复核材料包括 `work/group_meeting_20260929/build_analysis.py`、`analysis-output/analysis-report.md`、`stats-appendix.md`、`figure-catalog.md`、`provenance.json`、两张 PNG/PDF。未修改实验源码；未覆盖用户未跟踪的 `faithfulness_pilot_EXPERIMENT_LOG_2026-09-27.md`。
- 核验：图表构建脚本复核逐样本均值（解释框 n=8 为 −0.0268686；人工伪迹 n=146 为 −0.0082383），两图已目视检查；Obsidian 写入后逐文件字节比较通过；八条论文笔记链接对应的文件 8/8 存在，两个嵌入图片 2/2 存在；`git diff --check` 通过。此任务是已有数据整理与汇报撰写，未追加模型推理或训练，也未运行代码测试。
- 遗留：真正同类别正确接地的解释样本仍为 0；X-AIGD 局部正向对照没有通过，确认性错位率不可估计。Obsidian 文稿含绝对路径指向本地项目分析资料，跨设备阅读需同步这些资料或改成本地附件。建议 ChatGPT Web 下一步检查组会稿中“已支持/未决/已撤回”的判读边界，并优先讨论可信局部干预和盲审样本的下一轮设计。

## 2026-09-29 X-AIGD × FakeVLM 解释证据错位新实验

- 仓库：`brodyZhao/my-research-project`；分支：`codex/setup-github-workflow`；远端：`origin`；本阶段结果提交：`c217323`。
- 按用户授权在 AutoDL vGPU-32GB 上完成新鲜实验：X-AIGD 冻结 revision `92180f32030507ab54a40d6f1b88f39d6cec8178`，FakeVLM checkpoint × 208 fake + 109 SHA-256 核验 real。AUROC `0.939`（95% CI `[0.916,0.960]`），balanced accuracy `0.868`（`[0.832,0.903]`），能力门通过。
- 直接结果：原生解释 169/208（81.3%）重复同一泛化措辞，只有 11/208 可定位；明确索要证据后 18/208 可定位，独立类别接地为 0/18。最终 v2 干预共 856 条、208 no-op 全部精确复现。可干预解释框 n=8，目标-控制假图偏好差均值 `−0.0269`，UID bootstrap 95% CI `[−0.0495,−0.0085]`，生成器 cluster CI `[−0.0543,−0.0085]`；7/8 方向与依赖解释区域相反。人类伪迹参照 n=146，主效应均值 `−0.0082`，UID CI `[−0.0232,+0.0057]`，没有通过正向特异效应门。
- 判决：解释模板化/不可定位的较窄问题明确存在；强因果命题“已证明检测器依赖解释之外的另一组可识别证据”未确证。不得把 null 当成普遍不存在；也不建议本结果后直接训练 DPO/EPO。严格 ICLR/NeurIPS 主会尺度下，当前为单检测器 × 单基准 pilot，不能支持普遍性论文结论。
- QA 修正：v1 的词类子串规则把 `texture` 误判为 `text`，产生一个错误类别区域。已修复并完全重建/重评分 v2；v2 排除 4 个错误条目，v1/v2 856 个有效共同分数逐项相同。该误标组未进入最终分析。
- 交付报告：`outputs/新一轮解释与决策证据错位验证_预注册方案与结果.md`。全部脚本、冻结数据、manifest、逐样本原始输出、v1/v2 评分、日志和 v2 变体图 tar/解包副本均保存在 `work/x_aigd_decisive_study/`（git 忽略，不提交数据）。主要脚本：`build_blur_variants.py`、`score_interventions.py`、`analyze_interventions.py`。
- 测试：三份关键 Python 脚本 `py_compile` 通过；类别回归断言通过；最终 v2 manifest/scores `856/856` 唯一键一致；v2 SHA-256 与远端归档一致；所有 856 个本地输入图存在；v1/v2 有效评分逐项一致；`git diff --check` 通过。模型推理完整在远端完成，未训练偏好模型。
- 遗留：因 0 个解释类别与标注类别接地样本，无法估计预注册的确认性错位率；8 个局部解释框仅探索性；X-AIGD 区域干预本身没有稳定正向对照响应。下一步应先改进/验证正向干预操作并扩展独立检测器与数据来源，再考虑 Evidence Perturbation + Preference Optimization。建议 ChatGPT Web 审阅最终报告的因果判决、统计区间与类别错标修正，再决定是否开新一轮跨模型复现。

## 2026-09-28 无盲审表的自动化候选区域依赖结果

- 用户明确要求当前先直接验证检测器是否依赖解释所述证据，不先填人工盲审表。核查发现此前已完成自动 GroundingDINO 整段解释定位 + 同源双向 patch-swap pilot，因此复用其 held-out test 分数和统计，不另启动不改变测量定义的重复推理。远端当下 SSH/nvidia-smi 只读连通，实验产物可访问。
- 主要结果：19 个 source-video 簇、209 个变体分数。必要性 target-control gap +0.0568，95% CI [−0.0156,+0.1295]，Holm p=.3013；充分性 gap +0.0291，CI [−0.1015,+0.1580]，Holm p=.6687。目标区和 controls 的绝对移植效应都为正（+0.3065 vs +0.2773），但特异差值不确定。当前不能支持“依赖”也不能支持“不依赖”，判为未决。
- 自动定位针对整段 rationale 而非逐句 claim，且没有核验解释真实性；因此结论限于自动候选框的相对因果响应。自动化初筛无需人工盲审，但对“真实正确的解释证据”强主张仍需独立接地验证。旧 diff-derived GT mask 不用于解释该主终点。
- 新增 `outputs/不填盲审表的自动化验证结果.md`；更新 `outputs/解释证据与检测器决策依赖的因果验证方案.md`，说明盲审表对初筛不是硬门槛并收录结果。验证：核对原始 JSON/CSV/manifest 内样本数和统计；`git diff --check` 通过。未重新训练或重新打分。
- 远端只读复核：当前 FakeClue副本没有官方 mask 文件夹；`data/derived/fakeclue_ffpp/gt/masks` 中 mask 明确为阈值差分派生（summary 与逐样本 provenance 均如此），不是 FF++ 官方 mask。远端 GPU 空闲且此前 19-sample 结果可复用。
- 建议后续：先把本轮作为探索性直接答案；若要再做更强自动验证，需逐句拆分 rationale、分别做短语定位，在冻结的新增 test 子集上按视频簇检验，并先解决更可靠的操纵区域或 claim-localization 代理来源；当前 21 对 test 不足以支撑 A 会确认结论。

## 2026-09-28 框标注与实际操纵区域来源澄清

- 用户追问 claim/伪迹区域能否用方框，以及真实区域如何得知。已在 `outputs/盲审表填写说明.md` 增补标注粒度和 mask 来源说明。
- 文献核查到 FaceForensics++ 官方数据说明提供各操纵方法的 binary masks；其中 FaceSwap/Face2Face 区域较直观，Deepfakes mask 指 Poisson 融合区域，NeuralTextures mask 是 tracking 区域而未必覆盖实际改变的所有像素。故“操纵区域 mask”不能与“某条解释声称的可见伪迹”混为一谈。
- 方框可用于初始 claim 粗定位并栅格化为 mask，但作为像素干预会纳入框内非证据像素；确认性分析应尽量收紧边界并用匹配控制。claim 的真实性仍需独立判断；官方 FF++ mask 可替代手画操纵区域，但不验证文本 cue。
- 对当前实验的关键更正：此前失败的 GT mask 是由 paired image 差分派生，并非已核验的官方 FF++ mask。其小样本覆盖审计不通过；如能通过样本 ID/操纵方法/帧号关联官方 mask，应重新检查官方 mask 并单独验证干预算子。来源：FF++ 官方数据说明 https://github.com/ondyari/FaceForensics/blob/master/dataset/README.md 。
- 测试：仅文档更新；`git diff --check` 通过。无模型运行。
- 遗留：当前 FakeClue 目录是否包含官方 mask 未在本地数据盘核验（该数据不在工作站项目目录）；需要按原始序列名、操纵方法、帧号匹配后检查 mask 像素与图像尺寸。

## 2026-09-28 盲审表说明与精简模板

- 仓库：`brodyZhao/my-research-project`；分支：`codex/setup-github-workflow`；origin：`https://github.com/brodyZhao/my-research-project.git`。
- 用户询问解释接地盲审表的填写内容、是否可跳过及其作用。已新增 `outputs/盲审表填写说明.md`，解释盲审目的、逐列填写方式、自动派生字段、跳过后的结论边界与当前实验中的 mask 质量风险。
- 新增 A/B 两份各 19 行独立标注模板：`work/experiment_audit_20260928/human_claim_review_simple_rater_A.csv` 和 `..._B.csv`。模板保留样本元数据和解释文本，只要求标注者挑选一条具体 claim、评估真实性/可定位性、按条件标 mask、给置信度和备注。旧模板未覆盖。
- 验证：Python CSV 读取并确认 A/B 两份各 19 行、预填只读字段一致、人工标注字段为空；`git diff --check` 通过。无模型训练或推理。
- 遗留：远端图像路径必须对标注者可访问；实际伪迹 mask 不能默认用已审计有覆盖缺陷的 diff-derived mask 代替。人工盲审应在查看干预分数之前完成。
- 建议下一步：先确认两位标注者可读取图像，按说明各自完成 19 行；然后汇总一致性和可定位率，再决定是否重做冻结后的 test-only 区域干预。


## 2026-09-28 同源 patch-swap 必要性/充分性 pilot

- 仓库：`brodyZhao/my-research-project`；分支：`codex/setup-github-workflow`；本阶段开始 HEAD：`482fd31`；origin：`https://github.com/brodyZhao/my-research-project.git`。
- 本阶段结果记录提交：`7691511`；最终交接元数据随后提交。
- 用户要求寻找能判断检测器是否依赖其解释证据的方法。已重新连入远端现有 GPU 环境，只使用此前已准备的 FakeClue-FF++ test 图、FakeVLM checkpoint 和局部 mask，不覆盖旧结果。
- 方法：对同一 source-video 的 forged/pristine 配对作双向同源 patch swap。目标/控制区都执行 forged→pristine 恢复（必要性）与 pristine→forged 移植（充分性）；分数为固定候选的 `log P(fake)-log P(real)`。目标区来自已有 GroundingDINO claim box；每样本三个 DINO/外观匹配控制区。先前 fresh Gate0 在 21 对 test 图（42 张）通过；本轮 19 张 test forged 图有完整控制，2 张因无控制按 mask 可用性规则排除。评分 19×11=209 个版本，0 error，19 个独立视频簇。
- 结果：必要性 target-control gap `G_N` mean=+0.0568，SD=.1650，median=.0418，cluster bootstrap 95% CI [−.0156,+.1295]，exact two-sided sign-flip p=.1507，双主终点 Holm p=.3013。充分性 gap `G_S` mean=+.0291，SD=.2975，median=.0714，95% CI [−.1015,+.1580]，p=.6687，Holm p=.6687。target patch insertion 的绝对效应 +.3065、control insertion +.2773，显示局部移植普遍抬高 fake 分数，target-specific 差值不确定。no-op 精确为 0；whole-pair fake/pristine gap mean=+1.1635，95% CI [.9971,1.3242]。
- 判读：该设计比仅看绝对删除效应更直接，但现有框是整段 explanation 的自动 grounding、并未由人盲审；最小有意义效应 `δ` 也尚未冻结。当前 pilot 不支持也不反驳“检测器不依赖解释证据”；非显著不能当等效/无依赖结论。充分性 target/control 都上升提醒编辑边界有非特异效应，target-control 比较和人审质量门必须保留。
- 主要产物：`outputs/解释证据与检测器决策依赖的因果验证方案.md`；忽略目录 `work/experiment_audit_20260928/` 更新了 README、`build_source_swap_pilot_manifest.py`、`analyze_source_swap_pilot.py`、`human_claim_review_round1.csv`、本地原始分数、分析 JSON/CSV。远端新增目录 `results/stage_a3/continuation_20260928/source_swap_pilot_20260928/`。
- 测试/验证：remote manifest builder 成功，test candidates=21，manifest=19，排除=2；FakeVLM score variants 19/19 成功；审计脚本 `py_compile` 通过；实验目录 10 JSON、16 JSONL 均解析通过；source-swap 结果 CSV 与盲审模板各 19 行；`python3 -B -m unittest discover -s experiments/forensic_preference_pilot/stage_a3/tests -v` 3 项通过；`git diff --check` 通过。
- 遗留/下一步：先由两名标注者对 19 个原始解释盲审 claim 正确性、可定位性和区域，并独立画 claim/actual-artifact mask；查看分数前冻结 annotation。随后基于冻结 δ 和编辑噪声做功效分析，扩到完整 test 及更多伪造方法；只有 Gate、pair 对齐、盲审和阳性控制全部通过后才形成现象结论。此阶段不进入 DPO。
- 建议审阅 `outputs/解释证据与检测器决策依赖的因果验证方案.md` 的判读矩阵、双向公式和本轮区间；优先检查 `remote_recovery/effects_source_swap_pilot.json` 及 19 样本盲审表。

## 2026-09-28 test-only GPU 续跑与 GT 干预有效性复核（覆盖下方混合 split 结果）

- 仓库：`brodyZhao/my-research-project`；分支：`codex/setup-github-workflow`；本轮开始 HEAD：`6650090`；origin：`https://github.com/brodyZhao/my-research-project.git`。
- 本阶段实验结果记录提交：`a46d4a8`；最终交接元数据随后提交。
- 用户授权继续实验。重新连入已重启的远端 RTX 4080 SUPER（32,760 MiB）；新增运行均写入远端独立目录 `results/stage_a3/continuation_20260928/`，没有覆盖旧结果。
- **校正旧 test 估计**：原 249 对 Gate 0 输入是 228 train + 21 test；旧 242 行干预分数是 223 train + 19 test。下方/先前的 pooled 指标不是 held-out test 结果，不能用于研究主张。
- 当前 checkpoint fresh Gate 0 只打分 21 test 配对（42 图）：BA=0.9286，real recall=0.8571，fake recall=1.0000，AUROC=0.9932；视频簇 bootstrap 95% CI [0.8571,1.0000]；source-video label-swap Monte Carlo 双侧 p=0.000020。仅能说这个小型 selected pilot slice 通过 Gate 0。
- 对原有 test 伪造分数中有 GT 等面积控制的 9 张图重新跑了 95 个变体分数、9 个视频簇，无打分错误。claimed gap=+0.0251（SD 0.2219，video-cluster bootstrap 95% CI [−0.1066,+0.1654]，exact two-sided sign-flip p=0.7852，6 项证据效应 Holm p=1）；GT gap=−0.2571（SD 0.2043，95% CI [−0.3947,−0.1467]，p=0.0039，Holm p=0.0234）。GT restore `Δ` 反向，但不能解释成 detector 不依赖伪迹。
- 像素审计：242 张旧反事实记录都正确 join 到配对原图，242 个 GT restore 都严格按已有 mask 实现；但在本轮 9 样本里，diff-derived mask 对 `max-channel diff>25` 像素的覆盖中位数仅 66.1%，恢复后仍有 33.9% 阈值差异像素；23 个 GT controls 无一个是 pixel-exact no-op。No-op score=0、whole-pristine Δ=+1.0385 通过分数校准，但 GT 阳性干预不合格。
- 现阶段结论：核心“解释证据与检测器决策依据错位”仍未决。当前数据只能支持“局部 GT 测量/掩膜有效性失败，不能作忠实性因果判断”；claimed-gap 置信区间跨零，也不能支持选择性敏感或等效不敏感。停止在此数据上扩大样本和 DPO，先换独立 mask/验证恢复算子，并盲审文本 grounding。
- 本地材料（忽略目录 `work/`）包括最新实验报告 `work/experiment_audit_20260928/README.md`、分析报告/统计附录/图目录、像素审计、test-only 当前 Gate 0 JSON、GT controls 分析 JSON/CSV、原始分数、manifest、复算脚本与 `run_provenance_test_only.json`（含模型权重和输入/输出 hash）。因干预无效，本轮未绘制科学结果图。远端完整新分数也保留在 continuation 子目录。
- 测试/验证：test-only Gate 0 scorer 42/42 图完成；GT controls scorer 9/9 样本、95 变体分数，0 error；no-op exact；本地审计脚本 `py_compile` 通过；`python3 -B -m unittest discover -s experiments/forensic_preference_pilot/stage_a3/tests -v` 3 项通过；`git diff --check` 通过。未训练模型。
- 遗留：无 upstream model commit；当前 checkpoint 通过本地 config/index/三个 safetensors shard hash 标识。test 只有 21 对且干预只有 9 个视频簇。后续需全 test split、人工/独立 mask、通过的像素恢复与控制门槛、盲法 claim grounding、冻结 δ 与目标 prevalence，再讨论是否开展偏好优化。
- 建议下一位审阅者检查 `work/experiment_audit_20260928/analysis-report.md`、`stats-appendix.md` 与 `remote_recovery/effects_gt_controls_test_only.json`，尤其注意旧 pooled split 结论已明确作废。

## 2026-09-28 FakeVLM × FF++ 远端既有结果复核

- 仓库：`brodyZhao/my-research-project`；分支：`codex/setup-github-workflow`；任务开始时 HEAD：`1b617fc`；origin：`https://github.com/brodyZhao/my-research-project.git`。
- 本阶段结果记录提交：`7127254`（`docs: record remote experiment gate recheck`）；本行由随后的一次 HANDOFF 元数据提交补入。
- 用户授权继续先验证“解释证据是否真正影响鉴伪决策”的实验。此次是对远端**既有预测和干预分数**的本地重分析；没有启动新的 GPU 推理、没有修改远端文件、没有训练。
- 真假识别 Gate 0 通过：FakeClue-FF++ 有 249 个 pristine/forged 同源配对、498 张图、196 个视频簇；FakeVLM balanced accuracy 0.9096，real/fake recall 分别 0.8233/0.9960，AUROC 0.9980，视频簇 bootstrap 95% CI [0.8846, 0.9335]。结论限于此检查点与样本的真假区分能力，不代表解释接地或忠实。
- 干预复核：242 个有效样本、191 个视频簇。claimed 恢复效应均值 +0.0695（video-cluster bootstrap 95% CI [+0.0504,+0.0888]），面积较小的 claimed controls +0.0261（[+0.0158,+0.0368]），claimed gap +0.0434（[+0.0216,+0.0651]，video-cluster sign-flip Monte Carlo p=0.00014，未对该次聚类检验另做多重比较校正）。GT 恢复效应 −0.1354（[−0.1685,−0.1016]），与预期反向；whole-pristine +1.2415、no-op=0。当前文件没有 GT 等面积控制。
- 发现旧 `09_measure_effects.py` 会在 GT 等面积控制缺失时退回 claimed 控制，因此旧 JSON 的 `gt_gap` 不是有效 GT 阳性对照检验，相关解释应撤回。远端 Gate 7 还报告文本高度模板化（约 99.6% 假图解释提及 mouth），目前没有双人盲审定位证据；模型 checkpoint commit 字段缺失。
- 本阶段结论：核心“解释与检测器真实决策依据错位”仍未决。正 claimed-gap 仅是恢复算子下的敏感性，不等于解释内容事实正确或模型依赖伪迹；GT 阳性对照失败，因此不能声称支持或推翻核心现象，也不进入 DPO。
- 主要新增/更新：本地忽略目录报告 `work/experiment_audit_20260928/README.md`；聚类复核结果 `work/experiment_audit_20260928/remote_recovery/effects_ffpp_fakevlm_cluster_rechecked.json`；本交接记录。原始复核数据和脚本仍留在本地 `work/`，不提交 Git。
- 远端连接当前不可用：SSH alias 被关闭；按此前端口直连收到 public-key/password authentication failure。没有猜测或写入凭据。之前检查时实例为 RTX 4080 SUPER 32GB、数据盘 100GB。
- 测试：`python3 -B -m unittest discover -s experiments/forensic_preference_pilot/stage_a3/tests -v`，3 项通过；`git diff --check` 通过；视频簇干预重分析脚本成功，输出 242/242 有效样本及 191 个视频簇；Gate 0 JSON 已核验 249 对及配对身份检查。未运行新的推理/训练。
- 遗留/下一步：恢复远端访问后，检查逐像素 GT 恢复图与 pristine/forged 差分 mask 的一致性；补打分现有 `restore_gtcontrol_1..3`，若没有则从已验证配对重新派生。先过像素恢复/no-op/面积控制及盲法双人文本—区域核验，再判断现象；不能基于当前统计直接开始偏好优化。
- 建议下一位审阅者重点看 `work/experiment_audit_20260928/README.md` 的“远端 FakeVLM × FF++ 结果复核”与上述有效性边界，并确认在新建/复用的唯一输出目录运行重打分，保留原始旧结果。

## 2026-09-28 远端 vGPU 实例连通性复核

- 仓库：`brodyZhao/my-research-project`；分支：`codex/setup-github-workflow`；本轮开始时远端同步 HEAD：`ce2448a`；origin：`https://github.com/brodyZhao/my-research-project.git`。
- 用户要求连接已启动的远端 GPU 主机。本机既有 AutoDL SSH alias 可用，已成功连接；出于凭据卫生，交接记录不保存主机地址、用户指定端口或私钥信息。
- 只读检查确认 GPU 是 NVIDIA GeForce RTX 4080 SUPER，32760 MiB 显存（检查时空闲 32229 MiB），Driver 580.105.08 / CUDA 13.0；数据盘 `/root/autodl-tmp` 为 100G，余 59G；系统盘 30G，余 17G。
- 远端已存在约 42G 的 `/root/autodl-tmp/faithfulness_pilot`：data 约 4.9G、models 约 37G，含 FakeVLM、Qwen2.5-VL-7B 和 SDXL inpainting 等。当前本地协议指定 Qwen3-VL-8B；已检查的 `models/` 目录未见该模型，不能用 Qwen2.5-VL 静默替换。
- 主要修改：`work/experiment_audit_20260928/README.md` 增加远端实况与下一步容量判断；该文件按项目约定留在本地忽略目录。此处交接保留硬件/磁盘摘要，不记录远端地址或端口。
- 结论：现有 100GB 数据盘的 59GB 可用空间预计可容纳 Qwen3 权重和目标批次产物，无需马上扩盘；条件是复用现有 SDXL/数据、HF cache 指向 `/root/autodl-tmp` 并避免重复下载。传输前要核对远端 data manifest 与冻结协议。
- 测试：SSH 连通成功；`nvidia-smi`、`df -h`、`du -sh` 均成功。未修改远端内容、未拷贝文件、未运行模型推理；`git diff --check` 将在本地交接提交前执行。
- 遗留：运行前先检查远端数据 README/manifest 是否与当前协议一致，检查 HF cache 路径，再对 Qwen3 和 SDXL 各运行单图 smoke test；仅在容量实测不足时扩盘。
- 建议下一步：确认目标实验使用 Qwen3-VL-8B，并从本地冻结协议的候选 manifest 核对远端现存样本；随后只同步缺失文件，避免复制已有 4.9G 数据或覆盖远端旧实验产物。

## 2026-09-28 vGPU-32GB 与数据盘容量评估

- 仓库：`brodyZhao/my-research-project`；分支：`codex/setup-github-workflow`；本轮容量评估提交：`c3760f9`（`docs: estimate vGPU experiment storage`）；origin：`https://github.com/brodyZhao/my-research-project.git`。
- 用户目标：判断 AutoDL `vGPU-32GB` 能否承载当前图像鉴伪证据验证，并估算要租多大的数据盘。
- 结论：该卡可作为当前 Qwen3-VL-8B 单图推理 + SDXL fp16 单图反事实重合成的候选，但要先用 `nvidia-smi`/PyTorch 查明实例实际 GPU 与显存，并做单图 smoke test；不能假定等同或快于 RTX 4090，也未评估为偏好优化/全量微调提供算力。
- 容量建议：当前单模型验证建议普通容器数据盘 100GB，80GB 是限制缓存/数据后的最低规划；若同盘同时留 FakeVLM、Qwen、SDXL 或重复 checkpoint/cache，建议 120GB。普通容器的系统盘与数据盘分开，Pro 仅有系统盘，需分别按 100/120GB 扩容系统盘。
- 主要修改：`work/experiment_audit_20260928/README.md` 增加 GPU 适用边界、盘容量组成、AutoDL 与 Hugging Face 官方来源及租机前 smoke test 门槛。本 README 在 `.gitignore` 的 `work/` 目录，按项目约定留在本地，不进入 Git；本交接文件跟踪并推送。
- 依据：AutoDL 文档将 `4080(S)-32G` 映射至 `v-32g-p`；Qwen3-VL-8B 官方仓库约 17.5GB；SDXL inpainting 仓库全量约 20.8GB，项目脚本使用 fp16 variant，所以按全量空间保守预算。数据/输出大小基于 A3/A4 项目协议，尚未在 vGPU 实例实测。
- 测试：`git diff --check` 通过。本轮为规格与磁盘预算核对，无可运行的 CUDA 测试；未复制数据、未创建实例、未进行 GPU 推理。
- 遗留：租到机器后先检查 `df -h /root/autodl-tmp` 与根分区，把 Hugging Face cache 指向数据盘，再运行 1 张 Qwen 图和 1 张 SDXL 重合成 smoke test，记录峰值显存与耗时后再决定批量运行。
- 建议下一步：用户可按目标工作量选择 100GB（Qwen + SDXL 现象验证）或 120GB（再加 FakeVLM 对照）容量；拷贝时仅带协议所需子集，避免上传未用完整压缩数据。

## 2026-09-28 八篇相关论文阅读笔记写入 Obsidian

- 仓库：`brodyZhao/my-research-project`；当前分支：`codex/setup-github-workflow`；开始本任务时最新 commit：`b685f3463d5ee44916b1278f4eff849824c02d19`。`origin` 为 `https://github.com/brodyZhao/my-research-project.git`。
- 用户目标：认真阅读 `outputs/A会相关工作与选题验证实验设计.md` 列出的八篇正式会议论文，制作易懂中文阅读笔记，说明 CCF 级别、论文工作、A 会水平的内容依据、局限和对当前课题的启发，并存入 Obsidian。
- 交付：八篇逐篇笔记及一份阅读导航，工作副本在忽略目录 `outputs/文献阅读笔记/`；九份文件已写入当前 Obsidian vault 的 `Literature/` 目录（`/Users/zhaomengchen/Documents/Obsidian Vault/Literature/`）。
- 覆盖论文：X-AIGD（ICLR 2026）、FakeXplain（ICLR 2026）、LEGION（ICCV 2025）、SaCo（CVPR 2024）、F-Fidelity（ICLR 2025）、FUD（ICLR 2026）、Truthful or Fabricated?（ICLR 2026）、DEPO（ACL 2026 Long Papers）。按照 CCF 2026 第七版人工智能方向目录，相关会议均为 A 类；笔记特别说明会议级别不等于对单篇论文的评级。“为什么可能达到 A 会水平”是基于内容的阅读分析，不是审稿意见。
- 主要阅读结论：定位与人类解释对齐不能单独证明分类器因果依赖相应证据；SaCo/F-Fidelity/FUD 指出解释评测可能受干预方式影响；Truthful or Fabricated? 提供输入反事实与模型输出变化的近邻设计；DEPO 表明证据扰动加偏好优化已有先例，当前研究需要突出鉴伪任务中的可验证证据干预和决策因果评价。
- Zotero 本地 API 在本次执行环境不可访问，因此没有生成虚构的 Zotero 条目键/链接；八篇笔记都包含正式论文页或全文链接及 CCF 目录来源。
- 验证：九份 Markdown 文件均有预期章节；写入 Obsidian 后逐份与工作区副本逐字比较，9/9 存在且无差异。未运行代码测试；本任务为文献整理与 Markdown 文件写入。
- 遗留事项：若后续 Zotero API 可用，可按官方 BibTeX/DOI 补入条目链接；研究本身的下一步仍按实验方案先完成干预算子阳性对照和证据效应验证，再考虑偏好优化训练。
- 建议 ChatGPT Web 下一步检查：在 Obsidian 中从 `Literature/00-阅读导航与综合.md` 开始阅读；重点复核各笔记的证据边界，尤其是人工定位/解释对齐与因果决策依赖的区别。

## 2026-09-28 现象主张实验审计与 Gate 修正

- 仓库：`brodyZhao/my-research-project`；分支：`codex/setup-github-workflow`；实验审计提交：`aedd5cd27e80450eb1e0034994ea9d21e838402b`（`fix: validate evidence faithfulness pilot gates`）；上一条交接状态提交 `8d7c011`，二者均已推送到 `origin/codex/setup-github-workflow`。`origin` 指向 `https://github.com/brodyZhao/my-research-project.git`。
- 用户目标：先做能支持、削弱或推翻“模型解释证据是否真影响鉴伪决策”的现象实验，不提前训练 DPO。
- 本地可复算实验：`stage_a_full_20260919/full_scores.jsonl` 80/80 条为 SynthScars 假图，fake recall=63/80=0.7875；Gate 0 更正为 `BLOCKED_SINGLE_CLASS`。原 Gaussian-blur 记录中 claimed gap=+2.078（n=80，bootstrap 95% CI [+0.956,+3.227]，双侧 sign-flip MC p=.00058，Holm p=.00116）；GT blur 的 `Δs`=-1.601（n=79，95% CI [-2.652,-.525]），GT gap=-1.044（95% CI [-2.056,-.050]，Holm p=.046），方向与证据移除预期相反。故当前结果否定旧 blur 的因果解释有效性，但既不支持也不推翻目标现象。
- 文件变更：修复 `stage_a3/scripts/04_gate0_accuracy.py`，要求真假两类并报告 balanced accuracy、混淆矩阵、两类 recall、AUROC、分层 bootstrap CI 和置换检验；新增三个 Gate0 单测。更新 A3/A4 与 L1 文档，撤回单类假图“准确率”、将解释唯一率从接地性准入中剥离，并把“无差异”结论改为预注册等效检验。
- 审计脚本与原始 JSON 保存在本地忽略目录 `work/experiment_audit_20260928/`（包括 `README.md`、`reanalyze_stage_a.py`、`stage_a_reanalysis.json`、`gate0_reassessment.json`）。80/80 原图、GT mask、claimed mask、796/796 变体图、636/636 变体 mask 与 Qwen3-VL 权重均不在本机；本机 `torch.cuda.is_available()` 为 false。故无法重跑原模型或正确的重合成确认性实验。
- 验证：`python3 -B -m unittest discover -s experiments/forensic_preference_pilot/stage_a3/tests -v`，3 项通过；两份 Python 脚本内存语法编译通过；Gate0 CLI 将单类数据标为 BLOCKED；`git diff --check` 通过。
- 遗留事项：代码、协议和交接状态已提交并推送；审计 JSON/脚本/README 位于被忽略的 `work/`，只保存在本机。实验尚不能确认现象，因为数据/权重未挂载且无 CUDA。
- 建议下一步：从原 GPU 主机同步或挂载真假两类同域原始预测、图像、GT/人工审核 mask、反事实变体及模型权重，或接入 GPU 主机；先校准可信局部恢复算子与效应界 `δ`，在冻结测试集上以 Gate0 + GT 阳性对照准入，再测试 claimed-vs-matched-control 的等效性及现象 prevalence。完成前不启动偏好优化。

## 2026-09-28 A 会相关工作与实验验证设计

- 仓库：`brodyZhao/my-research-project`；当前分支：`codex/setup-github-workflow`；本次开始时最新已有 commit：`f6800b6a95836577cf794fb1658021621922f399`。
- 本阶段报告与交接首轮提交：`8f48af7`（`docs: add A-tier related work and experiment plan`），已推送至 `origin/codex/setup-github-workflow`。按交接规则，本段状态补充会单独提交。
- 用户要求：检索可借鉴的 A 会正式主会论文，并为研一阶段设计验证“模型解释所述证据是否真正影响鉴伪决策”的实验；用户接受 ICLR 等领域顶会。
- 主要交付：`outputs/A会相关工作与选题验证实验设计.md`（本地输出目录被 gitignore，留在工作区供用户查看）；覆盖 X-AIGD、FakeXplain、LEGION、SaCo、F-Fidelity、FUD、Truthful or Fabricated?、DEPO，以及实验流程、停止条件、当前项目 Gate 风险和后续偏好学习对照组。
- 文献均从 ICLR/CVF Open Access/ACL Anthology 官方主会来源核查；不使用 workshop、Findings 或仅 arXiv 文章作为依据。报告将“解释事实/定位正确”与“证据对同一分类器有因果影响”分开，并明确冻结模型观察不能独立证明训练成因。
- 对已有项目材料的复核结论：必须先修复 `stage_a3/scripts/04_gate0_accuracy.py` 的类别指标问题（只统计 label=1）；CocoGlide 上当前低于随机的结果不适合作为主忠实性证据；SynthScars 重合成 GT 阳性对照未通过前，`gap≈0` 只能判为未决。
- 验证：阅读 AGENTS.md、HANDOFF.md、现有 L1/A3/A4 协议；检索并检查官方会议页面和若干论文全文；输出文档内含逐篇官方链接。执行 `git diff --check`，PASS；确认报告文件非空。未运行代码、模型推理或训练；本任务是文献与实验设计，不需要代码测试。
- 遗留事项：报告位于项目约定的 gitignore `outputs/` 目录，因此文件保存在本地工作区，不会进入 Git。研究设计下一步仍需执行 Gate 0 修复和 Stage A4 仪器复核。
- 建议下一步：修正 Gate 0 后重算所有准入样本；重新检查 Stage A4 的 GT 阳性对照与 matched/random/no-op 控制；确定 primary endpoint 和最小有意义效应后做小规模仪器 pilot，再据此做功效分析。通过现象验证前不要开始 DPO。

## 2026-09-28 X-AIGD 全文核查补充（覆盖下方旧状态）

- 仓库：`brodyZhao/my-research-project`；当前分支：`codex/setup-github-workflow`；最新已有 commit：`f6800b6a95836577cf794fb1658021621922f399`。
- 本次交付文件：`outputs/X-AIGD_2026_论文拆解与可借鉴实验方案.md`。官方 PDF、全文提取与第 26 页表格渲染的工作副本位于 `work/x_aigd/`。未修改实验源码。
- 已核查 ICLR 2026 官方 29 页 PDF 的正文 §3–6 与附录 B/C/D。主要发现：论文的决策依赖论证来自真假分类归因图与人工伪迹 mask 的重合、同一多任务模型分类头与分割头的比较，以及归因对齐训练；**未做伪迹删除/修复后的直接因果检验**。更正前次“已证明不依赖”的过强表述。
- 论文报告：多任务模型分割输出 IoU 27.3%（表 2），其分类归因图 IoU 4.8%（表 13）；AJ-only 分类归因图 IoU 8.8%。数字为论文结果，未独立复现。
- 附录 C.2 已讨论 FakeVLM 的泛化/模板式解释；单独将该现象视为本课题首次发现不可行。可能的增量是直接验证模型自述证据与同一决策路径的干预一致性。
- X-AIGD 的 real/fake 是语义配对，不是像素对齐 pristine，不能直接用于 paired pixel restoration。作者仓库在本次核查时已提供数据及指标代码；实验训练代码仍标记 TODO。
- 验证：PDF 文本提取成功，渲染第 26 页并目视核对表 13；报告数据、页码和原文再次核查。未运行模型或 GPU 训练；Git 操作仍受前次权限中断约束，未提交、未推送。
- 建议 ChatGPT Web 下一步检查：阅读报告和 X-AIGD 官方论文 §4–5、附录 C.2/D.3；优先确认真假两类评测与可信反事实干预方案，再判断具体“钉子”。

---

### 2026-09-30：核实“被动图像取证”术语

- 仓库：`brodyZhao/my-research-project`；分支：`codex/setup-github-workflow`；本轮开始时 HEAD：`dbb9e53`。
- 更新本地交付 `outputs/研究方向定位_2026-09-30.md`：确认“被动图像取证”有正式文献用法。ICCV 2023 的 DRAW 论文在 related work 中用 “Passive Image Manipulation Localization” 指称既有被动篡改定位方法，并与其 proactive RAW protection 区分。来源为 ICCV 官方论文页。
- 用词建议：可称“被动图像取证”，但研究题目应加具体对象，如“被动图像篡改检测/定位中的解释决策忠实性”；被动/主动是取证信号来源维度，不等于忠实性问题的定义。
- 检查：`git diff --check`；未运行代码或模型实验。本轮仅核实正式会议论文术语并更新研究笔记。
- 遗留问题：被动取证术语成立，但项目首阶段对象（局部篡改/编辑或整幅生成图）仍未定。
- 建议 ChatGPT Web 下一步检查：结合导师习惯，选定一个带具体任务边界的课题名称；正式实验继续优先限定一类取证对象。

---

### 2026-09-30：研究方向与学科分类定位

- 仓库：`brodyZhao/my-research-project`；分支：`codex/setup-github-workflow`；本轮开始时 HEAD：`15f377f`。
- 新增本地交付：`outputs/研究方向定位_2026-09-30.md`。结论：目前最准确的方向是“被动图像取证中的鉴伪解释决策忠实性研究”，属于可解释/可信机器学习与图像取证交叉；不是主动取证或主动防御。
- 澄清分类维度：被动/主动是取证信号来源；局部篡改/整幅 AI 生成是检测对象；解释决策忠实性是科学问题。用户此前的源图区域替换与编辑 mask 思路更适合有源图对应的局部篡改/编辑，但尚未正式限定任务范围。
- 检查：`git diff --check`；未运行代码或实验（本阶段为研究方向归类与文档整理）。
- 遗留问题：第一阶段需在局部篡改/编辑检测与整幅 AI 生成图像检测中选定一类，之后才能冻结数据配对和因果干预设计。建议下一步据此收窄确认性实验范围。
- 建议 ChatGPT Web 下一步检查：确认导师讨论用的方向名称与“被动/主动”“局部篡改/整幅生成”“解释忠实性”三维区分是否清晰；基于选择的检测对象继续做数据和干预可行性审计。

---

## 2026-09-27 选题审计交接（本节覆盖下方旧状态）

- 仓库：`brodyZhao/my-research-project`。
- 当前分支：`codex/setup-github-workflow`；最新已有 commit：`f6800b6a95836577cf794fb1658021621922f399`。
- 本次任务：按 CCF A 类及用户认可的 ICLR 等领域顶会主会论文，审查图像鉴伪解释忠实性问题及 Evidence Perturbation + Preference Optimization 的可行性。
- 已阅读：edition1–4、L1 分析、Stage A 运行记录、可用原始打分、关键 Gate/干预/指标脚本。未修改研究方案和实验源码。
- 主要修改文件：仅本交接文件。复现中间文件在忽略目录 `work/topic_audit/`。
- 核心结论：宽泛的忠实性问题有研究依据且已有相关工作；本项目尚未证明具体的因果错位，也未证明其成因是缺少决策价值监督。DPO 可作为候选优化手段，但解释偏好改善不等于检测决策依赖改变。
- 确认的评测问题：`04_gate0_accuracy.py` 只统计 label=1，将假类召回率误称为准确率；解释唯一率不是接地性或忠实性的充分条件；重合成匹配对照不能自动消除算子伪影；不显著不等于不依赖。
- 测试：用 Python 构造 50 real + 50 fake、恒判 fake 的明确合成测试数据，运行原 Gate 0 脚本。实际 balanced accuracy=0.5，脚本报告 accuracy=1.0、PASS，确认漏洞。结果：`work/topic_audit/gate0_repro.json`。这些是单元反例，不是模型实验结果。
- 验证限制：未运行 GPU 推理或训练；L1 引用的后续 `results/stage_a3/` 原始产物及 `faithpilot` 包未在当前目录找到，相关数字只按已有文档报告处理，未独立复算。
- 文献核查：DEPO（ACL 2026 主会）、FakeVLM（NeurIPS 2025）、LEGION（ICCV 2025）、FakeShield（ICLR 2025）、FakeXplain 与 X-AIGD（ICLR 2026）等均核查官方来源；部分全文访问受限，不能声称已完成穷尽性新颖性证明。具体来源和判断见本任务回复。
- Git 阻塞：创建 `codex/faithfulness-topic-audit` 被沙箱拒绝；提权请求被用户中断。未创建新分支、未 commit、未 push。当前仓库没有本地 main/master，仅有现有任务分支；未擅自创建主分支或修改 remote。
- 建议下一步：先补齐真假两类、模型原始输出与数据来源审计，纠正 Gate 0；保留模板化样本，审计事实/位置/决策依赖三个独立维度；在可验证配对局部篡改任务标定干预算子，预先规定等效界限及分组统计。通过后再比较同数据预算的 SFT、普通 DPO、干预监督和组合方法，避免立即扩大 DPO 训练。

---

## Repository

`brodyZhao/my-research-project`

Remote：`https://github.com/brodyZhao/my-research-project.git`

## Current Branch

`codex/setup-github-workflow`

## Latest Commit

`1f9a050` (`docs: refresh current research handoff`)

## Current Goal

确认局部篡改图像是否具备成对反事实、独立伪迹标注与可判读检测器输出，并评估构建窄范围因果评测集的可行性。

## Background

当前目录是空项目目录，没有现有业务源码。本次建立长期协作规则和交接模板，并将 `origin` 配置为用户提供的 GitHub 仓库，后续任务可直接在独立的 `codex/<task-name>` 分支上继续。

## Completed

- 创建 Codex 长期规则文件 `AGENTS.md`。
- 创建 Codex 与 ChatGPT Web 共用的任务交接文件 `HANDOFF.md`。
- 约定任务分支命名格式为 `codex/<task-name>`。
- 约定每次任务结束前更新交接信息、提交 commit，并在 remote 可用时 push。
- 已配置 `origin` 指向 `brodyZhao/my-research-project`。
- GitHub HTTPS/PAT 认证已经成功验证。
- `codex/setup-github-workflow` 已成功 push 到 `origin`。
- 远程分支已经建立，本地分支正在跟踪 `origin/codex/setup-github-workflow`。

## Files Changed

- `AGENTS.md`
- `HANDOFF.md`
- `.gitignore`

## Key Implementation Details

- `AGENTS.md` 覆盖项目规则、测试要求、分支策略、提交/push 流程和交接要求。
- `HANDOFF.md` 记录仓库、分支、commit、目标、修改文件、测试、遗留问题和下一步建议。
- 当前没有业务代码，因此没有算法、网络结构、接口或 tensor shape 变化。

## Tests Performed

已执行：

```bash
git status
git branch --show-current
git remote -v
git log --oneline -5
git --git-dir=/Users/zhaomengchen/Documents/Codex/2026-09-08/ban/work/git-metadata --work-tree=/Users/zhaomengchen/Documents/Codex/2026-09-08/ban status --short --branch
git --git-dir=/Users/zhaomengchen/Documents/Codex/2026-09-08/ban/work/git-metadata --work-tree=/Users/zhaomengchen/Documents/Codex/2026-09-08/ban branch --show-current
git --git-dir=/Users/zhaomengchen/Documents/Codex/2026-09-08/ban/work/git-metadata --work-tree=/Users/zhaomengchen/Documents/Codex/2026-09-08/ban remote -v
git --git-dir=/Users/zhaomengchen/Documents/Codex/2026-09-08/ban/work/git-metadata --work-tree=/Users/zhaomengchen/Documents/Codex/2026-09-08/ban log --oneline -5
git --git-dir=/Users/zhaomengchen/Documents/Codex/2026-09-08/ban/work/git-metadata ls-remote --heads origin codex/setup-github-workflow
git --git-dir=work/git-metadata --work-tree=. diff --check
python3 -m compileall -q .
git --git-dir=work/git-metadata --work-tree=. remote -v
```

结果：标准 `git` 命令因当前环境无法创建根目录 `.git` 而失败；使用现有 `git-dir/work-tree` 方式检查 PASS；远程分支 `codex/setup-github-workflow` 已返回 commit `73f35df`；`origin` fetch/push 地址正确；`python3 -m compileall -q .` PASS；当前没有业务源码或业务自动化测试。环境没有 `python` 命令，只有 `python3`。

## Known Issues

- 当前没有业务源码和业务自动化测试。
- 当前 Codex 沙箱拒绝在项目根目录创建 `.git`，标准 Git 仓库初始化因此受阻；需要在后续环境允许创建 `.git` 后重新执行 `git init`。

## Decisions Made

- 使用 `codex/setup-github-workflow` 作为本次协作流程初始化任务分支。
- 不猜测或绑定未知 GitHub 仓库。
- `work/` 和 `outputs/` 作为本地工作目录，不纳入项目代码提交。

## Questions for ChatGPT

1. 后续业务源码应继续放入当前目录，还是应切换到另一个已有项目目录？
2. 是否需要在后续业务代码稳定后补充 CI、PR 模板或分支保护规则？

## Recommended Next Step

由 ChatGPT Web 读取已 push 的 `AGENTS.md`、`HANDOFF.md` 和 `codex/setup-github-workflow` 分支，继续进行协作流程检查；后续业务任务从该分支或新的 `codex/<task-name>` 分支开始。
# 2026-09-29：可定位解释模型复验准备

- 仓库：`brodyZhao/my-research-project`；分支：`codex/setup-github-workflow`；本记录修改前最新 commit：`6605eb8`。当前无本地 `main/master`，继续沿用此前同一研究任务分支。
- 用户纠正上一轮 FakeVLM 实验缺少局部证据的问题，要求换用同时输出真假、定位和文字的 A 会检测器。已核查 FakeXplain (ICLR 2026)、LEGION (ICCV 2025)、SIDA (CVPR 2025)、FakeShield (ICLR 2025)。FakeXplain 指向的官方仓库当前为空；LEGION 作者说明最终检测权重遗失；故选公开 7B 解释版权重和区域真值的 SIDA 首先复验。
- 本地交付：`outputs/可定位解释模型复验_模型审计与SIDA数据核验_2026-09-29.md`；本地代码和原始数据审计：`work/sida_probe/prepare_assets.py`、`audit_dataset.py`、`dataset_audit.json`、`score_adapter.py`、`perturb.py`、`smoke_sida.py`、`power_gate.py`、`power_gate_results.csv`。本轮按用户要求先固定了门控实验方案：单图 smoke → validation 短基线门 → 官方独立 test → 配对区域反事实与真实掩码正对照；同次输出必须含明确位置文字和对应掩码。样本量复核后，确认性目标修正为至少 55 张正确且 IoU≥0.2 的篡改图（配对差标准差≤0.5 log-odds；方差更高则加样本）。`outputs/` 与 `work/` 依项目规则被 Git 忽略，不提交模型、数据或本地临时产物。未改动用户已有未跟踪文件 `faithfulness_pilot_EXPERIMENT_LOG_2026-09-27.md`。
- 远程主机：`root@connect.nmb1.seetacloud.com:27002`；代码 `/root/autodl-tmp/SIDA`，验证集和模型 `/root/autodl-tmp/sida_probe`。模型权重现已下载完成，约 16GB；独立 Python 3.10 环境正在安装 CUDA 版 PyTorch。源码 revision `6b1c3aa9097a79849ea7aae95601854763014a9d`；模型 revision `282cffe609bea1917d9d63138a4989aac7314e2a`；数据 revision `fa7a00ee2d68579630bb81d1bdcae7d3ff9c7a81`。
- 实际数据核验：解释数据 validation 300 张，三类各 100；文字均非空；100 张局部篡改均有非零真值掩码。14 张局部篡改图像与掩码尺寸不一致；掩码面积 0.1%—50% 且尺寸一致时有 67 张预估候选（此前更窄的 1%—30% 范围有 49 张）。原始统计在 `work/sida_probe/dataset_audit.json`。这只是数据审计，不是模型实验结论。作者的独立 `test.zip` 需经 Google Drive 获取，但远程对 Drive 的请求报网络地址分配错误，尚未下载。
- 测试：`python3 -m compileall -q work/sida_probe` 通过；`score_adapter` 的合成张量 smoke 通过；`perturb` 的等面积、非重叠、掩码外像素不变 smoke 通过。SIDA GPU smoke **未运行**。
- 当时的最近一次成功登录显示远程无 `/dev/nvidia*`，`torch.cuda.is_available() == False`，设备数 0；Google Drive 官方测试包也无法从该主机访问，独立 Python 环境仍在安装。故没有任何 SIDA 推理结果。较新的远程状态见下方更新。
- 建议 ChatGPT Web 下一步检查：GPU 与官方 test 数据可访问后，先运行 `work/sida_probe/smoke_sida.py`；检查三输出同源、长短生成分数差≤0.01；再在公开 validation 执行 30 张短基线门。只有 balanced accuracy≥0.70 且至少 5 个正确、有位置文字且 IoU≥0.2 的篡改样本时才解封官方 test。确认性实验要求至少 55 张合格样本（配对差标准差≤0.5 时）和真实掩码正对照通过；按方差上调样本量。不要把现有 validation 300 张冒充独立确认性 test。

### 2026-09-29：远程实验准备状态更新

- 仓库：`brodyZhao/my-research-project`；分支：`codex/setup-github-workflow`；本轮实验门槛更新 commit：`cae84bd`（本次 HANDOFF 补记前的最新 commit）。
- SIDA-7B-description 权重已下载完成（约 16 GB）；远程独立 Python 3.10 环境的依赖安装命令已成功，含 PyTorch `2.1.2+cu121`、Transformers `4.31.0`、Accelerate `0.21.0`、DeepSpeed `0.14.0`。
- 之后尝试复查 GPU 时，`connect.nmb1.seetacloud.com` 的 DNS 解析失败，SSH 未建立；因此无法确认设备状态或做模型导入 smoke test。此前最近一次成功 GPU 检查仍为 0 张可见 GPU。没有启动推理。
- 当前仍需恢复主机名/SSH、核实可见 GPU、获取官方独立 `test.zip`。完成后先执行单图 smoke 和固定 30 张基线门；门槛失败即停止，不跑长实验。
- 在任何模型推理前复核了统计检验：旧的 36 张对应检出非零差异，不适用于“排除≥0.2 log-odds的实质区域增益”。报告现已改为非劣效门槛：当每种扰动配对差 `σ≤0.5` 时每算子约 55 张以保证双算子联合功效约 0.80；`σ=0.6/0.7` 时目标约 79/107。主样本还必须有明确位置文字、对应掩码、预测正确且 IoU≥0.2。
- 本轮测试：`python3 -m compileall -q work/sida_probe` 通过；`python3 work/sida_probe/power_gate.py` 通过并保存 CSV，复现 `σ=0.5` 时 `n=55`、每算子功效约 0.900、双算子联合功效下界约 0.801；`git diff --check` 通过。模型推理 smoke 未运行，因为 SSH/DNS 失败且此前 GPU 检查为 0 张可见设备。
- 最新交付仍为 `outputs/可定位解释模型复验_模型审计与SIDA数据核验_2026-09-29.md`；本次记录更新不改变实验结论边界：尚无 SIDA 推理结果，不能判定现象成立或不成立。

### 2026-09-29：主实验模型选择复核

- 仓库：`brodyZhao/my-research-project`；分支：`codex/setup-github-workflow`；本次修改前最新 commit：`bd4ff3a`。
- 用户指出 SIDA 模型卡对 explanation checkpoint 的限制。已核对模型卡：`SIDA-7B-description` 为解释微调版；复现检测/定位结果应使用 `SIDA-7B`。因此 SIDA-description 不再作为论文性能代表或主确认性模型，仅保留已有下载作预研。
- 主模型改荐 FakeShield ICLR 2025 官方 `fakeshield-v1-22b`：DTE-FDM 输出分类、位置文字与依据；MFLM 以 DTE-FDM 输出和图像生成掩码。核心因果检验必须直接读取 DTE-FDM 分类分数，不能把 MFLM 对解释文字的掩码跟随性当作分类依赖性的证据。
- 新本地交付：`outputs/FakeShield与SIDA主模型选择复核_2026-09-29.md`。原 SIDA 方案报告开头已加撤销/后备说明。FakeShield 权重约 44.2 GB，另有 SAM 权重、测试数据和运行缓存；远端上次只余约 40 GB。远端当前 DNS 解析失败，之前最近一次成功设备检查为 0 GPU，故尚未下载 FakeShield 或运行推理。
- 推荐候选数据为论文使用的 IMD2020 评测集（原论文表列 414 张真实、2,010 张篡改），需从原始数据源取图像与掩码并审计独立性。HF 的 MMTD-Set-34k 只有 train split，不能充当独立测试集；其中解释文字由 GPT-4o 生成，不能当作解释真实性真值。
- 本轮只核查官方论文、模型卡、权重与数据页面并修订方案，没有模型实验。后续先恢复远端解析与 GPU、检查存储/显存；再做 FakeShield 单图 smoke 和 IMD2020 固定 pilot（15 real+15 tampered）：评分与生成标签一致≥29/30、BAcc≥0.70，且至少 5 张篡改图分类正确、掩码 IoU≥0.2、文字有明确位置，才继续。门未过就停，不跑批量反事实。

### 2026-09-29：FakeShield 因果实验理论可识别性审计（本条覆盖上述旧执行门）

- 仓库：`brodyZhao/my-research-project`；分支：`codex/setup-github-workflow`；审计前最新 commit：`3dbde63`。
- 按用户要求，在下载/推理前审查旧 FakeShield 方案。官方 DTE-FDM 路径用默认温度 0.2 的自由文本生成，没有公开真假分类 logit；固定 fake/real verbalizer 的条件 log-prob 不是原检测器分数。MFLM 同时读取原图与整段文字并生成掩码，ICLR 2025 论文明确讨论它能纠正错误位置描述。因此旧方案使用 log-odds、`δ=.2`、`n=55`、以及将 MFLM mask 当作解释区域均撤销。
- 审计结论：旧设计理论上不能回答“检测器是否依赖解释所述证据”。修订后的窄问题可行：用官方生成真假判决的固定协议作为因变量；冻结原图文字；独立盲审文字事实和区域；对目标区、匹配控制区、独立标注的另一真实可见线索区做有效反事实；固定原图 DTG tag 的直接视觉效应与重新计算 tag 的端到端效应分开。只有目标区对控制等效且另一独立线索通过阳性门，才支持“区域级错位”；无阳性线索时只能判未决。
- 本地新增/更新：`outputs/FakeShield因果依赖实验_理论可识别性审计_2026-09-29.md`（完整理论和方案）；`outputs/FakeShield与SIDA主模型选择复核_2026-09-29.md`（已改为撤销旧方案并保留模型候选判断）。`outputs/` 按项目规则被 Git 忽略，文件保存在本机项目目录，不提交权重或数据。
- 本次只读核对 ICLR 2025 FakeShield 论文、官方 DTE-FDM/MFLM 代码，以及 NeurIPS 2019 忠实性论文；没有下载 FakeShield、连接远端、运行推理或产生实验结果。文献限正式 A 会主会；官方代码仅作为实现核验。
- 检查：`git diff --check` 与审计文档关键断言检查均通过；交接记录已随 `39b5270` 提交并推送。尚无模型实验结论。旧的 FakeShield smoke 和 IMD2020 门不得执行；`SIDA` 旧样本量也不能迁移到新因变量。
- 遗留硬门：固定 FakeShield 代码/权重 revision；确认严格独立、有合适配对的测试数据与 mask 语义；独立标注文字 claim 和可见伪迹；证明可构造有效且质量合格的局部干预；用生成真假判决重新定效应界和样本量。未过这些门之前不启动确认性推理。
- 建议 ChatGPT Web 下一步先审查本地理论审计文档对主张、`Y`/`p_fake`、干预定义和判决规则的解释是否清楚；后续只按修订门继续，不再沿用旧 `log-odds` 与 MFLM 区域假设。

### 2026-09-29：成对数据与自建因果评测集可行性

- 仓库：`brodyZhao/my-research-project`；分支：`codex/setup-github-workflow`；本阶段开始最新 commit：`1f9a050`。
- 用户询问缺少“成对真假图 + 同一检测器的真假/解释/定位”时是模型还是数据的问题，以及能否自建数据。本次澄清：数据集不需预存模型输出，模型可冻结后对数据推理；数据负责图像标签、源图对应、编辑 mask、独立可见伪迹与 claim 标注。模型接口和数据因果配对是两个独立条件。
- 核对 ICLR 2025 FakeShield、ICLR 2026 FakeXplain/X-AIGD、ICLR 2025 Aligned Datasets。FakeShield 最接近三输出系统，但 DTE-FDM 和 MFLM 解耦，MMTD 描述由 GPT-4o 结合图像及 mask 生成；FakeXplain 给 AI 合成图人工框/描述但不提供逐图原始源图 patch 对；X-AIGD 可作为独立人类伪迹区域参考，但不是文字 claim 真值或像素同源 donor pair。
- 本地新增：`outputs/成对鉴伪数据与自建因果评测集可行性_2026-09-29.md`，建议先限定局部编辑鉴伪，建立小型评测集而非先训练 detector 或打造通用大数据集；明确区分源图/编辑图、编辑 mask、可见伪迹 mask、模型 claim 区域、预测定位 mask。
- 本轮只做正式 A 会主会文献核对和方案说明，没有新建/下载数据、模型推理或人工标注。文档/链接和 HANDOFF 提交前待执行 `git diff --check` 与本地文件存在性检查。
- 遗留：实际审计 FakeShield 公开测试样本是否逐张同源、几何对齐、mask/图像 ID 是否对应；若不满足，先构造少量可控局部编辑 pair，运行标注与 sham/控制/阳性对照可行性门。不得把整幅生成图的语义相似真图当作局部 patch donor。

---

### 2026-10-08：Scholar 扩展子式续检断点

- 仓库：`brodyZhao/my-research-project`；当前分支：`codex/forensic-explanation-literature`；远程：`origin https://github.com/brodyZhao/my-research-project.git`。本条交接写入前协议提交为 `969139319464a5e0da339b1c38e8ec2311a18df7`；本 HANDOFF 另行提交。
- 主要修改：`literature/forensic-explanation-search-protocol-v2-20261008.md` 追加本批方法、覆盖数和未完成项。原始逐页记录在忽略目录 `work/search_protocol_v2/execution_pages.json`；路线配置/输出在 `work/search_protocol_v2/fine_split_queries.json` 和 `outputs/图像鉴伪解释可靠性_重检_2026-10-05/`，均为本地可恢复进度，不提交临时日志或数据。用户原有未跟踪文件 `faithfulness_pilot_EXPERIMENT_LOG_2026-09-27.md`、`literature/forensic-explanation-relevance-20261004.md` 未改动、未暂存。
- 本批结果：`T08-F4-S4` 获得94位置并到可见末页；`T08-F4-S5` 149位置并到可见末页。`T02-F2-S1` 估算约14,200，只保存首屏，须继续细拆。补充窄式 `"image forgery" explainable grounding` 记录350个结果位置和空尾页；估算数646/496/300波动超过25%，必须回检，不能表述为穷尽。
- 最新检索审计：107父查询、59条可见末页、13,941个主查询位置；84个拆分/诊断子式、866个有效位置、11条到可见末页；补充引用28位置；总有效位置14,835（位置可重复，不是独立论文数）；10条受阻或查询不匹配观察。23条优先候选不是全部都已证明为直接可靠性实证。完整逐位置筛选规则辅助记录见交付74，路线审计75、85、87，计数/受阻审计83。
- 测试：`python3 -m compileall -q work/search_protocol_v2` PASS；`git diff --check` PASS；归档ZIP CRC与92个文件逐字节校验 PASS。Scholar依赖用户手动完成人机验证后读取正常结果，未尝试代解。
- 遗留：大量细分路线未执行；超大/索引变化查询需进一步拆分和复查；强相关文献原稿、版本及EFR等核心种子引文递归筛查未完成。未进入实验方案阶段。不要将本阶段标为重检完成。
- 建议下一步：从 `T02-F2-S1` 约14,200规模触发器着手，进一步按“image forgery / tampering / splicing / copy-move / synthetic image”等具体任务词与解释表达拆分，并先做结果量可行性测试；随后完成对应分页和逐条筛选，再核原稿与强相关引文链。用户已授权继续，不需重复确认。

### 2026-10-08：Scholar术语扩展与TriDF引文链续检

- 仓库：`brodyZhao/my-research-project`；分支：`codex/forensic-explanation-literature`；协议提交：`705cca3`（已推送）；本 HANDOFF 独立提交。
- 主要修改文件：`literature/forensic-explanation-search-protocol-v2-20261008.md` 追加检索断点和覆盖指标。逐页 Scholar 页面、拆分式和覆盖计算留在忽略目录 `work/search_protocol_v2/`。阶段交付目录 `outputs/图像鉴伪解释可靠性_重检_2026-10-05/` 新增候选/引文筛查记录，归档为 `outputs/图像鉴伪解释可靠性_重检阶段结果_2026-10-08.zip`（95个文件，CRC及逐文件字节检查通过）。用户已有未跟踪文件 `faithfulness_pilot_EXPERIMENT_LOG_2026-09-27.md`、`literature/forensic-explanation-relevance-20261004.md` 均未修改或暂存。
- 本轮工作：完成3个篡改类型×hallucination细式的分页并记录；新增12条可靠性/任务词诊断式。精确`"image forgery" "explanation quality"`记录38位置至可见末页；精确`"image forgery" "explanation reliability"`检出TriDF。宽泛`forensic "explanation faithfulness"`估算数波动且包含大量跨域记录，标记索引不稳定。筛查TriDF cited-by页5条：其中EFR是交叉引文，TRIDENT和DF-CBM留作原稿核验候选；ForgeryGPT cited-by页1条PDF伪造研究按主题排除。新增候选的边界与来源见阶段包90，TriDF引文逐条表见89。
- 最新审计：107父式、59父式可见末页、13,941父查询位置；119拆分/诊断式、3,266位置，其中50条可见末页、38条满足现行完整判据；总有效位置17,241（含34附加筛查/引用位置，位置会重复，非独立文献数）；12条历史受阻/无效观察、当前无活动阻断。强相关优先清单23条仍混合直接可靠性评测与核心机制两层，EFR 56条仅完成题名/摘要逐条初筛，不可表述为全部全文审阅。全面检索未完成，也未进入实验方案工作。
- 测试：`python3 work/search_protocol_v2/publish_execution_round.py` PASS；`python3 -m compileall -q work/search_protocol_v2` PASS；`git diff --check` PASS；95文件ZIP CRC和逐文件字节核验 PASS。
- 遗留：继续扩展非deepfake任务词组合并对索引不稳定路线拆分回检；核读新增REVEAL、证据接地deepfake、STeREx-Net、TRIDENT、DF-CBM等候选原稿；优先追踪新增强相关种子的参考文献与前向引用；完成剩余父式分页、版本去重及逐篇原稿筛选。不能宣称“一篇不漏”。
- 建议 ChatGPT Web 下一步：从阶段ZIP的90候选表及89 TriDF引文表核查新增候选原稿与直接评价终点；再继续扩大任务术语（image editing/manipulation/localization/authentication等）与解释方法别名覆盖，并将每条完整分页与逐篇筛选理由追加日志。

### 2026-10-08：人类评价路线动态回检与可解释鉴伪综述

- 仓库：`brodyZhao/my-research-project`；分支：`codex/forensic-explanation-literature`；本阶段开始commit：`25fec01d5d75f818e5fc2c196a806bd7daed4d07`。协议和HANDOFF按项目要求分别提交；已确认远程`origin https://github.com/brodyZhao/my-research-project.git`。
- 修改文件：`literature/forensic-explanation-search-protocol-v2-20261008.md`、`HANDOFF.md`。忽略目录`work/search_protocol_v2/execution_pages.json`写入10页Scholar动态回检快照。阶段结果：72优先清单35项、90候选33项、100逐位置观察220条、新建102前向引用筛查4条。归档包需重建并验证。
- 用户原有未跟踪文件`faithfulness_pilot_EXPERIMENT_LOG_2026-09-27.md`、`literature/forensic-explanation-relevance-20261004.md`未修改、未暂存。`outputs/`、`work/`按规则忽略，不提交Git。
- 本批回看`"image forgery" "human evaluation" explanation`从start=6到start=96，新增100个观察位置；结果估算数106–117浮动。自动审计有效21页/200位置，仍缺start=100，visible_terminal=False。检出并核读《Explainable Image-Centric Forgery Detection: A Survey》，为未经同行评审预印本，明确讨论faithfulness/consistency评价缺口，列为综述/引文种子，不算原创实证。其4条前向引用逐条筛查（2排除、2边界）。新候选含Rethinking VLMs、Explaining Deepfake Detection by Analysing Image Matching、OMNI-Fake；Evidence Fusion仍待原稿。
- 当前审计：107父式、59末页、13,941位置；120个拆分/诊断式，3,466位置、50末页、38通过严格完整条件；共17,486个记录位置，含重复，不是论文数。17条历史受阻、当前无活动阻断。全量检索未完成。
- 测试：`python3 work/search_protocol_v2/publish_execution_round.py`成功。提交前需重跑`python3 -m compileall -q work/search_protocol_v2`、`git diff --check`和阶段ZIP CRC/逐文件字节检查。
- 遗留：核查综述的核心反向参考及原稿；继续未执行检索式、非deepfake任务词、索引不稳定路线；核对新增候选原稿和引文链。直接可靠性实证、机制、综述/边界要分层，不把35项说成35篇解释faithfulness实验。
- 建议ChatGPT Web：审阅综述引文错位判断与4条前向引用筛选，再从阶段包90/102继续综述反向参考筛查。


### 2026-10-08：X²-DFD解释人评复核及其关键引文链续查（整体未完成）

- 本轮开始HEAD：`c18e4683b62cf8f028e06bd4d0bb7b02116e73ad`；分支`codex/forensic-explanation-literature`，origin已配置。用户原有两个未跟踪文件保持未改、未暂存。
- 继续核读X²-DFD（NeurIPS 2025；arXiv:2410.06126v4）。正文把解释可靠性/MLLM幻觉作为动机，并用特征级balanced accuracy筛查模型可用线索；解释评价含人工标注文本相似度和0–5人工评分。官方补充材料检索片段显示15名20–40岁受教育程度较高的参与者评100个deepfake图，维度为检测能力、解释合理性、细节程度。它是强相关直接人评文献；评分仍属主观解释质量，未检验同一模型决策的因果faithfulness、sanity/randomization或用户依赖；100样本描述均为deepfake图，不能视作真假平衡设计。候选目录已把错误的2026年份修正为NeurIPS 2025 / 首发2024，并更新强相关证据层级。
- 沿X²-DFD的评价链逐篇查4条直接相关参考：FakeShield（作者全文，解释文本+区域mask；主要测检测/定位、CSS及图像退化稳健性）、FFAA（作者全文，解释VQA、专家筛训练标签；主要测检测/泛化/鲁棒性）、Can ChatGPT Detect DeepFakes?（CVF官方论文，提示式鉴伪和解释输出）及A Hitchhiker’s Guide…（OpenReview论文，分阶段细粒度VQA并定性评价回答）。逐篇理由、限制和原页在输出103。新增X²-DFD进入72强相关优先清单第8位、90本轮候选；103包含4条逐篇筛查。
- 用户Chrome当前Google Scholar cited-by断点`cites=6391361178114081016`尝试读取时出现reCAPTCHA人工复选框；未尝试代替用户验证或绕过。断点逐项记录于输出104，并已在对话中请求用户完成当前页面验证。CUA tab已标记handoff。完成验证后，先读取当前页面并从该被引列表续查。
- 当前总目录/历史覆盖计数与上一阶段相同：107父查询、59条可见末页、13,941父结果位置；120子式、3,466位置、50条可见末页/38条严格完整；累计17,486条位置（有重复，不是论文数量）。历史受阻页计数经publish脚本仍为17，因为本次用户打开的被引页不属于计划路线；新受阻单独记录在104及执行快照。全项目检索仍未完成。
- 本轮改动：tracked `literature/forensic-explanation-search-protocol-v2-20261008.md`、`HANDOFF.md`；忽略输出包括`04`候选目录、`72`优先清单、`90`本轮候选、`103`四篇参考筛查、`104`Scholar阻断记录和输出归档ZIP；忽略工作日志execution_pages.json记录此次reCAPTCHA观察。
- 测试：`python3 work/search_protocol_v2/publish_execution_round.py`、`python3 -m compileall -q work/search_protocol_v2`、`git diff --check`通过；输出ZIP需在提交前执行CRC及逐文件字节校验。
- 建议下一步：等待当前Scholar验证完成，从此cited-by页面逐条筛查；继续X²-DFD/综述的直接相关反向引用和前向引用，登记每篇筛选理由；之后继续非deepfake任务词及未完成宽式/索引异常式。直接可靠性实证、解释机制、综述/边界论文分层，勿声称零遗漏。

## 2026-10-08 TriDF被引链续检与IAB末页复核（整体重检仍未完成）

- 仓库：`brodyZhao/my-research-project`；分支：`codex/forensic-explanation-literature`；检索方案阶段commit：`fbf9901`（已推送origin）；本HANDOFF更新将单独提交，最终HEAD以Git为准。
- 用户指出Google Scholar正常后重新核对浏览器：历史Chrome标签981694126触发验证，但Codex IAB中的TriDF被引页正常显示6条记录、无下一页。已完成逐篇筛选，详情在本机交付`105_TriDF前向引用6条逐篇筛查.csv`。EFR和DF-CBM是既有强相关/机制文献，不重复计数；新候选TRIDENT、Explainable Deepfake Detection Challenge分别加入优先清单72的第8和第9位。TRIDENT通过OpenReview PDF索引可见方法/公式片段记录CHAIR和precision-weighted F0.5，论坛页本轮未能直接打开，全文待直取；两项指标支持观测伪迹接地/幻觉评测，但都不等于模型决策因果忠实性或人类恰当依赖。另两篇检测综述记为背景/待核，不纳强相关。Chrome阻断记录104已更正为历史事件、IAB恢复成功。
- 继续核实用户打开的`"image forgery" "human evaluation" explanation`：当前IAB显示106条、第10页(start=96)、“下一页”禁用。10个结果已更新到100逐条记录；仅“Machine Learning for Evidence in Criminal Proceedings”保留为司法/证据可靠性背景，其余排除。100共有220个跨快照位置，含重复观察，不是220篇独立论文。
- 最新执行统计：107父查询，59条可见末页，13,941父查询位置；120细分/诊断查询，3,466位置，其中50可见末页、38满足严格完整性判据；有效结果位置总数17,492（含跨式重复、版本/引用等，不等于独立论文）；补充位置77；18个历史受阻/无效观察，当前阻断为空。优先清单38行，新增候选表36行；均混合直接可靠性研究、基准和核心机制，不能当成38篇独立因果忠实性研究。重检仍未完成。
- 主要跟踪修改：`literature/forensic-explanation-search-protocol-v2-20261008.md`。忽略目录检索原始数据在`work/search_protocol_v2/execution_pages.json`及其execution_audit，用户交付在`outputs/图像鉴伪解释可靠性_重检_2026-10-05/`；本阶段ZIP `outputs/图像鉴伪解释可靠性_重检阶段结果_2026-10-08.zip` 含111文件，CRC及逐文件字节比较通过，SHA-256清单为`106_本次阶段包_SHA256清单.csv`。用户未跟踪文件`faithfulness_pilot_EXPERIMENT_LOG_2026-09-27.md`和`literature/forensic-explanation-relevance-20261004.md`保留原样，未暂存。
- 测试：`python3 work/search_protocol_v2/publish_execution_round.py`通过；`python3 -m compileall -q work/search_protocol_v2`通过；`git diff --check`通过；检查优先排名1–38连续、105恰有6条唯一标题、72两篇新候选排位正确、100末页20条跨快照记录有终页标签、审计为17,492位置/无活动阻断；归档testzip与文件字节比较通过。无业务源码改动，无模型测试。
- 遗留：120细查询仍有82条未满足严格完整条件，48个大父查询须继续细拆；旧候选正文、索引波动回检、版本去重和强相关文献前后向引文递归尚未完成。ResearchSquare跨模态综述全文本轮访问失败，仅保留待核。建议下一轮继续未完整细查询和大式拆分，再核剩余强相关原稿及其参考/被引链；不可依据当前结果宣称零遗漏、目录完整或进入实验阶段。

### 2026-10-08：T02-F3人类评价路线继续扩展（当前等待用户恢复Scholar）

- 仓库：`brodyZhao/my-research-project`；分支：`codex/forensic-explanation-literature`；本阶段方案提交：`2ea75df`（待推送）；HANDOFF将在后续独立提交，origin为已配置的GitHub目标。本阶段包括可追溯的Scholar页日志和新增文献核查；页面全量记录位于忽略目录，用户已有未跟踪文件保持未触碰。
- 继续两条Scholar查询并逐条筛首页：image manipulation/editing × explanation × human evaluation（约2,670条）；image forgery/tampering/manipulation × human study/evaluation × explanation/attribution（约3,670条）。两者规模过大、结果异质，只记录首10个位置并拆式，未声称结果完整。每个位置的筛选理由在本机输出100和`work/search_protocol_v2/execution_pages.json`。
- 新核查/补入：ForenX（20名用户比较100图的解释质量，直接主观评价但不测因果faithfulness）；FakeXplain（ICLR 2026人工接地、定位/泛化机制，非已证实faithfulness实测）；AI-Generated Images: What Humans and Machines See…（100人、16种XAI，明确区分人类plausibility和faithfulness）；LayLens（ICMI 2025 Demo，15人自评可用性）；AIES 2025《Enhancing Image Comprehension…》（N=90上下文解释对受众影响，邻接）；ForgeryGPT（100个伪造图、5名参与者看解释前后的信心/判断，实验规模及对照不足；修正此前候选表误写“已在优先清单”的状态并加入优先清单）。详细限制和源页已写入72、90、100。
- 统计：父查询107/13,941位置/59可见末页；子查询122/3,486位置/50可见末页，其中38通过现有严格完整条件；全日志17,512位置（包括重复版本/引文，非独立论文数）；补充位置77；19条受阻/无效观察，其中当前有一个活动阻断；优先清单44行，候选表41行；100逐位置路线表230行。检索与引文递归仍未完成。
- 当前断点：提交`"AI-generated image detection" "human evaluation" explanation`后，Google Scholar转到自动流量限制页，无结果/无人工验证控件。原始记录标为阻断，不按零结果。用户已表示将手动恢复后回复“已恢复”。恢复后首先从此查询读取首页，判断规模，再分页筛查。
- 本地本阶段文件：跟踪文件`literature/forensic-explanation-search-protocol-v2-20261008.md`；忽略的逐页原始JSON及生成输出在`work/search_protocol_v2/`、`outputs/图像鉴伪解释可靠性_重检_2026-10-05/`。阶段ZIP已刷新：`outputs/图像鉴伪解释可靠性_重检阶段结果_2026-10-08.zip`，112文件，CRC和逐文件字节比较通过；SHA-256=`ae4bb78f4e3210c417a8063b709d23bd14ec717f713d4ae87430792977c0c8f5`。
- 检查：`python3 work/search_protocol_v2/publish_execution_round.py`通过，报告17,512位置/当前阻断链接正确；`python3 -m compileall -q work/search_protocol_v2`通过；`git diff --check`通过。阶段归档包已重建并通过逐文件校验；未运行源码测试（仓库无业务源码变更）。
- 遗留：等待用户恢复Scholar；继续当前REFINE2与宽式拆分；核对AI-Generated Images…正式Springer书目/全文评价细节；完成当前人类评价引文线索、候选原稿及相关种子前后向引文递归。全项目仍未完成，不能声称没有遗漏。
- 建议 ChatGPT Web：从本地72第39–44行和90/100新记录复核“人类plausibility、解释质量、人类影响”与“模型因果faithfulness”分层；确认无误后，从活动断点继续，不重跑已记录分页。

## 2026-10-09：Google Scholar恢复后窄式续检与引文补筛

- 仓库：`my-research-project`；当前分支：`codex/forensic-explanation-literature`；远程：`origin https://github.com/brodyZhao/my-research-project.git`。本阶段开始HEAD为 `4be369c6b449f784dbc238f63ee75aa8fc0d1366`；检索协议的最新内容提交为 `915aafd`（完整对象哈希见 `git rev-parse 915aafd`）；本次HANDOFF单独提交为随后文档提交。
- 用户回复“已恢复”后，IAB Scholar结果可读；Chrome扩展原标签仍落在Google reCAPTCHA，未代为操作验证码。沿既有 `"AI-generated image detection" "human evaluation" explanation` 读完7个结果页、66个可见位置，terminal页Next禁用；估计数66–77波动。逐位置结果在 `74_V2完整分页逐位置初筛.csv`，原始记录在 `work/search_protocol_v2/execution_pages.json`。题录位置含重复与无关项，不能称66篇相关论文。
- 追查AnomReason、FakeReasoning、ForenDeX的前向引文，分别完整筛查10、8、1个Scholar位置，新表 `101_AnomReason_FakeReasoning_ForenDeX前向引用逐条筛查.csv`。已逐条区分强相关、待核/邻接、跨视频/文档边界、排除。强种子参考文献递归还未完成。
- REVEAL作者v2 HTML已读方法、奖励、人工评价与相关附录。其证据链训练、忠实性奖励及100例/3位专家匿名解释偏好研究与题目高度相关；但小样本人类质量偏好不能证明决策的因果忠实性或普通用户的适当依赖。ForenDeX确认CVPR 2026 Findings官方记录与CVF PDF URL、Scholar精确题名及一条前向引用；官方PDF正文仍未能读取，故作为“高主题相关、原文待核”暂列优先表，未声称其可靠性指标已核。72优先表49条，90候选表50条（均非独立忠实性实证数量）。
- 修改文件：跟踪的 `literature/forensic-explanation-search-protocol-v2-20261008.md`、本 `HANDOFF.md`；忽略输出包含72/90/101以及刷新后的阶段ZIP `outputs/图像鉴伪解释可靠性_重检阶段结果_2026-10-08.zip`（113个文件）。原始搜索日志及查询计划在忽略的`work/search_protocol_v2/`；用户原有两个未跟踪文件保持未改动、未暂存。
- 计数：发布器报告17,597个结果位置（非独立论文数）；父查询107式/13,941位置，细分与引文路线125条/3,571位置，补充位置77；多出的8个位置已核对为两条旧补充记录：`CITEDBY-6391361178114081016` 6个位置、`GS-EXPL-TAMPERING-SURVEY` 2个位置；合并后三类分项及旧补充记录对齐17,597。54条子路线可见终页，42条达到严格完整判据。检索没有完成，未声称覆盖零遗漏。
- 验证：`python3 work/search_protocol_v2/publish_execution_round.py`通过；`python3 work/search_protocol_v2/enrich_t02_f3_refine2.py`通过；`python3 -m compileall -q work/search_protocol_v2`通过；`git diff --check`通过。阶段ZIP `testzip()`通过、113个文件全部与输出目录逐字节一致；当前SHA-256 `12f9072f04e929c08a4146a7dfa14c5b5bdec190c1b36eb886cec03b27deb77c`。CSV验证：72=49条连续排名，90=50条，101=19条逐项理由，74=17,597个位置。
- 遗留：查明8个位置的汇总分项差异；读取ForenDeX官方全文；继续REVEAL等强相关论文的参考/被引链和候选原稿核对；处理剩余大规模查询和索引波动路线。下一轮仍只做检索/筛选，不进入研究方案或实验设计。
- 建议 ChatGPT Web下一步：从101逐条表和72第13–14项复核REVEAL/ForenDeX证据等级，补齐ForenDeX原稿后确定排名；随后继续强相关种子引用链，同时追踪8位置统计差异。不要把当前阶段称为最终目录。

## 2026-10-09：T02-F3依赖/稳定性子式和新候选（仍在检索）

- 仓库：`my-research-project`；分支：`codex/forensic-explanation-literature`；远程：`origin https://github.com/brodyZhao/my-research-project.git`。本阶段内容提交：`8977a43ba8deb85a65d7ead4062c38bc74c8f2f6`；本段HANDOFF另行提交，最终HEAD见Git。
- 完成T02-F3-S2/S3/S4：S2 appropriate reliance 42位置；S3 trust calibration 53位置/6页，Scholar估算63变53；S4 explanation stability 11位置/2页。三条均见终页。每个位置的人工题录/摘要筛选记录在102、103及总台账74。S4命中已知《Beyond Accuracy》并新检出《Explainability-Guided Deepfake Detection for High-Fidelity Facial Edits》；后者以Side-VLM、像素级篡改掩码和CAM对齐评估解释faithfulness，暂列强相关优先表第51项，但当前仅核机构作者摘要、DOI与会议记录，全文协议还未检查。Surfacing Variations与Dynamic vs. One-Time作为人类可靠性/误信息判断邻接证据列入90，不计直接图像鉴伪解释实证。
- 计数：累计筛选台账17,703个结果位置，跨查询含重复，不是论文数。107条父式13,941位置/59可见末页；125条细分与引文路线3,677位置/57可见末页/45符合现有严格完整条件；另有77个补充位置。优先表51项、候选表58项，不代表51篇经全文确认的直接忠实性研究。
- 重要记录限制：raw `execution_pages.json`不含全部历史页面；重建器曾把累计台账由归档的17,597错误压到17,350。现已从上一ZIP恢复累计表，合并S2的42条及S3/S4的64条；本机`publish_execution_round.py`已改为保留历史筛选行并合并新结果。此行为`work/`中的临时脚本，不提交。旧页以累计74和阶段ZIP为准；不能把当前raw文件当作完整历史镜像。
- 当前阻断：新试检T02-F3-S1人类评价宽式估计约2,670条，立即跳出人机验证页，未取得结果列表；已记录为第20条历史阻断，绝非零命中/末页。当前Scholar URL见`83_V2本批计数与受阻观察审计.json`。手动恢复后应从首页重试，先按可靠性/任务同义词拆分，避免宽式直接分页。
- 本阶段输出：`102_T02-F3-S2图像操作适当依赖式逐位置筛选.csv`（42行）；`103_T02-F3-S3_S4信任校准与解释稳定性逐位置筛选.csv`（64行）；72优先表51项；90候选表58项；累计74为17,703行。阶段ZIP：`outputs/图像鉴伪解释可靠性_重检阶段结果_2026-10-08.zip`，115个文件，SHA-256=`c63f71a385cfa34908b46ebb4d632d24f1a9569e48a9ecafecaf49f475c2e2bc`。原有两个用户未跟踪文件保持原样、未暂存。
- 主要跟踪变更：`literature/forensic-explanation-search-protocol-v2-20261008.md`。检查：`python3 -m compileall -q work/search_protocol_v2`通过；`git diff --check`通过；74有17,703个唯一ID且所有行理由非空；72名次1–51连续；102/103理由完整；zip CRC与115个文件逐字节一致。没有业务源码或模型改动。
- 下一步：用户完成当前Scholar的人机验证后，从T02-F3-S1首页重新记录；优先取得并全文核《Explainability-Guided Deepfake Detection…》，检查其faithfulness、mask alignment、场景划分和稳定性定义；继续ForenDeX全文、强相关参考与前向引用递归，随后处理其他未试检细式/宽式拆分。整体任务未完成，不能承诺零遗漏。

### 2026-10-09：Scholar恢复后深伪解释人评细式续检

- 仓库：`brodyZhao/my-research-project`；分支：`codex/forensic-explanation-literature`；origin仍是`https://github.com/brodyZhao/my-research-project.git`。本handoff写入前协议提交：`679ecb0`（`docs: log resumed deepfake explanation searches`）。
- 主要跟踪修改：`literature/forensic-explanation-search-protocol-v2-20261008.md`追加本批检索式、筛选边界、来源和统计。输出目录`outputs/图像鉴伪解释可靠性_重检_2026-10-05/`及忽略目录`work/search_protocol_v2/`保存逐位置表、累计日志、路线状态及临时脚本；这些输出不提交Git。用户已有未跟踪文件`faithfulness_pilot_EXPERIMENT_LOG_2026-09-27.md`和`literature/forensic-explanation-relevance-20261004.md`保持未修改/未暂存。
- 用户恢复Scholar后，重新尝试宽式T02-F3-S1（约2,670条、首页10位置），并测试三组深伪细式：人评广式约948（首页10）、`"deepfake detection" "human evaluation" explanation`约427（首页10）、`deepfake "human evaluation" "visual explanations"`显示估算77→67，7页67位置至Next禁用。新建筛选表104记录97个观察位置及逐条理由；其中原宽式首页10条已在旧74台账，避免重复计算，故累计台账74从17,703净增87至17,790个唯一result_id。
- 补充候选：DDL（TIFS 2025，DOI及作者机构页核对，全文待核）、Anchors深伪取证工具（2022，机构摘要与IEEE题录核对，评测公式待核）、ECCV 2022 FST-Matching模型机制解释（已查ECVA官方页/PDF和Springer会议卷）。72优先表现为54项；90候选表64行，包含机制、综述、边界和邻接材料，不等于同数直接faithfulness实证。ResearchGate唯一来源、身份未核实的“Human-in-the-Loop Deepfake Forensics…”已在逐位置表中隔离，不计入确认文献。
- 当前路线统计：107个父式/13,941主矩阵位置/59可见末页；细分与引文路线128式/3,764位置/58可见末页/46符合严格完整判据；总日志17,790个位置（含跨式重复，不是独立论文数）；补充位置77；历史阻断/异常观察20，当前无活动阻断。宽式、约948与427两式只读首页；整体检索、旧候选全文复核和强相关种子引文递归均未完成，不能声称零遗漏。
- 输出交付：`104_T02-F3-S1及深伪人评拆分式逐位置筛选.csv`、更新后的`74_V2完整分页逐位置初筛.csv`、`72_V2已复核强相关优先清单.csv`、`90_本轮新增强相关候选与引文复核.csv`、`83/85/87`计数/路线状态及阶段报告。归档包`outputs/图像鉴伪解释可靠性_重检阶段结果_2026-10-09.zip`共116个文件（含SHA清单），SHA-256=`0a351ea3386773f526b8b005edfbfd3f7951f5460368f2db6f52f878cdaac617`；CRC与116个文件逐字节校验通过。
- 验证：`python3 -m compileall -q work/search_protocol_v2`通过；`git diff --check`通过；74共17,790个唯一ID且筛选理由非空；104共97行且理由非空；72名次1–54连续；90共64行；85/87各128条；阶段包SHA清单及CRC/逐文件比较通过。仓库没有业务源码改动，无业务测试需要运行。
- 遗留/建议下一步：从T02-F3-S1细式向图像拼接、copy-move、inpainting/retouching、AI生成/合成图等非deepfake任务继续扩展；查询式先做规模验证，宽式不直接长分页。优先读DDL和Anchors全文以核实fidelity/affinity指标、人评样本与任务，再核2026预印本身份与原稿；继续高相关种子参考文献和前向引用逐条排查。不可把可解释性、可读性、人类解释偏好或掩码对齐自动当成解释因果faithfulness，也不可称检索“一个不漏”。


### 2026-10-09：文献重检继续（末页核对、来源审计、非deepfake术语受阻）

- 仓库：`my-research-project`；分支：`codex/forensic-explanation-literature`；远程：`origin https://github.com/brodyZhao/my-research-project.git`。本段更新前HEAD见Git；本段完成后协议与HANDOFF按项目规则分别提交并推送。
- 主要跟踪修改：`literature/forensic-explanation-search-protocol-v2-20261008.md`。本地忽略输出新增`108_DDL与Anchors原始证据和访问状态核查.csv`，并更新72、83、85、87；忽略的`work/search_protocol_v2/fine_split_queries.json`更新查询计划。
- 继续核实Scholar `deepfake "human evaluation" "visual explanations"`第7页确有67估算、7条末页结果、Next禁用；既有104已逐条记录这些条目，本次只复核终页、不重复加计。校正路线状态：REFINE=1页/10位置、约3,670估算、未分页；REFINE2=7页/66位置、末页Next禁用，之前的85/87“未执行”标记与74累计台账矛盾，现已更正。
- 新式 `("image forgery" OR "image tampering" OR "image splicing" OR "copy-move forgery") ("explanation faithfulness" OR "explanation fidelity" OR "sanity check" OR "parameter randomization")` 试检立即跳Google验证页，没有结果列表；用户需手动完成验证后再从首页续查。此次当前阻断记录在83及85/87，不作零命中处理。
- DDL与Anchors来源审计见108。DDL核实到TIFS 2025题录/摘要，但IEEE全文未读，Fidelity等评测方法与人评设计都待原文核实。Anchors核实到IEEE题录及莫拉图瓦大学会议摘要，实际公开条目类型为Conference-Abstract；70.23% anchor affinity已核，公式/人评未知。另有综述转述的89.58% fidelity未回原稿核实，不能与70.23%混同。IIT学位论文有PDF条目但本次下载超时。72优先表据此更新证据边界。
- 统计：结果位置累计维持17,790（重复路线位置，不是论文数）；父查询107式/13,941位置/59末页；子式与引文路线129式/3,764位置/58末页/46严格完整；补充77；历史受阻观察21、当前有一个新Scholar验证阻断。72优先项54条，不等同于54篇直接faithfulness实证。
- 测试：检查85/87与74路线状态对齐；校验74唯一ID和筛选理由、CSV列数、83状态字段；`python3 -m compileall -q work/search_protocol_v2`、`git diff --check`；更新阶段ZIP后执行CRC与逐文件比对。
- 用户未跟踪文件`faithfulness_pilot_EXPERIMENT_LOG_2026-09-27.md`、`literature/forensic-explanation-relevance-20261004.md`保持未修改、未暂存。
- 遗留：待用户手动恢复Scholar后从新窄式首页继续；另有两个深伪human-evaluation宽式仅首页；继续扩充非deepfake任务表达，核DDL/Anchors及旧候选原文，沿强种子参考与前向引文逐篇筛查，做版本去重。全面重检仍未完成；不能声称“一个不漏”。
- 建议 ChatGPT Web 下一步：从受阻窄式T01-F2-IMAGE-FORENSIC-RELIABILITY首页续分页，每页逐条筛选；随后对其命中论文分别核原稿，并跟进DDL全文获取和Anchors指标定义。

## 2026-10-09 Scholar恢复后：图像伪造忠实性式与证据一致性式（仍未完成）

- 仓库：`my-research-project`；分支：`codex/forensic-explanation-literature`；远程：`origin https://github.com/brodyZhao/my-research-project.git`。检索协议阶段提交：`747ba1959b2a5a12cfd70b36e97ddb1959c8604d`；本段交接提交后最终HEAD另记。
- 主要tracked修改：`literature/forensic-explanation-search-protocol-v2-20261008.md`。已提交。用户的两个未跟踪文件`faithfulness_pilot_EXPERIMENT_LOG_2026-09-27.md`与`literature/forensic-explanation-relevance-20261004.md`未修改、未暂存。
- 用户恢复Scholar后续检索T01-F2-IMAGE-FORENSIC-RELIABILITY：检索式以image forgery/tampering/splicing/copy-move替代deepfake，18页、179个可见结果位置、估算186–198；末页Next禁用但start=150跳至167，标为可见末页/索引缺口，不算严格完整。179条尚未逐行转录到累计74，须优先补齐。
- 完成T06-F2-S3（synthetic/generated image × explanation terms × “evidence consistency”）：26位置到可见末页，估算36→26（波动27.8%），索引不稳定，不算严格完整。逐位置行与理由已保存于`110_T06-F2-S3合成图证据一致性逐位置筛选.csv`并并入74。候选增加METER、INSIGHT、From Evidence to Verdict、VIGIL、STeREx-Net等；72优先表57项，90候选表74项。STeREx-Net身份/来源与原稿时间线待核，隔离不计确认文献。FakeBench及HAVE/PAVE已补入72，SGEVL仍待核Springer章节全文。
- 统计口径：74当前17,816行，含唯一ID且理由非空；另有T01-F2 179个页面可见位置已记于87路线状态但未导出至74。子式129条、实际路线结果3,969位置（含以上待导出179）、60条到可见末页、46条严格完整；父式107条/13,941位置/59条到可见末页；补充77位置。位置数不是去重论文数；任务仍未完成，不承诺零遗漏。
- 输出包：`outputs/图像鉴伪解释可靠性_重检阶段结果_2026-10-09.zip`，120个文件；CRC及逐文件字节比对通过，SHA-256=`5170c438fe2a6ed1939f678a1305560b20b400aacd8dd79f30d472cbef2a65b8`。本地忽略输出目录包含新110表、更新后的74/72/83/85/87/90及111清单。
- 验证命令：`python3 -m compileall -q work/search_protocol_v2`、`git diff --check`通过；CSV/JSON审计通过（74 17,816行唯一；110 26行；72排名1–57连续；90 74行；87 129式；83子式实际位置3,969）；ZIP CRC及逐文件一致通过。无业务源码修改。
- 后续优先工作：从浏览器已保存断点T06-F2-S3末页继续计划中的核心原文/引文链；先将T01-F2的179个可见题录逐条写入74并按原摘要筛选，然后补查start=160跳页/稳定性；复测T06-F2-S3并阅读全文核METER/INSIGHT/SGEVL等强候选。不要把工具解释、证据一致性或区域接地自动等同决策因果忠实性。
- 建议ChatGPT Web下一步：复核110中METER与AIFo的边界分类，并检查SGEVL原文是否实际给出了证据子图依赖检验；继续时先补齐T01-F2未导出的179行，再推进未完成强相关引文链。当前Scholar用户标签保留在T06-F2-S3 start=20末页。

### 2026-10-09：V109继续至第31页；第32页遇Scholar异常流量限制（未完成）

- 仓库`brodyZhao/my-research-project`；分支`codex/forensic-explanation-literature`。本批检索协议更新见`literature/forensic-explanation-search-protocol-v2-20261008.md`。用户现有未跟踪文件`faithfulness_pilot_EXPERIMENT_LOG_2026-09-27.md`和`literature/forensic-explanation-relevance-20261004.md`未更改、未暂存。
- V109主式估算约20,900条，已逐条完成前31页/310个结果位置；新增页日志`184_V109_image_forgery_xai_faithfulness_page31_10位置逐条初筛.csv`，并入忽略目录累计74。原有前30页日志（170–183）已保存。Scholar第32页start=310出现Google异常流量页，尚无结果，已在83审计中记为阻断；必须由用户手动恢复后从start=310续检，不能按零结果或末页记载。
- 新发现EFR（arXiv:2608.08009v1/ACM MM 2026元数据）在原稿§§3.2–3.3.1提出图文篡改证据anchor绑定和五项可验证reward；纳入72/90/153并标注边界：条件GT推理训练、定位/文本跨度一致不等于解释自然语言因果忠实性，也没有独立盲评/IAA。其56条引文此前逐条题名筛查，强相关引文若干已全文核读；递归引文闭包尚未完成。
- 新增原稿证据：BusterX++ 5名法证专家对100条图/视频样本做双盲成对解释偏好评估（模型胜82%），另100条正确fake样本中87%所述伪迹经专家确认可见；LaP-Forensics对246例的一致性图输入进行zero/donor反事实替换，mask mIoU 0.721降至0.604/0.611，但仅证明空间mask依赖，作者明确不外推为自由文本语义faithfulness。TextSleuth、TextShield-R1、IDseq逐篇加入90并区分自动推理分数/定位指标/数据质控与独立解释忠实度研究。输出72新增3项；90新增候选记录；153新增3项证据条目。
- 检查：`python3 -m compileall -q work/search_protocol_v2`、`git diff --check`；CSV列数/字段、累计ID唯一性、筛选理由非空和V109连续页数需在提交前再次执行。没有业务代码或模型改动。
- 遗留：Scholar当前异常流量阻断等待用户恢复；V109仅完成310/约20,900估算结果位置，其他并行路线、去重、候选原文、EFR/其他强相关种子引文递归都未完成。建议ChatGPT Web恢复后从V109 start=310继续，并优先沿EFR原文直接引文[43],[46]–[54],[61]–[63]及BusterX++专家评价/接地研究相关文献追查。

### 2026-10-09：V109分页续检到第46页，start=460再次触发验证（当前断点）

- 仓库：`my-research-project`；当前分支：`codex/forensic-explanation-literature`；origin为`https://github.com/brodyZhao/my-research-project.git`。本阶段开始HEAD为`aaf7b80`，包含本次tracked修改文件`literature/forensic-explanation-search-protocol-v2-20261008.md`与`HANDOFF.md`；之后待提交的最新hash以Git为准。用户现有未跟踪文件`faithfulness_pilot_EXPERIMENT_LOG_2026-09-27.md`和`literature/forensic-explanation-relevance-20261004.md`均未触碰、未暂存。
- Google Scholar V109宽式在用户恢复start=310后，已逐条登记第32–46页（150个新位置），总覆盖1–460；每个位置有筛选决定和理由。第41–46页单页文件为输出194–199，并已追加进74总台账。74当前19,116行/唯一结果ID/非空理由；这表示查询结果位置，含跨式重复，不表示独立论文数。87中V109记46页/460位置，当前下一步start=460；Scholar估算仍约20,900，因此远未完成。
- 第47页`start=460`跳转到Google reCAPTCHA，页面没有结果题录；没有记作零命中或末页。阻断已写进83，历史阻断观察累计23，当前活动阻断明确为V109 start=460。已在对话请求用户完成当前验证。恢复后从同一页读取并继续。
- 新全文候选：DocShield（arXiv:2604.02694v2）和Can GPT…（IH&MMSec 2025/arXiv:2504.11686）已按§节、表格、效度限制加入72/90/153。DocShield的文本相似度和IoU、代理生成/审核注释不等于人评或因果faithfulness；Can GPT的GPT-4V-as-judge测定位/可读性/完整性，不能替代解释理由真实性的人评或反事实干预。其它邻接项包括Going Beyond XAI、ManTraNet、通用LVLM长回答幻觉、Frontiers多模态假新闻人评，均按任务边界降级。详细证据见tracked检索协议与忽略输出194–199、72、74、83、87、90、153、199。
- EFR的56条参考文献已有03/162逐条题名初筛、7条强相关引文169做原文核读；本轮未完成全部前后向引文闭包。候选优先清单75行（含标题行，即74项），不等同74篇直接因果解释faithfulness实证。整体检索继续进行，不能承诺绝对零遗漏。
- 检查：待提交前执行`python3 -m compileall -q work/search_protocol_v2`、`git diff --check`、CSV唯一ID/空理由/路线断点检查；本阶段尚未运行这些最终检查。工作区仅两份用户未跟踪文件应保持原状。完成后仅暂存tracked协议与HANDOFF，按AGENTS.md提交并push当前分支，不merge主分支。
- 建议下一步：用户完成start=460验证后先筛查第47页10个结果；继续第48页与V109宽式，其后处理非deepfake术语覆盖和强种子引文递归。若验证迟迟未完成，可继续候选论文/参考文献的独立来源核查。

### 2026-10-09：V109恢复后续筛至Scholar第70页（继续进行）

- 仓库：`my-research-project`；分支：`codex/forensic-explanation-literature`；远程：`origin https://github.com/brodyZhao/my-research-project.git`。本阶段修改tracked文件为检索协议和本交接文件。用户未跟踪文件`faithfulness_pilot_EXPERIMENT_LOG_2026-09-27.md`及`literature/forensic-explanation-relevance-20261004.md`保持原样、未暂存。
- Google Scholar宽式V109已在用户恢复后从start=460继续并筛至第70页/700个结果位置，Scholar估算约20,900，下一页断点start=700。第63–70页新增80位置，逐项记录在输出216–223，并并入累计74。累计台账当前19,356行数据、ID唯一、逐项筛选理由已填写；位置数含重复/多版本/引文卡片，不是独立文献数。整体检索仍未完成。
- 新的直接或强邻接候选包括：MoFAIR（AIGC取证解释并关注幻觉解释）、Kadam等2021年图像伪造检测与XAI综述、Lin等2023年遗传编程AI生成图像检测解释、OMNI-fake（检测/定位/解释benchmark）、ForgerySpotter、LLM+Grad-CAM解释AI生成艺术、图像/视频篡改法证分析等。部分只到摘要级；可靠性是否得到有效验证需继续核全文，分清解释保真、定位/热图质量、自然语言可读性、准确率及人类偏好等不同终点。
- 候选表90新增/核对记录；来源核查确认2021综述与2023遗传编程论文的题录/摘要为直接主题命中。此外确认CVPR 2025 Forensic Self-Descriptions是由残差得到的图像表征，并非自然语言解释；相应保留为方法邻接。完整筛选理由与分层见输出216–223、候选表90及检索协议。
- 审计83总结果位置更新为19,356；父路线107/13,941、子/引文路线149/4,837、补充82、其他独立补充位置496；当前无活动验证码阻断，历史阻断观察仍23。V109状态在87记录为70页/700位置，下一页start=700；complete=false。
- 验证已通过：`python3 -m compileall -q work/search_protocol_v2`、`git diff --check`；74共19,356条、ID唯一、筛选理由齐全，216–223各10行，83/87计数对齐。阶段ZIP含230个文件且CRC通过，SHA-256=`5d2de22cd6bd59ef14c058a65caa2ae9197badbdd80a80f67b0e779465c2c908`。仅暂存本交接文件和检索协议；两份用户未跟踪文件保持未触碰。
- 下一步：继续Scholar start=700的每页筛查；优先取得并核读Kadam 2021综述、Lin et al. 2023、MoFAIR、OMNI-fake、ForgerySpotter等原稿，记录解释可靠性评估协议和边界；随后沿强相关种子的前后向引文继续扩展，尤其完整闭合EFR引文链。不能把当前高召回日志宣称为零遗漏完成版。

### 2026-10-09：V109续检到第75页，新发现解释基准论文（仍在进行）

- 本分支：`codex/forensic-explanation-literature`；origin为项目GitHub远程。Tracked阶段文件：检索协议与HANDOFF。用户两份未跟踪文件保持未修改、未暂存。
- V109宽式从start=700继续筛查第71–75页50个结果位置，新增输出224–228，全部写入累计74。累计Scholar位置台账现为19,406条，ID唯一、筛选理由非空；结果位置会重复，不是唯一论文数。V109共75页/750位置，Scholar约20,900，下一断点start=750；搜索尚未完成。
- 重大候选纠漏：已从Springer原文确认《Dissecting Deepfake Artifacts via Multimodal Explanations》（Bai et al., MMM 2026, DOI 10.1007/978-981-95-6950-2_3），其摘要提出FakeArti数据集/解释评价benchmark、1,414张深伪图、4,170个像素级伪迹mask，且明确提到接地难与相互矛盾输出会损害解释可靠性。列为极高优先全文审查对象。其40条参考文献应单独逐篇筛，优先直接读参考19（deepfake XAI量化评价）、25 FakeShield、26 SIDA、24 Forensics-Bench等；不要把解释benchmark/定位精度直接当成faithfulness证明。
- 其他高优先候选：Skyra（CVPR 2026视频伪迹grounding与人工注释），NVMS-Net（图像处理操纵检测并声称model explainability），Journal of Forensic Sciences 2026 Stable Diffusion法证似然比和解释可视化。均需核原稿；像素定位、检测分数校准、文本可读性与解释忠实性应分开评估。人类心理物理deepfake检测工作记为人类任务邻接，不视作XAI用户研究。
- 83更新至总位置19,406（父107/13,941；子149/4,837；补充82；其他546），V109为75页/750位置；历史阻断23，当前无阻断，整体complete=false。单页日志224–228及候选90记录新发现。
- 下一步：从V109 start=750继续，并建立Dissecting Deepfake Artifacts正式参考文献逐条审查表。优先取原文核查FakeArti标注、解释事实性/一致性和ADAD指标；沿其参考文献追查FakeShield/SIDA和定量解释评价。继续至分页/检索末端，并回头做不同检索路线和EFR的引文闭包。
- 本阶段验证已通过：`python3 -m compileall -q work/search_protocol_v2`、`git diff --check`；累计74共19,406行且ID唯一、理由与位置齐全；216–228各10行；83/87断点对齐。阶段ZIP含235个文件，CRC通过，SHA-256=`31e1b3e3a55aba7a0993e895b3047f68c410fdc609e4887fc6aad75abfa1cf92`。本阶段仅提交HANDOFF和检索协议；两份用户未跟踪文档未触碰。

### 2026-10-09：V109宽式续检至第84页（未完成；断点start=840）

- 仓库：`brodyZhao/my-research-project`；分支：`codex/forensic-explanation-literature`。本阶段在V109从start=750连续筛查至start=830，新增90条逐位置记录，页面表229–237；总账74现19,496条、result_id均唯一、筛选理由均非空。输出归档`outputs/图像鉴伪解释可靠性_重检阶段结果_2026-10-09.zip`已更新，282成员、CRC通过、SHA-256 `5796144b281ebceef1f4c00f1ffd7f51d647b6b9e2004b736a996075b89aca69`。这些是结果位置，不是去重论文数。
- V109 Scholar估算约20,900，84页/840位置已筛，尚未到末页；下一页start=840。强相关候选待核名单新增：Detection of AI-generated synthetic images with a lightweight CNN；Reliability map estimation for CNN-based camera model attribution；From Sharp Eyes to Expert Mind；Score-based Likelihood Ratios for Deepfake Image Evidence；DGR-Net；Forged anomaly detection using advanced deep learning；BioForensNet；DiffSeg。不能仅凭摘要提升为已验证强相关。
- `Dissecting Deepfake Artifacts via Multimodal Explanations` Springer正式页已读取摘要及40条参考文献，显示核心引文链入口（定量评估XAI深伪检测、Forensics-Bench、FakeShield、SIDA等）；应下一步建40条逐篇筛查并深读关键引文。其它宽式页中的相邻方法论文已在页面日志说明为何只作方法迁移背景。
- 测试/检查：累计74行数、唯一ID、非空理由通过；229–237每表10条；83/87计数更新；归档ZIP CRC通过。完成`python3 -m compileall -q work/search_protocol_v2`和`git diff --check`后提交并push本分支。没有模型/业务代码修改。用户自有未跟踪文件继续保留且不暂存。
- 后续：从当前Chrome Scholar标签的start=840继续；批量复核新增候选原文；展开新Springer强相关论文40条参考文献和前向引用；所有剩余式、跨式去重及原稿效度复核仍未完成。ChatGPT Web建议先抽查候选题名与方法学边界，再继续start=840。

### 2026-10-09：V109宽式续检至第91页（未完成；断点start=910）

- 当前仓库`brodyZhao/my-research-project`、分支`codex/forensic-explanation-literature`。上一个提交`dc613c2`已推送；本检查点新增页面238–244、每页10条，全部合并到总账74。累计74共19,566位置，ID唯一且筛选理由无空值。用户自有两份未跟踪文档未暂存。
- V109 Google Scholar宽式约20,900条，已筛第1–91页/910位置，下一页`start=910`；搜索整体仍未完成。新强候选待核：`OmniVL-Guard`；`Enhanced CNN architecture… AI-generated image detection`；2009综述`Image forgery detection`（前史线索）；`TrueFake`及DCNN似然比分值法证评价作为相邻背景。第89页WireLLM条目虽出现FakeShield专家评价引用片段，标题任务是无线资源管理，已标为Scholar引用摘要噪声并保留FakeShield追踪线索。
- 83/87总计更新：累计19,566，域外补充706；V109 91页/910位；归档ZIP 289成员CRC通过，SHA-256 `ffce10b78a116778981507a3805050e54921361e256edd7bd8b2de8edbbb5f35`。检查通过：`python3 -m compileall -q work/search_protocol_v2`、`git diff --check`、74唯一ID/非空理由。
- 后续立即从Scholar start=910继续，优先核查OmniVL-Guard原文；建立并完成`Dissecting Deepfake Artifacts via Multimodal Explanations`40条参考文献逐篇筛查，再围绕Ref.19、FakeShield、SIDA、Forensics-Bench等扩大前后向引文链。其余检索路线、去重与强候选原稿效度核实仍未完成。

### 2026-10-09：按论文级去重并完成 AnomReason 全文及57条参考文献筛查

- 仓库：`brodyZhao/my-research-project`；分支：`codex/forensic-explanation-literature`；远程：`origin https://github.com/brodyZhao/my-research-project.git`。本阶段开始HEAD=`db9a9f1c7a71d38455fd530eea73c8c081daa8d3`。用户原有未跟踪文件`faithfulness_pilot_EXPERIMENT_LOG_2026-09-27.md`与`literature/forensic-explanation-relevance-20261004.md`未修改、未暂存。
- 为减少重复工作，按规范化精确题名审计候选表90，发现AnomReason此前有两条不同检索命中的重复论文记录；已合并为一条并保留两个检索来源。候选90由221条降至220条，标题全唯一；72中rank64更新为全文复核证据。
- 全文核读AnomReason（Tan et al., ICLR 2026, arXiv:2510.10231）§§3.2–4.2、附录B/E和ICLR官方记录。确认其AnomReason-Deepfake用结构化异常现象/理由与人工筛选真值匹配，并设置仅在分类正确时计分的CSemAP/CSemF1；这是直接的语义解释接地/联合有效性评测证据，但不代表内部特征因果忠实度。数据注释由单名训练标注员逐候选accept/reject/unsure，未报告IAA；1,000图对比未见解释真实性盲评或用户依赖研究。AnomReason的57条参考文献均逐条筛入忽略输出`outputs/图像鉴伪解释可靠性_重检_2026-10-05/101_AnomReason全部57条参考文献逐篇筛查.csv`；其中直接取证解释链与评估方法背景逐级区分，既有论文复用表90/72判定。
- Google Scholar V110在此前已筛至第100页/994个可见位置，`start=1000`空结果容器但仍显示估算结果；本阶段不重复翻页。单独的AnomReason Cited-by 10页面经用户报告恢复后重新载入仍显示reCAPTCHA；没有读取或记为零，被引路线仍待手动恢复。审计JSON继续记录总位置20,781、complete=false；计数为跨式结果位置，不是唯一论文数。
- 修改/生成文件：ignored outputs中的72、90、101、83和阶段ZIP；tracked文件`HANDOFF.md`。验证通过：`python3 -m compileall -q work/search_protocol_v2`、`git diff --check`；90共220条且题名唯一；101共57条、参考编号1–57连续唯一、理由齐全；74共20,781个唯一结果位置ID；阶段ZIP含337个文件、CRC和逐文件字节比对通过，SHA-256=`be253cd7f0d27f175aad2e8b17331257ea1ff66700d5e957f1c9bca05c4abfee`。仅提交HANDOFF，不暂存两份用户文件。
- 遗留：整体检索尚未完成；V109宽式与其他多条细式存在分页上限、索引漂移或验证码断点；AnomReason前向引用列表、EFR及其他强相关种子的引文递归闭包未完成。建议继续时从尚未完成且未重复筛过的高精度路线推进；遇到已见题名直接复用90/72的原判定，只核新原稿和未读引文链。

#### 同日补记：AnomReason引文再发现一篇遗漏的直接论文

- 对57条参考文献与候选总表做标题/变体交叉匹配时，发现Ref.49 `Rethinking Vision-Language Model in Face Forensics: Multi-Modal Interpretable Forged Face Detector`（M2F2-Det, CVPR 2025, arXiv:2503.20188）此前没有入表。已核读原稿§§3–4：它同时输出检测分数、文本解释和伪造attention map；解释文字按DD-VQA答案计算BLEU-4、CIDEr、ROUGE-L、METEOR、SPICE。故属直接强相关的解释生成/自动文本质量评价论文，但这些分数不是因果faithfulness；正文未见解释盲评或appropriate-reliance实验。已补入72（rank79）和90；90目前221篇且题名唯一，72目前82条。
- AnomReason Ref.50 `X2-DFD`与表90既有`X²-DFD`为题名字符变体，复用原筛查，不重复核读。Ref.49/50匹配状态已更正至101。官方来源：[CVF Open Access](https://openaccess.thecvf.com/content/CVPR2025/html/Guo_Rethinking_Vision-Language_Model_in_Face_Forensics_Multi-Modal_Interpretable_Forged_Face_CVPR_2025_paper.html)、[arXiv全文](https://arxiv.org/html/2503.20188)。
- 变更后复核仍待执行，并刷新ignored阶段ZIP；所有Scholar结果位置不变（74仍20,781），全局检索仍未完成。当前用户所见V110标签正常；另一个后台AnomReason Cited-by标签仍显示验证码，已不要求用户切换去寻找该隐藏标签，引用链暂记独立阻断。

- 补记验证：`python3 -m compileall -q work/search_protocol_v2`、`git diff --check`通过；90共221条且题名唯一、72共82条、101编号1–57连续唯一、74共20,781条唯一位置ID。ZIP 337个文件，CRC及逐文件比对通过，SHA-256=`5568ff72aaa14947bf51f94322d0031a0adf221d185b29934953d73b932b451f`。本补记前HEAD=`26f621d`。

### 2026-10-09：按M2F2-Det的97条参考文献去重筛查与复用既有全文结果（检索仍未完成）

- 仓库`my-research-project`；分支`codex/forensic-explanation-literature`；本轮开始HEAD=`9ebfab8a24d96f7493deb9b52dcad9f3ca7f1882`。输出位于忽略目录`outputs/图像鉴伪解释可靠性_重检_2026-10-05/`；用户原有两个未跟踪文件继续未修改、未暂存。
- 对M2F2-Det原稿References逐项筛查97条，并新建`102_M2F2-Det全部97条参考文献逐篇筛查.csv`。标题/版本交叉匹配发现：Can ChatGPT Detect DeepFakes? 已在EFR参考链及全文证据中核过；Common Sense Reasoning for Deepfake Detection已有100全文效度记录；HiFi-Net、HiFi-Net++、PSCC-Net也已有题录/方法记录。本次只在候选90和优先72补充两篇统一索引及M2F2-ref来源，明确复用既有全文结论，不重复获取或重读。优先清单现82篇（原84条中两篇同题重复记录已合并，保留全文核查和第二次发现来源，rank唯一连续）；候选90现223条且题名唯一。
- 新审的M2F2 Ref.76 `Cheap-fake Detection with LLM using Prompt Engineering` 官方arXiv摘要显示研究真实照片与误导图注构成的out-of-context误用，以GPT-3.5提取caption关系特征进行cheap-fake检测；不是模型生成鉴伪解释，也没有解释事实性、因果faithfulness或依赖校准终点，因此仅作低/中邻接，不进强相关核心。其他检测算法、基准数据和通用BLEU/CIDEr等评价工具均逐项标成任务邻接、数据或指标背景。
- Scholar位置计数未变化：累计74仍20,781个结果位置（ID唯一），跨式位置不等于独立论文数；总体状态仍`complete=false`。V110主式已有100页/994位置、start=1000为空容器但估算仍高；V109路线和引用链仍有受限断点，不能称穷尽。AnomReason Cited-by CAPTCHA为后台独立标签，用户看不到时不再要求其寻找隐藏页。
- 验证及归档：102共97条且编号连续、理由齐全；72共82篇且题名/排名唯一连续；90共223篇且题名唯一；74共20,781个位置ID唯一且筛选理由非空。`python3 -m compileall -q work/search_protocol_v2`与`git diff --check`通过。阶段ZIP含338个文件，CRC与逐文件字节比对通过，SHA-256=`3a06f154b622c0a893a64df244d16b5b31419468b4f66f8a3df0edb04c57b242`。没有源码或模型改动，不需模型测试。按仓库规则本应只提交HANDOFF，但本地`git add`因沙箱将`.git`设为只读而失败；申请提升权限后，自动审批拒绝commit/push，理由是现有证据不足以证明配置的GitHub remote为用户信任的目标。未提交、未推送；当前HEAD仍为`9ebfab8a24d96f7493deb9b52dcad9f3ca7f1882`。两个用户未跟踪文件未暂存。阶段输出包已本地生成，待用户明确授权该remote后再完成交接提交与推送。
- 后续优先沿其他已核强相关种子前后向引文继续；已见标题先查crosswalk复用既有结论，只为未见标题和缺失原稿投入新阅读。ChatGPT Web下一步检查M2F2引文表的97行连续性及复用记录，再推进V109/V110可用断点与剩余独立引文链。

# 2026-10-09 合成图信任校准闭合与深伪接地/幻觉首屏续检（仍未完成）

- 仓库 `brodyZhao/my-research-project`；分支 `codex/forensic-explanation-literature`；本阶段延续此前检索，不改业务源码。用户现有两个未跟踪文件未改动、未暂存。Google Scholar 使用 Codex IAB 页面；用户此前授权继续检索和推送。
- 完成精确子式 T06-F3-S3：`("synthetic image" OR "generated image") (explanation OR explainable OR interpretability OR interpretable OR attribution OR saliency OR rationale OR reasoning) ("trust calibration")`。Scholar显示121条；记录13页/121位置，start=120只有1条且Next禁用，按当时可见索引记录为终端闭合（不代表主题穷尽）。逐位置题录初筛记录在 `113_T06-F3-S3_trust-calibration逐位置筛查.csv`；121条位置均有题名、页码、决定、理由和查询页链接。该专表为本轮人工转录题名，不逐条保存目标文献URL；能匹配到的候选以既有稳定URL为准。前向/反向引用与全文仍未覆盖。
- T06结果去重后，加入/补齐优先清单的邻接项：`Believing without Seeing`（ACL 2026，VLM解释质量/用户可靠性判断）、`Effect of AI Performance...`（深伪检测中的人类依赖，但未操纵解释）、`Surfacing Variations...`（图像描述可靠性人因研究）。三者清楚标记为方法/人因近邻，不作为解释faithfulness直接证据。`72`现87个连续rank；增补项暂按低优先级顺序放在末端。
- 继续试检T11深伪解释子式。S1 `... (grounding)` 首屏10/约11,400，S2 `... (hallucination)` 首屏10/约4,830；均未到末页或完成分页。日志分别为 `114_T11-F2-S1_deepfake_grounding_首屏逐位置筛选.csv`、`115_T11-F2-S2_deepfake_hallucination_首屏逐位置筛选.csv`。10+10位置都与已有目录交叉匹配；保留重复位置审计且复用原稿核查，未重复全文。新加候选Fake-in-Facext（arXiv:2510.20531，待全文核验）和ExDDV（WACV 2026，视频邻接候选、待核全文/标注构念）。T11-S1/S2仍待续页或拆分。
- `74_V2完整分页逐位置初筛.csv`现20,922行，result_id唯一、理由无空；其中新追加位置141条（T06 121 + T11-S1/S2各10）。请勿把位置数说成独立文献数；路线表按有效页/位置汇总与主表会有历史路由计数差异，不应将不同汇总字段相加推导独立论文数。`87`现150条子查询，状态表位置数重新汇总6,573；全局`complete=false`。当前另有大量未试检子式、受限路线、全局去重以及强相关论文引文链未完成。
- 阶段ZIP已重建为 `outputs/图像鉴伪解释可靠性_重检阶段结果_2026-10-09.zip`；应以本次执行的成员数/字节数/SHA校验结果为准。验证 `python3 -m compileall -q work/search_protocol_v2`、`git diff --check`，主表ID唯一/理由非空、T06位置1–121连续、T11首屏各10位连续、72优先rank连续均通过。无模型或源码测试需求。
- 建议下一步优先：1) 按高相关性拆分T11 grounding/hallucination，而不是继续宽式重复分页；2) 全文核验Fake-in-Facext与ExDDV；3) 沿EFR、TriDF、X²-DFD、FakeReasoning、ForenDeX、PRPO、FakeBench等核心种子的双向引文链；4) 最后完成候选版本去重和统一相关性排序。不能承诺Google Scholar“一个不漏”。

### 2026-10-09：T11-F2-S2 深伪 hallucination 宽式续检至第90页（仍未完成）

- 仓库 `brodyZhao/my-research-project`；分支 `codex/forensic-explanation-literature`；本检查点开始HEAD=`8068fc0ea26ce90914928394b79df06ce808f411`。origin仍为已配置的项目GitHub仓库。用户明确要求继续并推送。两份既有用户未跟踪文档保持原样、未暂存。
- Google Scholar 查询为 `(deepfake OR "face forgery" OR "facial manipulation") (explanation OR explainable OR interpretability OR interpretable OR attribution OR saliency OR rationale OR reasoning) (hallucination)`。本阶段从第77页`start=760`继续至第90页`start=890`，新增14页/140条逐位置初筛；各页独立日志为 `T11-F2-S2_20261009_第77页逐位置筛选.csv` 至 `第90页`，已逐条填写题名/元数据/来源页/判断/理由。累计主表74为21,812个结果位置ID，全部唯一且筛选理由非空；位置数不是独立论文数。该子式目前90页/900位置，Scholar仍估约4,800且有下一页；路线未闭合，整体检索继续标记`complete=false`。下一页断点为`start=900`。曾短暂误点页81后已返回补筛79、80，页81只计一次，分页偏移没有缺口。
- 新发现或提升的待核引用候选（均未直接升级为核心）：`BC-IFL: A Multimodal Bias Correction Framework for Enhanced Image Forgery Localization`（Scholar摘要称其评估MLLM幻觉对伪造定位的影响；当前未能从IEEE Xplore取得原文，尚不确定幻觉对象是否解释文本，列强邻接待核）；Preprints.org未同行评审综述`AI-Driven Digital Forensics: Capabilities, Limitations, and Research Challenges`（讨论多媒体法证、解释性、验证和法律证据，作广域引文入口）；Bristol 2025博士论文`Integrating Human, LLM, and Visual Engagement for Cognitive Analysis of Online Misinformation`（多模态社媒误导的人类/LLM分析，方法邻接，不能等同图像伪造检测解释实验）；Springer 2026`Dictionary learning-based super-resolution restoration for detecting low-quality facial forged videos`（直接深伪视频检测，关注压缩恢复过程中不要生成伪造样伪迹，无解释faithfulness终点）；以及`AI in Digital and Mobile Forensics: A Thematic Literature Review`（广域法证解释/可靠性引用入口，原文可访问性和期刊质量待核）。这些已记录在候选表90；强相关优先表72未改动，避免把邻接候选误算进已核核心。
- 领域回收的关键旧文`Deepfake Forensics Analysis: An Explainable Hierarchical Ensemble of Weakly Supervised Models`已在候选表90存在，复用原记录，不重复添候选或重读；本轮第85页俄语法证综述摘要中出现该文题名，仅将其记作再发现来源。`A survey of safety and trustworthiness of large language models through the lens of verification and validation`已核Springer官方摘要和范围，虽可提供通用V&V背景，但论文明确聚焦通用LLM、未覆盖fake-image detection，故只保留为方法邻接，不作为直接证据。
- 来源核对：官方Springer说明该V&V综述讨论falsification/evaluation、verification、runtime monitoring，并明确其重点范围不包含fake-image detection；官方Bristol库提供2025年论文全文（217页），摘要确认其研究在线误导、人类/LLM标注和视觉特征，仍需区分社媒语境与取证解释；Springer 2026面人伪造视频论文直接指出超分会产生类似伪造痕迹的伪迹，并提出时空字典恢复，但不是解释方法。链接见候选表90和逐位置表74。
- 检查通过：主表21,812行/result_id唯一/理由齐全；第77–90页每页10行且位置761–900无缺；87中T11-F2-S2记90页/900位置、next=`start=900`、complete=false；83总位置21,812、子查询位置7,003与主表对齐。校正第77、78页捕获时间为当时实际UTC记录，未改原筛选依据。
- 本阶段无源码/模型更改；计划继续Scholar到下一个验证码/页面断点，然后按仓库Git规则推送当前分支。下一步优先从`start=900`继续，但对新题名先查候选/已核记录复用，再将精力留给新出现的强候选原稿和EFR/其他强相关种子的未闭合前后向引文；不要把这条4,800条宽式90页误称为完成或零遗漏。
