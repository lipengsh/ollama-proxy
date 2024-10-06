import requests
import json


# Update BASE_URL to match your API server address
BASE_URL = "http://localhost:11434"


def test_chat_endpoint():
    # Prepare request data
    chat_request = {
        "stream": True,
        "messages": [{"role": "user", "content": "如何学习 python"}],
        "model": "glm-4-plus",  # Ensure the model name is correctly formatted
    }

    # Send POST request to /api/chat
    with requests.post(
        f"{BASE_URL}/api/chat", json=chat_request, stream=True
    ) as response:
        # Check response status code
        assert response.status_code == 200

        # Process streaming response
        response_content = ""
        final_response = None
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8").strip()

                # Parse JSON data
                if decoded_line.startswith("data:"):
                    json_data = decoded_line[5:].strip()  # Remove "data: " prefix
                    try:
                        data = json.loads(json_data)
                        if data.get("done"):
                            final_response = data
                        else:
                            # print content
                            print(f"content: {data['message']['content']}")
                            response_content += data["message"]["content"]
                    except json.JSONDecodeError as e:
                        print(f"JSON decode error: {e}")

        # Check response content
        assert isinstance(response_content, str)
        print(f"Full response content: {response_content}")

        # Check final response
        assert final_response is not None
        assert final_response.get("done") is True
        print(f"Final response: {final_response}")


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
