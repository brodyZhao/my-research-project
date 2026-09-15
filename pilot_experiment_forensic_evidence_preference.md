# Pilot Experiment：反事实证据引导的图像鉴伪偏好学习

> 目标：用最小资源先验证 **Evidence Perturbation + Preference Optimization** 这把“锤子”在图像鉴伪中是否成立。  
> 当前基线：Qwen3-VL。  
> 当前数据：已有 80 张可进行严格对照的候选图像；若存在对应 pristine/original 图与 GT forgery mask，优先使用。  
> 本文件面向 Codex 执行，**先完成 Stage A，再决定是否进入 Stage B**。

---

## 0. Pilot 只回答三个问题

### H1：证据是否具有可测的“决策价值”
模型真正应该依赖的伪造证据被反事实干预后，`P(fake)` 应明显变化；无关区域被同样干预后，变化应更小。

### H2：能否自动构造偏好对
是否可以稳定得到：

- `preferred`: 正确且具有较强决策作用的 forensic evidence
- `rejected`: 语言合理，但证据错误或决策作用很弱的 evidence

### H3：小规模偏好学习是否有收益
在不明显损害真假检测准确率的前提下，LoRA + DPO 后：

- Evidence Correctness ↑
- Decision Faithfulness ↑
- 对无关区域的敏感性不增加

> **停止原则：** 如果 H1 都无法稳定成立，不进入大规模 DPO；先检查反事实构造方式和指标定义。

---

## 1. 推荐模型与资源配置

### Pilot 默认模型

优先使用：

```text
Qwen/Qwen3-VL-4B-Instruct
```

原因：

- 单张 RTX 4090 更容易完成推理、LoRA 和小规模 DPO；
- Pilot 的目标是验证机制，不是追求最终 SOTA；
- 验证成立后，再迁移到 8B 做正式实验。

第二阶段可尝试：

```text
Qwen/Qwen3-VL-8B-Instruct
```

但必须使用 4-bit QLoRA、gradient checkpointing、小 batch，并尽量冻结 vision tower。

---

## 2. 建议仓库目录

请 Codex 在现有项目内创建：

```text
experiments/
└── forensic_preference_pilot/
    ├── README.md
    ├── configs/
    │   ├── stage_a.yaml
    │   └── stage_b_dpo.yaml
    ├── data/
    │   ├── metadata.csv
    │   ├── splits/
    │   ├── originals/
    │   ├── forged/
    │   ├── gt_masks/
    │   ├── claimed_masks/
    │   └── counterfactuals/
    ├── scripts/
    │   ├── 01_prepare_data.py
    │   ├── 02_run_baseline.py
    │   ├── 03_build_interventions.py
    │   ├── 04_measure_effects.py
    │   ├── 05_build_preference_pairs.py
    │   ├── 06_train_dpo.py
    │   └── 07_evaluate.py
    ├── outputs/
    │   ├── baseline/
    │   ├── interventions/
    │   ├── preference_pairs/
    │   ├── checkpoints/
    │   └── evaluation/
    └── notebooks/
        └── pilot_analysis.ipynb
```

---

## 3. 环境

建议新建独立环境，不改动主项目已有环境。

核心依赖：

```text
python >= 3.10
torch
transformers
accelerate
peft
trl
bitsandbytes
qwen-vl-utils
pillow
opencv-python
numpy
pandas
scikit-learn
matplotlib
```

Codex 需要：

1. 先检查当前 CUDA / PyTorch / transformers 版本；
2. 不盲目升级整个环境；
3. 固定可运行版本到 `requirements_pilot.txt` 或 `environment_pilot.yml`；
4. 运行一次最小 Qwen3-VL 图像推理确认环境正常。

---

## 4. 数据整理

建立 `metadata.csv`，至少包含：

```text
sample_id
forged_path
original_path
gt_mask_path
label
source_dataset
manipulation_type
```

如果当前 80 张不是每张都有 pristine/original：

- 有 pristine pair 的样本：作为 **主实验集**
- 没有 pristine pair 的样本：暂时只用于 baseline explanation 分析，不进入严格反事实主实验

### 数据划分

必须先按 `sample_id/source image` 划分，再生成候选解释和干预图，防止泄漏。

建议 Pilot：

```text
train: 56
val:   12
test:  12
```

若样本类别/来源不均衡，使用分层划分。

---

## 5. Stage A：不训练，先验证“证据决策价值”

### Step A1：固定 baseline 输出格式

