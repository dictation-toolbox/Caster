# Install Visual Studio for Python 2.7

Function Update-ScriptPath {
  $env:PATH = [Environment]::GetEnvironmentVariable('PATH', [EnvironmentVariableTarget]::Machine);
}

Function Install-FromMsi {
  Param(
    [Parameter(Mandatory)]
    [string] $name,
    [Parameter(Mandatory)]
    [string] $url,
    [Parameter()]
    [switch] $noVerify = $false,
    [Parameter()]
    [string[]] $options = @()
  )

  $installerPath = Join-Path ([System.IO.Path]::GetTempPath()) ('{0}.msi' -f $name);

  Write-Host ('Downloading {0} installer from {1} ..' -f $name, $url);
  (New-Object System.Net.WebClient).DownloadFile($url, $installerPath);
  Write-Host ('Downloaded {0} bytes' -f (Get-Item $installerPath).length);

  $args = @('/i', $installerPath, '/quiet', '/qn');
  $args += $options;

  Write-Host ('Installing {0} ...' -f $name);
  Write-Host ('msiexec {0}' -f ($args -Join ' '));

  Start-Process msiexec -Wait -ArgumentList $args;

  # Update path
  Update-ScriptPath;

  if (!$noVerify) {
    Write-Host ('Verifying {0} install ...' -f $name);
    $verifyCommand = (' {0} --version' -f $name);
    Write-Host $verifyCommand;
    Invoke-Expression $verifyCommand;
  }

  Write-Host ('Removing {0} installer ...' -f $name);
  Remove-Item $installerPath -Force;

  Write-Host ('{0} install complete.' -f $name);
}
# VCForPython27.msi on OneDrive 
$vcForPythonUrl = 'https://onedrive.live.com/download?cid=E31C5E4C89FA0C0E&resid=E31C5E4C89FA0C0E%211131&authkey=ANXY9t9F3-KpKC0';

# Alternatively from web.archive.org
# https://web.archive.org/web/20200709160228if_/https://download.microsoft.com/download/7/9/6/796EF2E4-801B-4FC4-AB28-B59FBF6D907B/VCForPython27.msi
# Source: https://web.archive.org/web/20190720195601/http://www.microsoft.com/en-us/download/confirmation.aspx?id=44266

Install-FromMsi -Name 'VCForPython27' -Url $vcForPythonUrl -NoVerify;