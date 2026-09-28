# Stage A.4 预注册：反事实重合成算子
## Counterfactual Re-synthesis for Forensic Evidence–Decision Faithfulness

> **本文件在结果产出之前写定。** 算子定义、冻结参数、判据与指标一经写下，不得因结果而调整；
> 任何偏离必须在报告中显式声明并单独归类。
>
> 取代 `edition3_stage_A3_evidence_utility_protocol.md` 的 §A3.3（基于 pristine 的像素恢复）。
> edition3 的其余部分（Gate 体系、指标定义、对照要求、禁止事项）仍然有效。

---

## 0. 为什么必须换掉旧算子

| 旧算子 | 实际行为 | 已实证的后果 |
|---|---|---|
| Gaussian blur | 往区域里**加入** blur artifact，而非移除证据 | edition1：`delta_gt < 0` 达 **54/80**；V3 necessity p=0.056 → Holm 后 **0.338**（不显著） |
| 黑块遮挡 | 引入 OOD 遮挡，测的是"模型对黑块的响应" | edition2 §17 已禁止作为主结果 |
| 像素恢复 `forged·(1−M)+pristine·M` | 需要 pristine | **纯 AI 生成图原理上没有 pristine**（SynthScars / GenImage / Chameleon），edition2 在目标域上不可执行 |

三者共同的死结：**要么绕开 pristine 而干预无效，要么需要 pristine 而目标域没有。**

---

## 1. 算子定义（冻结）

```
x_resynth(E) = Inpaint(x_forged, mask = M_E, prompt = P_frozen)
```

以图像其余部分为条件，用扩散 inpainting **重写** E 区域的内容。E 内的原始伪迹被覆盖，
**不需要 pristine**。

**冻结参数**（写死于 `07_resynthesize.py` 默认值，运行时写入输出供审计）：

| 参数 | 值 |
|---|---|
| 模型 | `diffusers/stable-diffusion-xl-1.0-inpainting-0.1`（fp16） |
| prompt | `""`（空 —— 最中性，不注入语义内容） |
| negative_prompt | `""` |
| steps | 30 |
| guidance | 7.5 |
| seed | 20260921（全局固定，对所有样本一致） |
| 尺寸处理 | padding 到 8 的倍数 → inpaint → 裁回原尺寸（`original` 变体不经此路径） |

**区域集合**（每样本）：

```
claimed        模型自己声称的证据区域（Qwen3-VL 原生 evidence_regions 光栅化）
control_1..3   等面积、语义匹配、不重叠的对照（DINOv2 冻结特征；复用 faithpilot.control_matching）
random         等面积随机矩形（测算子的一般效应）
gt             SynthScars 人工标注的真实伪迹区域（阳性对照）
original       原图未改动副本（必要性差值的基准，必须与其他变体同轮打分）
```

---

## 2. 算子成立的前提：自伪影可被对照抵消

重合成**会引入生成模型自身的渲染特征**（已由盲审确认）。这不是缺陷，而是算子必须配套对照的理由：

```
Δs(E) 同时包含两件事：(a) E 内原始伪迹被移除的效应
                      (b) 新生成内容自身特征的效应
```

(a) 只在目标区出现，(b) 在目标区与对照区**同量出现** → `gap = Δs(E) − Δs(control)` 消去 (b)。

**因此：**

- **`gap` 是唯一可用于主结论的量**，裸的 `Δs(E)` 不得单独解释为"证据被移除的效应"
- **必须同时报告 `Δs(random)`**：若 `Δs(random)` 与 `Δs(control)` 量级相当且都远小于 `Δs(E)`，
  说明算子的一般效应可控、特异性真实存在；若 `Δs(random)` 本身就很大，
  说明**算子在驱动判定**，本阶段结论作废，须回到算子设计

---

## 3. 历史 Gate 状态更正（2026-09-28）

