# nnU-Net Revisited - Presentation for Professor

**Paper:** arXiv:2404.09556 | **GPU:** RTX 3090 | **Date:** 2026-06-18

## One-minute summary

| Phase | Data | Key result |
|-------|------|------------|
| A (synthetic) | 10 cases | Pipeline + ablations; ResEnc M +7.3% vs baseline |
| B (real) | 260 MSD cases | **Dice 87.5%** after 5 epochs (ResEnc M, fold 0) |

## Completed work
- nnUNet v2.8.0 pipeline: plan, preprocess, train, validate
- 5 synthetic ablations + GPU benchmark
- Real Hippocampus downloaded from AWS S3, converted, trained, validated

## Still optional for full paper reproduction
- 1000 epochs, 5-fold CV, ACDC dataset, baseline on real data

## Key lesson
Synthetic NoMirroring showed 93% Dice (artifact). Real data: 87.5% Dice - trustworthy result.

## Charts
See 
esults/figures/01_synthetic_vs_real_dice.png and related files.

## Vietnamese talking point
Em da chay pipeline nnU-Net v2 tren Hippocampus that (260 cases), ResEnc M dat 87.5% Dice sau 5 epochs. Buoc tiep: ACDC + 5-fold CV de so voi paper (91.99%).
