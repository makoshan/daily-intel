$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$newPaths = @("C:\ghcup\bin", "C:\ghcup\ghc\9.6.7\bin")
$needsUpdate = $false

foreach ($path in $newPaths) {
    if ($userPath -notlike "*$path*") {
        Write-Host "Adding $path to User Path"
        $userPath = "$userPath;$path"
        $needsUpdate = $true
    }
    else {
        Write-Host "$path is already in User Path"
    }
    
    # Update current session as well
    if ($env:Path -notlike "*$path*") {
        Write-Host "Adding $path to current session Path"
        $env:Path = "$env:Path;$path"
    }
}

if ($needsUpdate) {
    [Environment]::SetEnvironmentVariable("Path", $userPath, "User")
    Write-Host "User Path updated successfully."
}
else {
    Write-Host "No changes needed for User Path."
}

# Verify access
Write-Host "Verifying commands..."
Get-Command cabal -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source
Get-Command ghc -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source
