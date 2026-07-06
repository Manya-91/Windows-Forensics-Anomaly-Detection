@echo off
title Disk Forensic Analysis - Complete
echo ========================================
echo DISK FORENSIC ANALYZER - COMPLETE RUN
echo ========================================
echo.

echo Step 1: Collecting real system data...
echo ----------------------------------------
python collect_data.py
if %errorlevel% neq 0 (
    echo Warning: Python data collection had issues
)

echo.
echo Step 2: Collecting PowerShell data...
echo ----------------------------------------
powershell -ExecutionPolicy Bypass -File collect_ps.ps1

echo.
echo Step 3: Running forensic analysis...
echo ----------------------------------------
python main.py --evidence_path "./data" --output_dir "./output"

echo.
echo ========================================
echo ANALYSIS COMPLETE!
echo Check the 'output' folder for results
echo ========================================
pause