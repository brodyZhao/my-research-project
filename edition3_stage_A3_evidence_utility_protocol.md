# Stage A.3 / B Pilot Protocol
## 证据决策价值的仪器标定、现象刻画、指标审计与偏好学习

> 本文件是 `edition2_stage_A2_paired_restoration_protocol.md` 的修订版，不是补充。
> edition2 的 paired restoration 思路被完整继承，但有 6 处必须改动（第 0 节）。
> 本阶段最终仍只回答一件事：**这个课题能不能做。**
>
> 状态：待用户确认。数据获取性已实测，模型权重已在远程主机就位。

---

## 0. 相对 edition2 的六处改动

| # | edition2 的写法 | 问题 | 本版改为 |
|---|---|---|---|
| 1 | 数据沿用现有 80 张 SynthScars | **SynthScars 是整图合成数据集，pristine 原图原理上不存在**（LEGION, ICCV 2025）；`has_paired_original: 0` 已被实证 | 换用带原生 pristine 配对的 CocoGlide + InpaintCOCO |
| 2 | 只有 necessity（恢复 GT 区域）单方向 | **null 结果不可证伪**：`delta≈0` 无法区分"模型不依赖"与"仪器坏了" | 补回 sufficiency 臂，构成 2×2 判别 |
| 3 | 指标用 `p_fake_forged - p_fake_restore` | edition1 实测 `p_fake` 均值 0.785、63/80 ≥0.5，**天花板效应**；`claimed_gap` 均值/中位数差 24 倍 | 一律用 verdict 序列 **log-odds 差值**（无界、不饱和） |
| 4 | 只跑 Qwen3-VL-8B 单模型 | 无法区分"模型属性"与"单个模型怪癖" | FakeVLM 为主 + Qwen3-VL-8B 为对照（两者权重都已在远程） |
| 5 | 只测"判断是否依赖声称证据" | 漏掉审计文档点明的另一半：**现有解释指标会不会系统性高估这种依赖** | 新增阶段 2 指标审计 |
| 6 | 无真假二分类准入 | 若模型在评测集上接近瞎猜，"不忠实"是平凡结论 | 新增 Gate 0：两类样本上的 balanced accuracy 与不确定性检验 |

---

## 1. 数据（获取性已实测确认）

### 主数据集

**CocoGlide**（TruFor 官方发布，GRIP UNINA）
- 512 对：COCO val 裁 256×256 → GLIDE 扩散 inpainting 生成同类新物体
- 三元组齐全：原图 crop / 篡改图 / 二值 mask
- 117 MiB，256×256 PNG
- 直链：`https://www.grip.unina.it/download/prog/TruFor/CocoGlide.zip`

**InpaintCOCO**（HF `phiyodr/InpaintCOCO`）
- 1,260 对：COCO 2017 val 512×512 → Stable Diffusion v2 inpainting
- 字段：`coco_image`（原图）/ `mask` / `inpaint_image`（篡改图）
- 1.06 GB，**parquet 格式**
- 走镜像：`https://hf-mirror.com/datasets/phiyodr/InpaintCOCO/resolve/main/data/test-0000{0,1,2}-of-00003.parquet`

> 选它们的原因：篡改 = **扩散模型对真实照片做局部 inpainting**。既满足 `x_restore` 公式（pristine 就是那张真实原图），又保留"AI 生成的局部伪迹"叙事，不必改写成换脸。且 mask 是**原生精确的 inpainting 区域**，不是自造的代理 mask。

### 跨域复现数据集（阶段 1 后半段使用）

**FakeClue 的 ff++ 子集**（HF `lingcco/FakeClue`，即 FakeVLM 论文的配套数据）
- ff++ 部分 1.9 GB：5,517 real + 22,055 fake（Deepfakes / FaceSwap / Face2Face / NeuralTextures）
- 配对键：`real/youtube/c23/frames/<video>/<frame>.png` ↔ `fake/<Method>/c23/frames/<video>_<clip>/<frame>.png`
- **下载方式**：`train.zip`（28.4 GB）里 `train/ff++/` 是**连续字节块**（6,879,319,776..8,688,547,665），一条 HTTP Range 即可只取 1.81 GB；test.zip 的 ff++ 另约 0.09 GB。已实测：Range 返回 206，重定向到 `cas-bridge.xethub.hf.co` 后在远程主机可达
- ⚠️ 三个 caveat：**无 mask**（需 RetinaFace/dlib 自造人脸 mask）；256×256 有损 c23，且**可能是 16:9 压扁**（未证实）；**`label: 1 = real, 0 = fake`，语义与直觉相反**

