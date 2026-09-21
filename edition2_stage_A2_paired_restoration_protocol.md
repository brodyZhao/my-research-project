# Stage A.2 Pilot Experiment
## Paired Restoration for Forensic Evidence–Decision Faithfulness

> 目标：修正 Stage A 中 Gaussian blur 无法代表“删除伪造证据”的问题，使用 **pristine–forged paired restoration** 验证：  
> **模型声称的 forensic evidence 是否真的参与 authenticity decision。**
>
> 当前基线模型：`Qwen3-VL-8B-Instruct`  
> 当前状态：Stage A（blur diagnostic）未通过，不进入 DPO。  
> 本阶段只做 **更严格的因果诊断**，仍然不训练。

---

## 0. 为什么需要 Stage A.2

Stage A 的问题不是代码失败，而是 intervention 本身不够干净。

Gaussian blur 实际执行的是：

```text
原有伪造区域
→ 加入 blur artifact
```

而不是：

```text
原有伪造区域
→ 恢复为真实内容
```

因此 Stage A 中出现：

```text
GT 区域被 blur 后
P(fake) 反而上升
```

不能解释为：

```text
GT evidence 没有参与决策
```

更可能是：

```text
blur 本身引入了新的异常取证信号
```

Stage A.2 必须尽可能接近真正的：

```text
do(forensic evidence = removed)
```

---

## 1. Stage A.2 只回答两个问题

### H1：GT evidence 是否真的具有决策作用

对于伪造图像：

```text
x_forged
```

如果把真实伪造区域恢复成 pristine image 对应内容：

```text
x_restore_gt
```

那么应观察：

```text
P(fake | x_forged)
>
P(fake | x_restore_gt)
```

即：

```text
delta_gt_restore > 0
```

### H2：模型声称的 evidence 是否具有同样作用

如果模型声称区域：

```text
E_claimed
```

确实是模型真实使用的证据，那么恢复该区域后：

```text
P(fake)
```

也应下降。

比较：

```text
delta_claimed_restore
```

和：

```text
delta_control_restore
```

如果：

```text
delta_claimed_restore
>
delta_control_restore
```

说明 claimed evidence 至少具有一定 decision utility。

---

## 2. 数据要求

Stage A.2 **必须优先使用 paired data**。

每个样本至少有：

```text
sample_id
forged_path
pristine_path
gt_mask_path
claimed_mask_path
```

其中：

- `forged_path`：篡改图
- `pristine_path`：对应原图
- `gt_mask_path`：真实篡改区域
- `claimed_mask_path`：Qwen3-VL 声称区域

---

## 3. 建议样本规模

Pilot 不需要一开始做很多。

优先：

```text
20–40 对 paired samples
```

如果资源允许：

```text
40–80 对
```

要求：

- pristine 与 forged 必须严格空间对应；
- 不允许不同裁剪、缩放、旋转版本直接配对；
- 如果存在尺寸差异，需要先确认是否能无损对齐；
- 无法可靠对齐的样本直接剔除；
- 不要为了凑数量强行使用不可靠 pair。

---

## 4. 建议目录结构

在现有实验目录下新增：

```text
experiments/
└── forensic_preference_pilot/
    ├── stage_a2/
    │   ├── configs/
    │   │   └── stage_a2.yaml
    │   ├── data/
    │   │   ├── paired_manifest.jsonl
    │   │   └── aligned_pairs/
    │   ├── scripts/
    │   │   ├── 01_validate_pairs.py
    │   │   ├── 02_build_restorations.py
    │   │   ├── 03_score_variants.py
    │   │   ├── 04_measure_effects.py
    │   │   └── 05_generate_report.py
    │   └── outputs/
    │       ├── restorations/
    │       ├── scores/
    │       ├── metrics/
    │       └── report/
```

---

## 5. Step A2.1：验证 pristine–forged pair

Codex 先检查：

```text
forged.size == pristine.size
```

如果不一致：

1. 检查是否只是无损 resize；
2. 检查是否存在 crop offset；
3. 如果无法确定像素级对应关系，剔除该 pair。

### 必做质量检查

对每对图像输出：

```text
absolute_difference_map
```

并计算：

```text
mean_abs_diff_inside_gt
mean_abs_diff_outside_gt
```

理想情况：

```text
inside_gt >> outside_gt
```

如果：

```text
outside_gt
```

也很大，说明 pristine/forged 并非严格配对。

建议定义：

```text
pair_quality_ratio =
mean_abs_diff_inside_gt
/
(mean_abs_diff_outside_gt + eps)
```

低质量 pair 单独标记。

---

## 6. Step A2.2：重新固定 baseline evidence

仍使用现有固定 forensic prompt。

对每张：

```text
x_forged
```

重新获取：

```text
verdict
rationale
claimed bbox/mask
```

要求：

