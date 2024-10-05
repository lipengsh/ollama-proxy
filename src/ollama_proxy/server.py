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


def create_app(config_file: str, model_name: str):
    try:
        # 读取配置文件
        models_list = toml.load(open(config_file, "r"))

        if model_name not in models_list:
            raise ValueError(f"模型 {model_name} 在配置文件中未找到")

        model_config = models_list[model_name]
        provider = model_config.get("provider")
        service_url = model_config.get("url")
        api_key = model_config.get("api_key")

        model_service = create_model_service(provider, service_url, api_key)

        app = FastAPI(lifespan=lifespan)

        @app.post("/api/chat")
        async def chat(request: ChatRequest):
            stream_generator = model_service.stream_chat(
                request.messages, **request.kwargs
            )
            return StreamingResponse(stream_generator, media_type="text/event-stream")

        @app.get("/api/tags")
        async def list_models():
            print("开始处理 /api/tags 请求")
            try:
                model_data = {
                    "name": parse_model_name(model_name),
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
                print(f"获取到的模型信息: {model_data}")
                return JSONResponse(content={"models": [model_data]})
            except Exception as e:
                print(f"发生异常: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

        return app
    except Exception as e:
        print(f"创建应用时发生错误: {str(e)}")
        raise  # 重新抛出异常，以便调用者知道发生了错误
