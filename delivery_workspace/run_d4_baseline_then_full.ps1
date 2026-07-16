$ErrorActionPreference = "Continue"
$env:nnUNet_raw = "F:\Desktop\NN-Net\delivery_workspace\nnUNet_raw"
$env:nnUNet_preprocessed = "F:\Desktop\NN-Net\delivery_workspace\nnUNet_preprocessed"
$env:nnUNet_results = "F:\Desktop\NN-Net\delivery_workspace\nnUNet_results"
$env:KMP_DUPLICATE_LIB_OK = "TRUE"
$env:Path = "C:\Users\80033194\AppData\Roaming\Python\Python313\Scripts;" + $env:Path
$baseLog = "F:\Desktop\NN-Net\delivery_workspace\log_train_baseline_real_d4.txt"
$fullLog = "F:\Desktop\NN-Net\delivery_workspace\log_train_resencm_full_d4.txt"
function Write-Log($path, $msg) { Add-Content -Path $path -Value $msg -Encoding ASCII }
Write-Log $baseLog "=== BASELINE TRAIN START $(Get-Date) PID=$PID ==="
& nnUNetv2_train.exe 4 3d_fullres 0 -tr nnUNetTrainer_5epochs --npz *>> $baseLog
$baselineExit = $LASTEXITCODE
Write-Log $baseLog "=== BASELINE TRAIN DONE $(Get-Date) exit=$baselineExit ==="
if ($baselineExit -ne 0) {
  $fold = "F:\Desktop\NN-Net\delivery_workspace\nnUNet_results\Dataset004_Hippocampus\nnUNetTrainer_5epochs__nnUNetPlans__3d_fullres\fold_0"
  if (Test-Path (Join-Path $fold "checkpoint_final.pth")) {
    Write-Log $baseLog "=== BASELINE CONTINUE -c $(Get-Date) ==="
    & nnUNetv2_train.exe 4 3d_fullres 0 -tr nnUNetTrainer_5epochs --npz -c *>> $baseLog
    $baselineExit = $LASTEXITCODE
    Write-Log $baseLog "=== BASELINE CONTINUE DONE $(Get-Date) exit=$baselineExit ==="
  }
}
if ($baselineExit -eq 0) {
  Write-Log $fullLog "=== FULL RESENC M TRAIN START $(Get-Date) PID=$PID ==="
  & nnUNetv2_train.exe 4 3d_fullres 0 -p nnUNetResEncUNetMPlans --npz *>> $fullLog
  Write-Log $fullLog "=== FULL RESENC M TRAIN DONE $(Get-Date) exit=$LASTEXITCODE ==="
} else {
  Write-Log $fullLog "=== SKIPPING FULL RESENC M (baseline exit=$baselineExit) ==="
}
