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

        buffer = ""
        async for chunk in response.content.iter_any():
            line = chunk.decode('utf-8').strip()
            print(f'original line: {line}')

            if not line:
                print("line is empty")
                continue

            # get line from buffer and send left buffer to next loop
            buffer += line
            lines = buffer.split("\n\n")

            # 处理所有完整的行
            for i in range(len(lines)):
                if lines[i].startswith("data: ") and lines[i].endswith("}"):
                    print(f"complete lines[{i}]: {lines[i]}")
                    # 处理完整的 JSON 数据

                    if not line.startswith("data: "):
                        print("line is not start with data: ")
                        continue

                    # Check if line contains "[DONE]", means the stream is done
                    if "[DONE]" in line:
                        print("process_stream_lines: stream is done")
                        session.close()
                        return

                    try:
                        json_data = json.loads(line[6:])
                    except json.JSONDecodeError as e:
                        print(f"JSON解析错误: {e}")
                        print(f"问题数据: {line[6:]}")
                        return

                    choices = json_data.get("choices", [])
                    if choices:
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
                else:
                    print(f"no complete lines[{i}]: {lines[i]}")
                    # 如果发现不完整的行
                    if i < len(lines) - 1:
                        # 如果不是最后一个，丢弃
                        print("continue")
                        continue  # 退出循环，不处理后续行
                    else:
                        print("break")
                        # 如果是最后一个，保留到 buffer
                        buffer = lines[i] + "\n\n"  # 保留最后一行不完整的命令
                        break  # 退出循环
            else:
                print("all lines are complete")
                # 如果所有行都是完整的，清空 buffer
                buffer = ""

             