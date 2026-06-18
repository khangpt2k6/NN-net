# Research Findings

## Synthetic vs Real
- Synthetic ResEnc M: 0.236 | Real ResEnc M: **0.875**
- Synthetic is for pipeline debug only

## Paper alignment
- Paper ACDC: baseline 91.54% -> ResEnc M 91.99%
- Same ResEnc > baseline direction in our synthetic ablation

## Cautionary tale: NoMirroring
- 0.926 Dice on synthetic = artifact (fixed labels)
- Paper Section 2 pitfalls validated firsthand

## Engineering
- Data on F: (7.6 TB free), C: was full and broke validation
