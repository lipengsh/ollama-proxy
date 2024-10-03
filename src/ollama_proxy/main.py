import os
import click
import signal
import uvicorn
import logging
from .server import create_app

# 使用环境变量或默认值来设置配置文件路径
DEFAULT_CONFIG_PATH = os.environ.get("OLLAMA_PROXY_CONFIG", "keys.toml")


def shutdown_handler(signum, frame):
    """
    处理系统信号以优雅地关闭服务器。

    参数:
    - signum: 信号编号。
    - frame: 当前的堆栈帧。
    """
    print("收到关闭信号。正在退出...")
    raise SystemExit(0)  # 退出程序


@click.command()
@click.option("--config", default=DEFAULT_CONFIG_PATH, help="Toml 配置文件的路径")
@click.option("--host", default="127.0.0.1", help="服务器主机地址")
@click.option("--port", default=8000, type=int, help="服务器端口")
@click.option("--reload", is_flag=True, help="启用热重载")
def main(config, host, port, reload):
    """启动 Ollama 代理服务器"""
    global app
    # 注册信号处理器
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    try:
        app = create_app(config)
        if app is None:
            raise ValueError("create_app 返回了 None")
    except Exception as e:
        logging.error(f"无法创建应用: {str(e)}")
        raise

    # 启动 uvicorn 服务器
    uvicorn.run("src.ollama_proxy.main:app", host=host, port=port, reload=reload)


app = create_app(DEFAULT_CONFIG_PATH)
