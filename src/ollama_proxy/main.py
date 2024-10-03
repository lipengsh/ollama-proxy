import click
import signal
import uvicorn
from .server import create_app
from fastapi import FastAPI


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
@click.option("--config", default="config.toml", help="Toml 配置文件的路径")
@click.option("--host", default="127.0.0.1", help="服务器主机地址")
@click.option("--port", default=8000, type=int, help="服务器端口")
def main(config, host, port):
    """启动 Ollama 代理服务器"""
    # 注册信号处理器
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    # 创建应用
    app = create_app(config)

    # 如果 app 仍然为 None,可以添加一个检查
    if app is None:
        raise ValueError("create_app 返回了 None,请检查 create_app 函数的实现")

    # 启动 uvicorn 服务器
    uvicorn.run("src.ollama_proxy.main:app", host=host, port=port)


if __name__ == "__main__":
    main()
