from fastapi import FastAPI, HTTPException
import asyncio
from contextlib import asynccontextmanager
from .define import ChatRequest
from .services import create_model_service
import toml
from fastapi.responses import StreamingResponse, JSONResponse
from datetime import datetime
import random
import string

shutdown_event = asyncio.Event()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI 应用的生命周期管理器，用于处理启动和关闭事件。
    """
    try:
        yield
    finally:
        print("Shutting down...")
        shutdown_event.set()
        await asyncio.sleep(1)  # 给其他任务一些时间来清理
        print("All tasks cancelled.")


def parse_model_name(section_name):
    parts = section_name.split("-", 1)
    return f"{parts[0]}:{parts[1]}" if len(parts) > 1 else section_name


def generate_random_digest(length=64):
    return "".join(random.choices(string.hexdigits.lower(), k=length))


def create_app(config_file: str = "keys.toml"):
    try:
        # 读取配置文件
        models_list = toml.load(open(config_file, "r"))

        app = FastAPI(lifespan=lifespan)

        @app.post("/api/chat")
        async def chat(request: ChatRequest):
            # 解析模型名称
            model_name = request.model
            if ":" in model_name:
                model_parts = model_name.split(":")
                model_name = f"{model_parts[0]}-{model_parts[1]}"
            elif model_name.endswith(":latest"):
                model_name = model_name[:-7]  # 移除 ':latest' 后缀

            # 更新请求中的模型名称
            request.model = model_name

            # 获取模型配置
            model_config = models_list.get(request.model)

            if not model_config:
                return {"error": f"模型 {request.model} 未配置"}

            provider = model_config.get("provider")
            service_url = model_config.get("url")
            api_key = model_config.get("api_key")

            model_service = create_model_service(provider, service_url, api_key)

            # 直接使用 model_service.stream_chat 作为生成器
            stream_generator = model_service.stream_chat(
                request.messages, **request.kwargs
            )

            # 返回流式响应
            return StreamingResponse(stream_generator, media_type="text/event-stream")

        @app.get("/api/tags")
        async def list_models():
            """
            列出所有可用的模型。
            """
            print("开始处理 /api/tags 请求")

            try:
                # 从 models_list 中获取详细的模型信息
                models = []
                for section_name, model_info in models_list.items():
                    model_name = parse_model_name(section_name)
                    model_data = {
                        "name": model_name,
                        "modified_at": datetime.now().isoformat(),
                        "size": 1000000000,  # 默认大小，例如 1GB
                        "digest": generate_random_digest(),
                        "details": {
                            "format": "gguf",  # 默认格式
                            "family": "llama",  # 默认系列
                            "families": None,
                            "parameter_size": "14b",  # 默认参数大小
                            "quantization_level": "Q4_0",  # 默认量化级别
                        },
                    }
                    models.append(model_data)

                print(f"获取到的模型列表: {models}")

                return JSONResponse(content={"models": models})
            except Exception as e:
                print(f"发生异常: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        return app
    except Exception as e:
        print(f"创建应用时发生错误: {str(e)}")
        raise  # 重新抛出异常，以便调用者知道发生了错误
