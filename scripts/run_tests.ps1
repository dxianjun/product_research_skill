$ErrorActionPreference = "Stop"

Write-Host "[test] running unit tests..."
python -m unittest discover -s tests -p "test_*.py" -v

if ($LASTEXITCODE -ne 0) {
  Write-Host "[test] failed"
  exit $LASTEXITCODE
}

Write-Host "[test] passed"