对每张 forged image 使用固定 prompt，让 Qwen3-VL 输出 JSON：

```json
{
  "prediction": "fake",
  "fake_probability": 0.91,
  "region": {
    "type": "bbox",
    "coordinates": [x1, y1, x2, y2]
  },
  "trace_type": "boundary_inconsistency",
  "explanation": "..."
}
```

要求：

- prompt 完全固定；
- temperature 固定为 0 或极低；
- 保存 raw response；
- 如果无法直接得到可靠 probability，额外保存 `fake/real` token logits 或统一的可比较 score；
- 不允许人工事后修改 region。

输出：

```text
outputs/baseline/predictions.jsonl
```

---

### Step A2：定义三类证据区域

每张样本至少构造三种区域：

#### 1. `E_gt`
Ground-truth forgery evidence：

```text
真实 GT mask / GT 篡改区域
```

#### 2. `E_claimed`
模型声称的 evidence：

```text
Qwen3-VL 输出的 bbox/mask
```

#### 3. `E_control`
匹配控制区域：

要求尽量满足：

- 面积与 `E_claimed` 接近；
- 不与 GT mask 重叠，或 IoU 极低；
- 尽量位于相似语义区域；
- 每张图至少随机生成 3 个 control，最后取均值。

---

### Step A3：构造反事实图像

#### 优先方案：paired restoration

如果有 pristine/original image：

对于区域 `E`，将 forged image 对应区域替换为 original image 中同位置内容：

```text
x_cf(E) = forged image outside E + original image inside E
```

分别生成：

```text
cf_gt
cf_claimed
cf_control_1
cf_control_2
cf_control_3
```

#### 暂时不要把黑块遮挡作为主实验

黑块、纯色覆盖、强 blur 容易产生 OOD artifact。

可以保留以下方法作为后续 ablation：

```text
paired restoration
inpainting
blur
gray masking
```

但 Pilot 主结果优先 paired restoration。

---

### Step A4：重新运行模型

对：

```text
original forged image
cf_gt
cf_claimed
cf_control
```

使用**完全相同 prompt 与生成参数**重新推理。

记录：

```text
p_fake_original
p_fake_cf_gt
p_fake_cf_claimed
p_fake_cf_control_mean
```

计算：

```text
delta_gt      = p_fake_original - p_fake_cf_gt
delta_claimed = p_fake_original - p_fake_cf_claimed
delta_control = p_fake_original - p_fake_cf_control_mean
```

---

### Step A5：核心指标

#### 1. GT Evidence Effect

```text
GT_Effect = mean(delta_gt)
```

#### 2. Claimed Evidence Effect

```text
Claimed_Effect = mean(delta_claimed)
```

#### 3. Specificity Gap

```text
Specificity = delta_claimed - delta_control
```

#### 4. Evidence Correctness

至少记录：

```text
IoU(E_claimed, E_gt)
```

#### 5. 正确但不忠实样本

重点统计：

```text
IoU(E_claimed, E_gt) 高
但
delta_claimed 低
```

这类样本是当前研究最重要的 failure case。

---

## 6. Stage A 成功标准

Pilot 不要求统计结论达到论文级，只判断这把锤子值不值得继续。

建议满足至少两个条件：

### 条件 1

```text
mean(delta_gt) > mean(delta_control)
```

且差异稳定存在。

### 条件 2

存在数量可观的：

```text
Evidence Correctness 高
但 Decision Effect 低
```

样本。

### 条件 3

可以根据 `delta` 稳定把 candidate evidence 分成：

```text
high-utility evidence
low-utility evidence
```

如果以上成立，则进入 Stage B。

---

## 7. 构造 Preference Pair

对每张训练图生成 3–5 条候选 evidence/explanation。

每条 candidate 记录：

```text
region
trace_type
explanation
IoU_with_GT
delta_fake
control_adjusted_delta
```

定义一个 Pilot 评分：

```text
score =
    w1 * evidence_correctness
  + w2 * decision_effect
  - w3 * control_sensitivity
```

第一版不要过度调参，可先：

```text
w1 = 1
w2 = 1
w3 = 0.5
```

同一张图中：

```text
最高分 candidate -> preferred
最低分但语言仍合理 candidate -> rejected
```

特别保留：

```text
plausible-but-unfaithful
```

作为 hard negative。

输出：

```text
outputs/preference_pairs/train.jsonl
outputs/preference_pairs/val.jsonl
```

每条数据：