> 它的定位是**跨域复现**，不是主实验。理由：FF++ 的篡改区域是**整张脸**，与"局部伪迹"叙事不符；且无原生 mask。

### 磁盘
`/root/autodl-tmp` 当前 17 G 可用。三个数据集合计 3.1 GB，余量充足。
（可选回收：`SynthScars.zip` 1.7 G + 从未被使用的 train 集 1.6 G。**未经确认不删除。**）

---

## 2. 模型

| 角色 | 模型 | 权重 | 状态 |
|---|---|---|---|
| **主模型** | FakeVLM（`lingcco/fakeVLM`, NeurIPS 2025） | 14 GB | 已在远程 |
| **对照模型** | Qwen3-VL-8B-Instruct | 17 GB | 已在远程 |

主模型选 FakeVLM 的理由见 `research/LITERATURE_NOVELTY_AUDIT_2026-08-30.md`：专业解释型鉴伪模型，同时输出判断与伪迹解释，且其论文明确报告"解释监督同时改善检测"——这使忠实性检验具备理论针对性。

⚠️ **两个未验证风险**：FakeVLM 的 `config.json` 架构是否为 LLaVA（若是其他架构，`LlavaForConditionalGeneration` 会直接加载失败）；`transformers 5.16.1` 对 LLaVA 的支持需实测。**第一次跑之前先做 1 张图的兼容性小测。**

---

## 3. 指标定义（本节替换 edition2 §10）

所有效应量定义在 **log-odds** 上，不用 `p_fake` 差值：

```text
s(I) = logP("fake" | I, prompt) - logP("real" | I, prompt)     # forced-choice 序列 log-odds

delta_gt_restore      = s(x_forged) - s(x_restore_gt)
delta_claimed_restore = s(x_forged) - s(x_restore_claimed)
delta_control_restore = s(x_forged) - mean_i s(x_restore_control_i)

claimed_gap_restore   = delta_claimed_restore - delta_control_restore
gt_gap_restore        = delta_gt_restore      - delta_gt_control_restore
```

**充分性方向**（新增，edition2 缺失）：

```text
x_suff_gt       = x_pristine 之外 + x_forged 的 GT 区域内
suff_gt         = s(x_suff_gt) - s(x_pristine)
suff_claimed    = s(x_suff_claimed) - s(x_pristine)
suff_gap        = suff_claimed - suff_control
```

> **禁止**用 `p_fake` 差值作为主指标。edition1 的饱和实证：`p_fake_original` 均值 0.785，63/80 ≥ 0.5，`claimed_gap` 均值 +0.0576 而中位数仅 +0.0024。

---

## 4. 阶段 0：仪器标定

### A3.1 配对验证
对每对 (forged, pristine)：
```text
forged.size == pristine.size                 # 不等则先查是否无损 resize / crop offset，无法确定则剔除
absolute_difference_map
mean_abs_diff_inside_gt / mean_abs_diff_outside_gt
pair_quality_ratio = inside / (outside + eps)
```
理想 `inside >> outside`。低质量 pair 单独标记，不进入主分析。

**预先注册的准入条件**（2026-09-21 实测后定，不得事后调整）：

```text
mask 面积占比准入带：0.02 <= mask_area_ratio <= 0.30
```

理由：面积 >0.30 时"恢复 GT 区域"已近似"整图替换为原图"，A3.5 的局部 vs 全图对照退化；面积 <0.02 时恢复对像素的改变过小，效应会淹没在噪声里。实测可用量：

| 数据集 | 全部配对数 | 面积 ≤0.30 | 面积 ≤0.20 |
|---|---|---|---|
| CocoGlide | 512 | **346** | 286 |
| InpaintCOCO | 1260 | **730** | 489 |
| 合计 | 1772 | **1076** | 775 |

**两数据集的仪器差异（必须分别报告，不可混算）**：

| | CocoGlide | InpaintCOCO |
|---|---|---|
| 生成器 | GLIDE | Stable Diffusion 2 inpainting |
| mask 格式 | 单通道 `L` 二值图 | RGB 三通道恒等，含抗锯齿灰边 |
| mask 推导 | `> 127` | `mask.max(axis=2) > 127` |
| 配对键 | `table.csv`（**三目录基名不一致，必须用 csv**） | parquet 同行 |
| `pair_quality_ratio` 中位数 | **210.9** | 10.3 |
| mask 外差异 | **≈0.00（真合成：区域外原样复制）** | 4–21（SD2 会把整图过一遍 VAE） |
| 分辨率 | 256×256 | 512×512 |

