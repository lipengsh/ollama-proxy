from typing import Tuple
import re

def parse_model_name(model_name: str) -> Tuple[str, str, str]:
    """
    解析模型名称,返回命名空间、模型名和标签。

    参数:
    - model_name: 完整的模型名称字符串

    返回:
    - 元组 (namespace, model, tag)
    """
    parts = model_name.split('/')
    if len(parts) > 1:
        namespace = parts[0]
        model_and_tag = parts[1]
    else:
        namespace = ""
        model_and_tag = parts[0]
    
    model_parts = model_and_tag.split(':')
    model = model_parts[0]
    tag = model_parts[1] if len(model_parts) > 1 else "latest"
    
    return namespace, model, tag

def route_to_cloud_service(model_name: str) -> Tuple[str, str]:
    """
    根据模型名称路由到不同的云服务,并返回提供商和模型名称。

    参数:
    - model_name: 完整的模型名称字符串

    返回:
    - 元组 (provider, model_name)
    """
    namespace, model, _ = parse_model_name(model_name)
    
    if namespace.lower() == "openai" or re.match(r"gpt-\d+", model):
        return "openai", model
    elif namespace.lower() == "anthropic" or model.startswith("claude-"):
        return "anthropic", model
    else:
        return "ollama", model_name  # 对于 Ollama,返回完整的模型名称
