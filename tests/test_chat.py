import requests
import json


# 更新 BASE_URL 以匹配您的 API 服务器地址
BASE_URL = "http://localhost:11434"


def test_chat_endpoint():
    # 准备请求数据
    chat_request = {
        "stream": True,
        "messages": [{"role": "user", "content": "如何学习 python"}],
        "model": "glm-4-plus",  # 确保模型名称格式正确
    }

    # 发送 POST 请求到 /api/chat
    with requests.post(
        f"{BASE_URL}/api/chat", json=chat_request, stream=True
    ) as response:
        # 检查响应状态码
        assert response.status_code == 200

        # 处理流式响应
        response_content = ""
        final_response = None
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8").strip()

                # 解析 JSON 数据
                if decoded_line.startswith("data:"):
                    json_data = decoded_line[5:].strip()  # 去掉 "data: " 前缀
                    try:
                        data = json.loads(json_data)
                        if data.get("done"):
                            final_response = data
                        else:
                            # print content
                            print(f"content: {data['message']['content']}")
                            response_content += data["message"]["content"]
                    except json.JSONDecodeError as e:
                        print(f"JSON 解码错误: {e}")

        # 检查响应内容
        assert isinstance(response_content, str)
        print(f"完整响应内容: {response_content}")

        # 检查最终响应
        assert final_response is not None
        assert final_response.get("done") is True
        print(f"最终响应: {final_response}")


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
