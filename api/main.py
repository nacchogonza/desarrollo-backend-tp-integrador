from fastapi import FastAPI

import api.resources.cliente.endpoint
import api.resources.location.endpoint
import api.resources.stock.endpoint
import api.resources.producto.endpoint
import api.resources.proveedor.endpoint

app = FastAPI()

prefix_base = "/api/v1"
app.include_router(api.resources.cliente.endpoint.router, prefix=f"{prefix_base}/cliente")
app.include_router(api.resources.location.endpoint.router, prefix=f"{prefix_base}/location")
app.include_router(api.resources.stock.endpoint.router, prefix=f"{prefix_base}/stock")
app.include_router(api.resources.producto.endpoint.router, prefix=f"{prefix_base}/producto")
app.include_router(api.resources.proveedor.endpoint.router, prefix=f"{prefix_base}/proveedor")