**这个差异有实质影响**：CocoGlide 上 `x_restore_gt` 与 `pristine` 逐像素相同，恢复零伪影；InpaintCOCO 上 mask 外不是原始像素，`delta_control_restore` 会包含 VAE 重编码差异。因此：

- **CocoGlide 作为主仪器标定集**（最干净）
- **InpaintCOCO 作为跨数据集复现**（更真实，但 control 基线更脏）
- 两者的 control 效应量级必须分别报告

### A3.2 固定 baseline evidence
- 模型固定、`do_sample=False`、prompt 完全不变、`max_pixels` 固定
- 保存 raw response + parsed evidence
- claimed region **必须来自模型在 `x_forged` 上的原始输出**，不得在 restoration 上重选，不得人工修改

### A3.2b 声称证据的落地：text → region grounding（**方案 A，必做**）

**为什么需要**：FakeVLM 冻结的官方 prompt 只输出自然语言解释，**不输出 bbox/mask**（已实测：`raw_output = "This is a fake image. Although it does not show obvious artifacts..."`，无任何区域字段；FakeClue 的参考答句同为纯文本）。而 Qwen3-VL 原生输出 `evidence_regions[].bbox`。若不加约束，就会出现"一个模型用原生框、另一个用落地框"的不对称，把**仪器差异**混进**模型差异**。

**仪器**：GroundingDINO（`transformers` 原生内置，已实测 5.16.1 下 `GroundingDinoForObjectDetection` / `GroundingDinoProcessor` 可导入；权重 `IDEA-Research/grounding-dino-tiny` 在 hf-mirror 未 gated）。

**冻结的 query 构造规则**（写死，见 §10）：
```text
解释文本 → 去掉开头的 verdict 句（"This is a fake/real image."）
        → 取其余部分，小写化、句末以 "." 结尾
        → 整段作为 GroundingDINO 的 text query
```

**冻结的取框规则**：
```text
取 score 最高的单框
score < τ → 记为 no_region（τ 首版 0.25，须在验证子集上定下后冻结）
面积占比 > 40% → 依 MODEL_ADAPTER_SPEC.md 判为 overlocalized，单独标记
```

**对称性要求**：
- **两个模型都必须走同一落地流程**产生 grounded region，作为主分析的 `M_claimed`
- Qwen3-VL 的原生 bbox 只作为**次级变体**（native region）单独报告，不与 grounded region 混用
- 理由：主分析里 `M_claimed` 的定义必须对两个模型完全一致

**落地仪器本身的验证**（Gate 6）：
- 抽 20 张人工盲审，判断"框是否落在解释文本所指的物件上"，报告通过率
- **必须报告 `no_region` 比例**。若 > 30%，说明落地仪器不适配本任务，须退回方案 B（改文本级判定）或 C（换主模型）

**工程注意**：GroundingDINO 与 FakeVLM **不同时驻留显存**（14 GB + 各自开销会顶到 24 GB 上限），必须顺序执行。

### A3.2c 落地仪器的实测几何性质（2026-09-21，CocoGlide 前 50 个合规样本）

```text
no_region（无框）        4/50 = 8%          → 远低于 Gate 6 的 30% 上限
GT mask 面积      median 0.102
grounded box 面积 median 0.165   max 1.000  ← 有样本框满全图
box / GT 面积比   median 1.49x
IoU(box, GT mask) median 0.410   IoU >= 0.5 仅 37%
box score         median 0.519
```

**三项设计后果（必须写进流程）**：

**1. IoU 必须双轨报告。** grounded region 是物体外接矩形，GT 是紧贴的不规则多边形，形状不匹配会把 IoU 系统性压到 ~0.41：

```text
IoU_box_vs_gtmask    严格，惩罚形状不匹配        ← 保守下界
IoU_box_vs_gtbox     对 GT 取外接矩形后再算      ← 形状无关的定位精度
```

edition2 §11 的 "High overlap: IoU ≥ 0.5" 分档**必须建立在 `IoU_box_vs_gtbox` 上**，否则高分组只剩 37%，分档失去意义。

**2. 面积准入带必须同时施加于 claimed region。** 实测 12/46 个样本 GT 合规但 box 面积 >0.30，最极端的一个 box 面积 = **1.000（框满全图）**。若只按 GT 过滤，会混入"恢复 claimed 区域 ≈ 整图替换"的样本，A3.5 的对照再次退化。新增准入条件：

