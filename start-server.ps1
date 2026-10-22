$ErrorActionPreference = 'Stop'

function Set-SecureEnvironmentVariable([string]$Name, [string]$Prompt) {
    $secret = Read-Host $Prompt -AsSecureString
    $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secret)
    try {
        [Environment]::SetEnvironmentVariable($Name, [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer), 'Process')
    }
    finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer)
    }
}

try {
    Set-SecureEnvironmentVariable 'ADMIN_PASSWORD' 'Contraseña del panel (mínimo 12 caracteres)'
    if ($env:ADMIN_PASSWORD.Length -lt 12) {
        throw 'La contraseña debe tener al menos 12 caracteres.'
    }

    $env:DB_HOST = Read-Host 'Servidor MySQL (por ejemplo 127.0.0.1)'
    $env:DB_PORT = Read-Host 'Puerto MySQL [3306]'
    if (-not $env:DB_PORT) { $env:DB_PORT = '3306' }
    $env:DB_NAME = Read-Host 'Nombre de la base de datos'
    $env:DB_USER = Read-Host 'Usuario de la base de datos'
    Set-SecureEnvironmentVariable 'DB_PASSWORD' 'Contraseña de MySQL'
    $env:HOST = '127.0.0.1'
    $env:PORT = '8000'
    $env:COOKIE_SECURE = '0'

    Push-Location $PSScriptRoot
    try {
        $pythonExe = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python312\python.exe'
        if (-not (Test-Path -LiteralPath $pythonExe)) {
            $pythonCommand = Get-Command python -ErrorAction Stop
            $pythonExe = $pythonCommand.Source
        }
        & $pythonExe server.py
    }
    finally {
        Pop-Location
    }
}
finally {
    Remove-Item Env:ADMIN_PASSWORD,Env:DB_PASSWORD,Env:DB_HOST,Env:DB_PORT,Env:DB_NAME,Env:DB_USER,Env:HOST,Env:PORT,Env:COOKIE_SECURE -ErrorAction SilentlyContinue
}
