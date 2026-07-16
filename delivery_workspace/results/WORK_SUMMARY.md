# NN-Net — Work Summary

**Paper:** [nnU-Net Revisited](https://arxiv.org/abs/2404.09556) (arXiv:2404.09556)  
**Stack:** nnU-Net v2.8.0 · PyTorch 2.6.0+cu124 · NVIDIA RTX 3090  
**Repo:** https://github.com/khangpt2k6/NN-net  
**Updated:** 2026-07-15

---

## Why full training stopped (2026-07-07)

| Fact | Detail |
|------|--------|
| Last completed epoch | **24 / 1000** at 13:04 |
| What was saved | `checkpoint_best.pth` (~207 MB) — EMA best |
| What was missing | `checkpoint_latest.pth` (nnU-Net only writes this every **50** epochs) |
| Process state | Parent trainer gone; orphaned workers left |
| Likely cause | Session/process kill, machine sleep, or interactive session ended — **not** a training crash mid-epoch |

**Fix (2026-07-15):** Copied `checkpoint_best.pth` → `checkpoint_latest.pth`, then resumed with `--c` from **epoch 25**. Training is running again (~122 s/epoch, ETA ~34 h → ~2026-07-17 morning).

Status file: `delivery_workspace/TRAINING_STATUS.txt`

---

## What is done

### Phase A — Synthetic pipeline (10 cases, fold 0, 5 epochs)

| Experiment | FG Dice | vs Baseline |
|------------|---------|-------------|
| Baseline 3d_fullres | 0.220 | — |
| 2D | 0.209 | −1.2% |
| ResEnc M | 0.236 | **+7.3%** |
| DiceLoss | 0.402 | +82% |
| NoMirroring | 0.926 | **artifact** (fixed labels) |
| GPU benchmark (full) | 10.65 s/epoch | — |
| GPU benchmark (no data load) | 7.55 s/epoch | — |

### Phase B — Real MSD Hippocampus (260 cases, fold 0, 5 epochs)

| Trainer | Plans | FG Dice |
|---------|-------|---------|
| ResEnc M (`nnUNetTrainer_5epochs`) | nnUNetResEncUNetMPlans | **87.46%** |
| Baseline (`nnUNetTrainer_5epochs`) | nnUNetPlans | **87.16%** |

ResEnc M edge on real data: **+0.3%** (vs +7.3% on synthetic).

### Phase C — Full ResEnc M (1000 epochs) — IN PROGRESS

- Resumed 2026-07-15 ~23:30 from epoch 25
- Pseudo Dice at resume: ~89.6% / 87.7%

---

## Paper compliance (approx. ~30%)

Done: pipeline, ResEnc M, real Hippocampus, baseline compare, NoMirroring pitfall.  
Running: 1000 epochs.  
Not yet: 5-fold CV, ACDC 91.99%, multi-dataset suite.

---

## Key lessons

1. Synthetic ≠ real for absolute Dice.
2. NoMirroring 93% on synthetic = memorization artifact.
3. Long jobs need durable sessions; checkpoints only every 50 epochs for `checkpoint_latest`.
4. Resume tip: copy `checkpoint_best.pth` to `checkpoint_latest.pth` then `--c`.

---

## Next steps

1. Finish 1000-epoch validation Dice.
2. Folds 1–4.
3. ACDC → paper Table 1 target 91.99%.