```text
claimed_area_ratio <= 0.30
```

**3. claimed vs GT 的裸 delta 对比受面积混淆。** box 面积中位数是 GT 的 1.49 倍，恢复面积更大 → 效应天然更大。因此：

- **主结论只能建立在 `claimed_gap_restore` 之上**（对比等面积 matched control），它自带面积控制
- `delta_claimed_restore` vs `delta_gt_restore` 的裸对比**不得作为主结论**；若确要比，须额外构造**面积匹配的 GT 变体**：
  ```text
  x_restore_gt_areamatched    # 将 M_gt 膨胀/腐蚀至面积等于 claimed 后再恢复
  ```

**4（实测追加）. Qwen3-VL 会违反它自己 prompt 的面积约束。** prompt v2 要求"框面积 ≤ 图像 25%"，而实测 **6/25 ≈ 24%** 的输出超限：

```text
cocoglide_0017  bbox [100,170,575,780]   面积 29%
cocoglide_0018  bbox [0,480,1000,997]    面积 52%
→ parse_error: "v2 evidence bounding box exceeds 25% area limit"（该校验在
  run_qwen3vl_originals.py 内，不在 faithpilot/model_output.py，排查时注意）
```

处理：**记录拒绝率，排除该样本**，不得把解析失败当成模型"没有声称证据"。这是模型行为（过度定位）而非管线缺陷。
附带好处：Qwen3-VL 自身的 25% 约束比本协议要求的 30% 更严，**解析通过的样本自动满足准入带**。

**5. 落地框可能再次超面积带。** 实测用 GroundingDINO 落地时 box 面积中位数是 GT 的 1.49 倍，最大值达 1.000。所以 `claimed_area_ratio <= 0.30` 的准入必须**在落地之后**再施加一次，不能只依赖模型自带的 25% 约束。

### A3.3 构造恢复版本
```text
x_restore_gt      = x_forged * (1 - M_gt)      + pristine * M_gt
x_restore_claimed = x_forged * (1 - M_claimed) + pristine * M_claimed
x_restore_control_i                                                              # 3–5 个
```

**control 必须匹配**（edition2 §7 的 Level 1/2，优先级从高到低）：
1. 同一物体内部、2. 同类语义区域、3. 仅面积匹配
- **禁止**随机平移照搬（edition1 的 `shifted_control_mask` 就是这种降级实现）
- **可直接复用远程已有的 `faithpilot/control_matching.py`**：它基于 DINOv2 表征做语义匹配控制区，正是这里要求的 Level 1/2。edition1 没用上它，是本地精简脚本的损失。

### A3.4 阳性对照（**新增，最关键**）
必须构造一组经盲审确认包含目标证据、且可由全图配对或独立验证证明可影响标签的阳性对照，验证仪器能够测出变化：

```text
阳性对照候选：
(a) sufficiency 方向：pristine + 明显伪迹区域 → s 应显著上升
(b) 整图恢复：x_pristine 本身 → 若模型判 fake 能力正常，s 应显著下降
(c) 已知强伪迹样本（肉眼可见的结构崩坏）→ 恢复后 delta 应远大于 0
```

**判定规则**：若阳性对照测不出显著效应，则**仪器或模型不具备局部敏感性，停止解读任何模型结果**，不得把 null 结果解释为"模型不依赖证据"。

### A3.5 全图 vs 局部（**新增**）
```text
delta_whole = s(x_forged) - s(x_pristine)      # s(x_pristine) 用真实原图
```
对比 `delta_whole` 与 `delta_gt_restore`：若整图恢复有效而局部 GT 恢复未达预注册效应界，结果与模型使用全局/分布线索相容，但仍需排除局部恢复质量与干预范围不足；若整图恢复也无效，则无法声称“检测器识别图像内容但不依赖局部证据”。

---

## 5. Gate 表（阶段 0 通过才进入阶段 1）

