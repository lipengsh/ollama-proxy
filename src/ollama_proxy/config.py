import toml
from .services import create_model_service


def init_model_service(config_file: str, model_name: str):
    try:
        # 读取配置文件
        models_list = toml.load(open(config_file, "r"))

        if model_name not in models_list:
            raise ValueError(f"模型 {model_name} 在配置文件中未找到")

        model_config = models_list[model_name]
        provider = model_config.get("provider")
        service_url = model_config.get("url")
        api_key = model_config.get("api_key")

        model_service = create_model_service(provider, service_url, api_key)

        return model_service
    except Exception as e:
        raise ValueError(f"加载配置或创建模型服务时出错: {str(e)}")
