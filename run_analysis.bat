@echo off
title Disk Forensic Timeline Analyzer
echo Starting Forensic Analysis...

python main.py --evidence_path "C:\Evidence" --output_dir "output"

echo Analysis complete!
echo Check the 'output' folder for results.
pause