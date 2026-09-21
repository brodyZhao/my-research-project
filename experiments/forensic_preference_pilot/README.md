# Forensic Evidence Preference Pilot

This directory implements the local, auditable workflow described in
`pilot_experiment_forensic_evidence_preference.md`.

The implementation deliberately stops at Stage A unless the measured gate
passes. It never edits source images, never fabricates model probabilities,
and preserves raw model responses beside parsed evidence.

## Repository layout

```text
forensic_preference_pilot/
├── configs/
├── data/
├── scripts/
├── outputs/
└── notebooks/
```

## Local setup

Use an isolated Python environment and install the pinned pilot dependencies:

```bash
python3 -m venv .venv-pilot
source .venv-pilot/bin/activate
python -m pip install -r experiments/forensic_preference_pilot/requirements_pilot.txt
```

The current Codex machine was checked before this scaffold was created: it
has PyTorch 2.13.0 but no CUDA device, and does not have the optional model
training packages installed. Therefore no Qwen inference or DPO training was
run locally. A CUDA-capable host is needed for those steps.

## Required data

Put the candidate images and masks under `data/` or use absolute paths in
`data/metadata.csv`. The CSV must contain:

```text
sample_id,forged_path,original_path,gt_mask_path,label,source_dataset,manipulation_type
```

`source_image_id` is optional but recommended. If it is absent,
`sample_id` is used as the split group. Rows without an original image or GT
mask are retained in validation metadata but excluded from strict paired
restoration effects.

## Execution order

Run each command from this directory or pass `--pilot-root` explicitly.

```bash
python scripts/01_prepare_data.py --pilot-root .
python scripts/02_run_baseline.py --pilot-root . --max-samples 10
python scripts/03_build_interventions.py --pilot-root . --max-samples 10
python scripts/04_measure_effects.py --pilot-root . --max-samples 10
python scripts/05_build_preference_pairs.py --pilot-root .
python scripts/06_train_dpo.py --pilot-root . --dry-run
python scripts/07_evaluate.py --pilot-root .
```

For the first pass, use `--max-samples 10`. Do not expand to all samples
until the counterfactual images have been inspected and the Stage A report
shows that the gate is worth pursuing.

Every model-running command accepts `--dry-run` and records a manifest or
training plan without downloading a model. This is useful for checking paths,
schemas, and resource requirements before using a GPU host.

## Stage A gate

The preference-pair builder requires `outputs/interventions/summary.json` and
checks whether `mean(delta_gt) > mean(delta_control)`. Use `--force` only
after manually documenting why a failed gate is being explored as a
diagnostic; do not use it to make results look positive.

## Outputs

Important artifacts include:

```text
outputs/baseline/predictions.jsonl
outputs/interventions/manifest.jsonl
outputs/interventions/effects.csv
outputs/interventions/summary.json
outputs/preference_pairs/train.jsonl
outputs/preference_pairs/val.jsonl
outputs/evaluation/summary.csv
outputs/evaluation/per_sample.csv
outputs/evaluation/failure_cases.md
```

Raw responses, parsed regions, image paths, scores, configuration, and seed
are retained so later results can be audited. No credentials, model cache,
private data, or checkpoints should be committed.
