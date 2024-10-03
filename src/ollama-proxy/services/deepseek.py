from .base import BaseModelService
import aiohttp
import json
from typing import List, Dict, Any, AsyncGenerator


class DeepseekModelService(BaseModelService):
    def __init__(self, provider: str, url: str, api_key: str):
        super().__init__(provider, url, api_key)

    async def chat(self, messages: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
        """
        实现 Deepseek 模型的聊天功能。

        参数:
        - messages: 聊天消息列表
        - kwargs: 其他可选参数

        返回:
        - 聊天响应字典
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        data = {"messages": messages, **kwargs}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.url}/v1/chat/completions", headers=headers, json=data
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception(f"API 请求失败: {response.status}")

    async def stream_chat(
        self, messages: List[Dict[str, Any]], **kwargs
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        实现 Deepseek 模型的流式聊天功能。

        参数:
        - messages: 聊天消息列表
        - kwargs: 其他可选参数

        返回:
        - 异步生成器，用于流式返回聊天响应
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        data = {"messages": messages, "stream": True, **kwargs}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.url}/v1/chat/completions", headers=headers, json=data
            ) as response:
                if response.status == 200:
                    async for line in response.content:
                        if line:
                            yield json.loads(line.decode("utf-8").strip())
                else:
                    raise Exception(f"API 流式请求失败: {response.status}")
