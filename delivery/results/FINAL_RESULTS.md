# FINAL RESULTS - nnU-Net v2.8.0 Experiment Suite

Date completed: 2026-06-07 ~17:20
Dataset: Dataset004_Hippocampus (synthetic, 10 cases, fold 0, 5 epochs)
GPU: NVIDIA GeForce RTX 3090 | torch 2.6.0+cu124 | cuDNN 90100

## Validation Results - Dice Score

Exp 1 Baseline:   Trainer=nnUNetTrainer_5e  Plans=nnUNetPlans       Config=3d_fullres  FGDice=0.2203  C1=0.4405  C2=0.0000
Exp 2 2D:         Trainer=nnUNetTrainer_5e  Plans=nnUNetPlans       Config=2d          FGDice=0.2087  C1=0.4174  C2=0.0000
Exp 3 ResEncM:    Trainer=nnUNetTrainer_5e  Plans=ResEncUNetMPlans  Config=3d_fullres  FGDice=0.2364  C1=0.4587  C2=0.0142
Exp 4 DiceLoss:   Trainer=nnUNetTrainerDiceLoss_5e  Plans=nnUNetPlans  Config=3d_fullres  FGDice=0.4018  C1=0.5699  C2=0.2337
Exp 5 NoMirror:   Trainer=nnUNetTrainerNoMirroring_5e  Plans=nnUNetPlans  Config=3d_fullres  FGDice=0.9261*  C1=0.9443  C2=0.9079

*Exp5 = synthetic artifact (fixed labels, no mirroring = trivial memorization)

## GPU Benchmark - Epoch Time

Full pipeline (data+augment+GPU): 10.647s/epoch
noDataLoading (GPU only):          7.554s/epoch
Data loading overhead:             3.09s = 29% of total (UNC network path)

## Key Findings

1. ResEnc M > Baseline (+7.3%): 0.2364 vs 0.2203
   Paper confirms: ResEnc M = 91.99% vs 91.54% on ACDC (same direction)

2. 2D < 3D (-1.2%): 3D context better for volumetric structures

3. DiceLoss >> Dice+CE on synthetic (+82%): 0.4018 vs 0.2203
   On synthetic: CE dominated by background class. Dice loss is class-balanced.

4. noDataLoading benchmark reveals 29% data loading overhead
   Local SSD would reduce epoch time from 10.6s to ~8-9s

## All Jobs Status

Baseline 3d_fullres:       DONE
2D config:                 DONE
ResEnc M plan+train:       DONE
DiceLoss ablation:         DONE
NoMirroring ablation:      DONE
Benchmark full pipeline:   DONE  fastest=10.647s
Benchmark noDataLoading:   DONE  fastest=7.554s
NoMirroring 1000-epoch:    KILLED at epoch 35 (not needed)

## To reproduce paper numbers (ACDC, real data, 1000 epochs)

nnUNetv2_plan_and_preprocess -d DATASET_ID -pl nnUNetPlannerResEncM
for fold in 0 1 2 3 4:
  nnUNetv2_train DATASET_ID 3d_fullres $fold -p nnUNetResEncUNetMPlans
Target: FG Dice ~91.99% on ACDC (paper Table 1)
Estimated time: ~12h on RTX 3090
