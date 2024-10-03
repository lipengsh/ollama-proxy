from fastapi import FastAPI
import asyncio
from contextlib import asynccontextmanager
from define import ChatRequest
from services import create_model_service
import toml


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


def create_app(config_file: str = "keys.toml"):
    # 读取配置文件

    models_list = (toml.load(open(config_file, "r")) if True else {}) if True else {}

    app = FastAPI(lifespan=lifespan)

    @app.post("/api/chat")
    async def chat(request: ChatRequest):
        # 获取模型配置
        model_config = models_list.get(request.model)

        if not model_config:
            return {"error": f"模型 {request.model} 未配置"}

        provider = model_config.get("provider")
        service_url = model_config.get("url")
        api_key = model_config.get("api_key")

        model_service = create_model_service(provider, service_url, api_key)

        async def chat_stream():
            return model_service.stream_chat(request.messages, **request.kwargs)
