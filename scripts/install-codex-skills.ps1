param(
    [string]$CodexHome = "$env:USERPROFILE\.codex",
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$projectSkills = Join-Path $projectRoot ".codex\skills"
$targetSkills = Join-Path $CodexHome "skills"

if (-not (Test-Path $projectSkills)) {
    throw "Pasta de skills do projeto não encontrada: $projectSkills"
}

New-Item -ItemType Directory -Force -Path $targetSkills | Out-Null

$installed = 0
$skipped = 0

Get-ChildItem -Directory $projectSkills | ForEach-Object {
    $destination = Join-Path $targetSkills $_.Name

    if ((Test-Path $destination) -and -not $Force) {
        Write-Host "Pulando $($_.Name): já existe. Use -Force para sobrescrever."
        $script:skipped += 1
        return
    }

    Copy-Item -Path $_.FullName -Destination $targetSkills -Recurse -Force
    Write-Host "Instalada: $($_.Name)"
    $script:installed += 1
}

Write-Host ""
Write-Host "Concluído. Instaladas: $installed | Puladas: $skipped"
Write-Host "Destino: $targetSkills"
