import toml
from .services import create_model_service


def init_model_service(config_file: str, model_name: str):
    """
    Initialize and return a model service based on the configuration file and model name.
    
    Args:
        config_file (str): Path to the configuration file.
        model_name (str): Name of the model to initialize.
    
    Returns:
        A model service instance.
    
    Raises:
        ValueError: If the model is not found in the config or if there's an error in initialization.
    """
    try:
        # 读取配置文件
        models_list = toml.load(open(config_file, "r"))

        if model_name not in models_list:
            raise ValueError(f"Model {model_name} not found in the configuration file")

        model_config = models_list[model_name]
        provider = model_config.get("provider")
        service_url = model_config.get("url")
        api_key = model_config.get("api_key")

        model_service = create_model_service(provider, service_url, api_key)

        return model_service
    except Exception as e:
        raise ValueError(f"Error loading configuration or creating model service: {str(e)}")


def check_model_name(model_name, config):
    """
    Check if the given model name exists in the configuration file.

    Parameters:
    model_name (str): The model name to check
    config (str): Path to the configuration file

    Raises:
    ValueError: If the model name is not found in the configuration file
    """

    with open(config, "r") as f:
        config = toml.load(f)


    if model_name not in config:
        return False
    
    return True