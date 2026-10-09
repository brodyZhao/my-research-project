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

旧82篇全部进入68重审队列，旧55标签不继承为V2最终计数。现已按已有原页证据重审21篇的主题与评价边界（72/79），没有冒称重新全文读完82篇。其余61篇和英文候选继续按本协议筛；已有原文与逐位置日志保留，不删除证据。最终交付相关性排序、每篇评价对象与指标/证据等级、版本去重、完整筛选日志及覆盖缺口。任何一批完成只报该批状态，不能把检索量当完成度。

首批执行：T12-F1两位置、T13-F1六位置、T03-F1七位置、T04-F1十一位置，共26位置，完整可见分页/逐位置题录初筛见73。MDPI拼接解释候选原页Web429，未记正文取得。原105式第一轮与补方法试验不是完备性证明，48式估计≥900必须拆分再执行。

交付文件：

- [67_检索方案V2_完整查询矩阵.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/67_检索方案V2_完整查询矩阵.csv)
- [68_既有82篇核心_V2逐篇重审队列.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/68_既有82篇核心_V2逐篇重审队列.csv)
- [69_V2试检全部结果位置初筛.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/69_V2试检全部结果位置初筛.csv)
- [70_V2检索式验证与锚点回检.json](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/70_V2检索式验证与锚点回检.json)
- [72_V2已复核强相关优先清单.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/72_V2已复核强相关优先清单.csv)
- [73_V2首批细检索全部26位置筛选.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/73_V2首批细检索全部26位置筛选.csv)

## 2026-10-08 细检索与引文续检批次

107父查询中59条已经顺序到达Scholar可见末页（非领域穷尽证明）：全部15条F1、全部15条F5、11条F3、8条F2、10条F4。主查询13,941个结果位置，附加ForensicChat题名1/全部版本3/前向引用24个位置，合计13,969。位置可跨查询、版本重复，不是独立论文数；1125首页试检位置不能再直接相加。逐位置规则辅助初筛见74，路线页码连续性/末页与未决见75。保留8次受阻观察，恢复后的正常页面才计覆盖（83）。当前T01-F4-S1（普通图像伪造×合理性检查）子式首页受自动查询限制，未取得有效试检。48父查询仍未全分页。59条可见结束中T12-F2/T08-F4/T01-F4估计数大幅变化，仍需拆词回检；其余56条没有本批识别出的这一索引异常；48个大查询仍须拆分，原稿、递归引文和版本核验也未全部完成。

强相关优先清单现有22条：旧目录21篇范围重审，加新检出的ForensicChat。直接可靠性评价与核心解释机制分别注明，未把全部22条当作独立忠实性证据。视觉VLM反事实评价论文为迁移方法，不计直接鉴伪强相关。ForensicChat65参考、视觉反事实48参考、HexMIL48参考，新增161参考位置全题录初筛；不表示161被引原稿全已读。ForensicChat24前向引用逐题名人工初筛见82，相关候选原稿尚待核验。EFR既有56参考日志保留，后续继续追查强相关候选，不能因之前目录已有题名就判全文审查完成。

本批原稿核查：ForensicChat的解释得分与真假判决正确性耦合；视觉反事实方法存在编辑/提及识别误差且非鉴伪任务；HexMIL正文表3/4支持架构与定位比较，不能视作已完成固定模型解释随机化检验。HexMIL切片标签还使用结节轴坐标，热图含阈值和平滑，补充材料未核。详见78、81。World Scientific DOI 10.1142/S0218001426400343仍有安全验证；不可访问留待核，不作无关排除。

新交付：74分页日志；75路线覆盖；76/77/80参考初筛；78原稿边界；79既有十二篇重审；81 HexMIL复核；82前向引用；83计数审计。下一步继续较小F2/F4，拆分过大父查询，再执行B1/B2、原稿重审及强相关递归引文。所有工作仍属重检，不进入实验设计。

ATAR本轮重新核读作者v1的工具机制、训练消融与解释评价（84）：200图裁判、50图/3人验证，另报TP幻觉率；ATAR额外给裁判工具热图而基线没有，评分比较不对称。指标名称Faithfulness不等于固定模型对证据的因果依赖已被检验。原页列MM2026 DOI，正式版本对应尚待核。该条为既有核心的重审，不是新增独立论文。

索引异常：T12-F2取得750位置后，start750空尾页显示总数由约750骤降525；T08-F4取得100位置后空尾页，显示数从首页241到尾页82/92波动。当前都无Next，仅记可见结束，不能当稳定充分覆盖。75记录估计数最小/最大与风险，原始页面留档，后续拆词重检，不把Google显示数当独立论文总数。

本轮恢复拼接分支后新增4条可见结束：T03-F4 466位置、T13-F4 500位置、T07-F4 569位置、T10-F4 743位置；T15-F4正常130位置后第14页受阻。74记录每位置规则辅助题录初筛，不声称全部人工全文核查。恢复后先读取当前T15-F4页，再顺序分页；优先继续剩余小规模F4与索引异常回检，再拆过大的父查询。

本轮遥感T15-F4 765位置、图像取证T09-F4 797位置到可见末页；T01-F4保存680位置后start680空尾页总数由约805跌到538，列新增索引风险。针对16条大细查询和3条索引异常，生成19父/83子式（85），逐项分配可靠性OR词，所有原父式任务与解释限定保留；逻辑并集等价验证见86，不能据此声称语义或数据库召回完备。先逐子式实际试检，≥900仍需更细拆分；83子式当前只有T01-F4-S1尝试一次且受阻（87），其余尚未执行。不能把83计划子式当已检索。恢复后先读取当前子式页，再判断规模是否可完整分页。


### 2026-10-08 继续检索：扩散图子式与过宽查询复核

- 用户确认 Scholar 人机验证已完成。读取恢复页面后，继续 `T08-F4-S4`（diffusion-generated × deletion）并按页记录：offset 0–90 共94个结果位置，第10页后无Next；首页估算104、末页94。此前验证码页保留为受阻观察，不按零结果。
- 完成 `T08-F4-S5`（同一任务 × insertion）：15页、149个结果位置至末页（start=140，无Next），显示估算161–149。
- 实际规模试检发现 `T02-F2-S1`（image manipulation/editing × explanation terms × grounding）约14,200条，不能作为可穷尽的分页单元；只记录了首页10个位置，状态为需进一步拆分。基于此增加诊断式 `T02-F2-S1A`：`"image forgery" explainable grounding`，无年份下限。其有效页面为offset 0–340，共350个位置；start=350为空尾页，无Next。估算从646变至496、300，超过25%波动，故虽已到可见空尾页，仍标记为索引不稳定并需回检。此前有一条请求/实际查询不一致的旧宽式页，日志保留但校验器排除。不能据此宣称完整召回。首屏检出 FakeShield、Fakebench、FakeXplain、ForgeryGPT、Where and Why、TruthLens、ATAR等题录；重复版本、跨域和仅机制相关结果须去重并查作者原文，题录命中不代表可靠性评价证据。
- 最新计数：主矩阵107条、可见末页59条、主矩阵13,941个位置；拆分/诊断式84条、有效位置866个，其中11条到可见末页；全部有效日志14,835个位置（主矩阵+补充引用28+细分866），位置可重复，非独立文献数；受阻/查询不匹配观察10条。强相关优先记录23篇。更新详情见交付74、75、85、87、83；归档包需与此批同更。
- 未完成：83条原计划细分路线中尚有大量未试检；14,200条规模查询需按具体鉴伪任务词、解释词和时间段继续拆分；索引波动需重复验证；相关题录逐篇原文与强相关论文引文链尚未完结。任务仍是文献检索与筛选，不转入实验设计。

