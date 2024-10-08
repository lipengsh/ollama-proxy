from .base import BaseModelService
import json
import datetime
import aiohttp
from typing import AsyncGenerator
from ..define import ChatRequest

class DeepseekModelService(BaseModelService):
    def __init__(self, provider: str, url: str, api_key: str):
        super().__init__(provider, url, api_key)

    async def chat(
        self,
        chat_request: ChatRequest,
    ) -> AsyncGenerator[str, None]:
        """
        实现DeepSeek模型的流式聊天功能。

        参数:
        - chat_request: 聊天请求对象

        返回:
        - 异步生成器，产生格式化为SSE的字符串
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        # debug
        model_name = "deepseek-chat"

        data = {
            "model": model_name,
            "messages": [message.model_dump() for message in chat_request.messages],
            "stream": True
        }

        session = aiohttp.ClientSession()


        response = await session.post(self.url, headers=headers, json=data)

        if response.status != 200:
            yield f"API请求失败，状态码：{response.status}"
            return


        async for line in response.content:
            decode_line = line.decode('utf-8').strip()
            print(f"decode_line: {decode_line}")
            continue

            if not decode_line:
                continue

            if not decode_line.startswith("data: "):
                print("line is not start with data: ")
                continue

            # Check if line contains "[DONE]", means the stream is done
            # if "[DONE]" in decode_line:
            #     print("process_stream_lines: stream is done")
            #     session.close()
            #     return

            try:
                json_data = json.loads(decode_line[6:])
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
                print(f"问题数据: {decode_line[6:]}")
                return

            choices = json_data.get("choices", [])
            if not choices:
                print("choices is empty")
                continue

            delta = choices[0].get("delta", {})
            content = delta.get("content", "")
            # Check null content
            if content is None:
                print("content is None")
                return

            finish_reason = choices[0].get("finish_reason")
            
            response_data = {
                "model": json_data.get("model", "deepseek"),
                "created_at": datetime.datetime.fromtimestamp(json_data.get("created", 0)).isoformat(),
                "done": finish_reason is not None,
                "message": {
                    "role": delta.get("role", "assistant"),
                    "content": content,
                    "images": None,
                } if content else None,
            }

            if finish_reason is not None:
                response_data.update({
                    "total_duration": 4883583458,
                    "load_duration": 1334875,
                    "prompt_eval_count": 26,
                    "prompt_eval_duration": 342546000,
                    "eval_count": 282,
                    "eval_duration": 4535599000,
                })

            json_response_data = json.dumps(response_data)
            print(f"json_response_data: {json_response_data}")
            yield f"{json_response_data}\n"

            if finish_reason is not None:
                print("finish_reason is not None")
                return



             