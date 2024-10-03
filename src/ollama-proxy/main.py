from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict
import json
import asyncio
from datetime import datetime

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str
    images: Optional[List[str]] = None
    tool_calls: Optional[List[Dict]] = None

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    stream: Optional[bool] = True
    format: Optional[str] = None
    options: Optional[Dict[str, Union[str, int, float, bool]]]] = None
    tools: Optional[List[Dict]] = None
    keep_alive: Optional[Union[str, int]] = "5m"

class ChatResponse(BaseModel):
    model: str
    created_at: str
    message: Message
    done: bool
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    prompt_eval_duration: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None

@app.post("/api/chat")
async def chat(request: ChatRequest):
    if not request.messages:
        # 如果消息列表为空,则加载模型
        return load_model(request.model, request.keep_alive)
    
    async def chat_stream():
        # 这里应该实现实际的聊天逻辑
        # 以下是一个简单的模拟示例
        for i in range(5):
            await asyncio.sleep(1)  # 模拟处理时间
            response = ChatResponse(
                model=request.model,
                created_at=datetime.now().isoformat(),
                message=Message(role="assistant", content=f"这是第 {i+1} 条模拟的回复消息。"),
                done=i == 4,
                total_duration=1000000000,
                load_duration=100000000,
                prompt_eval_count=10,
                prompt_eval_duration=200000000,
                eval_count=20,
                eval_duration=700000000
            )
            yield json.dumps(response.dict(), ensure_ascii=False).encode('utf-8') + b"\n"

    if request.stream:
        return StreamingResponse(chat_stream(), media_type="text/event-stream")
    else:
        # 非流式响应
        response = ChatResponse(
            model=request.model,
            created_at=datetime.now().isoformat(),
            message=Message(role="assistant", content="这是一个非流式的模拟回复。"),
            done=True,
            total_duration=1000000000,
            load_duration=100000000,
            prompt_eval_count=10,
            prompt_eval_duration=200000000,
            eval_count=20,
            eval_duration=700000000
        )
        return response.dict()

def load_model(model: str, keep_alive: Union[str, int]):
    # 这里应该实现实际的模型加载逻辑
    # 以下是一个简单的模拟示例
    response = ChatResponse(
        model=model,
        created_at=datetime.now().isoformat(),
        message=Message(role="assistant", content=""),
        done=True,
        done_reason="load"
    )
    return response.dict()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=11434)
