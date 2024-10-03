# 模型服务列表
from typing import Dict
from .base import BaseModelService
from .deepseek import DeepseekModelService
from .glm import GLMModelService


def create_model_service(provider: str, url: str, api_key: str) -> BaseModelService:
    """
    创建并返回适当的模型服务实例。

    参数:
    - provider: 服务提供商名称
    - url: 服务 URL
    - api_key: API 密钥

    返回:
    - BaseModelService 的子类实例
    """
    service_map: Dict[str, type] = {
        "ollama": BaseModelService,
        "glm": GLMModelService,
        "deepseek": DeepseekModelService,
    }

    service_class = service_map.get(provider.lower())
    if not service_class:
        raise ValueError(f"不支持的服务提供商: {provider}")

    return service_class(provider, url, api_key)


# 导出工厂函数
__all__ = ["create_model_service"]
