from fastapi import FastAPI, Request
import asyncio
from contextlib import asynccontextmanager
from define import ChatRequest
from services import create_model_service
import toml
from fastapi.responses import StreamingResponse


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
        stream_generator = model_service.stream_chat(request.messages, **request.kwargs)

        # 返回流式响应
        return StreamingResponse(stream_generator, media_type="text/event-stream")
