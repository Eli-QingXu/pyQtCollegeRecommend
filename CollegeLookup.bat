@echo off
:: Ensure the script runs from its current directory
cd %~dp0

:: Specify the Python script's filename here
set SCRIPT_NAME=pyQCollegeLookup.py

:: Execute the Python script
python %SCRIPT_NAME% > log.txt

:: Pause the command line to view the output
pause