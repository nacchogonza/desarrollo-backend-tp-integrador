from fastapi import FastAPI

import api.resources.cliente.endpoint
import api.core.endpoint

app = FastAPI()

prefix_base = "/api/v1"
app.include_router(api.resources.cliente.endpoint.router, prefix=f"{prefix_base}/cliente")
app.include_router(api.core.endpoint.router, prefix=f"{prefix_base}/core")