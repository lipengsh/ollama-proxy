from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from .define import ChatRequest
from .models import list_models
from .depends import get_model_service, get_model_name


class Router:
    def __init__(self):
        self.router = APIRouter()
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("/api/chat", self.chat, methods=["POST"])
        self.router.add_api_route("/api/tags", self.get_models, methods=["GET"])

    async def chat(
        self,
        chat_request: ChatRequest,
        model_service=Depends(get_model_service),
    ):
        print("got chat")
        model_name = await get_model_name()
        print(f"model_name: {model_name}")
        print(f"model_service: {model_service}")
        try:
            stream_generator = model_service.stream_chat(
                messages=chat_request.messages,
                model=chat_request.model,
                stream=chat_request.stream,
                format=chat_request.format,
                options=chat_request.options.model_dump()
                if chat_request.options
                else None,
                tools=chat_request.tools,
                keep_alive=chat_request.keep_alive,
            )

            if chat_request.stream:
                return StreamingResponse(
                    stream_generator, media_type="text/event-stream"
                )
            else:
                response_content = "".join([chunk for chunk in stream_generator])
                return JSONResponse(content={"response": response_content})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"处理聊天请求时出错: {str(e)}")

    async def get_models(self, model_name=Depends(get_model_name)):
        try:
            result = list_models(model_name)
            return JSONResponse(content=result)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_router(self) -> APIRouter:
        return self.router
