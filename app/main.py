from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.configs import settings
from api.v1.api import router

app = FastAPI(title="Loja-Lu API",
              version="1.0"
)
app.include_router(router, prefix=settings.API_V1_STR)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, log_level="info" ,reload=True) 