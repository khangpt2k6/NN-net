# Durable launcher: resume Dataset004 Hippocampus ResEnc M 3d_fullres fold_0
# Survives parent shell exit when started via Start-Process -WindowStyle Hidden
$ErrorActionPreference = "Continue"
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$logOut = Join-Path $scriptRoot "log_train_resencm_full_d4_resume.txt"
$logErr = Join-Path $scriptRoot "log_train_resencm_full_d4_resume_err.txt"

$env:nnUNet_raw = Join-Path $scriptRoot "nnUNet_raw"
$env:nnUNet_preprocessed = Join-Path $scriptRoot "nnUNet_preprocessed"
$env:nnUNet_results = Join-Path $scriptRoot "nnUNet_results"
$env:KMP_DUPLICATE_LIB_OK = "TRUE"

$extra = @(
  (Join-Path $env:APPDATA "Python\Python313\Scripts"),
  (Join-Path $env:LOCALAPPDATA "anaconda3\Scripts"),
  (Join-Path $env:LOCALAPPDATA "Anaconda3\Scripts"),
  "C:\ProgramData\anaconda3\Scripts"
)
foreach ($p in $extra) {
  if ($p -and (Test-Path $p)) { $env:Path = "$p;$env:Path" }
}

$stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"[$stamp] resume_train_d4.ps1 starting PID=$PID" | Tee-Object -FilePath $logOut -Append
"nnUNet_raw=$env:nnUNet_raw" | Tee-Object -FilePath $logOut -Append
"nnUNet_preprocessed=$env:nnUNet_preprocessed" | Tee-Object -FilePath $logOut -Append
"nnUNet_results=$env:nnUNet_results" | Tee-Object -FilePath $logOut -Append

$cmd = Get-Command nnUNetv2_train -ErrorAction SilentlyContinue
if (-not $cmd) {
  "[$stamp] ERROR: nnUNetv2_train not found on PATH" | Tee-Object -FilePath $logErr -Append
  exit 1
}
"Using: $($cmd.Source)" | Tee-Object -FilePath $logOut -Append

# Resume Hippocampus ResEnc M 1000-epoch fold 0
& nnUNetv2_train 4 3d_fullres 0 -p nnUNetResEncUNetMPlans --c 2>> $logErr | Tee-Object -FilePath $logOut -Append
$exit = $LASTEXITCODE
$stamp2 = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"[$stamp2] nnUNetv2_train exited code=$exit" | Tee-Object -FilePath $logOut -Append
exit $exit