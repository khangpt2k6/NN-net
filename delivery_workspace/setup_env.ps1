# nnUNet environment for delivery_workspace
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:KMP_DUPLICATE_LIB_OK = "TRUE"
$env:nnUNet_raw = Join-Path $scriptRoot "nnUNet_raw"
$env:nnUNet_preprocessed = Join-Path $scriptRoot "nnUNet_preprocessed"
$env:nnUNet_results = Join-Path $scriptRoot "nnUNet_results"
$scripts = Join-Path $env:APPDATA "Python\Python313\Scripts"
if (Test-Path $scripts) { $env:Path = "$scripts;$env:Path" }
Write-Host "nnUNet_raw=$env:nnUNet_raw"
Write-Host "nnUNet_preprocessed=$env:nnUNet_preprocessed"
Write-Host "nnUNet_results=$env:nnUNet_results"
