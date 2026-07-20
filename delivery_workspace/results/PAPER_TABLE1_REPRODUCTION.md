# Paper Table 1 Reproduction Plan

**Paper:** [nnU-Net Revisited](https://arxiv.org/abs/2404.09556) (arXiv:2404.09556)  
**Hardware target:** NVIDIA RTX 3090 24 GB → **ResEnc M** (not XL)  
**Updated:** 2026-07-19

---

## Full Table 1 reference — nnU-Net org. / ResEnc M / ResEnc L

Mean DSC (%) from paper Table 1 (columns: BTCV, ACDC, LiTS, BraTS, KiTS, AMOS).  
VRAM / runtime (RT) as reported in the paper.

| Method | BTCV (n=30) | ACDC (n=200) | LiTS (n=131) | BraTS (n=1251) | KiTS (n=489) | AMOS (n=360) | VRAM [GB] | RT [h] |
|--------|-------------|--------------|--------------|----------------|--------------|--------------|-----------|--------|
| **nnU-Net (org.)** | 83.08 | **91.54** | 80.09 | 91.24 | 86.04 | 88.64 | 7.70 | 9 |
| **nnU-Net ResEnc M** | 83.31 | **91.99** | 80.75 | 91.26 | 86.79 | 88.77 | 9.10 | 12 |
| **nnU-Net ResEnc L** | 83.35 | 91.69 | 81.60 | 91.13 | 88.17 | 89.41 | 22.70 | 35 |

ResEnc XL (for context only; not our primary target): BTCV 83.28, ACDC 91.48, LiTS 81.19, BraTS 91.18, KiTS 88.67, AMOS 89.68; VRAM **36.60 GB**, RT 66 h.

---

## Table 3 — dataset suitability (Inter/Intra ratio)

From the paper’s suitability / method-separability analysis (Inter-method SD / Intra-method SD). Higher ratio ⇒ dataset better separates methods (more useful for ranking).

| Dataset | Inter/Intra ratio (all methods) | Inter/Intra w/o A3DS |
|---------|----------------------------------|----------------------|
| BTCV | 94% | 65% |
| ACDC | 357% | 102% |
| LiTS | 132% | 63% |
| BraTS2021 | 127% | 53% |
| KiTS2023 | 435% | 163% |
| AMOS2022 | 474% | 477% |

**Interpretation for us:** ACDC is a good **protocol check** (small expected ResEnc M vs org. gap: +0.45 pp) but rankings can be noisy; **KiTS / AMOS** are better for stressing ResEnc gains. BraTS/LiTS/BTCV are more saturated or noisier depending on the method pool.

---

## What WE can reproduce on RTX 3090

### Primary (start here)

1. **ACDC — ResEnc M, 5-fold CV** → target mean DSC **91.99%**
2. **ACDC — nnU-Net org. baseline, 5-fold** → target **91.54%**

### Next (if data available)

3. KiTS → ResEnc M **86.79%** vs org. **86.04%**
4. AMOS → ResEnc M **88.77%** vs org. **88.64%**

### Not planned on this GPU

- ResEnc **XL** (≈36 GB VRAM)
- Full 6-dataset Table 1 suite in one shot (time/data limited)

### Explicitly out of scope for Table 1

- **MSD Hippocampus (Dataset004)** — **not in paper Table 1**; used only for pipeline / engineering validation in this repo.

---

## Protocol we follow

| Item | Value |
|------|--------|
| Epochs | **1000** |
| CV | **5-fold** |
| Metric | mean **DSC** |
| ResEnc plans | `nnUNetResEncUNetMPlans` |
| Baseline plans | `nnUNetPlans` |
| Config | `3d_fullres` (unless paper recipe says otherwise for a dataset) |
| Train cmd (example) | `nnUNetv2_train <DATASET_ID> 3d_fullres <FOLD> -p nnUNetResEncUNetMPlans` |

---

## ACDC data

1. Download: https://www.creatis.insa-lyon.fr/Challenge/acdc/databases.html  
2. Convert with nnU-Net’s `Dataset027_ACDC.py` (dataset ID **027** in the nnU-Net conversion scripts).  
3. Plan/preprocess, then 5-fold train org. + ResEnc M.

---

## Current local status vs paper targets

| Track | Status | vs paper |
|-------|--------|----------|
| Hippocampus ResEnc M fold0 1000-ep | Resumed; last full epoch **440** / 1000; EMA pseudo Dice ~0.886 | **Not a Table 1 number** — pipeline only |
| Hippocampus 5-ep smoke (real) | ResEnc M FG Dice **87.46%** vs baseline **87.16%** | Directionally ResEnc ≥ org. |
| ACDC 5-fold ResEnc M | **Not started** | Target **91.99%** |
| ACDC 5-fold org. | **Not started** | Target **91.54%** |
| KiTS / AMOS | Data / runs TBD | See Table 1 above |

Launcher for Hippocampus resume: `delivery_workspace/resume_train_d4.ps1`  
Live status: `delivery_workspace/TRAINING_STATUS.txt`

---

## Realistic mini-reproduction plan (this lab)

1. **Finish** Hippocampus ResEnc M fold0 to 1000 epochs (engineering confidence, checkpoints, logging).  
2. **Obtain ACDC** → convert Dataset027 → preprocess.  
3. Run **org. + ResEnc M**, folds 0–4, 1000 epochs each (or fold0 first as a milestone).  
4. Report mean DSC vs **91.54% / 91.99%**.  
5. If time/data allow: **one** of KiTS or AMOS at ResEnc M (higher suitability ratios).  
6. Stay on **ResEnc M**; skip XL; use ResEnc L only if a single 22 GB-class job fits after tuning.

**Budget note:** Paper ResEnc M RT ~12 h scale is challenge-dependent; local Hippocampus is ~143 s/epoch → ~40 h / 1000 epochs / fold. Plan calendar time accordingly.
