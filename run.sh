#!/bin/bash

# Check if necessary packages are installed
check_and_install() {
    if ! poetry run python -c "import $1" &> /dev/null; then
        echo "$1 未安装。正在尝试安装..."
        poetry add $1
    fi
}

check_and_install uvicorn
check_and_install click
check_and_install fastapi

# Set default values
CONFIG="keys.toml"
HOST="localhost"
PORT=11434
RELOAD=true
MODEL="glm-4-plus"

# Parse command line arguments
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

# Check if a model name is provided
if [ -z "$MODEL" ]; then
    echo "Error: Model name is required"
    echo "Usage: $0 <model_name> [--config <config_file>] [--host <host>] [--port <port>] [--reload]"
    exit 1
fi

# Get the absolute path of the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Add the project root directory to PYTHONPATH
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# Start the service
echo "Starting Ollama proxy server, running model: $MODEL"

# Build application arguments
APP_ARGS="$MODEL --config $CONFIG --host $HOST --port $PORT"
if [ "$RELOAD" = true ]; then
    APP_ARGS="$APP_ARGS --reload"
fi

# Run the application
poetry run start $APP_ARGS
