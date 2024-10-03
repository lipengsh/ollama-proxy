import argparse
import signal
from .server import create_app


def shutdown_handler(signum, frame):
    """
    处理系统信号以优雅地关闭服务器。

    参数:
    - signum: 信号编号。
    - frame: 当前的堆栈帧。
    """
    print("Received shutdown signal. Exiting...")
    raise SystemExit(0)  # 退出程序


parser = argparse.ArgumentParser(description="启动 Ollama 代理服务器")

# 添加配置文件参数
# --config: 可选参数,用于指定配置文件的路径
# type=str: 参数类型为字符串
# default="config.toml": 如果未指定,默认使用 "config.toml" 文件
# help: 参数的帮助说明,在使用 -h 或 --help 时显示
parser.add_argument(
    "--config", type=str, default="config.toml", help="Toml 配置文件的路径"
)

# 解析命令行参数
args = parser.parse_args()

# 注册信号处理器
signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

# 创建应用
app = create_app(args.config)
