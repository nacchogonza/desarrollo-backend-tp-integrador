from fastapi import FastAPI

import api.cliente.endpoint
import api.core
import api.core.endpoint
""" import api.deposito.endpoint """

app = FastAPI()

prefix_base = "/api/v1"
app.include_router(api.cliente.endpoint.router, prefix=f"{prefix_base}/cliente")
app.include_router(api.core.endpoint.router, prefix=f"{prefix_base}/core")