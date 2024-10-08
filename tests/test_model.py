from src.ollama_proxy.config import check_model_name



def test_check_model_name():

    sample_config = "keys.toml"

    result = check_model_name('deepseek-coder-v2', sample_config)
    print(f'result:{result}')

    # 测试存在的模型名称
    assert check_model_name('glm-4-plus', sample_config)
    assert check_model_name('deepseek-chat', sample_config)
    assert not check_model_name('deepseek-chat-2', sample_config)
    assert not check_model_name('deepseek-coder-v2', sample_config)
    

