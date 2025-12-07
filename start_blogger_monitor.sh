#!/bin/bash
# 博主监控启动脚本 (Linux/macOS)

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未找到 Python3${NC}"
    exit 1
fi

# 检查配置文件
CONFIG_FILE="config/blogger_config.yaml"
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${YELLOW}配置文件不存在，正在创建...${NC}"
    python3 blogger_monitor.py --init-config
    echo -e "${GREEN}配置文件已创建: $CONFIG_FILE${NC}"
    echo -e "${YELLOW}请编辑配置文件后重新运行${NC}"
    exit 0
fi

# 显示菜单
show_menu() {
    echo -e "${GREEN}=== TrendRadar 博主监控工具 ===${NC}"
    echo "1) 单次运行（测试）"
    echo "2) 守护进程模式（持续监控）"
    echo "3) 查看配置文件"
    echo "4) 查看日志"
    echo "5) 集成到 TrendRadar 推送"
    echo "0) 退出"
    echo -e "${YELLOW}请选择操作:${NC}"
}

# 单次运行
run_once() {
    echo -e "${GREEN}执行单次监控检查...${NC}"
    python3 blogger_monitor.py --once
}

# 守护进程模式
run_daemon() {
    echo -e "${GREEN}启动守护进程模式...${NC}"
    echo -e "${YELLOW}按 Ctrl+C 停止监控${NC}"
    python3 blogger_monitor.py
}

# 查看配置
view_config() {
    echo -e "${GREEN}当前配置:${NC}"
    cat config/blogger_config.yaml | less
}

# 查看日志
view_logs() {
    echo -e "${GREEN}最近50行日志:${NC}"
    if [ -f "blogger_monitor.log" ]; then
        tail -50 blogger_monitor.log
    else
        echo -e "${YELLOW}暂无日志文件${NC}"
    fi
}

# 集成推送
integrate_notification() {
    echo -e "${GREEN}处理新通知并集成到 TrendRadar...${NC}"
    python3 integrations/blogger_integration.py
}

# 主循环
main() {
    while true; do
        show_menu
        read -n 1 -s choice
        echo ""

        case $choice in
            1)
                run_once
                echo -e "${GREEN}按回车继续...${NC}"
                read
                ;;
            2)
                run_daemon
                ;;
            3)
                view_config
                echo -e "${GREEN}按回车继续...${NC}"
                read
                ;;
            4)
                view_logs
                echo -e "${GREEN}按回车继续...${NC}"
                read
                ;;
            5)
                integrate_notification
                echo -e "${GREEN}按回车继续...${NC}"
                read
                ;;
            0)
                echo -e "${GREEN}再见！${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}无效选择，请重试${NC}"
                sleep 1
                ;;
        esac
    done
}

# 如果有参数，直接执行
if [ $# -gt 0 ]; then
    case $1 in
        --once)
            run_once
            ;;
        --daemon)
            run_daemon
            ;;
        --config)
            view_config
            ;;
        --logs)
            view_logs
            ;;
        --notify)
            integrate_notification
            ;;
        *)
            echo "用法: $0 [--once|--daemon|--config|--logs|--notify]"
            exit 1
            ;;
    esac
else
    # 显示交互菜单
    main
fi