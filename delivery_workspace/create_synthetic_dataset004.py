import json
from pathlib import Path
import numpy as np
import nibabel as nib

dw = Path(__file__).resolve().parent
raw = dw / "nnUNet_raw" / "Dataset004_Hippocampus"
for sub in ("imagesTr", "labelsTr", "imagesTs"):
    (raw / sub).mkdir(parents=True, exist_ok=True)

dataset_json = {
    "channel_names": {"0": "MRI"},
    "labels": {"background": 0, "Anterior": 1, "Posterior": 2},
    "numTraining": 10,
    "file_ending": ".nii.gz",
}
(raw / "dataset.json").write_text(json.dumps(dataset_json, indent=2))

rng = np.random.default_rng(42)
shape = (48, 56, 48)
spacing = (1.0, 1.0, 1.0)
for i, case in enumerate([f"hippocampus_{i:03d}" for i in range(1, 11)]):
    img = rng.normal(100, 20, size=shape).astype(np.float32)
    seg = np.zeros(shape, dtype=np.uint8)
    seg[10:30, 15:35, 10:30] = 1
    seg[30:40, 20:30, 20:35] = 2
    aff = np.diag([*spacing, 1.0])
    nib.save(nib.Nifti1Image(img, aff), raw / "imagesTr" / f"{case}_0000.nii.gz")
    nib.save(nib.Nifti1Image(seg, aff), raw / "labelsTr" / f"{case}.nii.gz")
    if i == 0:
        nib.save(nib.Nifti1Image(img, aff), raw / "imagesTs" / f"{case}_0000.nii.gz")
print("Created synthetic Dataset004 at", raw)

