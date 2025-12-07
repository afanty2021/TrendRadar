@echo off
REM 博主监控启动脚本 (Windows)

setlocal enabledelayedexpansion

REM 颜色定义
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "NC=[0m"

REM 项目目录
cd /d "%~dp0"

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%错误: 未找到 Python%NC%
    pause
    exit /b 1
)

REM 检查配置文件
set CONFIG_FILE=config\blogger_config.yaml
if not exist "%CONFIG_FILE%" (
    echo %YELLOW%配置文件不存在，正在创建...%NC%
    python blogger_monitor.py --init-config
    echo %GREEN%配置文件已创建: %CONFIG_FILE%%NC%
    echo %YELLOW%请编辑配置文件后重新运行%NC%
    pause
    exit /b 0
)

REM 显示菜单
:menu
cls
echo %GREEN%=== TrendRadar 博主监控工具 ===%NC%
echo 1) 单次运行（测试）
echo 2) 守护进程模式（持续监控）
echo 3) 查看配置文件
echo 4) 查看日志
echo 5) 集成到 TrendRadar 推送
echo 0) 退出
echo.
set /p choice=%YELLOW%请选择操作: %NC%

if "%choice%"=="1" (
    call :run_once
    pause
    goto menu
)
if "%choice%"=="2" (
    call :run_daemon
)
if "%choice%"=="3" (
    call :view_config
    pause
    goto menu
)
if "%choice%"=="4" (
    call :view_logs
    pause
    goto menu
)
if "%choice%"=="5" (
    call :integrate_notification
    pause
    goto menu
)
if "%choice%"=="0" (
    echo %GREEN%再见！%NC%
    exit /b 0
)
echo %RED%无效选择，请重试%NC%
timeout /t 1 >nul
goto menu

REM 单次运行
:run_once
echo %GREEN%执行单次监控检查...%NC%
python blogger_monitor.py --once
goto :eof

REM 守护进程模式
:run_daemon
echo %GREEN%启动守护进程模式...%NC%
echo %YELLOW%按 Ctrl+C 停止监控%NC%
python blogger_monitor.py
goto :eof

REM 查看配置
:view_config
echo %GREEN%当前配置:%NC%
type config\blogger_config.yaml | more
goto :eof

REM 查看日志
:view_logs
echo %GREEN%最近50行日志:%NC%
if exist blogger_monitor.log (
    powershell "Get-Content blogger_monitor.log | Select-Object -Last 50"
) else (
    echo %YELLOW%暂无日志文件%NC%
)
goto :eof

REM 集成推送
:integrate_notification
echo %GREEN%处理新通知并集成到 TrendRadar...%NC%
python integrations\blogger_integration.py
goto :eof

REM 如果有参数，直接执行
if "%1"=="--once" (
    call :run_once
    goto :eof
)
if "%1"=="--daemon" (
    call :run_daemon
    goto :eof
)
if "%1"=="--config" (
    call :view_config
    goto :eof
)
if "%1"=="--logs" (
    call :view_logs
    goto :eof
)
if "%1"=="--notify" (
    call :integrate_notification
    goto :eof
)
if "%1"=="" (
    goto menu
) else (
    echo 用法: %~nx0 [--enable --daemon --config --logs --notify]
    exit /b 1
)