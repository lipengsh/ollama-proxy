import requests
import pytest

# 更新 BASE_URL 以匹配您的 API 服务器地址
BASE_URL = "http://localhost:11434"


def test_chat_endpoint():
    # 准备请求数据
    chat_request = {
        "messages": [{"role": "user", "content": "你好"}],
        "model": "test_model",
        "stream": False,
        "format": "json",
        "options": None,
        "tools": None,
        "keep_alive": 0,
    }

    # 发送 POST 请求到 /api/chat
    response = requests.post(f"{BASE_URL}/api/chat", json=chat_request)

    print(f"API 响应: {response.json()}")

    # 检查响应
    assert response.status_code == 200
    response_data = response.json()
    assert "response" in response_data
    assert isinstance(response_data["response"], str)
    print(f"API 响应: {response_data['response']}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
