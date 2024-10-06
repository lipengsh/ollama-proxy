from typing import Dict
from .base import BaseModelService
from .deepseek import DeepseekModelService
from .glm import GLMModelService


def create_model_service(provider: str, url: str, api_key: str) -> BaseModelService:
    """
    Create and return an appropriate model service instance.

    Parameters:
    - provider: Name of the service provider
    - url: Service URL
    - api_key: API key

    Returns:
    - An instance of a BaseModelService subclass
    """
    service_map: Dict[str, type] = {
        "zhipu": GLMModelService,
        "deepseek": DeepseekModelService,
    }

    service_class = service_map.get(provider.lower())
    if not service_class:
        raise ValueError(f"Unsupported service provider: {provider}")

    return service_class(provider, url, api_key)


__all__ = ["create_model_service"]
