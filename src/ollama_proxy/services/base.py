from abc import ABC, abstractmethod
import aiohttp
from typing import List, Dict, Any, AsyncGenerator


class BaseModelService(ABC):
    def __init__(self, provider: str, url: str, api_key: str):
        self.provider = provider
        self.url = url
        self.api_key = api_key

    @abstractmethod
    async def chat(
        self, messages: List[Dict[str, Any]], **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        抽象方法，用于实现流式聊天功能。

        参数:
        - messages: 聊天消息列表
        - kwargs: 其他可选参数

        返回:
        - 异步生成器，产生符合 SSE 格式的字符串
        """
        pass

    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> AsyncGenerator[str, None]:
        """
        抽象方法，用于实现流式文本生成功能。

        参数:
        - prompt: 生成提示
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
