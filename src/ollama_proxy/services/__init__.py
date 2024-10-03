# 模型服务列表


from .base import BaseModelService
from .deepseek import DeepseekModelService
from .qwen import QwenModelService
from .glm import GLMModelService


def create_model_service(provider: str, url: str, api_key: str) -> BaseModelService:
    """
    创建模型服务的工厂函数。

    参数:
    - provider: 服务提供商
    - url: 服务URL
    - api_key: API密钥

    返回:
    - BaseModelService 的子类实例
    """
    if provider == "deepseek":
        return DeepseekModelService(provider, url, api_key)
    elif provider == "aliyun":
        return QwenModelService(provider, url, api_key)
    elif provider == "zhipu":
        return GLMModelService(provider, url, api_key)
    else:
        raise ValueError(f"不支持的服务提供商: {provider}")


# 导出工厂函数
__all__ = ["create_model_service"]