| Gate | 条件 | 不通过的含义 |
|---|---|---|
| **Gate 0 二分类准入** | 清单同时含 `label=0 real` 和 `label=1 fake`；balanced accuracy ≥ 0.65、分层 bootstrap 95% CI 下界 > 0.5，且预测置换检验 p < 0.05；同时报告两类 recall、AUROC 和 confusion matrix | 缺任一类即 **BLOCKED**；单类 recall 不能验证真假判别能力。未过准入时不能把零效应解释为“不依赖证据” |
| **Gate 1 仪器** | 阳性对照（A3.4）测出显著效应 | 仪器坏了，不得解读模型结果 |
| **Gate 2 GT 恢复** | 先冻结最小有意义效应 `δ`；`mean(delta_gt_restore)` 的 95% CI 下界 > `δ` | 阳性对照效应不足或符号不符 → 回查配对/恢复边界/mask 质量，不解读 null |
| **Gate 3 claimed 特异性** | `claimed_gap_restore` 的 95% CI 下界 > `δ`；若主张无额外价值，须以 90% CI 完全落入 `[-δ,+δ]` 做等效检验 | 普通“不显著”不能证明无决策特异性；未过等效检验则记未决 |
| **Gate 4 配对质量** | `pair_quality_ratio` 达标比例 + 盲审通过 | 配对不严格 → 结论无效 |
| **Gate 5 噪声底** | `noop` 漂移明显小于 target/control 变化 | 打分管线噪声过大 |
| **Gate 6 落地仪器** | 盲审通过率达标 **且** `no_region` 比例 ≤ 30% | 文本→区域落地不可靠 → 退回方案 B/C，不得继续空间分析 |
| **Gate 7 解释接地性** | 对冻结样本做盲法事实核验与证据区域定位评估；报告标注者一致性、claim 可定位率及与人工/GT 区域的一致性 | 解释唯一率只描述文本多样性，不构成接地性准入；接地核验缺失时，不得声称文字解释已对应伪迹 |

### 历史解释唯一率结果（2026-09-22；不等于 Gate 7 接地性）

以下是探索性文本统计。解释唯一率高低只反映字符串是否重复，尚无盲法人评/事实核验，不能据此判定解释是否接地。

| 组合（历史 label=1 假图子集） | n | fake recall | 唯一解释率 | 最常见一条占比 |
|---|---|---|---|---|
| FakeVLM × FF++ | 249 | 0.996 | **0.092** | **0.410** |
| FakeVLM × CocoGlide | 345 | 0.186 | 1.000 | 0.003 |
| Qwen3-VL × CocoGlide (v4) | 345 | 0.220 | 0.707 | 0.136 |

**描述性现象**：低 fake-recall 批次的文本更不重复，高 fake-recall 批次的文本更重复。由于各项只含假图，且跨数据集/提示设置比较，这不证明模型总体检测能力与解释接地性之间存在关系。

```text
"the person's mouth looks too rigid to convey expressions"
    → 覆盖 41% 的样本，且跨越四种篡改方法
      （Face2Face 只改表情 / NeuralTextures 只改纹理 / FaceSwap 整脸替换）
```

落地框中心的标准差只有 **0.021**（画面宽度的 2%），说明落地区域高度集中；这可提示模板化，但不单独证明定位错误或因果不忠实。

**后果（必须写进所有结论）：**

- **Gate 7 尚未评估** → 唯一解释率/落地区域方差不能替代盲法事实核验与定位评测；`IoU(claimed, GT)` 只在人工/GT 区域可靠、样本来源匹配后解释
- **必要性检验仍可运行**：声称区域虽集中，仍可测"恢复它是否改变判定"
  以及"是否比等面积匹配对照更重要"。结论的表述要相应改为
  **"模型对它所声称的那一类区域是否敏感"**，而非"对这张图的证据是否敏感"

**新增的接地性检验**（`15_explanation_grounding_test.py`，不需要任何图像干预）：
把同一批样本的 pristine 真实图喂给同一模型，比较

```text
(a) 真实版与伪造版的解释是否逐字相同   → 相同则解释与图像内容脱钩
(b) 真实图上的假阳性率（真实图被判 fake 的比例）
```

若 (a) 很高，可标记解释文本对配对干预不敏感；若 (b) 很高，说明真实样本上有较多假阳性。两项分别描述文本不变性和分类错误，不能单独证明解释/判定不依赖图像内容，也不能代替因果必要性检验。

### Gate 0 历史结果更正（2026-09-28）

本节旧表把只含 `label=1` 的子集上的判假比例称为“准确率”。代码 `stage_a3/scripts/04_gate0_accuracy.py` 当时只筛选 `label==1`，因此这些数值至多是**fake recall**；当数据只包含假图时，balanced accuracy、real recall 和 AUROC 均不可计算。对单类子集做的与 0.5 二项检验，也不是“真假分类优于随机”的检验。以下旧结果不得用于 Gate 0 PASS/FAIL，原判断撤回；必须在包含真假两类的同域测试集上重跑。

