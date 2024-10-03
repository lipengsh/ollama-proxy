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

# 此时, args 是一个包含解析后参数的对象
# args.config 将包含配置文件的路径,可能是用户指定的值,也可能是默认值 "config.toml"

# 示例: 使用解析后的配置文件路径
print(f"使用的配置文件路径: {args.config}")

# 接下来,您可以使用 args.config 来加载配置文件
# 例如:
# import toml
# with open(args.config, 'r') as f:
#     config = toml.load(f)

# 注意: 实际使用时,您应该添加错误处理,以防配置文件不存在或格式不正确

app = create_app(args.config)


# 注册信号处理器
signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)
