from .base import BaseModelService
import aiohttp
import json
from typing import List, Dict, Any, AsyncGenerator


class DeepseekModelService(BaseModelService):
    async def chat(
        self, messages: List[Dict[str, Any]], **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        Implement streaming chat functionality for Deepseek models.

        Parameters:
        - messages: List of chat messages
        - kwargs: Other optional parameters

        Returns:
        - Asynchronous generator producing strings formatted as SSE
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        data = {
            "model": kwargs.get("model", "deepseek-chat"),
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "top_p": kwargs.get("top_p", 1),
            "stream": True,
            "max_tokens": kwargs.get("max_tokens", 2048),
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.url}/chat/completions", headers=headers, json=data
            ) as response:
                if response.status != 200:
                    raise Exception(f"API request failed: {response.status}")

                async for line in response.content:
                    decoded_line = line.decode("utf-8").strip()
                    if decoded_line.startswith("data: "):
                        json_data = json.loads(decoded_line[6:])
                        if json_data["choices"][0]["finish_reason"] is not None:
                            break
                        content = json_data["choices"][0]["delta"].get("content", "")
                        if content:
                            yield f"data: {json.dumps({'content': content})}\n\n"
