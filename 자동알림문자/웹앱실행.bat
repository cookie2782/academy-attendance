@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ========================================
echo 학원 등원/하원 웹 앱 시작
echo ========================================
echo.

C:\Users\lg\AppData\Local\Microsoft\WindowsApps\python.exe web_app.py

pause


