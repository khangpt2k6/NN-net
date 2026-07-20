# nnU-Net Revisited — Paper Summary

**Citation:** Isensee, Wald, Ulrich, Baumgartner, Roy, Maier-Hein, Jaeger. *nnU-Net Revisited: A Call for Rigorous Validation in 3D Medical Image Segmentation.* arXiv:2404.09556 (2024).  
**Link:** https://arxiv.org/abs/2404.09556

## Thesis

A properly configured U-Net (nnU-Net) remains highly competitive. Many recent “SOTA” claims overstate gains because of weak baselines, inconsistent protocols, and datasets that cannot discriminate methods. The paper introduces residual-encoder nnU-Net variants (ResEnc M/L/XL), a standardized benchmarking protocol, and evidence that dataset choice and validation rigor matter as much as architecture.

## Pitfalls called out

1. **Weak / outdated baselines** — comparing to under-tuned U-Nets or non-nnU-Net defaults.
2. **Inconsistent training budgets** — unequal epochs, patch sizes, or compute.
3. **Leaky or non-comparable validation** — different splits, metrics, or postprocessing.
4. **Datasets with low method-separability** — when inter-method variance ≈ intra-method noise, rankings are unstable (see suitability ratios).
5. **Overclaiming small Dice deltas** on saturated tasks (e.g., ACDC, BraTS).
6. **Hidden recipe advantages** — isotropic spacing, larger patches, or more VRAM presented as “architecture wins.”

## Protocol (paper)

- **Metric:** mean Dice similarity coefficient (DSC), typically 5-fold cross-validation where applicable.
- **Training length:** **1000 epochs** for nnU-Net family runs in the main tables.
- **Plans:** residual encoder via `nnUNetResEncUNetMPlans` / L / XL; original dynamic U-Net via `nnUNetPlans`.
- **Fairness focus:** same data, folds, and reporting; disclose VRAM and runtime.
- **Reference implementations** under the nnU-Net framework for ResEnc variants.

## Key findings

- **nnU-Net org.** remains a strong CNN baseline across six public datasets.
- **ResEnc M** often matches or slightly exceeds org. at modest VRAM (~9 GB) and runtime.
- **ResEnc L / XL** help more on harder / larger-organ tasks (e.g., KiTS, AMOS, LiTS) but need much more VRAM/time; XL (~36 GB) is beyond a single RTX 3090 24 GB for comfortable training.
- **Transformers / Mamba** are not universally better; gains are dataset-dependent.
- **Auto3DSeg variants** can underperform when not using the nnU-Net-style recipe.
- **Dataset suitability** (inter-/intra-method SD ratio) shows ACDC/BraTS are relatively saturated; KiTS/AMOS separate methods better.

## Tables in the paper (reference list)

| Table | Content |
|-------|---------|
| **Table 1** | Main DSC results: BTCV, ACDC, LiTS, BraTS, KiTS, AMOS — methods incl. nnU-Net org., ResEnc M/L/XL, MedNeXt, STU-Net, SwinUNETR, etc. + VRAM & runtime |
| **Table 2** | (Related) compute / scaling / fold-0 style experiments (GPU hours, VRAM, epochs, patch, spacing) |
| **Table 3** | Method-separability / suitability: intra- vs inter-method SD and **Inter/Intra ratio** per dataset |
| **Further tables** | Per-class or alternate metrics; isotropic spacing ablations; STU-Net pretrain note |

**Note for this lab:** MSD Hippocampus (Dataset004) is used here for **pipeline validation only**. It is **not** one of the six Table 1 datasets.

## Lab takeaway

On **RTX 3090 (24 GB)**, target **ResEnc M** (and org. baseline), not XL. Reproduce Table 1 starting with **ACDC** (ResEnc M **91.99%** vs org. **91.54%**), then KiTS/AMOS if data and time allow. See `PAPER_TABLE1_REPRODUCTION.md`.
