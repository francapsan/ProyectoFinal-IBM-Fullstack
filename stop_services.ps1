# Detener procesos en los puertos 8000, 3030 y 5000
$ports = 8000, 3030, 5000
foreach ($p in $ports) {
    $connections = Get-NetTCPConnection -LocalPort $p -ErrorAction SilentlyContinue
    if ($connections) {
        foreach ($c in $connections) {
            Stop-Process -Id $c.OwningProcess -Force -ErrorAction SilentlyContinue
            Write-Host "Puerto $p liberado (PID $($c.OwningProcess))." -ForegroundColor Green
        }
    }
}
Write-Host "Servicios detenidos." -ForegroundColor Cyan
