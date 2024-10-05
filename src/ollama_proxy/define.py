from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Union, Any


class Image(BaseModel):
    data: str


class ToolCall(BaseModel):
    id: str
    type: str
    function: Optional[Dict[str, Any]] = None
    retrieval: Optional[Dict[str, Any]] = None
    web_search: Optional[Dict[str, Any]] = None


class Message(BaseModel):
    role: str
    content: str
    images: Optional[List[Image]] = None
    tool_calls: Optional[List[ToolCall]] = None


class Image(BaseModel):
    data: str


class ToolCall(BaseModel):
    id: str
    type: str
    function: Optional[Dict[str, Any]] = None
    retrieval: Optional[Dict[str, Any]] = None
    web_search: Optional[Dict[str, Any]] = None


class Choice(BaseModel):
    index: int
    finish_reason: str
    delta: Dict[str, Union[str, None]]
    tool_calls: Optional[List[ToolCall]] = None


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class WebSearchResult(BaseModel):
    icon: str
    title: str
    link: str
    media: str
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    request_id: Optional[str] = None
    do_sample: Optional[bool] = True
    stream: Optional[bool] = False
    temperature: Optional[float] = 0.95
    top_p: Optional[float] = 0.7
    max_tokens: Optional[int] = 1024
    stop: Optional[List[str]] = Field(default_factory=list)
    tools: Optional[List[ToolCall]] = Field(default_factory=list)
    tool_choice: Optional[Union[str, Dict[str, Any]]] = "auto"
    user_id: Optional[str] = None
    keep_alive: Optional[Union[str, int]] = "5m"


class ChatResponse(BaseModel):
    id: str
    created: int
    model: str
    choices: List[Choice]
    usage: Optional[Usage] = None
    web_search: Optional[List[WebSearchResult]] = None
    done: bool
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    prompt_eval_duration: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None
