#!/bin/bash

# 检查是否安装了 uvicorn
if ! command -v uvicorn &> /dev/null
then
    echo "uvicorn 未安装。正在尝试安装..."
    pip install uvicorn
fi

# 启动服务
uvicorn src.ragservice.main:app --host 0.0.0.0 --port 8000
