@echo off
echo ========================================
echo   数字人民币智能合约预付卡平台
echo   Gym Smart Contract Demo
echo ========================================
echo.

REM 启动 Flask 后端（后台运行）
echo [1/2] 启动 Flask 服务...
start "GymApp-Flask" /MIN python gym_smart_contract_app.py

REM 等 Flask 启动
echo 等待 Flask 启动中...
timeout /t 3 /nobreak >nul

REM 启动 cloudflared 隧道
echo [2/2] 启动公网隧道...
echo.
echo 正在获取公网地址，稍等...
echo 出现 "trycloudflare.com" 链接后，复制发给别人即可
echo.
echo 按 Ctrl+C 关闭隧道，再关掉 Flask 窗口即可
echo ========================================
echo.

%USERPROFILE%\cloudflared.exe tunnel --url http://127.0.0.1:5000

pause
