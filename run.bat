call %~dp0\venv\Scripts\python.exe main.py
powershell -nop -c "& {sleep 10}"
RUNDLL32.EXE USER32.dll, UpdatePerUserSystemParameters
RUNDLL32.EXE USER32.DLL, UpdatePerUserSystemParameters 1, True