### 2026-10-08：Scholar续检与种子引文链（本轮）

- 本轮在用户恢复页面后，从 `"copy-move forgery" hallucination` 第3页继续。该页估算22条、实际仅2条目录/索引类记录且无下一页，均非直接相关。补齐此前三个图像篡改子式的检索日志，并另新增12个解释可靠性词项/领域替代词诊断式，连同上述3式共15式；细式配置增至119条。查询式含 `"image forgery" "explanation reliability/accuracy/quality/bias/error/robustness/completeness"`、`"image manipulation" "faithful explanation"`、`forensic "explanation faithfulness"`、`"media forensics" "explanation faithfulness"` 等。所有空结果仅是该精确短语在Scholar的零命中，不证明主题无文献。
- 可行性与筛选发现：宽式 `"image forgery" explanation reliability` 约4,590条，只读首页并立即拆分；精确短语 `"image forgery" "explanation reliability"` 1条，命中TriDF。`"image forgery" "explanation accuracy"` 2条；`"image forgery" "explanation quality"` 从36变38条，38个结果位置均已保存、到可见末页，估计变化不超过25%；`"image forgery" "explanation bias"`、`"image forgery" "explanation error"`、`"image forgery" "explanation robustness"`、`"image forgery" "explanation completeness"` 各为零命中。`"image forgery" "faithful explanation"` 4条，`"image manipulation" "faithful explanation"` 7条。前两组新的直接候选包括REVEAL、ForgeryGPT、Agentic Tool-Augmented Reasoning、STeREx-Net、Explainable Deepfake Detection with Feature-robust Augmentation等；逐条清单在90，只有已明确核原稿的仍记入优先清单72，其余标为待核候选。
- `forensic "explanation faithfulness"` 至少读取offset 0–70；页20曾出现服务器内部错误，重试后恢复。结果估算在49–88之间变化，末页为空且无Next；路线标为索引不稳定，不能据此认定穷尽。该式出现多模态媒体、语音、医疗等跨域文献，仍按视觉鉴伪主题筛除。
- 引文追踪：核对了ForgeryGPT的Scholar cited-by列表，页面显示1条，题为PDF文档编辑/伪造研究，逐条排除。TriDF页面显示6次引用，cited-by列表实际返回5条；逐条记录在89，其中EFR是TriDF的引用来源，另发现TRIDENT挑战赛和DF-CBM为待核候选，两个跨模态检测综述保留背景。EFR此前56条参考文献均已逐条做题名/摘要级核筛（55个公开页面记录+1个作者PDF，12强相关、1边界）；这不表示56篇均读完全文。此引文链把强相关种子之间的交叉引用纳入，不把引文位置误报为独立论文。
- 最新审计：父查询107式；可见末页59式；父查询结果位置13,941。拆分/诊断子式119条、有效结果位置3,266，其中50条到可见末页、38条通过当前完整性条件（无分页缺口、无估计冲突且估计变化不超25%）。总有效结果位置17,241，包含34个附加筛查/引用位置；位置会重复，不能作为论文数。历史受阻/无效页面观察12条，目前没有活动阻断。23条优先记录含直接解释可靠性实证与核心机制两种层级，不能统称为23篇因果忠实性实证。逐页证据见忽略目录 `work/search_protocol_v2/execution_pages.json`；本地交付更新后另附ZIP。
- 验证：`python3 work/search_protocol_v2/publish_execution_round.py` 成功；`python3 -m compileall -q work/search_protocol_v2` 与 `git diff --check` 通过。检索仍未完成；未做任何实验/方案推进。下一步继续按非deepfake领域词扩展和核候选原稿，随后围绕新增强种子参考文献与前向引用继续逐篇筛查；保留索引不稳定路线并优先用更窄任务/可靠性词复测。

### 2026-10-08：人类评价路线动态回检与可解释鉴伪综述引文链

- Scholar检索式`"image forgery" "human evaluation" explanation`继续复核到start=96；估算数在117、114、115、116、106间波动。自动审计为21个有效分页、200个位置，仍缺start=100，未见稳定末页。新增100个逐位置回检观察，保留重复位置；不是100篇新论文。页面原始快照在忽略目录work/search_protocol_v2/execution_pages.json，逐条记录见阶段包100。
- 新核读《Explainable Image-Centric Forgery Detection: A Survey》（Wu等，TechRxiv 2025，DOI 10.36227/techrxiv.176101439.91738583/v1；SSRN 5691366）。该综述按定位、来源归因、判断依据整理图像鉴伪解释，明确提出解释质量、faithfulness和一致性缺少标准化评价。它是领域地图/引文挖掘种子，不是原创可靠性实验；TechRxiv标明未经同行评审。稿件引用编号存在疑似错位，全部关键参考必须回到原稿。72清单增至35项，将该文列在直接实验研究之后并标明证据层级。
- 该综述Scholar cited-by结果4条逐条筛查：图文本OOD与图像OOD两篇排除，ProCoS篡改定位鲁棒性与PURE内容捷径检测保留为边界/方法候选。表见102。尚未逐篇筛完综述全部参考文献。另检出Rethinking VLMs for Image Forgery Detection and Localization（CVPR 2026 Findings）、Explaining Deepfake Detection by Analysing Image Matching（ECCV 2022）、OMNI-Fake等候选。Evidence Fusion正文仍受访问验证限制，只留候选。
- 当前计数：107父查询、59条可见末页、13,941父查询位置；120拆分/诊断式、3,466位置、50可见末页、38满足严格完整判据；17,486总位置含重复/版本/引文，非论文数。17条历史阻断观察、当前无活动阻断。全面检索未完成。
- 阶段交付更新：72共35项、90共33项、100共220条路线观察、102含4条前向引用筛查记录；归档包待本次阶段更新后重新验证。下一步继续综述关键引用回查、未试检的宽词/非deepfake路线、候选原稿与索引异常回检；不得声称穷尽。


### 2026-10-08：X²-DFD直接人评与核心引用链筛查

X²-DFD官方页面确认发表于NeurIPS 2025，arXiv首发2024、v4日期2025-05-29。其正文明确以解释可靠性/幻觉为动机；用feature-level balanced accuracy与人工核验筛选生成解释依据，并在DD-VQA及未标注场景采用文本相似度、人工/GPT-4o质量评分。官方补充材料检索结果记录15名20–40岁受教育程度较高参与者评100个deepfake样本，按检测能力、解释合理性和细节程度给0–5分。因此归为强相关的人评证据，但不能把质量/合理性评价等同于对原分类器的因果忠实性；目前未核到sanity/randomization、反事实依赖或使用者信任/依赖效应。样本说明仅称100个deepfake images，故尚无证据显示有真实图或假阴性对照。

X²-DFD评测/相关工作链中4篇直接相关文献已逐篇记录在输出`103_X2DFD评价链相关参考文献逐条筛查.csv`：FakeShield、FFAA、Can ChatGPT Detect DeepFakes?、A Hitchhiker’s Guide to Fine-Grained Face Forgery Detection。四篇均属于任务/解释或细粒度评测强相关，但各自的检测、定位、鲁棒性、专家筛选或答案质量终点均需与解释faithfulness区分。X²-DFD已补入72优先表和90候选表，正式年限/版本与原先候选的错误2026记录已校正。

