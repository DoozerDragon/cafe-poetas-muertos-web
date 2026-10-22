$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$sourceRoot = Join-Path $projectRoot 'public'
$pagesRoot = Join-Path $projectRoot 'docs'

New-Item -ItemType Directory -Force -Path $pagesRoot | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $pagesRoot 'images') | Out-Null
Copy-Item -Path (Join-Path $sourceRoot 'images\*') -Destination (Join-Path $pagesRoot 'images') -Recurse -Force

Copy-Item -LiteralPath (Join-Path $sourceRoot 'design.css') -Destination (Join-Path $pagesRoot 'design.css') -Force

function Convert-ToStaticPage {
    param(
        [Parameter(Mandatory)] [string] $Source,
        [Parameter(Mandatory)] [string] $Destination
    )

    $content = Get-Content -Raw -LiteralPath $Source
    $content = $content.Replace("<?= date('Y') ?>", (Get-Date).Year.ToString())
    $content = $content.Replace('index.php', 'index.html')
    $content = $content.Replace('menu.php', 'menu.html')
    $content = $content.Replace('eventos.php', 'eventos.html')
    $content = $content.Replace('<a href="admin.php">Acceso administración</a>', '')
    Set-Content -LiteralPath $Destination -Value $content -Encoding utf8
}

Convert-ToStaticPage -Source (Join-Path $sourceRoot 'index.php') -Destination (Join-Path $pagesRoot 'index.html')
Convert-ToStaticPage -Source (Join-Path $sourceRoot 'menu.php') -Destination (Join-Path $pagesRoot 'menu.html')
Convert-ToStaticPage -Source (Join-Path $sourceRoot 'eventos.php') -Destination (Join-Path $pagesRoot 'eventos.html')
Set-Content -LiteralPath (Join-Path $pagesRoot '.nojekyll') -Value '' -Encoding ascii

Write-Host "GitHub Pages build created at $pagesRoot"
