@echo off

:: Step 1: Check for Python Installation and Install if not present
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Installing Python...
    powershell -command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe -OutFile %TEMP%\python-3.12.0-amd64.exe"
    powershell -command "Start-Process '%TEMP%\python-3.12.1-amd64.exe' -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait"
) else (
    echo Python is already installed.
)

:: Step 2: Install Python packages
echo Installing required Python packages...
python -m pip install PyQt5 pandas

:: Step 3: Verify the installation
python -c "import PyQt5; import pandas; print('Setup completed successfully.')"

pause
