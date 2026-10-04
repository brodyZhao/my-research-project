# Project Handoff

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