用户当时打开的Scholar cited-by参数`cites=6391361178114081016`在一次读取后显示人工reCAPTCHA。该观察记入忽略目录execution_pages.json和输出`104_谷歌学术被引链断点与受阻记录.csv`；不计作空结果、零命中或末页。页面已交还用户人工恢复，并标记handoff，恢复后继续。

### 2026-10-08：TriDF被引链续检及人类评价式末页复核

用户指出Google Scholar页面正常后，改用当前Codex IAB重新核对，确认先前触发挑战的是Chrome标签，而IAB当前TriDF cited-by页正常。Scholar页面标示6条结果、无下一页：EFR、DF-CBM、Explainable Deepfake Detection Challenge、Deepfake Detection Beyond Benchmark Accuracy、AI-Generated Content Detection: A Cross-Modal Survey、TRIDENT。逐条筛选见输出105；EFR与DF-CBM已有原稿/评价边界记录，不重复计为新增论文。Chrome历史阻断在104中更正为已通过IAB恢复；18条历史无效/受阻观察保留为历史记录，当前没有活动阻断。

新纳入优先表的两条直接评价候选：TRIDENT使用可观察伪迹标注，报告幻觉伪迹率CHAIR和偏重precision的F0.5；它检验解释说出的伪迹是否有观测真值支撑，不证明分类器因果依赖这些理由。OpenReview论坛页本轮无法直接打开，方法段落依据其PDF索引可见文本并另核ACM MM官方日程，完整PDF待直取。Explainable Deepfake Detection Challenge针对图像深伪，结合EntityScore、EvidenceScore与参考语义/可读性指标；作者把grounding评估可靠性及解释能否帮助用户行动列为未来方向，因此它是直接benchmark候选，但未证明内部决策忠实或用户恰当依赖。两条进入72的第8、9位，既有名次顺延；优先记录38条，涵盖可靠性实证和机制/基准，不是38篇独立因果忠实性实证。90新增候选表增至36行；其中行数含既有重复版本/非独立来源风险。

被引页其余两篇逐条判断为边界背景：Deepfake Detection Beyond Benchmark Accuracy（Preprints.org未同行评审综述）主要综述二元检测、跨域泛化、鲁棒与复现；文中提及可解释可信取证方向，但不是解释评价综述。AI-Generated Content Detection跨模态综述本轮未能打开Research Square全文，只从Scholar题录/摘要核到宽泛检测范围，暂不纳入强相关且保持待核。不能只凭标题为该文补写解释可靠性内容。

同时在用户打开的`"image forgery" "human evaluation" explanation`末页（start=96）核实：当前IAB页面显示估计106条、第10页，“下一页”禁用；10个位置逐条记录更新到100，其中仅刑事诉讼机器学习证据可靠性一条列背景边界，其余一般多模态/预测维护/电商/指令调优/bug报告/3D生成/中风预测/会议元数据等排除。末页观察不代表该查询之外或整个主题穷尽。100维持220条跨快照位置，含重复位置而非220篇论文。

本次新增6个有效Scholar被引结果位置后，审计合计17,492个有效结果位置（跨式/跨页重复，不是文献数）；父查询13,941位置、可见末页59/107；细分查询3,466位置，50/120可见末页、38/120满足严格完整性条件；补充位置数77。受阻/无效历史观察18，当前阻断为空。重检仍未完成：未试检细查询、大查询拆分、其余旧候选原稿、更多强相关引文递归和版本去重仍待做。

