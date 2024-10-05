from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from .define import ChatRequest
from .models import list_models
from .config import init_model_service

router = APIRouter()


@router.post("/api/chat")
async def chat(chat_request: ChatRequest, request: Request):
    print("收到聊天请求")

    print(f"app state: {request.app}")
    print(f"chat request: {chat_request}")

    model_name = request.app.state.model_name
    config_path = request.app.state.config
    print(f"配置路径: {config_path}")
    print(f"模型名称: {model_name}")

    model_service = init_model_service(config_path, model_name)
    try:
        stream_generator = model_service.stream_chat(
            messages=chat_request.messages,
            model=chat_request.model,
            stream=chat_request.stream,
            format=chat_request.format,
            options=chat_request.options.model_dump() if chat_request.options else None,
            tools=chat_request.tools,
            keep_alive=chat_request.keep_alive,
        )

        if chat_request.stream:
            return StreamingResponse(stream_generator, media_type="text/event-stream")
        else:
            response_content = "".join([chunk for chunk in stream_generator])
            return JSONResponse(content={"response": response_content})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理聊天请求时出错: {str(e)}")


@router.get("/api/tags")
async def get_models(request: Request):
    try:
        model_name = request.app.state.model_name
        result = list_models(model_name)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/ping")
async def ping():
    """
    一个简单的ping-pong测试端点
    """
    return JSONResponse(content={"message": "pong"})
