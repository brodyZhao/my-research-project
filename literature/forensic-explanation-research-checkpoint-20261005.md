# 解释可靠性文献重检：2026-10-05阶段索引

用户要求在Google Scholar重新扩大检索，并记录全部结果的逐条筛选和强相关种子引用链；旧目录遗漏EFR，不能继续作为完整检索。

当前为受Google Scholar限流影响的阶段交付，尚未完成，不声称零遗漏。21条路线中19条观察到可见终页，其中GS007触及第100页且估计总数仍超过实际可见数，标注显示边界风险；无此风险的可见终页为18条。GS007待分段补查、GS010第62页受阻、GS020待继续。正常范围4063个结果位置，异常过滤15个位置另存，逐条日志合计4078条。所有初筛注明证据范围；规则辅助初筛不写成人工全文审读。

EFR全部56条参考文献已逐篇写出筛选理由并取得原页或作者公开稿；其当前被引用1条已查完。另11篇核心种子620个参考位置已提取初筛，未完成全部被引论文的原页核验。旧337条全部重新对照，不继承旧验证标签。当前28篇核心论文的原页摘要及部分方法/实验段已人工复核，按照相关性给出阅读顺序。

工作目录和outputs按仓库规则留在本地；本索引不上传论文全文、候选网页或原始下载文件。

本地交付入口：

- [00_重检阶段报告_未完成.md](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/00_重检阶段报告_未完成.md)
- [12_原页复核核心文献_按相关性排序.md](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/12_原页复核核心文献_按相关性排序.md)
- [02_谷歌学术全部结果逐条筛选.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/02_谷歌学术全部结果逐条筛选.csv)
- [03_EFR全部56条参考文献逐篇排查.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/03_EFR全部56条参考文献逐篇排查.csv)
- [04_重检候选目录_暂按相关性排列.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/04_重检候选目录_暂按相关性排列.csv)
- [09_强相关种子620个参考文献位置初筛.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/09_强相关种子620个参考文献位置初筛.csv)
- [10_旧337条逐项重审与对照.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/10_旧337条逐项重审与对照.csv)
- [05_检索路线覆盖与终页核对.json](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/05_检索路线覆盖与终页核对.json)
- [17_文件与覆盖一致性检查.json](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/17_文件与覆盖一致性检查.json)

验证：EFR 56条ID与本地证据文件SHA256相符；逐位置、引用链、旧目录、核心表CSV读回计数一致；页码连续；限流不计终页；稳定ID与核心序号无冲突；检索脚本compileall、git diff --check通过。这些检查验证文件完整性，不验证召回率或结论全部正确。

后续必须继续：GS010第62页起和GS020分页、GS007分段补查，并执行扩展术语路线，核查未审原稿、所有强相关种子前向/后向链及新发现的衍生分支。Google Scholar曾返回automated queries限制，间隔十分钟仍受限，未出现验证码；已请求用户检查是否恢复。

2026-10-05恢复续查：新增2064个实际结果位置，原始日志解析零错误；稳定性63页627个位置、可靠性26页254个位置、不可辨识性10条已到可见终页。反事实第62页再次返回automated queries，无验证码。全局重检未完成，没有推进后续分析。
