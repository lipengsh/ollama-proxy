from pydantic import BaseModel
from typing import List, Optional, Union, Dict


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
    options: Optional[Dict[str, Union[str, int, float, bool]]] = None
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
