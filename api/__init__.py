if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000)) # 8000 es el valor por defecto si no se encuentra la variable
    uvicorn.run("main:app", host="0.0.0.0", port=port)