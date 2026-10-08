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
