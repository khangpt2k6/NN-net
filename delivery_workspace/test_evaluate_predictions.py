import json
import shutil
from pathlib import Path
import numpy as np
import nibabel as nib
from nnunetv2.evaluation.evaluate_predictions import compute_metrics_on_folder

dw = Path(__file__).resolve().parent
gt = dw / "metrics_tmp" / "gt"
pred = dw / "metrics_tmp" / "pred"
for p in (gt, pred):
    if p.exists():
        shutil.rmtree(p)
    p.mkdir(parents=True)

shape = (32, 32, 32)
aff = np.diag([1.0, 1.0, 1.0, 1.0])
for name in ["case001", "case002"]:
    seg = np.zeros(shape, dtype=np.uint8)
    seg[8:24, 8:24, 8:24] = 1
    pred_seg = seg.copy()
    pred_seg[20:28, 20:28, 20:28] = 2
    nib.save(nib.Nifti1Image(seg, aff), gt / f"{name}.nii.gz")
    nib.save(nib.Nifti1Image(pred_seg, aff), pred / f"{name}.nii.gz")

labels = {"background": 0, "Anterior": 1, "Posterior": 2}
out = dw / "metrics_tmp" / "summary.json"
compute_metrics_on_folder(str(gt), str(pred), str(out), labels, 8)
print("summary written", out)
print(out.read_text()[:500])
