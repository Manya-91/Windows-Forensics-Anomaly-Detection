# PowerShell script to collect basic system information
Write-Host "Collecting system information..." -ForegroundColor Green

# Create data directory
New-Item -ItemType Directory -Force -Path ".\data\raw" | Out-Null

# Get running processes
Get-Process | Select-Object ProcessName, Id, CPU, WorkingSet | Export-Csv -Path ".\data\raw\processes.csv" -NoTypeInformation

# Get network connections
Get-NetTCPConnection | Export-Csv -Path ".\data\raw\network_connections.csv" -NoTypeInformation

# Get services
Get-Service | Export-Csv -Path ".\data\raw\services.csv" -NoTypeInformation

# Get recent event logs (last 100 events)
Get-WinEvent -LogName System -MaxEvents 100 | Select-Object TimeCreated, Id, ProviderName, Message | Export-Csv -Path ".\data\raw\system_events.csv" -NoTypeInformation

Write-Host "Collection complete!" -ForegroundColor Green