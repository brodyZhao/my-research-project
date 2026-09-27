#!/bin/bash
# 抓取 FakeClue 的 ff++ 子集（约 1.9 GB / 25k 张 PNG）。
#
# 策略：train.zip 有 28.4 GB，ff++ 只占 1.8 GB 且近乎连续。逐成员抓需 2.5 万次
# HTTP 请求（数小时），因此改为：读中央目录拿偏移 → 区间下载 → 按偏移精确抽取。
# 抽取后立即删除 blob，避免峰值占用过大。
#
# 用法：bash fetch_fakeclue_ffpp.sh   （在远端项目根执行，或改 PROJ）
set -u

PROJ=/root/autodl-tmp/faithfulness_pilot
PY=/root/miniconda3/envs/faithpilot/bin/python
OUT="$PROJ/data/raw/FakeClue_ffpp"
SCRIPTS="$PROJ/stage_a3/scripts"
NCHUNK=8

mkdir -p "$OUT"
cd "$PROJ" || exit 1

echo "=== [1/2] 读取中央目录，定位 ff++ 成员偏移 ==="
$PY "$SCRIPTS/10_fakeclue_meta.py" --out-dir "$OUT" || { echo "元数据阶段失败"; exit 1; }

for split in train test; do
  eval "$($PY -c "
import json
d = json.load(open('$OUT/ffpp_meta.json'))['$split']
print('FIRST=%d LAST=%d' % (d['first_offset'], d['last_end']))
print('URL=%s' % d['url'])
")"
  size=$((LAST - FIRST))
  chunk=$(( (size + NCHUNK - 1) / NCHUNK ))
  echo "=== [2/2] $split：区间 $((size / 1000000)) MB，分 $NCHUNK 块并行下载 ==="

  rm -f "$OUT/$split.part"*
  for i in $(seq 0 $((NCHUNK - 1))); do
    s=$((FIRST + i * chunk))
    e=$((s + chunk - 1))
    [ "$e" -ge "$LAST" ] && e=$((LAST - 1))
    want=$((e - s + 1))
    (
      for attempt in $(seq 1 20); do
        curl -sL --max-time 900 -r "$s-$e" -o "$OUT/$split.part$i" "$URL"
        got=$(stat -c%s "$OUT/$split.part$i" 2>/dev/null || echo 0)
        [ "$got" -eq "$want" ] && break
        echo "  $split.part$i 第 $attempt 次不完整（$got/$want），重试"
        sleep 3
      done
    ) &
  done
  wait

  echo "  拼接分块..."
  cat "$OUT/$split.part"* > "$OUT/$split.blob"
  rm -f "$OUT/$split.part"*
  echo "  blob 实际大小 $(stat -c%s "$OUT/$split.blob")，期望 $size"

  echo "  按偏移抽取..."
  $PY "$SCRIPTS/11_fakeclue_extract.py" \
    --meta "$OUT/ffpp_meta.json" --split "$split" \
    --blob "$OUT/$split.blob" --out-dir "$OUT" || echo "  抽取失败：$split"

  rm -f "$OUT/$split.blob"
  echo "  已删除 blob，释放磁盘"
  df -h /root/autodl-tmp | tail -1
done

echo "FAKECLUE_FFPP_DONE $(date)"
echo "抽出 PNG 总数: $(find "$OUT" -name '*.png' | wc -l)"