```json
{
  "image": "...",
  "prompt": "...",
  "chosen": "...",
  "rejected": "...",
  "metadata": {
    "chosen_iou": 0.72,
    "chosen_delta": 0.31,
    "rejected_iou": 0.65,
    "rejected_delta": 0.02
  }
}
```

---

## 8. Stage B：最小规模 LoRA + DPO

### 目的

只验证：

```text
Evidence-aware preference learning
是否能让模型更倾向输出高决策价值证据
```

不追求最终 SOTA。

### 训练建议

默认：

```text
model: Qwen3-VL-4B-Instruct
quantization: 4-bit NF4
training: LoRA / QLoRA
vision tower: freeze
batch size per device: 1
gradient accumulation: 8~16
gradient checkpointing: on
epochs: 1~3
```

优先只给语言侧/跨模态高层模块加 LoRA。

不要第一版就全参数训练。

### 对照组

至少做：

```text
A. Base Qwen3-VL
B. 普通 SFT（可选）
C. Evidence-aware DPO
```

如果时间有限，先做：

```text
Base vs Evidence-aware DPO
```

---

## 9. Stage B 评价

只在独立 test split 上评价。

必须同时报告：

### Detection

```text
Accuracy / F1 / AUC（按当前数据条件选）
```

### Evidence Correctness

```text
IoU / Dice
```

### Decision Faithfulness

```text
mean(delta_claimed)
Specificity = delta_claimed - delta_control
```

### 关键成功条件

最理想结果：

```text
Detection Accuracy 基本不下降
Evidence Correctness 上升或保持
Decision Faithfulness 明显上升
Control sensitivity 不上升
```

---

## 10. 必须保存的实验产物

Codex 每一步都要保存中间结果，不允许只打印到终端。

至少保存：

```text
config
random seed
model name
model revision
prompt
raw model response
parsed evidence
counterfactual image
all probability/logit scores
all masks / boxes
preference pairs
checkpoint
evaluation csv/json
plots
```

实验结果最终生成：

```text
outputs/evaluation/summary.csv
outputs/evaluation/per_sample.csv
outputs/evaluation/failure_cases.md
```

---

## 11. 必做可视化

生成以下 4 张图：

1. `delta_gt` vs `delta_control`
2. `delta_claimed` vs `delta_control`
3. `IoU` vs `delta_claimed` 散点图
4. Base vs DPO 的 Decision Faithfulness 对比

同时人工挑选至少：

```text
5 个成功案例
5 个 correct-but-unfaithful 案例
5 个明显失败案例
```

保存成案例页供组会查看。

---

## 12. Codex 执行顺序

严格按以下顺序：

```text
[ ] 1. 检查数据和环境
[ ] 2. 创建实验目录和 config
[ ] 3. 固定 baseline prompt
[ ] 4. 跑 10 张图 smoke test
[ ] 5. 检查 bbox/mask 与 score 是否能稳定解析
[ ] 6. 对 10 张构造 paired restoration
[ ] 7. 计算 delta_gt / delta_claimed / delta_control
[ ] 8. 人工检查反事实图是否自然
[ ] 9. 若结果合理，再扩展到全部 80 张
[ ] 10. 生成 Stage A 分析报告
[ ] 11. 只有 Stage A 通过，才构造 preference pairs
[ ] 12. 使用 4B + QLoRA 跑极小规模 DPO
[ ] 13. Base vs DPO 独立测试
[ ] 14. 输出 summary + failure cases
```

---

## 13. Codex 不应自行做的事情

未经明确确认，不要：

- 改变原始 80 张样本；
- 删除已有实验文件；
- 将 train/test 的同源图像混在一起；
- 为了让结果好看而调整阈值；
- 将人工修正后的模型解释重新当作“模型原始输出”；
- 一上来训练 8B/30B 大模型；
- 在 Stage A 未通过前做大规模 DPO；
- 把简单黑块删除当作最终因果证据。

---

## 14. Pilot 最终需要回答的一句话

实验结束后必须明确回答：

> **在图像鉴伪中，能否通过反事实证据扰动稳定识别“真正具有决策价值的 forensic evidence”，并利用这种信号构造 preference pair，使轻量偏好学习后的模型更倾向于依赖和输出这些证据？**

如果答案为“是”，再进入正式论文方法设计阶段，并考虑：

```text
Forensic-specific Evidence Perturbation
+ Hard-Negative Construction
+ Sensitivity–Invariance Preference
+ Dynamic Evidence Resampling
```

作为相对 DEPO 的领域化改造。