此前记录的 0.727（95% CI [0.652, 0.795]，p=7.8e-09）来自 161 张 SynthScars 假图上的判假比例。Stage-A 原始记录仅含 `label=1`；旧 Gate 0 脚本只统计假类。因此该值是 **fake recall**，旧二项检验不是真假检测优于随机的检验。真实类 recall、balanced accuracy 与 AUROC 均不可由该批样本估计。旧 Gate 0 PASS 撤回，状态更正为 **BLOCKED_SINGLE_CLASS**；恢复真假两类同域样本并用修正脚本重算后，才可进入忠实性主分析。

161 张解释互不相同只说明文本没有重复，不能单独证明解释接地或可用于 per-sample 空间因果分析。Gate 7 需按其独立的定位/事实核验定义重新审查，不得把唯一率当作接地性通过证据。

| Gate | 历史记录 | 更正状态 |
|---|---|---|
| **Gate 0 二分类检测能力** | 假图子集 fake recall 0.727；旧 CI 与 p 值检验的是该假类比例 | **BLOCKED_SINGLE_CLASS**；无 real 样本，不能估计二分类能力 |
| **解释唯一率** | 1.000（161 张各有不同解释） | 只作文本多样性描述，不等同 Gate 7 接地性 |
| Gate 1 仪器阳性对照 | 旧 blur/resynthesis 结果 | 依当前可访问的 80 样本重分析，GT blur 方向与证据移除预期相反；算子未通过，见 `work/experiment_audit_20260928/` |
| Gate 5 噪声底 | noop 漂移为 0 | 仅说明 log-likelihood 打分重复性，不验证干预有效性 |

**Gate 0 的意义**：只有当真假两类均被纳入并且检测器确有判别力时，才适合讨论其证据忠实性。此前“模型在该数据集上有实际判别力”的结论撤回。Gate 7 的唯一率解释亦不再作为空间因果分析前提通过的依据。

---

## 4. 指标定义（log-odds，不用 p_fake）

```
s(I)       = logP(fake|I) − logP(real|I)                两路 log-odds
Δs(E)      = s(original) − s(resynth_E)                 必要性
Δs(random) = s(original) − s(resynth_random)            算子一般效应
Δs(gt)     = s(original) − s(resynth_gt)                阳性对照
Δs(ctrl)   = mean_i Δs(control_i)
gap(E)     = Δs(E) − Δs(ctrl)                           特异性（主结论量）
```

**为何不用 `p_fake`**：edition1 实测其已饱和（均值 0.785、63/80 ≥ 0.5），
`claimed_gap` 均值 +0.0576 而中位数仅 +0.0024（相差 24 倍），天花板效应会吞掉真实效应。

**打分必须同轮**：`original` 与所有变体在**同一次运行、同一 prompt、同一模型实例**下打分，
差值运行内自洽，不得跨运行拼接。

---

## 5. 确认性判据（先校准等效界 δ，再冻结测试）

`δ` 是可忽略与有实际意义的最小差异，不得从确认性测试结果倒推。应先用独立校准集估计重复推理噪声、盲审通过的阳性对照效应与测量误差，然后冻结 `δ`、primary endpoint、测试样本、随机种子和排除规则。统计单位是独立 source image；同源多次篡改须按 source image 做 cluster bootstrap。

对于文字上正确、可定位、且经盲审确认与伪迹相关的解释，主终点为 `G = Δs(claimed) − mean(Δs(matched controls))`。单独的“未显著”不能写作 `G≈0`；只有置信区间完整落在预注册等效区间 `[-δ,+δ]` 才能支持“自述区域相对匹配对照没有额外决策价值”。

| `gap(claimed)` | `Δs(gt)` | 结论 |
|---|---|---|
| 95% CI 下界 > `δ` | GT 阳性对照有效（95% CI 下界 > `δ`） | 支持模型对所述且经核验的区域有特异决策依赖；会削弱“该类解释通常不是检测依据”的说法 |
| 90% CI 完全位于 `[-δ,+δ]` | GT 阳性对照有效，且 Gate 0 通过 | 支持该目标域中“模型对真实伪迹有反应，但自述区域不比匹配控制更有决策价值” |
| GT 或整图阳性对照失败，或 Gate 0 失败 | 任意 | **BLOCKED**：不能解读为有依赖或无依赖 |
| 区间既未越过 `δ`，也未落入等效区间 | 任意 | **INCONCLUSIVE**：增加样本或改进测量，不做二分结论 |
| 95% CI 上界 < `−δ` | 任意 | 方向与假设冲突；先审计算子、区域匹配和分数定义，不直接作机制结论 |

