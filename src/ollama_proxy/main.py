import os
import click
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from .define import ChatRequest
from .config import init_model_service
from .models import list_models

# 使用环境变量或默认值来设置配置文件路径
DEFAULT_CONFIG_PATH = os.environ.get("OLLAMA_PROXY_CONFIG", "keys.toml")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("服务器正在启动")
    app.state.config_path = os.environ.get("CONFIG_PATH", DEFAULT_CONFIG_PATH)
    app.state.model_name = os.environ.get("MODEL_NAME", "default_model")

    yield
    print("服务器正在关闭")
    # 在这里可以清理资源，比如关闭数据库连接


app = FastAPI(lifespan=lifespan)


@app.post("/api/chat")
async def chat(chat_request: ChatRequest, request: Request):
    if not hasattr(request.app.state, "model_name") and hasattr(
        request.app.state, "config_path"
    ):
        print("app.state 缺少 model_name 或 config_path 属性")
        return JSONResponse(
            content={"error": "app.state 缺少 model_name 或 config_path 属性"}
        )

    model_name = request.app.state.model_name
    config_path = request.app.state.config_path

    model_service = init_model_service(config_path, model_name)

    try:
        stream_generator = model_service.chat(chat_request)
        if chat_request.stream:
            return StreamingResponse(stream_generator, media_type="text/event-stream")
        else:
            response_content = ""
            async for chunk in stream_generator:
                response_content += chunk
            return JSONResponse(content={"response": response_content})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理聊天请求时出错: {str(e)}")


@app.get("/api/tags")
async def get_models(request: Request):
    try:
        model_name = request.app.state.model_name
        result = list_models(model_name)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ping")
async def ping():
    """
    一个简单的ping-pong测试端点
    """
    return JSONResponse(content={"message": "pong"})


@click.command()
@click.argument("model_name")
@click.option("--config", default=DEFAULT_CONFIG_PATH, help="Toml 配置文件的路径")
@click.option("--host", default="127.0.0.1", help="服务器主机地址")
@click.option("--port", default=8000, type=int, help="服务器端口")
@click.option("--reload", is_flag=True, help="启用热重载")
def run(model_name, config, host, port, reload):
    """运行特定的模型"""

    # 设置环境变量以便在 startup 事件中使用
    os.environ["CONFIG_PATH"] = config
    os.environ["MODEL_NAME"] = model_name

    uvicorn.run(
        "ollama_proxy.main:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    run()
