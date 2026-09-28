# Project Handoff

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
