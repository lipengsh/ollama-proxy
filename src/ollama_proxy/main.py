import os
import click
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from .define import ChatRequest
from .config import init_model_service
from .models import list_models
from .config import check_model_name

# Use environment variables or default values to set the configuration file path
DEFAULT_CONFIG_PATH = os.environ.get("OLLAMA_PROXY_CONFIG", "keys.toml")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.config_path = os.environ.get("CONFIG_PATH", DEFAULT_CONFIG_PATH)
    app.state.model_name = os.environ.get("MODEL_NAME", "default_model")

    yield
    # Here you can clean up resources, such as closing database connections


app = FastAPI(lifespan=lifespan)


@app.post("/api/chat")
async def chat(chat_request: ChatRequest, request: Request):
    if not hasattr(request.app.state, "model_name") and hasattr(
        request.app.state, "config_path"
    ):
        print("app.state is missing model_name or config_path attribute")
        return JSONResponse(
            content={"error": "app.state is missing model_name or config_path attribute"}
        )

    model_name = request.app.state.model_name

    print(f"api model_name: {model_name}")
    # Check if model_name is in the list of config file
    if not check_model_name(model_name, request.app.state.config_path):
        print(f"Model name {model_name} is not available.")
        return JSONResponse(
            content={"error": f"Model name {model_name} is not available."}
        )


    config_path = request.app.state.config_path
    model_service = init_model_service(config_path, model_name)

    try:
        stream_generator = model_service.chat(chat_request)
        if chat_request.stream:
            return StreamingResponse(stream_generator, media_type="text/event-stream")
        else:
            response_content = ""
            async for chunk in stream_generator:
                response_content += chunk
            return JSONResponse(content={"response": response_content})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")


@app.get("/api/tags")
async def get_models(request: Request):
    try:
        model_name = request.app.state.model_name
        result = list_models(model_name)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ping")
async def ping():
    """
    A simple ping-pong test endpoint
    """
    return JSONResponse(content={"message": "pong"})




@click.command()
@click.argument("model_name")
@click.option("--config", default=DEFAULT_CONFIG_PATH, help="Path to the Toml configuration file")
@click.option("--host", default="localhost", help="Server host address")
@click.option("--port", default=11434, type=int, help="Server port")
@click.option("--reload", is_flag=True, help="Enable hot reloading")
def run(model_name, config, host, port, reload):
    """Run a specific model"""

    os.environ["CONFIG_PATH"] = config
    os.environ["MODEL_NAME"] = model_name

    # Check if model_name is in the list of config file
    if not check_model_name(model_name, config):
        print(f"Model name {model_name} is not in the list of config file {config}, please check the model name and try again.")
        return


    uvicorn.run(
        "ollama_proxy.main:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    run()
