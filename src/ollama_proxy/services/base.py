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
        Abstract method for implementing streaming chat functionality.

        Parameters:
        - messages: List of chat messages
        - model_name: Model name
        - kwargs: Other optional parameters

        Returns:
        - Asynchronous generator producing strings formatted as SSE
        """
        pass

    async def list_models(self) -> List[Dict[str, Any]]:
        """
        Get the list of available models.

        Returns:
        - List of dictionaries containing model information
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
