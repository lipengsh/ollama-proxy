from .base import BaseModelService
import aiohttp
import time
import jwt
from typing import List, Dict, Any, AsyncGenerator


class GLMModelService(BaseModelService):
    def generate_token(self, exp_seconds: int = 60) -> str:
        try:
            id, secret = self.api_key.split(".")
        except Exception as e:
            raise Exception("无效的API密钥", e)

        payload = {
            "api_key": id,
            "exp": int(round(time.time() * 1000)) + exp_seconds * 1000,
            "timestamp": int(round(time.time() * 1000)),
        }

        return jwt.encode(
            payload,
            secret,
            algorithm="HS256",
            headers={"alg": "HS256", "sign_type": "SIGN"},
        )

    async def chat(
        self, messages: List[Dict[str, Any]], **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        实现 GLM 模型的流式聊天功能。

        参数:
        - messages: 聊天消息列表
        - kwargs: 其他可选参数

        返回:
        - 异步生成器，产生符合 SSE 格式的字符串
        """

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.generate_token(60),  # 生成60秒有效的token
        }

        data = {
            "prompt": messages,
            "temperature": kwargs.get("temperature", 0.9),
            "top_p": kwargs.get("top_p", 0.7),
            "incremental": True,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=headers, json=data) as response:
                if response.status != 200:
                    raise Exception(f"API 请求失败: {response.status}")

                async for line in response.content:
                    decoded_line = line.decode("utf-8").strip()
                    if decoded_line.startswith("data:"):
                        yield f"{decoded_line}\n\n"
