#!/bin/bash

# 检查是否安装了必要的包
check_and_install() {
    if ! python -c "import $1" &> /dev/null; then
        echo "$1 未安装。正在尝试安装..."
        pip install $1
    fi
}

check_and_install uvicorn
check_and_install click
check_and_install fastapi

# 设置默认值
CONFIG="keys.toml"
HOST="0.0.0.0"
PORT=11434

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
        *)
            echo "未知选项: $1"
            exit 1
            ;;
    esac
done

# 启动服务
echo "正在启动 Ollama 代理服务器..."
python -m src.ollama_proxy.main --config "$CONFIG" --host "$HOST" --port "$PORT"