以当前可访问的 Stage-A 文件 `stage_a_full_20260919/full_scores.jsonl` 为例，80/80 条 `label=1`。修正后的脚本计算得到 fake recall 63/80=0.7875，但 Gate 0 状态为 `BLOCKED_SINGLE_CLASS`。该样本上“恒判 fake”的基线 fake recall 为 1.0，进一步说明单类得分不能证明检测能力。

#### 历史单类结果（仅作 fake-recall 记录，不是准确率）

| 组合 | n | fake recall（label=1 子集） | 旧 95% bootstrap CI | 旧二项检验 vs recall=0.5 | Gate 0 |
|---|---|---|---|---|---|
| FakeVLM × CocoGlide | 345 | **0.186** | [0.145, 0.229] | p = 3.1e-12 | **BLOCKED** |
| FakeVLM × FakeClue-FF++ | 249 | **0.996** | [0.988, 1.000] | p = 1.3e-12 | **BLOCKED** |

FakeVLM × CocoGlide 的旧结果说明 81%（281/345）的该批假图在给定 forced-choice 阈值下被判为 `real`；这提示该域存在大量假阴性，但**不能据此断言整体真假准确率低于随机**，因为本表没有真实图上的 specificity。文本 verdict 与 forced-choice verdict 一致（0.183 vs 0.186），这一一致性观察仍可保留。

**同一模型在两个假图子集上的 fake recall 对比（同 prompt、同打分流程）**：

```text
CocoGlide（域外）  0.186      18.6% 判假
FF++（训练域）     0.996      99.6% 判假      ← 248/249，log_odds 中位数 +0.983
```

这组差异是**假图检出率的跨域差异**，不是 overall accuracy 的跨域差异；只有补齐各域真实图结果，才能判断完整真假检测能力。FF++ 上 log_odds 分布在 [-0.036, +1.467] 的记录仍可用于描述假图分数，但不能替代 balanced accuracy。

**后果：实验矩阵必须按域拆分。**

| 模型 | CocoGlide / InpaintCOCO | FakeClue-FF++ |
|---|---|---|
| FakeVLM | Gate 0 未验证；0.186 是 fake recall | Gate 0 未验证；0.996 是 fake recall |
| Qwen3-VL-8B | 待测（GPU 空闲后执行） | 待测 |

**FF++ 无 GT mask 的后果与对策**：FakeClue 不提供 mask，因此 ff++ 臂无法直接计算 `IoU(claimed, GT)` 或构造 `x_restore_gt`。但——

> **本课题的核心检验（claimed 区域必要性）不需要 GT mask。**
> `x_restore_claimed` 的构造只需要 claimed 区域和 pristine 图，两者都有。

GT 掩码可由 (real, fake) 差分图派生作为**代理**（步骤 13），但必须标注 `gt_mask_source="derived_from_diff"` 并做质量盲审；涉及 GT 的结论（`delta_gt_restore`、`IoU_box_vs_gtmask`）在 ff++ 臂上只能作为次要结果报告。

统计：bootstrap 95% CI（≥2000 次）、paired sign-flip test、positive fraction、median、mean。多重比较用 Holm 校正。

---

## 6. 阶段 1：现象刻画

### A3.6 核心指标
```text
IoU(M_claimed, M_gt), Dice
delta_claimed_restore, claimed_gap_restore, suff_claimed, suff_gap
```

### A3.7 correct-but-unfaithful 单元格
```text
IoU >= 0.5  且  delta_claimed_restore <= 0.05
```
必须报告**占比 + bootstrap CI**，不是只报个数。

### A3.8 wrong-but-useful 单元格
```text
IoU < 0.2  且  delta_claimed_restore 高
```
不丢弃，作为 shortcut suppression 的证据。

### A3.9 跨模型复现
同一套流程跑 FakeVLM 与 Qwen3-VL-8B。**只有两个模型都出现同一方向的错位，现象才算成立。**

### A3.10 跨域复现
在 FakeClue ff++ 子集上重复 A3.6–A3.8（用自造人脸 mask，结论需标注 mask 来源）。

---

## 7. 阶段 2：指标审计（**新增，本版最重要**）

审计文档把待答问题写成两半，edition2 只测了前半。本节测后半：

> **"现有解释指标会不会系统性高估证据—判断忠实性？"**

做法：对每个样本计算现有解释指标，与反事实测得的作用量做相关性分析。

