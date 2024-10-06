# ollama-proxy

**ollama-proxy** is a service that adheres to the Ollama external interface protocol. It enables connections to various large model services, such as **glm-4-plus** and **deepseek-coder-v2**, through the Ollama interface protocol. The primary goal of this project is to facilitate integration with **zed.dev**, allowing it to utilize additional large model services beyond the official configuration.

## Installation

To install **ollama-proxy**, a command-line tool, you can use the following command:

```bash
pip install ollama-proxy
```

## Command Line Usage

The `ollama-proxy` command-line interface (CLI) allows you to run the proxy server with specific configurations. Below are the details on how to use the CLI, including available options and their descriptions.

## Command Structure

To run the `ollama-proxy`, use the following command structure:

```bash
ollama-proxy <model_name> --config <config_path> --host <host> --port <port>
```

### Arguments

- **`model_name`**: 
  - **Type**: String
  - **Description**: A required argument that specifies the name of the model you want to run.

- **`config`**: 
  - **Type**: String
  - **Default**: `keys.toml`
  - **Description**: The path to the TOML configuration file.

### Options

- **`--host`**: 
  - **Type**: String
  - **Default**: `127.0.0.1`
  - **Description**: The host address for the server. For **zed.dev**, only `localhost` is allowed.

- **`--port`**: 
  - **Type**: Integer
  - **Default**: `11434`
  - **Description**: For **zed.dev**, the port number must be `11434`.

## Example Usage

To start the `ollama-proxy` with a specific model and configuration, you can run:

```bash
ollama-proxy glm-4-plus --config path/to/config.toml --host localhost --port 11434 --reload
```

In this example:
- `glm-4-plus` is the name of the model you want to run.
- The configuration file is located at `path/to/config.toml`.
- The server will listen on `localhost` at port `11434`.
- Hot reloading is enabled.

## Notes

- Ensure that the specified configuration file exists and is correctly formatted in TOML.
- The server will print logs to the console, indicating its status and any errors that may occur.

## Configuration TOML File

To configure **ollama-proxy**, create a configuration file in TOML format. This file allows you to specify various settings for the proxy.

### Example Configuration (config.toml)

```toml
[glm-4-plus]
provider = "zhipu"
url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
api_key = "your_api_key_here"

[deepseek-coder-v2]
provider = "deepseek"
url = "https://api.deepseek.com/chat/completions"
api_key = "your_api_key_here"
```

- The section name corresponds to the model name, such as `glm-4-plus` or `deepseek-coder-v2`.
- The `provider` specifies the name of the large model service provider.
- The `url` is the endpoint of the large model service provider.
- The `api_key` is the API key for the large model service provider.

When you run `ollama-proxy`, it will load the configuration file. For example, running `ollama-proxy glm-4-plus` will use `glm-4-plus` as the running model name. If `glm-4-plus` is not specified in the configuration file, an error will be raised.

## TODO

- [ ] Support more large model providers
- [ ] Add xinference as a local model provider
- [ ] Support cursor