# 解释可靠性文献重检：2026-10-05阶段索引

用户要求在Google Scholar重新扩大检索，并记录全部结果的逐条筛选和强相关种子引用链；旧目录遗漏EFR，不能继续作为完整检索。

当前为受Google Scholar限流影响的阶段交付，尚未完成，不声称零遗漏。已执行30条路线，其中28条观察到可见终页，27条未触及分页边界。GS007原查询第100页存在显示边界风险，已用GS023（≤2025）55页548个位置与GS024（≥2026）56页552个位置补查，查出126个原查询未显示的题名位置；无年份条目及索引穷尽性仍未证明。正常范围6034个结果位置，异常过滤15个位置另存，逐条日志合计6049条，本轮新增1971个位置。规则辅助初筛不冒充人工全文审读。

EFR全部56条参考文献已逐篇写出筛选理由并取得原页或作者公开稿；其当前被引用1条已查完。另11篇核心种子620个参考位置已提取初筛，未完成全部被引论文的原页核验。旧337条全部重新对照，其中183条在本轮主题或引文链已有匹配，不继承旧验证标签。当前30篇核心论文的原页摘要及部分方法/实验段已人工复核，按相关性给出阅读顺序；本轮新增DocShield与Quantifying Explainability with Multi-Scale Gaussian Mixture Models。后者核对作者PDF§4–7，日期待正式题录核验；不把显著图分布相似性当成决策因果忠实性。

本轮已查完GS010反事实81页807个位置、GS022图像拼接2页11个位置、GS025保真度35页350个位置、GS026明确解释保真度4页33个位置、GS027删除/插入23页224个位置、GS028参数随机化7个位置、GS029健全性检查3页29个位置。GS030生成图像解释事实性记录了前2页20个位置，第3页再次返回automated queries限制，无验证码，断点start=20；不当作零命中或终页。

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
- [18_分页上限分段补查_差集初筛.csv](/Users/zhaomengchen/research/faithfulness/my-research-project/outputs/图像鉴伪解释可靠性_重检_2026-10-05/18_分页上限分段补查_差集初筛.csv)

验证：EFR 56条ID与本地证据文件SHA256相符；逐位置、引用链、旧目录、核心表CSV读回计数一致；页码连续；限流不计终页；稳定ID与核心序号无冲突；检索脚本compileall、git diff --check通过。这些检查验证文件完整性，不验证召回率或结论全部正确。

后续必须继续：GS030第3页及GS020分页，剩余扩词、强相关文献引用链、原稿核验和版本去重；GS007分段已查完但索引边界风险仍需在最终检索边界中说明。2026-10-05 15:22上海时间Scholar再次限制，已请用户手动确认恢复。没有推进研究方案或模型实验阶段。

2035个公开原页URL已尝试获取，1223个HTML响应身份尚待人工核对、62个PDF未提取正文、134个空响应、615次失败，另1份GMM作者PDF已提取并人工核对。获取成功不等于题录或结论可靠性已核验。原稿证据留在work，不上传论文全文。

本轮采集增加无损重复字段引用，导出器严格还原，当前零解析错误；GS027第17页曾部分加载，已重读补全，并增加页面底部加载检查以防误判终页。