```text
现有指标（自变量）：
  - IoU / Dice(M_claimed, M_gt)          定位正确性
  - ROUGE-L / 文本相似度 vs 参考解释       解释文本质量（FakeClue 自带参考解释可用）
  - CLIP / 视觉语言相似度
  - MLLM-judge 打分
  - 检测置信度 / p_fake                    模型自信度

作用量（因变量）：
  - delta_claimed_restore                 必要性
  - claimed_gap_restore                   特异性
  - suff_claimed                          充分性

输出：
  - 相关系数矩阵 + CI
  - 关键量：IoU 与 delta 的关联及其不确定性；相关性接近 0 只能算探索性结果
```

**若相关性接近 0**，不能直接得出“现有解释评测测的不是忠实性”。需报告 CI、功效、非线性/混杂检查，并在独立数据上验证该指标是否能预测因果终点；相关性分析只用于假设生成。

---

## 8. 阶段 3：偏好学习（仅在阶段 0–2 通过后启动）

### 数据
每张训练图生成 3–5 条候选 evidence，记录：
```text
region / trace_type / explanation / IoU_with_GT / delta_fake / control_adjusted_delta
score = w1*evidence_correctness + w2*decision_effect - w3*control_sensitivity    # 首版 w1=1, w2=1, w3=0.5
```
同图内最高分 → chosen；最低分但**语言仍合理** → rejected（hard negative）。
输出 `train.jsonl` / `val.jsonl`。

### 训练
```text
模型：Qwen3-VL-8B（FakeVLM 若结构不兼容则不做）
量化：4-bit NF4；LoRA/QLoRA；vision tower 冻结；bs=1；grad accum 8–16；gradient checkpointing on；epochs 1–3
```
⚠️ **环境缺 `peft` / `trl` / `bitsandbytes`，必须先安装并记录版本。**

### 四条对照臂（**缺一不可**）
```text
A. Base（不训练）
B. SFT-only
C. DPO-on-random-pairs        ← 打乱/随机的偏好对。没有这一臂，无法把增益归因于 utility 信号而非 DPO 本身
D. Evidence-utility DPO       ← 本方法
（可选 E. DPO-on-plausibility-pairs：只按语言合理性构造 → 直接对比"合理性监督 vs 决策价值监督"，这才是框架的真正卖点）
```

### 非循环评价（**硬性要求**）
- pair 用 A 信号构造 → 评价必须用**不同的干预算子**（如构造用整 mask，评价用膨胀/腐蚀版本）
- 训练用 CocoGlide → 测试用 **InpaintCOCO**（跨数据集）
- 检测指标（Accuracy / F1 / AUC）是外部指标，**必须不退化**

> 用自己定义的信号训练、再用同一信号评价 = 循环论证，审稿人一眼看穿。

---

## 9. 判别矩阵（2×2）

| 必要性 | 充分性 | 结论 | 下一步 |
|---|---|---|---|
| `G` 的 95% CI 下界 > `δ` | Gate 0/GT 阳性对照通过 | 经核验的自述区域有相对匹配控制的额外决策价值 | 削弱“自述证据通常未被使用”的说法 |
| `G` 的 90% CI 完全落入 `[-δ,+δ]` | Gate 0/GT 阳性对照通过 | **目标现象**：GT 证据可影响分数，而正确自述区域没有额外决策价值 | 在预注册目标域检验 prevalence |
| 任何准入/阳性对照失败 | — | BLOCKED；无法区分检测器无效与解释不忠实 | 修复测量再测 |
| 区间既未超过 `δ` 也未落入等效区间 | — | 未决 | 增加样本或改善仪器 |

**Case 特例**：若 `delta_whole` 的区间未达到预注册效应界，只能说该实验未测到可辨别的整图效应；不能据此断言模型完全不依赖图像内容。

---

## 10. 不允许的做法

继承 edition2 §17 全部条目，并新增：

- ❌ 用 `p_fake` 差值作为主指标（饱和失真）
- ❌ 没有阳性对照就解读 null 结果
- ❌ 用 SynthScars 声称做过 paired restoration（无 pristine，原理上不可能）
- ❌ 用生成式 inpainting 冒充真实 pristine restoration
- ❌ 用随机平移 control 冒充语义匹配 control
- ❌ 看到结果后调整 grounding 的 query 规则或阈值 τ
- ❌ 对不同模型用不同的落地方式（制造不对称，把仪器差异当成模型差异）
- ❌ 只报 grounded region 而不报 `no_region` 比例
- ❌ 让 GroundingDINO 与 FakeVLM 同时驻留显存（会顶爆 24 GB）
- ❌ 用自己构造偏好对的同一信号做评价（循环论证）
- ❌ 未过 Gate 0（二分类准入）就讨论忠实性
- ❌ 人工移动 claimed mask 以提高 IoU
- ❌ 根据最终结果挑阈值
- ❌ 丢掉 negative cases

