import os
import click
import signal
import logging
import asyncio
from .app import init_application, get_application
from .router import Router
from hypercorn.asyncio import serve
from hypercorn.config import Config
from watchfiles import run_process

# 使用环境变量或默认值来设置配置文件路径
DEFAULT_CONFIG_PATH = os.environ.get("OLLAMA_PROXY_CONFIG", "keys.toml")

# 设置日志级别
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def shutdown_handler(signum, frame):
    logger.info("收到关闭信号。正在退出...")
    raise SystemExit(0)


async def startup_event():
    pass


async def start_app(model_name, config, host, port, use_reload):
    app = get_application()

    # init router
    router = Router().get_router()

    # init application
    init_application(model_name, config, startup_event=startup_event, router=router)

    print(f"start_app.app.routes: {app.routes}")

    config = Config()
    config.bind = [f"{host}:{port}"]
    config.use_reloader = use_reload
    await serve(app, config)


def run_app(model_name, config, host, port, use_reload):
    asyncio.run(start_app(model_name, config, host, port, use_reload))


@click.command()
@click.argument("model_name")
@click.option("--config", default=DEFAULT_CONFIG_PATH, help="Toml 配置文件的路径")
@click.option("--host", default="127.0.0.1", help="服务器主机地址")
@click.option("--port", default=8000, type=int, help="服务器端口")
@click.option("--reload", is_flag=True, help="启用热重载")
@click.option("--debug", is_flag=True, help="启用调试模式")
def run(model_name, config, host, port, reload, debug):
    """运行特定的模型"""
    if debug:
        logger.setLevel(logging.DEBUG)

    # 注册信号处理器
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    if reload:
        # 使用 watchfiles 来实现热重载
        run_process(".", target=run_app, args=(model_name, config, host, port, reload))
    else:
        run_app(host, port, reload)


if __name__ == "__main__":
    run()
