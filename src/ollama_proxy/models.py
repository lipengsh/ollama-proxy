from datetime import datetime
import random
import string


def parse_model_name(section_name):
    parts = section_name.split("-", 1)
    return f"{parts[0]}:{parts[1]}" if len(parts) > 1 else section_name


def generate_random_digest(length=64):
    return "".join(random.choices(string.hexdigits.lower(), k=length))


def list_models(model_name):
    try:
        model_data = {
            "name": parse_model_name(model_name),
            "modified_at": datetime.now().isoformat(),
            "size": 1000000000,  
            "digest": generate_random_digest(),
            "details": {
                "format": "gguf",  
                "family": "llama",  
                "families": None,
                "parameter_size": "14b",  
                "quantization_level": "Q4_0",  
            },
        }
        return {"models": [model_data]}
    except Exception as e:
        raise Exception(str(e))