---

## 11. 必存产物

```text
data/raw/{CocoGlide,InpaintCOCO}/           原始数据（不提交 git）
data/derived/pairs/{validated_pairs.jsonl, pair_quality.csv}
data/derived/restorations/{gt,claimed,control,positive_control,suff}/
outputs/scores/forced_choice_scores.jsonl   log-odds 原始分数
outputs/metrics/{per_sample.csv, summary.json}
outputs/metric_audit/correlation_matrix.csv
outputs/report/stage_a3_report.md           + success/correct_but_unfaithful/failure 案例页
outputs/preference_pairs/{train,val}.jsonl
outputs/checkpoints/                        LoRA/DPO 权重
```

每步保存：config、seed、模型名与 revision、prompt 原文、raw response、解析后 evidence、干预图、全部 logits/log-odds、mask/box、评价 csv/json、图。

---

## 12. 报告必须回答

| Q | 问题 |
|---|---|
| Q0 | 模型在评测集上是否显著优于随机？（Gate 0） |
| Q1 | 恢复真实 GT 区域后，判断是否稳定下降？（Gate 2） |
| Q2 | 恢复 claimed 区域是否比恢复 matched control 下降更多？（Gate 3） |
| Q3 | 充分性方向是否成立？（新增） |
| Q4 | 是否存在 Evidence Correctness 高但 Decision Faithfulness 低的样本？占比与 CI？ |
| Q5 | 现有解释指标与反事实作用量的相关性如何？（新增） |
| Q6 | 文本→区域落地仪器是否可靠？`no_region` 比例多少？（新增，Gate 6） |
| Q7 | 是否值得进入偏好学习？ |

最终只允许输出：**PASS / PARTIAL PASS / FAIL**，附明确理由。

---

## 13. 执行顺序

```text
[ ]  1. 装配环境：装 pyarrow（读 InpaintCOCO）+ peft/trl/bitsandbytes，记录版本
[ ]  2. 下 GroundingDINO-tiny 权重（hf-mirror，未 gated），单张图跑通落地
[ ]  3. 落地仪器标定：固定 query/取框规则，20 张盲审，报告 no_region 比例（Gate 6）
[ ]  4. 下载并解包 CocoGlide + InpaintCOCO；FF++ 子集用 HTTP Range 按需取
[x]  5. FakeVLM 单张兼容性小测 —— **已完成（2026-09-21）**：`LlavaForConditionalGeneration` 在 transformers 5.16.1 下加载无报错，1.67 s/图，`log_odds_total=10.0`（未饱和）
[ ]  6. 配对验证（尺寸/差分图/pair_quality_ratio）
[ ]  7. 固定 prompt，跑 baseline，取 claimed evidence（含 A3.2b 落地）
[ ]  8. 构造 restoration（gt / claimed / control×3–5 / 阳性对照 / suff）
[ ]  9. 人工盲审至少 10–20 张恢复图质量
[ ] 10. Gate 0 二分类准入检验（真假两类、balanced accuracy、CI、置换检验）
[ ] 11. forced-choice log-odds 打分（noop 噪声底必查）
[ ] 12. 算 delta / gap / CI / sign-flip / Holm
[ ] 13. 2×2 判别 + correct-but-unfaithful 单元格占比 + CI
[ ] 14. 阶段 2 指标审计相关性
[ ] 15. 跨模型（Qwen3-VL-8B）与跨域（FakeClue ff++）复现
[ ] 16. 按 Gate 决定是否进入偏好学习
[ ] 17. 四臂训练 + 非循环评价
[ ] 18. 生成 stage_a3_report.md（PASS / PARTIAL PASS / FAIL）
```

---

## 14. 本阶段最重要的原则

**edition2 §22 说目标是"让'假设不成立'和'实验方法不可靠'尽可能可以区分"——但按 edition2 的设计做不到，因为没有阳性对照，null 结果永远是二义的。本版补上阳性对照与 2×2 方向，才是真正可证伪的设计。**

只有当仪器本身被证明有效之后，"证据 → 决策"的因果讨论才有意义。
