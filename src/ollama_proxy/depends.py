import asyncio
from fastapi import HTTPException
from .config import load_config_and_create_service


class ModelServiceWrapper:
    def __init__(self):
        self.model_service = None
        self.model_name = None
        self._init_lock = asyncio.Lock()
        self._initialized = asyncio.Event()

    async def initialize(self, config, model_name):
        async with self._init_lock:
            if not self._initialized.is_set():
                (
                    self.model_service,
                    self.model_name,
                ) = await load_config_and_create_service(config, model_name)
                self._initialized.set()

    async def get_model_service(self):
        await self._initialized.wait()
        if self.model_service is None:
            raise HTTPException(status_code=500, detail="Model service not initialized")
        return self.model_service

    async def get_model_name(self):
        await self._initialized.wait()
        if self.model_name is None:
            raise HTTPException(status_code=500, detail="Model name not initialized")
        return self.model_name


model_service_wrapper = ModelServiceWrapper()


async def initialize_model_service(config, model_name):
    await model_service_wrapper.initialize(config, model_name)


async def get_model_service():
    return await model_service_wrapper.get_model_service()


async def get_model_name():
    return await model_service_wrapper.get_model_name()


async def get_model_service_status():
    await model_service_wrapper._initialized.wait()
    return {
        "initialized": model_service_wrapper.model_service is not None,
        "model_name": model_service_wrapper.model_name,
        "model_service_type": type(model_service_wrapper.model_service).__name__
        if model_service_wrapper.model_service
        else None,
    }