- model 固定为 `Qwen3-VL-8B-Instruct`
- `do_sample=False`
- prompt 完全不变
- max_pixels 固定
- 保存 raw response
- 保存 parsed evidence
- 不允许人工修改 claimed region

---

## 7. Step A2.3：构造四类 restoration

每张样本构造以下 variant。

### Variant 0：原始伪造图

```text
x_forged
```

### Variant 1：GT restoration

定义：

```text
x_restore_gt
=
x_forged outside GT
+
x_pristine inside GT
```

公式：

```text
x_restore_gt
=
x_forged * (1 - M_gt)
+
x_pristine * M_gt
```

目标：

```text
尽可能真正移除 GT forensic evidence
```

### Variant 2：Claimed restoration

定义：

```text
x_restore_claimed
=
x_forged outside claimed
+
x_pristine inside claimed
```

如果 claimed region 与 GT overlap 很高：

```text
应该观察到 P(fake) 下降
```

如果 claimed region 位置正确但 decision utility 低：

```text
P(fake) 可能变化很小
```

### Variant 3：Matched control restoration

control 不能只随机平移。

至少匹配：

```text
面积
位置层级
语义区域
```

优先顺序：

#### Level 1：同一物体内部匹配

例如：

```text
claimed region 在脸部
→ control 也在脸部其他区域
```

#### Level 2：同类语义区域匹配

例如：

```text
claimed region 在文字区域
→ control 也选文字区域
```

#### Level 3：仅面积匹配

如果无法做语义匹配，再退化到：

```text
equal-area
non-overlap
```

每张图至少：

```text
3 个 control
```

最好：

```text
5 个 control
```

最终取均值。

---

## 8. Restoration 质量约束

恢复后不能引入明显边界。

建议：

```text
直接像素替换
```

优先于：

```text
blur
inpainting
masking
```

如果 mask 边界存在 1–2 像素错位，可以测试：

```text
GT mask dilation: 1 px
GT mask dilation: 3 px
GT mask dilation: 5 px
```

但第一版主结果必须固定一种策略。

### 必做可视化

每张至少保存：

```text
forged
pristine
gt mask
claimed mask
restore_gt
restore_claimed
restore_control_1
```

人工检查至少：

```text
10–20 个样本
```

确认：

- restoration 没有明显接缝；
- 没有新 blur artifact；
- 没有错位；
- 没有把无关语义大面积替换掉。

---

## 9. Step A2.4：模型打分

继续使用 Stage A 已验证过的 forced-choice scoring。

对每个 variant 计算：

```text
P(fake)
P(real)
log_odds(fake/real)
```

至少记录：

```text
p_fake_forged
p_fake_restore_gt
p_fake_restore_claimed
p_fake_restore_control_mean
```

---

## 10. 核心指标

### 10.1 GT Restoration Effect

```text
delta_gt_restore
=
p_fake_forged
-
p_fake_restore_gt
```

预期：

```text
delta_gt_restore > 0
```

### 10.2 Claimed Restoration Effect

```text
delta_claimed_restore
=
p_fake_forged
-
p_fake_restore_claimed
```

### 10.3 Control Restoration Effect

```text
delta_control_restore
=
p_fake_forged
-
mean(p_fake_restore_control_i)
```

### 10.4 Claimed Specificity Gap

```text
claimed_gap_restore
=
delta_claimed_restore
-
delta_control_restore
```

预期：

```text
claimed_gap_restore > 0
```

### 10.5 GT Specificity Gap

```text
gt_gap_restore
=
delta_gt_restore
-
delta_gt_control_restore
```

如果给 GT 单独构造 control：

```text
gt_gap_restore > 0
```

---

## 11. Evidence Correctness

计算：

```text
IoU(claimed_mask, gt_mask)
Dice(claimed_mask, gt_mask)
```

至少将样本分成三组：

```text
High overlap
Medium overlap
Low overlap
```

例如：

```text
High:   IoU >= 0.5
Medium: 0.2 <= IoU < 0.5
Low:    IoU < 0.2
```

阈值仅作 Pilot 使用，可后续调整。

---

## 12. 关键分析：Correct-but-Unfaithful

重点寻找：

```text
IoU 高
但
delta_claimed_restore 低
```

例如：

```text
IoU >= 0.5
delta_claimed_restore <= 0.05
```

这类样本代表：

```text
模型“说对了位置”
但“判断并不依赖这个位置”
```

这是当前研究最重要的现象。

---

## 13. 关键分析：Wrong-but-Useful

也记录：

```text
IoU 低
但
delta_claimed_restore 高
```

这可能说明：

```text
模型依赖的是错误或 shortcut region
```

不要丢弃这些样本。

它们可能成为后续：

```text
shortcut suppression
```

的重要证据。

---

## 14. Statistical Test

至少保留：

```text
bootstrap 95% CI
paired sign-flip test
positive fraction
median
mean
```

核心比较：

```text
delta_gt_restore vs 0
delta_claimed_restore vs 0
claimed_gap_restore vs 0
```

