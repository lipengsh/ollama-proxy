from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Union, Any


class Image(BaseModel):
    data: str


class ToolCall(BaseModel):
    id: str
    type: str
    function: Dict[str, Any]


class Message(BaseModel):
    role: str
    content: str
    images: Optional[List[Image]] = None
    tool_calls: Optional[List[ToolCall]] = None


class Options(BaseModel):
    num_ctx: Optional[int] = None
    num_predict: Optional[int] = None
    stop: Optional[List[str]] = Field(default_factory=list)
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    # 可以根据需要添加更多选项


class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    stream: bool = True
    format: Optional[str] = None
    options: Optional[Options] = None
    tools: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    keep_alive: Optional[Union[str, int]] = "5m"

    class Config:
        extra = "allow"  # 允许额外的字段


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
