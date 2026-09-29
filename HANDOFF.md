# Project Handoff

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

`483bc0a` (`docs: update GitHub handoff status`)

## Current Goal

在当前项目建立 Codex、GitHub 与 ChatGPT Web 之间的稳定协作流程。

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
- 本地交付：`outputs/可定位解释模型复验_模型审计与SIDA数据核验_2026-09-29.md`；本地代码和原始数据审计：`work/sida_probe/prepare_assets.py`、`audit_dataset.py`、`dataset_audit.json`、`score_adapter.py`、`perturb.py`、`smoke_sida.py`。本轮按用户要求先固定了门控实验方案：单图 smoke → 30 张基线门 → 官方独立 test → 配对区域反事实与真实掩码正对照；需至少 36 张正确且 IoU≥0.2 的篡改图才做确认性判断。`outputs/` 与 `work/` 依项目规则被 Git 忽略，不提交模型、数据或本地临时产物。未改动用户已有未跟踪文件 `faithfulness_pilot_EXPERIMENT_LOG_2026-09-27.md`。
- 远程主机：`root@connect.nmb1.seetacloud.com:27002`；代码 `/root/autodl-tmp/SIDA`，验证集和模型 `/root/autodl-tmp/sida_probe`。模型权重现已下载完成，约 16GB；独立 Python 3.10 环境正在安装 CUDA 版 PyTorch。源码 revision `6b1c3aa9097a79849ea7aae95601854763014a9d`；模型 revision `282cffe609bea1917d9d63138a4989aac7314e2a`；数据 revision `fa7a00ee2d68579630bb81d1bdcae7d3ff9c7a81`。
- 实际数据核验：解释数据 validation 300 张，三类各 100；文字均非空；100 张局部篡改均有非零真值掩码。14 张局部篡改图像与掩码尺寸不一致；掩码面积 0.1%—50% 且尺寸一致时有 67 张预估候选（此前更窄的 1%—30% 范围有 49 张）。原始统计在 `work/sida_probe/dataset_audit.json`。这只是数据审计，不是模型实验结论。作者的独立 `test.zip` 需经 Google Drive 获取，但远程对 Drive 的请求报网络地址分配错误，尚未下载。
- 测试：`python3 -m compileall -q work/sida_probe` 通过；`score_adapter` 的合成张量 smoke 通过；`perturb` 的等面积、非重叠、掩码外像素不变 smoke 通过。SIDA GPU smoke **未运行**。
- 当前阻塞：SSH 可达但远程仍无 `/dev/nvidia*`，`torch.cuda.is_available() == False`，设备数 0；用户需恢复 GPU。Google Drive 官方测试包也暂时无法从该主机访问。PyTorch CUDA 环境安装仍在进行。故没有任何 SIDA 推理结果。
- 建议 ChatGPT Web 下一步检查：GPU 与官方 test 数据可访问后，先运行 `work/sida_probe/smoke_sida.py`；检查三输出同源、长短生成分数差≤0.01；再执行 30 张短基线门。只有 balanced accuracy≥0.70 且至少 5 个正确且 IoU≥0.2 的篡改样本时才做完整基线；确认性实验要求至少 36 张合格样本和真实掩码正对照通过。不要把现有 validation 300 张冒充独立确认性 test。

---
