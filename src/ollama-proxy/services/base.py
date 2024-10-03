from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseModelService(ABC):
    def __init__(self, provider: str, url: str, api_key: str):
        self.provider = provider
        self.url = url
        self.api_key = api_key

    @abstractmethod
    async def chat(self, messages: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
        """
        抽象方法，用于实现聊天功能。

        参数:
        - messages: 聊天消息列表
        - kwargs: 其他可选参数

        返回:
        - 聊天响应字典
        """
        pass

    @abstractmethod
    async def stream_chat(self, messages: List[Dict[str, Any]], **kwargs):
        """
        抽象方法，用于实现流式聊天功能。

        参数:
        - messages: 聊天消息列表
        - kwargs: 其他可选参数

        返回:
        - 异步生成器，用于流式返回聊天响应
        """
        pass

    def get_model_info(self) -> Dict[str, str]:
        """
        获取模型信息。

        返回:
        - 包含模型信息的字典
        """
        return {"provider": self.provider, "url": self.url}
