from fastapi import FastAPI

import api.resources.cliente.endpoint
import api.resources.location.endpoint
import api.resources.stock.endpoint

app = FastAPI()

prefix_base = "/api/v1"
app.include_router(api.resources.cliente.endpoint.router, prefix=f"{prefix_base}/cliente")
app.include_router(api.resources.location.endpoint.router, prefix=f"{prefix_base}/location")
app.include_router(api.resources.stock.endpoint.router, prefix=f"{prefix_base}/stock")