并额外比较：

```text
delta_gt_restore
vs
delta_claimed_restore
```

---

## 15. Stage A.2 Gate

只有满足以下条件，才进入 preference construction / DPO。

### Gate 1：GT restoration 有效

要求：

```text
mean(delta_gt_restore) > 0
```

并且：

```text
95% CI 不跨 0
```

理想情况：

```text
sign-flip p < 0.05
```

### Gate 2：claimed evidence 有 specificity

要求：

```text
mean(claimed_gap_restore) > 0
```

并优先希望：

```text
95% CI 不跨 0
```

### Gate 3：存在 correct-but-unfaithful 样本

至少存在一批：

```text
IoU 高
但
decision effect 低
```

否则：

```text
当前“证据正确但决策不忠实”的钉子可能并不稳定
```

---

## 16. 结果解释矩阵

### Case A

```text
GT restore effect > 0
Claimed restore effect > control
且存在 correct-but-unfaithful
```

结论：

```text
当前钉子得到支持
Evidence Perturbation + Preference Optimization 值得继续
```

下一步：

```text
Stage B preference pair construction
```

### Case B

```text
GT restore effect > 0
Claimed restore effect ≈ GT restore effect
```

结论：

```text
模型实际上较忠实
“claimed evidence 不参与决策”的问题没有预期严重
```

需要重新评估课题重要性。

### Case C

```text
GT restore effect ≈ 0
```

结论：

```text
模型可能主要依赖全局特征 / shortcut
而非局部 forensic evidence
```

下一候选方向：

```text
shortcut suppression
global-local evidence decomposition
```

### Case D

```text
GT restore effect < 0
```

即恢复 GT 后反而更容易判假。

优先检查：

```text
pair alignment
restoration boundary
GT mask quality
model scoring
```

如果这些都正常，再考虑：

```text
模型确实使用其他 shortcut
```

---

## 17. 不允许的做法

Codex 不应：

- 用 blur 作为 Stage A.2 主结果；
- 用黑块遮挡作为主结果；
- 没有 pristine pair 时伪造“restoration”；
- 用生成式 inpainting 冒充真实 pristine restoration；
- 人工移动 claimed mask 以提高 IoU；
- 根据最终结果挑阈值；
- 丢掉 negative cases；
- Stage A.2 gate 未通过就进入 DPO。

---

## 18. 推荐新增脚本

建议：

```text
01_validate_pairs.py
02_build_restorations.py
03_score_restorations.py
04_measure_restore_effects.py
05_analyze_correct_but_unfaithful.py
06_generate_stage_a2_report.py
```

---

## 19. 输出文件

至少生成：

```text
outputs/stage_a2/
├── metadata/
│   ├── validated_pairs.jsonl
│   └── pair_quality.csv
├── restorations/
├── scores/
│   └── forced_choice_scores.jsonl
├── metrics/
│   ├── per_sample.csv
│   └── summary.json
└── report/
    ├── stage_a2_report.md
    ├── success_cases/
    ├── correct_but_unfaithful/
    └── failure_cases/
```

---

## 20. 最终报告必须回答

Codex 最终生成的 `stage_a2_report.md` 必须明确回答：

### Q1

```text
恢复真实 GT 伪造区域后，
Qwen3-VL-8B 的 P(fake) 是否稳定下降？
```

### Q2

```text
恢复模型声称区域后，
P(fake) 是否比恢复 matched control 区域下降更多？
```

### Q3

```text
是否存在：
Evidence Correctness 高
但 Decision Faithfulness 低
的样本？
```

### Q4

```text
当前结果是否支持进入 Stage B：
Forensic Evidence Preference Learning？
```

最终只允许输出：

```text
PASS
PARTIAL PASS
FAIL
```

并附上明确理由。

---

## 21. 最推荐的执行顺序

```text
[ ] 1. 找到 20–40 对 pristine–forged paired data
[ ] 2. 检查像素级对齐
[ ] 3. 检查 GT mask
[ ] 4. 重新生成 claimed evidence
[ ] 5. 构造 GT restoration
[ ] 6. 构造 claimed restoration
[ ] 7. 构造 3–5 个 matched controls
[ ] 8. 人工检查 restoration 质量
[ ] 9. forced-choice score
[ ] 10. 计算 delta / gap / CI / p-value
[ ] 11. 分析 IoU vs decision effect
[ ] 12. 搜索 correct-but-unfaithful cases
[ ] 13. 根据 Gate 决定是否进入 Stage B
```

---

## 22. 本阶段最重要的原则

Stage A.2 不是为了证明我们的假设一定正确。

目标是：

```text
设计一个足够干净的 intervention，
让“假设不成立”和“实验方法不可靠”
尽可能可以区分。
```

只有当：

```text
paired restoration
```

本身可靠以后，

```text
evidence → decision
```

的因果讨论才有意义。
