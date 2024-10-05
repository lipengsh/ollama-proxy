import datetime
import json
from zhipuai import ZhipuAI
from .base import BaseModelService
from typing import AsyncGenerator
from ..define import ChatRequest


class GLMModelService(BaseModelService):
    def __init__(self, provider: str, url: str, api_key: str):
        super().__init__(provider, url, api_key)
        self.client = ZhipuAI(api_key=self.api_key)

    async def chat(
        self,
        chat_request: ChatRequest,
    ) -> AsyncGenerator[str, None]:
        """
        使用智谱 SDK 实现 GLM 模型的流式聊天功能。

        参数:
        - chat_request: 聊天请求对象

        返回:
        - 异步生成器，产生符合 SSE 格式的字符串
        """
        messages_json = [message.model_dump() for message in chat_request.messages]

        model_name = chat_request.model.replace(":", "-", 1)

        # 使用智谱 SDK 进行请求
        response = self.client.chat.completions.create(
            model=model_name, messages=messages_json, stream=True
        )

        # 解析响应
        for chunk in response:
            # check if chunk is [DATA] ,means the stream is end
            end = True if chunk == "[DATA]" else False

            # 假设 response 是一个包含多个元组的列表
            # 你可能需要解包元组
            content = chunk.choices[0].delta.content

            print(f"content: {content}")

            #

            response_data = {
                "model": "glm",
                "created_at": datetime.datetime.now().isoformat(),
                "done": end,
                "message": {
                    "role": "assistant",
                    "content": content if content is not None else "",
                    "images": None,
                }
                if content is not None
                else None,
            }

            # 如果 content 为 None，则构建 final_response
            if content is None:
                print("content is None")
                # 构建 final_response
                response_data.update(
                    {
                        "total_duration": 4883583458,
                        "load_duration": 1334875,
                        "prompt_eval_count": 26,
                        "prompt_eval_duration": 342546000,
                        "eval_count": 282,
                        "eval_duration": 4535599000,
                    }
                )

            json_response_data = json.dumps(response_data)

            print(f"end: {end}")

            yield json_response_data
