call %~dp0\venv\Scripts\python.exe cleanup.py
powershell -nop -c "& {sleep 10}"
RUNDLL32.EXE USER32.dll, UpdatePerUserSystemParameters
RUNDLL32.EXE USER32.DLL, UpdatePerUserSystemParameters 1, True
powershell -File .\toast.ps1 "Archived old images!" "Tuftpaper Cleanup"