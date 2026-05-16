$ErrorActionPreference = "Stop"

Write-Host "[quality] syntax and import check..."
python -m compileall src tests
if ($LASTEXITCODE -ne 0) {
  Write-Host "[quality] compile check failed"
  exit $LASTEXITCODE
}

Write-Host "[quality] ruff lint..."
ruff check src tests
if ($LASTEXITCODE -ne 0) {
  Write-Host "[quality] ruff failed"
  exit $LASTEXITCODE
}

Write-Host "[quality] mypy type check..."
mypy
if ($LASTEXITCODE -ne 0) {
  Write-Host "[quality] mypy failed"
  exit $LASTEXITCODE
}

Write-Host "[quality] unit tests..."
python -m unittest discover -s tests -p "test_*.py" -v
if ($LASTEXITCODE -ne 0) {
  Write-Host "[quality] unit tests failed"
  exit $LASTEXITCODE
}

Write-Host "[quality] passed"
