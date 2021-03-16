from fastapi import FastAPI

from interfaces.frontend_rpc.views import router

app = FastAPI()

app.include_router(router)
