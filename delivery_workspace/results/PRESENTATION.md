# nnU-Net Revisited — Presentation

**Paper:** [arXiv:2404.09556](https://arxiv.org/abs/2404.09556) · **GPU:** RTX 3090 · **Date:** 2026-07-15  
**Full write-up:** [`WORK_SUMMARY.md`](WORK_SUMMARY.md)  
**Repo:** https://github.com/khangpt2k6/NN-net

## One-minute summary

| Phase | Result |
|-------|--------|
| A — Synthetic (10 cases) | Pipeline + ablations; ResEnc M **+7.3%** vs baseline |
| B — Real MSD (260 cases, 5 ep) | ResEnc M **87.46%** / baseline **87.16%** |
| C — Full 1000 ep | **Resumed** from epoch 25 (2026-07-15); ETA ~2026-07-17 |

## Status

- Training restarted after session kill at epoch 24 (no `checkpoint_latest` until epoch 50).
- Resume: copy `checkpoint_best.pth` → `checkpoint_latest.pth`, then `nnUNetv2_train ... --c`.
- See `delivery_workspace/TRAINING_STATUS.txt` for live PIDs / epoch.

## Still needed for paper Table 1

Finish 1000 epochs → 5-fold CV → ACDC (target **91.99%**).

## Key lesson

Synthetic NoMirroring ~93% Dice was a memorization artifact. Real Hippocampus ~87.5% is the trustworthy signal.