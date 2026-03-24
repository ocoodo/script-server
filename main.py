from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from app.routers.pages import router as page_router
from app.routers.api import router as api_router
from app.database import init_db
from app.engine import RunnerEngine


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.runner = RunnerEngine()
    app.state.runner.scheduler.start()
    await init_db()
    yield
    app.state.runner.scheduler.shutdown() 


app = FastAPI(lifespan=lifespan)

app.mount('/styles', StaticFiles(directory='app/static'), name="styles")
app.include_router(page_router)
app.include_router(api_router)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
