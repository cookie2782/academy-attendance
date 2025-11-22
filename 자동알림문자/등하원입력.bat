@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo ========================================
echo 학원 등원/하원 입력 시스템
echo ========================================
echo.
echo 1. 콘솔 버전 (텍스트 기반)
echo 2. GUI 버전 (그래픽 인터페이스)
echo.
set /p choice="선택하세요 (1 또는 2): "

if "%choice%"=="1" (
    C:\Users\lg\AppData\Local\Microsoft\WindowsApps\python.exe attendance_input.py
) else if "%choice%"=="2" (
    C:\Users\lg\AppData\Local\Microsoft\WindowsApps\python.exe attendance_gui.py
) else (
    echo 잘못된 선택입니다.
    pause
)

