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
        Implement streaming chat functionality for GLM models using the Zhipu SDK.

        Parameters:
        - chat_request: Chat request object

        Returns:
        - Asynchronous generator producing strings formatted as SSE
        """
        messages_json = [message.model_dump() for message in chat_request.messages]

        model_name = chat_request.model.replace(":", "-", 1)

        # Use Zhipu SDK to make the request
        response = self.client.chat.completions.create(
            model=model_name, messages=messages_json, stream=True
        )

        # Parse the response
        for chunk in response:
            # check if finish_reason is a property of chunk
            finish_reason = chunk.choices[0].finish_reason
            end = True if finish_reason == "stop" else False

            # Assuming response is a list of tuples
            # You may need to unpack the tuples
            content = chunk.choices[0].delta.content

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

            # If end is True, build final_response
            if end:
                # Build final_response
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


            yield f"{json_response_data}\n"