**同时报告 `Δs(random)`、`Δs(whole)`、`Δs(gt)` 和 matched controls** 以验证算子及区分局部与整图线索。若 claimed 区域经事实/定位核验失败，将其标记为解释错误，单独报告，不混入“正确解释是否被决策使用”的主终点。

**correct-but-unfaithful 单元格**：

```
IoU(claimed, gt) 达到预注册定位标准  且  G 的 90% CI ∈ [−δ,+δ]
                                                     ← "位置经核验"但无相对控制区的额外决策价值
```

必须报告 prevalence、按 source image cluster bootstrap CI，以及定位标注一致性；定位阈值和 δ 均需在测试前冻结。

---

## 6. 统计

cluster bootstrap 95% CI（≥2000 次）、paired sign-flip、positive fraction、median、mean；主终点只设一个。次要检验用 Holm 校正。对“无额外效应”必须做预注册等效检验，不能把普通零假设检验的 p≥0.05 当作证据。

---

## 7. 不允许的做法

继承 edition3 §10 全部条目，并新增：

- ❌ 用裸的 `Δs(E)` 作为主结论（未扣除算子自身效应）
- ❌ 不报告 `Δs(random)` 就声称特异性
- ❌ 看到结果后调整算子参数（prompt / steps / guidance / seed / 区域选取规则）
- ❌ 跨运行拼接 `s(original)`
- ❌ 把降级对照（`fallback_random_rect`）与语义匹配对照混算（必须分层报告）
- ❌ 把 `original` 变体排除在本轮打分之外

---

## 8. 产物

```text
data/derived/stage_a3/resynth_synthscars161/
  images/<sample_id>__{original,resynth_claimed,resynth_control_1..3,resynth_random,resynth_gt}.png
  masks/<sample_id>__{claimed,control_1..3,random,gt}.png
  crops_before/  crops_after/        干预前后裁剪，供盲审
  resynthesis.jsonl                  区域、面积、对照来源、算子参数
  resynthesis_summary.json

results/stage_a3/
  scores_resynth_synthscars161.jsonl 同轮打分（含 original）
  effects_synthscars161.json         Δs / gap / CI / Holm / 单元格
  effects_synthscars161_per_sample.csv
```

---

## 9. 本阶段必须回答

| Q | 问题 |
|---|---|
| Q1 | 重写模型**自己声称的**区域，是否比重写等面积匹配对照更改变判定？(`gap > 0`?) |
| Q2 | `Δs(random)` 与 `Δs(ctrl)` 量级是否相当且远小于 `Δs(claimed)`？（算子是否可控） |
| Q3 | 重写**真实伪迹区域**（GT）是否产生显著效应？（阳性对照） |
| Q4 | 是否存在 IoU 高但 gap 低的样本？占比与 CI？ |
| Q5 | 结论是否支持进入 Stage B（偏好学习）？ |

最终只允许输出 **PASS / PARTIAL PASS / FAIL**，附明确理由。

---

## 10. 与旧结果的关系

本阶段**取代**而非补充：

- edition1 / V3 的 blur 干预结果（`necessity p=0.056 → 0.338`）**作废**，不得与本次结果并列引用
- edition3 §A3.3 的 pristine 像素恢复在目标域上不可执行，**整节作废**
- edition1 / V3 的解释文本、claimed 区域与 SynthScars 标注仍可作输入审计材料；旧 Gate 0 数值仅可视为 label=1 子集上的 fake recall，不能作为二分类准入。仅保留的 intervention scores 也不代表原图/掩膜/模型权重可用。
