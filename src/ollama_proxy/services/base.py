from abc import ABC, abstractmethod
import aiohttp
from typing import List, Dict, Any, AsyncGenerator
from ..define import ChatRequest


class BaseModelService(ABC):
    def __init__(self, provider: str, url: str, api_key: str):
        self.provider = provider
        self.url = url
        self.api_key = api_key

    @abstractmethod
    async def chat(self, chat_request: ChatRequest) -> AsyncGenerator[str, None]:
        """
        抽象方法，用于实现流式聊天功能。

        参数:
        - messages: 聊天消息列表
        - model_name: 模型名称
        - kwargs: 其他可选参数

        返回:
        - 异步生成器，产生符合 SSE 格式的字符串
        """
        pass

    async def list_models(self) -> List[Dict[str, Any]]:
        """
        获取可用的模型列表。

        返回:
        - 包含模型信息的字典列表
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.url}/api/tags") as response:
                if response.status != 200:
                    raise Exception(f"API 请求失败: {response.status}")
                data = await response.json()
                return data.get("models", [])

    def get_model_info(self) -> Dict[str, str]:
        """
        获取模型信息。

        返回:
        - 包含模型信息的字典
        """
        return {"provider": self.provider, "url": self.url}

    def __str__(self) -> str:
        return f"{self.provider} {self.url}"
