from datetime import datetime
import random
import string


def parse_model_name(section_name):
    parts = section_name.split("-", 1)
    return f"{parts[0]}:{parts[1]}" if len(parts) > 1 else section_name


def generate_random_digest(length=64):
    return "".join(random.choices(string.hexdigits.lower(), k=length))


def list_models(model_name):
    print("开始处理 /api/tags 请求")
    try:
        model_data = {
            "name": parse_model_name(model_name),
            "modified_at": datetime.now().isoformat(),
            "size": 1000000000,  # 默认大小，例如 1GB
            "digest": generate_random_digest(),
            "details": {
                "format": "gguf",  # 默认格式
                "family": "llama",  # 默认系列
                "families": None,
                "parameter_size": "14b",  # 默认参数大小
                "quantization_level": "Q4_0",  # 默认量化级别
            },
        }
        print(f"获取到的模型信息: {model_data}")
        return {"models": [model_data]}
    except Exception as e:
        print(f"发生异常: {str(e)}")
        raise Exception(str(e))
