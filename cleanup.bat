call %~dp0\venv\Scripts\python.exe cleanup.py
powershell -nop -c "& {sleep 10}"
powershell -File .\toast.ps1 "Archived old images!"