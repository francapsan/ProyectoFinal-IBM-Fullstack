# Script de inicio para todos los servicios
Write-Host "Iniciando servicios en segundo plano..." -ForegroundColor Cyan

# 1. Express
$expressProc = Start-Process node -ArgumentList "server.js" -WorkingDirectory "$PSScriptRoot\express-mongo-service" -PassThru -WindowStyle Hidden
Write-Host "Express (Puerto 3030) iniciado PID: $($expressProc.Id)" -ForegroundColor Green

# 2. Sentiment Analyzer
$sentimentProc = Start-Process python -ArgumentList "app.py" -WorkingDirectory "$PSScriptRoot\sentiment-analyzer" -PassThru -WindowStyle Hidden
Write-Host "Sentiment Analyzer (Puerto 5000) iniciado PID: $($sentimentProc.Id)" -ForegroundColor Green

# 3. Django Web App
$djangoProc = Start-Process python -ArgumentList "manage.py", "runserver", "--noreload", "127.0.0.1:8000" -WorkingDirectory "$PSScriptRoot\django-app" -PassThru -WindowStyle Hidden
Write-Host "Django (Puerto 8000) iniciado PID: $($djangoProc.Id)" -ForegroundColor Green

Start-Sleep -Seconds 4

# Verificacion HTTP
try {
    $rDjango = Invoke-WebRequest -Uri "http://127.0.0.1:8000/" -UseBasicParsing -TimeoutSec 5
    Write-Host "[OK] Django Web App en http://localhost:8000 (Status: $($rDjango.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Django Web App en http://localhost:8000" -ForegroundColor Red
}

try {
    $rExpress = Invoke-WebRequest -Uri "http://127.0.0.1:3030/dealers" -UseBasicParsing -TimeoutSec 5
    Write-Host "[OK] Express API en http://localhost:3030/dealers (Status: $($rExpress.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Express API en http://localhost:3030" -ForegroundColor Red
}

try {
    $rSentiment = Invoke-WebRequest -Uri "http://127.0.0.1:5000/analyze/Fantastic%20services" -UseBasicParsing -TimeoutSec 5
    Write-Host "[OK] Sentiment Analyzer en http://localhost:5000 (Status: $($rSentiment.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Sentiment Analyzer en http://localhost:5000" -ForegroundColor Red
}

Write-Host "Servicios listos para pruebas y capturas de pantalla." -ForegroundColor Cyan
