import json
import os
import shutil
import glob

RESULTS_BASE = r'\\islfs04vs1.moffitt.org\UsersP$\80033194\Desktop\NN-Net\delivery_workspace\nnUNet_results\Dataset004_Hippocampus'
WORKSPACE = r'\\islfs04vs1.moffitt.org\UsersP$\80033194\Desktop\NN-Net\delivery_workspace'
DELIVERY = r'\\islfs04vs1.moffitt.org\UsersP$\80033194\Desktop\NN-Net\delivery_workspace'

# ---------------------------------------------------------------------------
# 1. Scan summary.json files
# ---------------------------------------------------------------------------
experiment_results = []

for root, dirs, files in os.walk(RESULTS_BASE):
    for fname in files:
        if fname == 'summary.json':
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, encoding='utf-8') as f:
                    data = json.load(f)
                dice = data.get('foreground_mean', {}).get('Dice', None)
                # derive experiment label from path
                rel = os.path.relpath(fpath, RESULTS_BASE)
                parts = rel.split(os.sep)
                # parts[0] = TrainerName__Plans__Config, parts[1] = fold_X, parts[2] = validation
                exp_dir = parts[0] if parts else rel
                fold = parts[1] if len(parts) > 1 else 'fold_0'
                experiment_results.append({
                    'experiment': exp_dir,
                    'fold': fold,
                    'dice': round(dice, 6) if dice is not None else None,
                    'summary_path': fpath
                })
            except Exception as e:
                experiment_results.append({'experiment': fpath, 'fold': '?', 'dice': None, 'error': str(e)})

experiment_results.sort(key=lambda x: (x['dice'] or 0), reverse=True)

# ---------------------------------------------------------------------------
# 2. Read benchmark results
# ---------------------------------------------------------------------------
benchmark_data = {}
bench_files = glob.glob(os.path.join(RESULTS_BASE, '**', 'benchmark_result.json'), recursive=True)
for bpath in bench_files:
    try:
        with open(bpath, encoding='utf-8') as f:
            raw = json.load(f)
        # get first value (the hardware key is variable)
        entry = next(iter(raw.values()))
        fastest = entry.get('fastest_epoch')
        gpu = entry.get('gpu_name', 'unknown')
        exp_dir = os.path.relpath(bpath, RESULTS_BASE).split(os.sep)[0]
        benchmark_data[exp_dir] = {
            'fastest_epoch_s': fastest,
            'gpu': gpu,
            'torch_version': entry.get('torch_version', '?')
        }
    except Exception as e:
        benchmark_data[bpath] = {'error': str(e)}

# ---------------------------------------------------------------------------
# 3. Assemble combined output
# ---------------------------------------------------------------------------
FULL_PIPELINE_EPOCH_S = 10.65  # baseline 3d_fullres with data loading

all_results = {
    'experiment_dice': experiment_results,
    'benchmark': benchmark_data,
    'baseline_epoch_time_s': FULL_PIPELINE_EPOCH_S,
    'notes': 'Trainers without _5epochs suffix were killed and recreated. Ablations used custom _5epochs variants.'
}

# ---------------------------------------------------------------------------
# 4. Print comparison table
# ---------------------------------------------------------------------------
print()
print("=" * 90)
print(f"{'EXPERIMENT':<65} {'FOLD':<8} {'DICE':>8}")
print("=" * 90)
for r in experiment_results:
    dice_str = f"{r['dice']:.4f}" if r['dice'] is not None else "  N/A "
    print(f"{r['experiment']:<65} {r['fold']:<8} {dice_str:>8}")
print("=" * 90)

print()
print("=" * 90)
print("BENCHMARK RESULTS (GPU compute only, no data loading)")
print("=" * 90)
for exp, binfo in benchmark_data.items():
    if 'error' not in binfo:
        fastest = binfo['fastest_epoch_s']
        ratio = (fastest / FULL_PIPELINE_EPOCH_S) * 100 if fastest else None
        ratio_str = f"{ratio:.1f}% of full pipeline" if ratio else "N/A"
        overhead_s = FULL_PIPELINE_EPOCH_S - fastest if fastest else None
        overhead_str = f"{overhead_s:.2f}s data loading overhead" if overhead_s else "N/A"
        print(f"  Experiment:       {exp}")
        print(f"  GPU:              {binfo['gpu']}")
        print(f"  Fastest epoch:    {fastest:.2f}s (noDataLoading)")
        print(f"  Full pipeline:    {FULL_PIPELINE_EPOCH_S:.2f}s (with data loading)")
        print(f"  GPU compute:      {ratio_str}")
        print(f"  Data loading:     {overhead_str}")
        print()

# ---------------------------------------------------------------------------
# 5. Save to delivery_workspace/all_results.json
# ---------------------------------------------------------------------------
out_path = os.path.join(WORKSPACE, 'all_results.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(all_results, f, indent=2)
print(f"Saved: {out_path}")

# ---------------------------------------------------------------------------
# 6. Copy to delivery/results/all_results.json
# ---------------------------------------------------------------------------
delivery_results_dir = os.path.join(DELIVERY, 'results')
os.makedirs(delivery_results_dir, exist_ok=True)
dest_path = os.path.join(delivery_results_dir, 'all_results.json')
shutil.copy2(out_path, dest_path)
print(f"Copied: {dest_path}")