原稿证据：[Explainable Deepfake Detection Challenge作者HTML](https://arxiv.org/html/2607.21007)；[TRIDENT OpenReview PDF](https://openreview.net/pdf?id=H7hsRMzu7B)（本轮只核到索引可见方法/指标片段，论坛页验证未通过）；[Deepfake Detection Beyond Benchmark Accuracy预印本](https://www.preprints.org/manuscript/202609.1394)。

### 2026-10-08：T02-F3 human-evaluation 扩展子式续检（仍未完成）

- 从前一轮断点继续测试 `T02-F3-S1`：`("image manipulation" OR "image editing") (explanation OR explainable OR interpretability OR interpretable OR attribution OR saliency OR rationale OR reasoning) ("human evaluation")`。Scholar约2,670条，首页主题混杂，停止宽式分页并按任务子域细分。追加了`T02-F3-S1-REFINE`：`("image forgery" OR "image tampering" OR "image manipulation") ("human evaluation" OR "human study" OR "user study") (explanation OR explainable OR rationale OR attribution OR saliency)`，估算约3,670条，首页10条逐位置筛选，仍过宽，未分页。
- 页面筛选记录：From Prediction to Explanation、X²-DFD、So-Fake、Generating Attribution Reports、ForgeryGPT等被识别为目录既有条目或版本位置，不重复计数；ForenX、FakeXplain、AI-Generated Images: What Humans and Machines See…、LayLens、Enhancing Image Comprehension进入优先清单/候选表。初筛与理由在交付`100_图像伪造人类解释评价路线_全部观察位置逐条筛选.csv`，页面原始JSON在忽略目录`work/search_protocol_v2/execution_pages.json`。
- 对新增重要原稿做了来源核查：ForenX作者HTML报告20名用户盲序比较100张写实AI生成图的理由，评准确性、相关性、合理性、完整性、总体质量；这是直接解释质量人评，但不能证明对检测决策的因果忠实、sanity或恰当依赖。FakeXplain为ICLR 2026论文，人工框/文字标注支撑接地推理、定位和检测；定位及泛化/鲁棒性证据不等于解释忠实性验证。AI-Generated Images…由100人给52张合成图标出区域并给出文字理由，对比16种XAI；原文明确其人类中心plausibility与faithfulness（模型决策对应性）不同，是主题边界/方法重要研究。ForgeryGPT作者HTML核到其100张全伪造图×5名参与者的看解释前后判断/信心实验，结果可反映说服力与潜在过度依赖，但N很小、无真实类及无解释控制，不证明总体准确性或解释忠实。LayLens是ICMI 2025 Demo、15人用户研究，主要报告自报清晰度/负担/信心；解释与图像重建界面捆绑。AIES 2025《Enhancing Image Comprehension…》为N=90的上下文叙事解释用户研究，测受众记忆、情境认知/意见变化，不是模型归因或检测器解释。
- 纠错：90表此前将ForgeryGPT标注“已在优先清单”，但当时72表并无该条目。本轮核查全文后修正90状态并把它加入72。72增至44个分层条目（直接人评/机制/grounding和人类影响邻接研究均明确标边界）；90候选41行，计数包含可能同篇/版本与已有条目，不代表独立文献篇数。
- 新增窄式`T02-F3-S1-REFINE2`：`"AI-generated image detection" "human evaluation" explanation`。提交后IAB跳到Google Scholar自动流量限制页（无结果列表、无人工验证控件），已逐条保存为受阻观察；用户表示将手动恢复后告知。不得按零结果处理。待恢复后从该式继续，先核页面可行性，再决定是否逐页。
- 更新后统计：父查询107条/13,941位置/59个可见末页；子式122条/3,486位置/50个可见末页，其中38条满足现有严格完整条件；全部日志17,512个结果位置（含重复、版本、引用，绝非独立论文数）；补充位置77；历史/当前受阻观察19，其中当前活动阻断为上述查询。100人类评价路线逐位置表230条。优先清单44行，候选表41行。全量重检仍未完成，不能承诺零遗漏。
- 验证：`python3 work/search_protocol_v2/publish_execution_round.py`通过，统计与本段一致；`python3 -m compileall -q work/search_protocol_v2`、`git diff --check`通过。阶段ZIP已重建为112个文件，CRC和逐文件字节比较通过；SHA-256为`ae4bb78f4e3210c417a8063b709d23bd14ec717f713d4ae87430792977c0c8f5`。接下来先等用户人工恢复，再从REFINE2读取结果；同时继续拆分规模仍达数千的宽式、复查索引波动与强相关文献引文链。


## 2026-10-09 Scholar恢复后续检与优先目录纠漏

- 用户回复“已恢复”后继续检索。Codex IAB的Google Scholar当前可正常读取；历史Chrome扩展标签仍显示reCAPTCHA页，本轮未替用户操作验证。对话中既有的IAB Scholar结果继续作为本批实际来源并逐页记录。
- 继续窄式 `"AI-generated image detection" "human evaluation" explanation`：原始执行日志已保存7页、66个可见结果位置（start=0,10,…,60；终页Next禁用）；Google显示估算在66–77间变化，位置含题录噪声/重复，不能把估算数当唯一文献数。逐位置筛选见74，raw页在`work/search_protocol_v2/execution_pages.json`。
- 沿AnomReason（10条）、FakeReasoning（8条）、ForenDeX（1条）Scholar前向引用逐位置筛查，新增输出101。三条是引文发现路线，不是完整领域检索路线。FakeReasoning链中ATAR是已知强相关；AnomReason链发现ForenDeX、GenShield、MIC及HumanForge等，后3项分别标为待核/邻接/视频边界。ForenDeX此前已出现在多个Scholar题名/引用结果及候选记录，但未进入强相关优先目录，本轮确认是目录升级遗漏，现加入72并将全文未核状态醒目标注。
- 全文核对REVEAL作者v2 HTML：方法以8个离线专家模型构造证据和CoE，奖励联合分类、理由和多视角一致性；作者声称结构性因果解释不等于经干预证实的因果忠实。附录0.E对100图（50 real/50 synthetic）、3位研究专家匿名比较REVEAL与AIGI-Holmes解释，按多数票判优；这属于小样本专家偏好/解释质量评估，不是ordinary-user appropriate reliance实验。该文补入72高相关目录，限制与原文范围写明。
- ForenDeX：Google Scholar精确题名命中1条，确认作者与2026 CVPR会议信息，CVF官方PDF URL与OpenReview官方CVPR 2026 Findings记录相符；Scholar前向引用页1条，指向《Understanding Why Foundation Models Work for Diffusion-Generated Image Detection》，作为机制背景筛查。当前浏览器和Web读取未取得ForenDeX PDF正文；因此纳入72仅为“主题强相关、官方全文待核”的暂定条目，不能写成人评/faithfulness结果已核。
- 本轮新增筛查表101共19个引文结果位置，逐项给出纳入/邻接/排除理由；旧REVEAL前向5条已在历史主逐条表中保留。本批不宣称参考文献递归完成。新录的raw citation page条目在execution_pages.json，路线计划 fine_split_queries.json。逐条表：[101_AnomReason_FakeReasoning_ForenDeX前向引用逐条筛查.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/101_AnomReason_FakeReasoning_ForenDeX前向引用逐条筛查.csv)。
- 更新计数时注意：最新发布审计报告17,597个结果位置，存在跨查询重复，不能读作独立文献数。报告分项为107条父查询/13,941位置、125条细分与引文路线/3,571位置、补充位置77；尚有8个补充位置来自未归入上述路线分项的两条旧记录：`CITEDBY-6391361178114081016` 6个位置，以及 `GS-EXPL-TAMPERING-SURVEY` 2个位置；计入后总数对齐。54条子路线到可见终页、42条达到严格完整判据。优先目录新增2项（REVEAL原稿核读；ForenDeX官方题录已核、原文待读），整体重检继续未完成。
- 遗留：继续强相关种子的参考文献全条目检查；优先取得/读取ForenDeX官方全文；完成剩余大规模/索引波动细查询和所有强候选原稿/版本审计。不得声称“一个不漏”或零遗漏，也不得把Scholar可见末页解释为领域穷尽。

### 2026-10-09：信任校准与解释稳定性子式续检

- 从断点完成`T02-F3-S2`（图像操作×appropriate reliance，5页/42位置）、新增`T02-F3-S3`（×trust calibration，6页/53位置，Scholar估算63→53）及`T02-F3-S4`（×explanation stability，2页/11位置）。三式均到可见末页；本轮S3/S4新增64个可见位置，连同S2为106个位置，均逐项记录筛选理由（输出103、102）。位置并非论文数；S3索引估算变化已标注，不能当作无波动或完整覆盖。
- S4再次命中已在优先清单的《Beyond Accuracy》，确认其主题命中不是新论文；新发现《Explainability-Guided Deepfake Detection for High-Fidelity Facial Edits》，机构摘要描述Side-VLM多视角像素级篡改掩码、CAM对齐训练以及鲁棒性/解释faithfulness评估，加入72第51项与90候选。当前仅核对机构作者摘要、DOI和会议记录，全文中的faithfulness定义、指标、数据切分、干预和稳定性协议仍待核；没有用户依赖实验。邻接记录《Surfacing Variations…》（15位盲人/低视力用户评估图像描述不可靠陈述）与《Dynamic vs. One-Time Detection…》（120人误信息判断）均分开列入90，不当成图像鉴伪检测器解释证据。
- 本轮所有可见位置逐项筛选结果：[102_T02-F3-S2图像操作适当依赖式逐位置筛选.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/102_T02-F3-S2图像操作适当依赖式逐位置筛选.csv)；[103_T02-F3-S3_S4信任校准与解释稳定性逐位置筛选.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/103_T02-F3-S3_S4信任校准与解释稳定性逐位置筛选.csv)。
- 计数：累计台账17,703个结果位置（不是独立论文数）；父式107条/13,941位置/59条可见末页，细分与引文路线125条/3,677位置/57条可见末页/45条符合当前严格完整判据，补充记录77位置；历史阻断观察20条，当前`T02-F3-S1`首次试检要求人机身份验证（约2,670条估算，未获得题录）。72优先表51项、90候选表58项，均含待全文核验与机制/邻接条目，不能当成全部直接忠实性研究。
- 完整性发现：本轮先用现存压缩执行日志重建总表，统计仅17,350，较上一阶段ZIP已核验的17,597少247；审计发现紧凑原始页文件未包含全部历史分页。立即从阶段ZIP恢复完整累计台账，并并入S2独立筛选表及本轮S3/S4记录，得到17,703；修改`publish_execution_round.py`为累积合并，避免将来重建覆盖归档过的人工筛选。已归档旧位置仍以74累计台账/阶段包为准；`execution_pages.json`并非完整历史原始页镜像，后续不能只靠它重建旧位置。
- 验证：本批S3/S4输出64行，理由非空；S2为42行/理由非空；累计74为17,703行且ID唯一；72排名1–51连续，90共58行。`python3 -m compileall -q work/search_protocol_v2`与`git diff --check`通过。整体检索与候选全文/引用递归仍未完成。
- 下一步：先在 Scholar 完成当前`T02-F3-S1`验证后从首页继续；约2,670条过宽，需筛选较细子式并保存每个结果位置。随后继续执行T02-F3其他未试检子式及父式拆分；优先取得并核读《Explainability-Guided Deepfake Detection…》全文，特别核定faithfulness、mask alignment、稳定性和场景隔离协议；继续完成ForenDeX全文与强种子参考/前向引文递归。保留“直接解释可靠性评价、机制基准、人类信任迁移”三层，不能宣称零遗漏。

### 2026-10-09：Scholar恢复后 T02-F3-S1 任务细分续检

- 用户回复已恢复后，IAB中的Scholar查询可读。宽式 `("image manipulation" OR "image editing") (explanation OR explainable OR interpretability OR interpretable OR attribution OR saliency OR rationale OR reasoning) ("human evaluation")` 显示约2,670条，只看首页10个结果；宽式首页此前已存在于累计台账，因此不重复加计。它以图像编辑/生成评测为主，不能当作鉴伪检索已完成。
- 按任务域做三组细式：`("deepfake detection" OR "face forgery detection" OR "facial manipulation detection") ("human evaluation" OR "human study" OR "user study") (explanation OR explainable OR rationale OR attribution OR saliency)`（约948，首页10条）；`"deepfake detection" "human evaluation" explanation`（约427，首页10条）；`deepfake "human evaluation" "visual explanations"`（显示估算77至67波动，连续7页、67个位置、末页Next禁用）。前两式只完成首页，不能宣称穷尽。全部97个本批可见题录位置逐行筛选见`104_T02-F3-S1及深伪人评拆分式逐位置筛选.csv`；与已有74台账相同的宽式首页10条保留在本批观察表但不重复并入累计台账，因此74净增87个唯一位置，累计17,790位置。位置不是论文数。
- 新识别/再次确认的直接候选包括《DDL: Effective and Comprehensible Interpretation Framework for Diverse Deepfake Detectors》（TIFS 2025；摘要涉及解释fidelity、可理解性、适用性与user study）、《A visually interpretable forensic deepfake detection tool using anchors》（2022；Anchors/anchor affinity与人评指标）、《Quantitative Metrics for Evaluating Explanations of Video Deepfake Detectors》、SNIPPET、X²-DFD、XPlainVerse及《Generating Attribution Reports for Manipulated Facial Images》。其中DDL的期刊与作者信息由上海交大机构作者页和DOI交叉核对，全文/实验方法仍待核。Anchors文献在Scholar摘要出现70.23% anchor affinity与89.58%人评fidelity两个口径，必须读原文核公式、受试者任务与数值定义，不把这些分数直接解释为决策因果忠实。
- 发现《Explaining Deepfake Detection by Analysing Image Matching》（ECCV 2022）为解释模型伪迹依赖机制的早期工作。已核ECVA/ECCV官方摘要/PDF与Springer会议卷元数据；其FST-Matching分析、概念/压缩稳定性实验不等于post-hoc XAI faithfulness或用户适当依赖检验。官方来源：[ECVA论文页](https://www.ecva.net/papers/eccv_2022/papers_ECCV/html/2423_ECCV_2022_paper.php)、[ECCV论文PDF](https://www.ecva.net/papers/eccv_2022/papers_ECCV/papers/136740018.pdf)、[Springer会议卷](https://link.springer.com/book/10.1007/978-3-031-19781-9)。Anchors机构摘要见[莫拉图瓦大学图书馆](https://dl.lib.uom.lk/items/751722ba-9145-4f7d-8358-6d2363947a5c)；DDL出版信息见[上海交大作者主页](https://www.cs.sjtu.edu.cn/en/jiaoshiml/ruanna.html)及[DOI](https://doi.org/10.1109/TIFS.2025.3553803)。
- Scholar题录还出现只由ResearchGate上传的《Human-in-the-Loop Deepfake Forensics: Evaluating Expert Detection Performance Assisted by Multi-Scale Heatmap Explanations from DenseNet Architectures》。缺独立确认的作者机构、DOI或正式出版记录，可见文本存在需要查证的不一致，故在104逐位置表中隔离，不计入确认文献。非deepfake图像编辑/生成评估、纯检测准确率人评、音频/视频/文本工作分别标作排除或邻接，不冒充静态图像解释可靠性。
- 逐位置台账校验：输出104包含97个本批观察位置，每行有决定与理由；累计74为17,790个唯一位置。85/87扩展到128条细分与引文路线；细分/子式结果3,764位置、58条到可见终页、46条符合当前严格完整判据。107条父式、13,941主矩阵位置和59条可见终页不变；补充位置77；20条历史受阻/异常观察仍保留，当前活动阻断为空。72优先表54项，90候选表64项；均含机制/综述/待核或邻接证据，不能解释为同样数量的直接faithfulness实证。
- 本批更新来源状态、位置筛选和估计变化见输出72、74、83、85、87、90、104及`work/search_protocol_v2/fine_split_queries.json`。本轮只完成若干查询子式，整体检索和强相关种子引文递归未完成；不能据Google Scholar可见末页、估算数或结果位置承诺领域“一个不漏”。


### 2026-10-09：末页复核、优先候选来源审计与非 deepfake 术语新试检

- 从Google Scholar当前IAB断点核实 `deepfake "human evaluation" "visual explanations"`：页面明确显示第7页、总估算67，start=60页有7条，Next禁用。该页跨领域/词语偶然共现记录逐条排除；总路线已在输出104保留67条逐位置筛选，本次仅重新确认终页，不重复增加累计台账。
- 对两条优先候选做来源级证据审计。DDL（Sun, Ruan, Li, TIFS 2025, DOI 10.1109/TIFS.2025.3553803）：交叉核实作者、卷页和公开摘要；摘要将fidelity、intelligibility、applicability列作评测维度，但本轮未获得IEEE全文，指标定义、扰动/随机化协议、人评样本与任务仍未知，故仍为“题录+摘要级强相关候选”，不作为已验证faithfulness证据。Anchors/XAIVIER（Jayakumar & Skandhakumar, IEEE ICITR 2022, DOI 10.1109/ICITR57877.2022.9993294）：IEEE题录与莫拉图瓦大学机构库交叉核实；该机构库条目实际类型为Conference-Abstract，公开摘要报告70.23% anchor affinity、检测准确率91.92%。IIT另列2022硕士论文PDF但本轮下载超时。无法核实anchor-affinity分母/公式、任何人评任务与样本；后续综述出现的89.58%“fidelity”说法未回原文核实，禁止与70.23%混同或解释为模型决策因果忠实。逐条来源状态和限制见输出108，72优先表已修正。
- 新增非deepfake精确术语式 `("image forgery" OR "image tampering" OR "image splicing" OR "copy-move forgery") ("explanation faithfulness" OR "explanation fidelity" OR "sanity check" OR "parameter randomization")`。导航即进入Google人机验证，未看到结果列表；记录为一次受阻试检，而不是零命中或可见末页。请求用户手动恢复后从首页继续。输出83/85/87、fine_split_queries.json已记当前阻断。
- 发现并纠正历史路线状态不一致：`T02-F3-S1-REFINE`在累计74实际有1页/10位置，约3,670估算、未分页；`T02-F3-S1-REFINE2`实际有7页/66位置至末页，而85/87仍标为未执行。本次将85/87和本地计划与逐位置台账对齐。累计位置数不变：17,790条跨路线位置，不能按论文篇数解释。子式/引文路线现为129条、3,764个结果位置、58条可见末页、46条达严格完整判据；新路线未获任何结果。父式107条/13,941位置/59条末页，补充位置77。历史阻断观察21，当前活动阻断为新非deepfake窄式。
- 检索仍未完成；人评宽式与deepfake人评宽式尚未分页，旧候选原稿仍有缺口，强相关参考/被引递归及版本去重未完成。不得承诺“一个不漏”。


### 2026-10-09：恢复非 deepfake 术语式并检索合成图证据一致性（仍未完成）

- 用户恢复 Google Scholar 后，检索式 `("image forgery" OR "image tampering" OR "image splicing" OR "copy-move forgery") ("explanation faithfulness" OR "explanation fidelity" OR "sanity check" OR "parameter randomization")` 到第18页，Next禁用，Scholar估算186条；实际可见179个题录位置。分页从start=150跳至167，末页估计186–198波动；标为“可见末页、索引/题录计数缺口待查”，不计严格完整。查询状态及分页断点见87/85。本次179条已累计到路线位置统计，但逐题名记录尚未写入74；汇总口径因此区分：累计74有17,816条已导出逐位置筛选记录；另有该路线179条可见位置待转录入74。不能把未导出记录说成逐条日志已完成。
- 第二条既定细式T06-F2-S3：`("synthetic image" OR "generated image") (explanation OR explainable OR interpretability OR interpretable OR attribution OR saliency OR rationale OR reasoning) ("evidence consistency")`。连续检索start=0/10/20到第3页Next禁用，观察26位置；Scholar估算从36降到26，变化27.8%，超过25%阈值。全部26位置已逐题名、摘要片段记录于110并并入74。路线虽到可见末页，仍因估算不稳定标为待复测/拆词，严格完整计数不增加。
- 新增候选并明确终点边界：METER（arXiv 2025）是多模态伪造解释/证据链基准，报告空间/时间IoU、伪造类型追踪和evidence consistency；这些指标不自动证明对检测决策的因果faithfulness。INSIGHT（arXiv 2025）用G-Eval/VLM judge作解释事实性核验，需审计评价器与标注来源。From Evidence to Verdict（arXiv 2025）分析多源取证工具可靠度/覆盖度及证据冲突，属程序性取证相邻工作。FakeBench（TIFS 2025）和HAVE/PAVE（arXiv 2026）已加优先表；SGEVL-Forensics在Scholar摘要明确提出解释是否依赖被引用证据子图，候选仍须读Springer章节原文。EFR在新式重复命中，沿用既有ID，不重复当新论文。
- STeREx-Net题录（Scholar指向MDPI Technologies 2026）暂隔离：检索片段中的特定实验叙述与本研究项目上下文高度相近，且本轮原始页面打开失败。先核正式元数据、作者/版本/出版历史与全文，验证前不纳入确认文献或强相关目录。
- 更新结果文件：110（26个逐位置审查记录）、74、72、83、85、87、90及`work/search_protocol_v2/fine_split_queries.json`。目前子式129条、路线观察60条到可见末页、严格完整46条；路线实际结果位置3,969（含未逐条导出的179条），可导出累计74为17,816个位置；父式13,941位置、补充77位置。179个T01-F2可见位置记录在路线审计但逐条筛选表尚待补齐，勿与已导出数混写；所有数都是检索位置/记录，不是去重论文数。整体重检、引文链递归、强候选原文审核仍在进行，不承诺零遗漏。
- 主要原始来源：SGEVL-Forensics Springer卷目录 `https://link.springer.com/book/10.1007/978-3-032-38407-2`；HAVE/PAVE arXiv `https://arxiv.org/abs/2608.01988`；FakeBench作者机构页 `https://scholars.cityu.edu.hk/en/publications/fakebench-probing-explainable-fake-image-detection-via-large-mult/`；METER `https://arxiv.org/abs/2507.16206`；INSIGHT `https://arxiv.org/abs/2511.22351`；AIFo `https://arxiv.org/abs/2511.00181`。页面摘要/目录级核查不代表这些全部阅读全文。

### 2026-10-09：V109宽式分页继续至start=310（未完成，当前受限）

- Google Scholar宽式 `("image forgery" OR "image manipulation" OR "image tampering") (explainable OR explanation OR interpretability OR attribution) (faithfulness OR fidelity OR grounding OR hallucination OR "sanity check" OR evaluation)` 显示约20,900条。本次逐条完成第31页start=300的10个题录，V109累计覆盖首页至第31页、结果位置1–310。页面日志为输出`184_V109_image_forgery_xai_faithfulness_page31_10位置逐条初筛.csv`，并已逐行并入74总账；筛选理由区分直接候选、引文/综述挖掘、任务邻接和排除。
- 第31页新命中`Evidence-Grounded Forensic Reasoning for Detecting and Grounding Multi-Modal Media Manipulation`（EFR，arXiv:2608.08009v1；ACM MM 2026 proceedings metadata）并与既有条目合并，不重复计篇。原稿§§3.2–3.3.1显示50K条件生成、规则/MLLM/人工筛选的取证推理数据；五组件reward包括分类、图像框、文本跨度和证据—anchor一致性。它是极强空间/语义证据绑定机制候选，但未见自然语言解释因果干预、独立盲评解释效度或评审一致性；不能因“evidence-grounded”术语直接称为faithfulness已验证。EFR全部56条参考文献已有03/162逐篇题名筛查，169对强相关引文保留原文核读证据；下一步继续更完整的强相关前后向引文闭包。
- 其他原稿核读补入90/153/72：BusterX++ v4含5名法证专家对100条混合图像/视频样本的双盲成对解释偏好比较（82%偏好模型），另对100个正确fake预测人工确认87%所述伪迹存在；这是直接人评与事实接地证据，但无IAA且非因果决策faithfulness。LaP-Forensics对246样本的zero/donor map干预使mask mIoU由0.721降至0.604/0.611；作者明确这只证明空间mask依赖一致性图，不证明自由文本解释语义faithfulness。TextSleuth、TextShield-R1、IDseq也已按原稿证据分别列为篡改文本解释构造/自动reasoning评价/多模态区域接地邻接工作，不冒充独立解释人评。
- 打开第32页start=310时Scholar跳转异常流量页，未获得结果列表。该观察写入83，当前暂停点仅是需要用户手动恢复，不记零命中或末页。87的V109状态维持未完成，下一页URL为start=310。恢复后从该页继续；同时可继续强相关候选和EFR参考/被引链检查。

### 2026-10-09：V109宽式从start=310恢复并连续筛至start=450（继续受限）

- 继续Google Scholar宽式V109：`("image forgery" OR "image manipulation" OR "image tampering") (explainable OR explanation OR interpretability OR attribution) (faithfulness OR fidelity OR grounding OR hallucination OR "sanity check" OR evaluation)`。用户恢复start=310后，逐条完成第32–46页，共150个新题录位置；连同先前1–310位置，本宽式已经逐页筛到1–460，46页/460个结果位置。Scholar仍估算约20,900条，尚未接近末页；结果高度异质，只能报位置覆盖，不能报“相关文献总数”或穷尽。
- 第41–46页页面日志是输出`194`–`199`（每页10条），均逐条记录纳入/排除理由并写入74。V109路由状态87更新为46页/460位置，下一URL为start=460。全量74现有19,116个唯一位置ID、19,116条逐位置理由；该数包含重复文献在不同检索式中的不同位置，绝非19,116篇独立论文。计数审计83更新为父查询107/13,941位置、子/引文路线149/4,837位置、补充82位置、其它独立位置256，导出位置总数19,116；完整性标记仍为false。受阻观察23条，当前活动阻断是V109 start=460的Google reCAPTCHA，不能记零命中/末页。
- 两个直接强相关候选已从全文核读后加入72/90/153：DocShield（arXiv:2604.02694v2）统一评估文本中心文档图像伪造检测、区域grounding和解释文本；用CSS/BERTScore、参考理由语义相似度、CCT/奖励消融，但无独立人类盲评、IAA或解释级因果干预，故只支持解释质量/空间接地，不能称为已证明faithfulness。Can GPT Tell Us Why These Images Are Synthesized?（IH&MMSec 2025, arXiv:2504.11686）由第二个GPT-4V结合真图、伪造图及mask评价自然语言定位的绝对/相对位置、可读性、完整性，且有多轮检测评分与few-shot敏感性分析；无独立人评解释理由事实性或解释因果干预，重复query主要测检测决策波动，不宜扩大解释稳定性结论。原文核读证据及效度边界记录于153。
- 另记录`Going Beyond XAI`为一般解释faithfulness综述/引文挖掘线索；ManTraNet IPOL 2022为取证响应真假阳性难区分及检测依据仍不明的可解释性缺口前史；`Why LVLMs Are More Prone to Hallucinations in Longer Responses`为通用长视觉回答幻觉方法邻接项（裁图、提示变化、跨prompt重现），不能算图像鉴伪解释研究。Frontiers 2025多模态假新闻工作报告解释有用性和信任人评，但不是图像伪造鉴定，且全文参与者数量/角色、κ值及结果口径有不一致，已降为谨慎使用的二圈参考。以上均在90及第41页筛选日志中明确分层。
- 已检查EFR全部56条参考文献的既有题名初筛（03/162）与7条强相关引文原文核读（169）；本批未宣称EFR前后向引文闭包完成。下一步仍需沿EFR和其他强种子的参考/被引关系继续递归，并继续宽式分页与非deepfake术语拆分。
- 当前Scholar断点：`https://scholar.google.com/scholar?start=460&q=(%22image+forgery%22+OR+%22image+manipulation%22+OR+%22image+tampering%22)+(explainable+OR+explanation+OR+interpretability+OR+attribution)+(faithfulness+OR+fidelity+OR+grounding+OR+hallucination+OR+%22sanity+check%22+OR+evaluation)&hl=zh-CN&as_sdt=0,5` 转入reCAPTCHA；当前未看到第47页结果。已请求用户在当前Google Scholar页完成验证，从start=460继续。
- 下一步恢复后先读当前页面并将可见10条逐项筛查，再检查第48页；用户此前强调非deepfake图像术语要充分覆盖，之后继续其它未完成的细式和强种子引文链。全项目仍未完成，不能承诺“一个不漏”。

### 2026-10-09：Google Scholar V109 宽式恢复后续筛查至第70页（未完成）

- 用户恢复Google Scholar后，从已有断点继续宽式V109：`("image forgery" OR "image manipulation" OR "image tampering") (explainable OR explanation OR interpretability OR attribution) (faithfulness OR fidelity OR grounding OR hallucination OR "sanity check" OR evaluation)`。第63–70页逐页筛查80个可见题录位置，单页记录为输出216–223，全部逐项写入累计台账74。当前V109累计第1–70页/700个位置，Scholar仍估算约20,900条；下一页为start=700，尚远未到可见末页。结果位置含重复、版本和引文卡片，不是独立论文篇数。
- 新候选优先线索：MoFAIR（ICIC 2026/LNCS，检测—解释统一并针对幻觉解释）、2021年《AHP validated literature review of forgery type dependent passive image forgery detection with explainable AI》、2023年《Enhancing Interpretability in AI-Generated Image Detection with Genetic Programming》、OMNI-fake（CVPR 2026，检测/定位/解释基准）、ForgerySpotter（多尺度证据定位）、《Using LLMs to explain AI-generated art classification via Grad-CAM heatmaps》及《Forensic Analysis of Manipulated Images and Videos》。其中2021综述与2023遗传编程论文在原始出版/作者来源查到直接主题证据；其余候选按领域核心/视频或艺术邻接分别标记。以上还不等于已证明忠实性：需逐篇阅读全文，核查解释输出定义、证据标注、因果/扰动评价、人评和效度局限。
- 边界复核：将“forensic self-description”区分为多尺度取证残差图像表示，而非自然语言理由；将source attribution与XAI attribution区分；注意普通分割定位、注意力图和视觉热图本身不证明模型解释faithfulness。将通用解释评价（What sketch explainability really means、AlignFace、反对抗归因图）作为方法学邻接，不并入图像鉴伪核心文献。
- 新候选与引文追查表90补录MoFAIR、ForgeryPrompting、OMNI-fake、2021图像伪造XAI综述、2023遗传编程解释检测、LLM解释AI生成艺术、视频伪造解释等条目，并明确摘要证据与待核效度之间的区别。页面逐条筛选表216–223保存到忽略输出目录并入74。
- 计数审计83更新：父路线107条/13,941位置、149条子路线/4,837位置、补充82位置不变；域外/独立补充日志增至496位置；合计19,356个结果位置。该数与累计74唯一ID数对齐。历史验证码阻断仍记23次；当前没有活动阻断。87中V109更新为70页/700位置，下一页start=700；整体complete仍为false。
- 已核来源：MoFAIR的Springer DOI/ICIC卷册元数据与摘要检索结果；2021综述期刊原始页/DOI；遗传编程论文IEEE DOI及会议目录；Forensic Self-Descriptions的CVF作者版确认其self-description并非自然语言解释；LLM生成艺术解释的CEUR原文；被篡改图像/视频法证分析的MDPI原文。其余无全文可访问项继续保持待核，不能把Scholar摘要作为全文效度结论。
- 后续从V109 `start=700`继续逐页筛查，同时优先全文审查新发现的2021综述与2023遗传编程论文并沿其参考文献/被引关系检索；之后完成剩余细式、跨路线去重和EFR强种子的递归引文链。不得承诺字面意义“一个不漏”或把20,900条估算等同论文总数。
- 验证：`python3 -m compileall -q work/search_protocol_v2`与`git diff --check`通过；累计74共19,356条，ID无重复且筛选理由齐全；本批8份页面表各10条；83/87计数和断点对齐。阶段ZIP重建为230个文件，CRC通过，SHA-256=`5d2de22cd6bd59ef14c058a65caa2ae9197badbdd80a80f67b0e779465c2c908`。

### 2026-10-09：V109宽式续检至第75页，命中多模态解释评测新核心文献（未完成）

- 延续V109从start=700检索并逐项筛查第71–75页，共50个新结果位置；单页表224–228并入累计74。V109累计第1–75页/750位置；Scholar估算仍约20,900、尚未到可见末页；断点start=750。累计台账现有19,406位置ID，均非空理由且唯一，包含不同查询交叉命中/版本/引文卡片，不等于独立论文数量。
- 重要新直接命中：Scholar将《Dissecting Deepfake Artifacts via Multimodal Explanations》标题缩短显示；已核Springer正式章节页：Bai et al., MMM 2026, LNCS 16412, pp.32–45, DOI `10.1007/978-981-95-6950-2_3`。出版商摘要写明：解释存在视觉接地困难和相互矛盾输出；FakeArti包含1,414张深伪图和4,170个像素级伪迹掩码，作为深伪解释评价基准；ADAD输出视觉伪迹定位和文本解释。这是本题直接核心候选。全文还需核benchmark的ground truth、解释正确性/faithfulness指标和评估效度，不能把benchmark存在等同因果解释faithfulness已证实。其参考文献含《Towards Quantitative Evaluation of Explainable AI Methods for Deepfake Detection》、FakeShield、SIDA、Forensics-Bench等，下一步应建独立参考文献逐条筛查并优先读这些强相关条目。
- 第71页另命中Skyra（CVPR 2026）：CVF官方摘要说明人工伪迹注释、视频伪迹接地推理与解释benchmark；按强相关视频邻接单列。第75页新候选NVMS-Net（摘要同时提通用图像操纵检测与model explainability）以及Journal of Forensic Sciences 2026的Stable Diffusion生成图像似然比法证评价（摘要提解释可视化与校准判据），均加入90候选表；需看原文验证解释定义、解释评估与检测分数校准的区别。第74页《Psychophysical evaluation of human performance in detecting digital face image manipulations》作为人类识别基线邻接，不冒充AI解释研究。
- 页面筛选边界继续区分：普通区域分割/注意力门不自动等于解释；synthetic attribution不等于XAI attribution；image fidelity可能指生成图像逼真度；医学图像伪造、假新闻/脱离语境、一般图像编辑作为邻接或排除项标注。
- 83/87更新：父路线107/13,941、子/引文149/4,837、补充82不变；其他路线外逐位置记录546；合计19,406。V109为75页/750位置，next start=750；历史验证码阻断23、当前无活动阻断。overall complete=false。
- 已验证：Scholar台账页71–75逐条筛查；Springer章节官方摘要/书目信息/参考文献；CVF Skyra官方页；IEEE/Wiley新候选摘要题录。新候选仍待全文，不应写成解释可靠性已验证结果。
- 验证：`python3 -m compileall -q work/search_protocol_v2`、`git diff --check`通过；74累计19,406行且ID唯一/理由和result_position齐全，本批13页日志各10行，83/87对齐。阶段ZIP含235个文件、CRC通过，SHA-256=`31e1b3e3a55aba7a0993e895b3047f68c410fdc609e4887fc6aad75abfa1cf92`。

### 2026-10-09：V109宽式续检至第84页（未完成；下一页start=840）

- Google Scholar宽式V109继续逐页筛查第76–84页（start=750–830），共新增90个结果位置。页面逐条专表229–237并入累计74。检索估算仍约20,900条，尚未到可见末页，不能视为全面覆盖完成或独立论文篇数。
- 新增高优先全文核查候选：`Detection of AI-generated synthetic images with a lightweight CNN`（摘要称讨论方法解释）；`Reliability map estimation for CNN-based camera model attribution`（像素级相机来源归因可靠性图）；`From Sharp Eyes to Expert Mind: Internalizing Expert Knowledge in MLLMs for Tampered Text Detection`（篡改图像文本的视觉接地/定位）；`Score-based Likelihood Ratios for Deepfake Image Evidence`（法证似然比解释）；`DGR-Net: Depth Information Guided Reconstruction Network for Interpretable Generated Image Detection`；`Forged anomaly detection using advanced deep learning`（摘要点明可解释性限制）；`BioForensNet`（科学图像像素级复制移动检测，摘要称可解释）；`DiffSeg`（扩散修补攻击检测和多特征可解释分割）。以上均为摘要筛查候选，只有全文核实解释构念、faithfulness/稳定性评估和数据/评审效度后才可提升为强相关结论。
- 纳入边界审查的邻近方法论文包括`Non-semantic evaluation of image forensics tools`、`FACT`、`MedEBench`、X-Detect、自动驾驶解释综述、PRNU相机归因稳健性等；这些提供可迁移的扰动稳健性、接地或解释保真度方案，但不是图像伪造解释核心实证。对image fidelity（生成图像质量）、似然比校准可靠性、文本/视频鉴伪也分别标明，不与视觉解释忠实性混为一谈。
- 已在Springer出版社页面复核`Dissecting Deepfake Artifacts via Multimodal Explanations`书目信息、摘要及40条参考文献：明确发现Ref.19 `Towards Quantitative Evaluation of Explainable AI Methods for Deepfake Detection`，及Forensics-Bench、FakeShield、SIDA、Face forensic解释等强相关源。下一阶段应建立40条引用逐篇题录筛查记录，并优先核读这些强相关论文，再对关键条目继续前后向引用闭包。Springer摘要显示FakeArti含1,414图和4,170像素级伪迹掩码，但仍需全文核实解释评价的构念效度。
- 计数与断点：累计74为19,496个位置，ID唯一、筛选理由齐全；V109覆盖84页/840位置，下一页`start=840`。父路线107/13,941、子/引文149/4,837、补充82保持此前口径；路线外补充位置636。历史Scholar阻断观察保留；本次恢复后当前无活动阻断；总任务`complete=false`。
- 验证：累计74检查19,496行、19,496个唯一ID、筛选理由无空；页面表229–237每表10行；更新83/87审计和输出归档ZIP。仍须续搜而非将大宽式分页当成已完成任务。

### 2026-10-09：V109宽式续检至第91页（未完成；下一页start=910）

- 延续Google Scholar宽式V109，从start=840筛查至start=900，第85–91页共70个新增位置，逐条表238–244已经并入74。Scholar约20,900条估算不变，尚无末页；V109累计910位置，下一页start=910。
- 本批新增优先原文核验对象：`OmniVL-Guard: Towards Unified Vision-Language Forgery Detection and Grounding via Balanced RL`（摘要含图像篡改定位任务和physical interpretability）；`Enhanced CNN architecture with residual blocks and regularization for AI-generated image detection`（摘要同时称使用XAI）；`A forensic evaluation method for DeepFake detection using DCNN-based facial similarity scores`（法证证据分值评价而非归因解释）；`TrueFake`（真实场景合成图数据集，作为泛化样本邻接）；`Image forgery detection`（2009年早期综述，作为概念和术语前史）。OmniVL-Guard优先级最高；其余依摘要证据分类，待全文确认后再定。
- Scholar对其他近似词条产生大量噪声：通用模型output fidelity、文本到图像生成quality、图像编辑image fidelity、医学/出版伦理图像操纵、多模态假新闻、人脸社会知觉和交互式图像操作均逐项注明排除/邻接理由。第89页的WireLLM条目摘要只引用FakeShield，按标题和实际任务排除，同时把其FakeShield引文作为引用追踪线索，避免把引用上下文误当成该文自身结果。
- 计数更新：总账74为19,566位置观察且ID唯一、理由完整；父107/13,941，子149/4,837，补充82，域外逐位置日志706。V109第1–91页/910位置；下一页start=910；整体complete=false。累计数字包括多路线重复版本/引用卡片，不等于独立论文。
- 检查：74累计行数与唯一ID均19,566、筛选理由零空值；单页表238–244各10条；83/87更新；归档ZIP 289个文件成员、CRC通过，SHA-256=`ffce10b78a116778981507a3805050e54921361e256edd7bd8b2de8edbbb5f35`；`python3 -m compileall -q work/search_protocol_v2`和`git diff --check`通过。仍需续检与闭合强相关论文的参考/被引链。
