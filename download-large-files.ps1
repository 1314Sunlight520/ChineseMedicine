$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$manifest = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'FILES.sha256.json') -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($file in $manifest) {
    if (-not $file.release_asset) { continue }
    $target = Join-Path $PSScriptRoot $file.path
    if (Test-Path -LiteralPath $target) {
        if ((Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash -eq $file.sha256) { Write-Host "Already verified: $($file.path)"; continue }
    }
    New-Item -ItemType Directory -Path (Split-Path $target -Parent) -Force | Out-Null
    $url = 'https://github.com/1314Sunlight520/ChineseMedicine/releases/download/student-files-v1/' + $file.release_asset
    Write-Host "Downloading: $($file.path)"
    $partial = $target + '.partial'
    Invoke-WebRequest -Uri $url -OutFile $partial -UseBasicParsing
    if ((Get-FileHash -LiteralPath $partial -Algorithm SHA256).Hash -ne $file.sha256) { throw "SHA256 mismatch: $($file.path)" }
    Move-Item -LiteralPath $partial -Destination $target -Force
}
Write-Host 'All large files downloaded and verified.'
