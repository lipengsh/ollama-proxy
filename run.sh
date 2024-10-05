#!/bin/bash

# 检查是否安装了必要的包
check_and_install() {
    if ! poetry run python -c "import $1" &> /dev/null; then
        echo "$1 未安装。正在尝试安装..."
        poetry add $1
    fi
}

check_and_install uvicorn
check_and_install click
check_and_install fastapi

# 设置默认值
CONFIG="keys.toml"
HOST="localhost"
PORT=11434
RELOAD=true
MODEL="glm-4-plus"

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --config)
            CONFIG="$2"
            shift 2
            ;;
        --host)
            HOST="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --reload)
            RELOAD=true
            shift
            ;;
        *)
            if [ -z "$MODEL" ]; then
                MODEL="$1"
                shift
            else
                echo "未知选项: $1"
                exit 1
            fi
            ;;
    esac
done

# 检查是否提供了模型名称
if [ -z "$MODEL" ]; then
    echo "错误: 必须提供模型名称"
    echo "用法: $0 <model_name> [--config <config_file>] [--host <host>] [--port <port>] [--reload]"
    exit 1
fi

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 将项目根目录添加到 PYTHONPATH
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# 启动服务
echo "正在启动 Ollama 代理服务器，运行模型: $MODEL"

# 构建应用程序参数
APP_ARGS="$MODEL --config $CONFIG --host $HOST --port $PORT"
if [ "$RELOAD" = true ]; then
    APP_ARGS="$APP_ARGS --reload"
fi

# 运行应用程序
poetry run start $APP_ARGS
