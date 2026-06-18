"""
Collect all nnUNet experiment results from delivery_workspace and produce comparison table.
"""
import json
import os
from pathlib import Path

results_root = Path(__file__).parent / "nnUNet_results" / "Dataset004_Hippocampus"
workspace = Path(__file__).parent

experiments = []

# Walk all trainer/config dirs looking for fold_0/validation/summary.json
for trainer_dir in sorted(results_root.iterdir()):
    if not trainer_dir.is_dir():
        continue
    summary_path = trainer_dir / "fold_0" / "validation" / "summary.json"
    benchmark_path = trainer_dir / "fold_0" / "benchmark_result.json"

    if summary_path.exists():
        data = json.loads(summary_path.read_text())
        fg = data.get("foreground_mean", {})
        per_class = data.get("mean", {})
        record = {
            "trainer_config": trainer_dir.name,
            "foreground_Dice": round(fg.get("Dice", float("nan")), 4),
            "foreground_IoU": round(fg.get("IoU", float("nan")), 4),
            "class1_Dice": round(per_class.get("1", {}).get("Dice", float("nan")), 4),
            "class2_Dice": round(per_class.get("2", {}).get("Dice", float("nan")), 4),
            "type": "validation",
        }
        experiments.append(record)

    elif benchmark_path.exists():
        data = json.loads(benchmark_path.read_text())
        for key, val in data.items():
            record = {
                "trainer_config": trainer_dir.name,
                "fastest_epoch_s": round(val.get("fastest_epoch", 0), 3),
                "gpu": val.get("gpu_name", ""),
                "torch": val.get("torch_version", ""),
                "type": "benchmark",
            }
            experiments.append(record)

# Print table
print("\n" + "=" * 80)
print("EXPERIMENT COMPARISON — Dataset004_Hippocampus (synthetic, 10 cases, fold 0)")
print("=" * 80)
print(f"\n{'Trainer / Config':<52} {'Type':<12} {'FG Dice':>8} {'FG IoU':>8} {'C1 Dice':>8} {'C2 Dice':>8}")
print("-" * 100)

for r in experiments:
    if r["type"] == "validation":
        print(f"{r['trainer_config']:<52} {'validation':<12} {r['foreground_Dice']:>8.4f} {r['foreground_IoU']:>8.4f} {r['class1_Dice']:>8.4f} {r['class2_Dice']:>8.4f}")
    else:
        print(f"{r['trainer_config']:<52} {'benchmark':<12} fastest={r['fastest_epoch_s']:.3f}s  gpu={r['gpu']}")

print("=" * 80)
print("\nNotes:")
print("  - Synthetic data: random MRI-like noise, identical labels across all cases")
print("  - 5 epochs only — results not comparable to paper (paper: 1000 epochs, real data)")
print("  - Dice scores show relative differences between trainers/configs, not absolute performance")
print("  - Class 2 (Posterior) often 0.0 — network hasn't learned this class in 5 epochs")

# Save JSON
output = {
    "experiment_info": {
        "dataset": "Dataset004_Hippocampus (synthetic)",
        "n_cases": 10,
        "fold": 0,
        "train_cases": 8,
        "val_cases": 2,
        "epochs": 5,
        "note": "Synthetic data only - relative comparison, not absolute paper replication"
    },
    "results": experiments
}
out_path = workspace / "all_results.json"
out_path.write_text(json.dumps(output, indent=2))
print(f"\nSaved: {out_path}")

# Also copy to delivery/results/
delivery_results = workspace.parent / "delivery" / "results"
delivery_results.mkdir(parents=True, exist_ok=True)
(delivery_results / "all_results.json").write_text(json.dumps(output, indent=2))
print(f"Saved: {delivery_results / 'all_results.json'}")
