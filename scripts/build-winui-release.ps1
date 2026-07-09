param(
    [string]$Version = "0.7.0"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$winuiProject = Join-Path $repoRoot "NoteCal.WinUI\NoteCal.WinUI.csproj"
$launcherProject = Join-Path $repoRoot "NoteCal.Launcher\NoteCal.Launcher.csproj"
$winuiPublishDir = Join-Path $repoRoot "NoteCal.WinUI\bin\Release\self-contained\win-x64"
$packageRoot = Join-Path $repoRoot "dist\NoteCal-$Version-winui3-win-x64-portable"
$runtimeDir = Join-Path $packageRoot "datas\runtime"
$zipPath = Join-Path $repoRoot "dist\NoteCal-$Version-winui3-win-x64-portable.zip"

function Invoke-Checked {
    param([string[]]$Command)

    $arguments = @()
    if ($Command.Count -gt 1) {
        $arguments = $Command[1..($Command.Count - 1)]
    }

    & $Command[0] @arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code ${LASTEXITCODE}: $($Command -join ' ')"
    }
}

Invoke-Checked @("dotnet", "restore", $winuiProject, "-p:Platform=x64", "-r", "win-x64")
Invoke-Checked @("dotnet", "publish", $winuiProject,
    "-c", "Release",
    "-p:Platform=x64",
    "-r", "win-x64",
    "--self-contained", "true",
    "-p:WindowsPackageType=None",
    "-p:PublishSingleFile=false",
    "-p:PublishTrimmed=false",
    "-p:PublishDir=$winuiPublishDir\")

Remove-Item -LiteralPath $packageRoot -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $runtimeDir | Out-Null
Copy-Item -Path (Join-Path $winuiPublishDir "*") -Destination $runtimeDir -Recurse -Force
Remove-Item -LiteralPath (Join-Path $runtimeDir "user") -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath (Join-Path $runtimeDir "data") -Recurse -Force -ErrorAction SilentlyContinue

Invoke-Checked @("dotnet", "publish", $launcherProject,
    "-c", "Release",
    "-r", "win-x64",
    "--self-contained", "true",
    "-p:PublishSingleFile=true",
    "-p:PublishTrimmed=true",
    "-p:DebugType=None",
    "-p:DebugSymbols=false",
    "-p:PublishDir=$packageRoot\")

Get-ChildItem -LiteralPath $packageRoot -File |
    Where-Object { $_.Name -ne "NoteCal.exe" } |
    ForEach-Object {
        $supportDir = Join-Path $packageRoot "datas\launcher"
        New-Item -ItemType Directory -Force -Path $supportDir | Out-Null
        Move-Item -LiteralPath $_.FullName -Destination (Join-Path $supportDir $_.Name) -Force
    }

New-Item -ItemType Directory -Force -Path (Join-Path $packageRoot "user") | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path $zipPath) | Out-Null
Compress-Archive -Path (Join-Path $packageRoot "*") -DestinationPath $zipPath -Force

Add-Type -AssemblyName System.IO.Compression
$zipArchive = [System.IO.Compression.ZipFile]::Open($zipPath, [System.IO.Compression.ZipArchiveMode]::Update)
try {
    if (-not ($zipArchive.Entries | Where-Object { $_.FullName -eq "user/" })) {
        $zipArchive.CreateEntry("user/") | Out-Null
    }
}
finally {
    $zipArchive.Dispose()
}

$exe = Join-Path $packageRoot "NoteCal.exe"
$exeHash = Get-FileHash -Algorithm SHA256 -LiteralPath $exe
$zipHash = Get-FileHash -Algorithm SHA256 -LiteralPath $zipPath
$zipItem = Get-Item -LiteralPath $zipPath

[pscustomobject]@{
    Exe = $exe
    ExeSHA256 = $exeHash.Hash
    Zip = $zipPath
    ZipSizeBytes = $zipItem.Length
    ZipSHA256 = $zipHash.Hash
} | Format-List
