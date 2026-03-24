from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

from engine import RunnerEngine


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.runner = RunnerEngine()
    app.state.runner.scheduler.start()
    yield
    app.state.runner.scheduler.shutdown() 


app = FastAPI(lifespan=lifespan)


app.mount('/styles', StaticFiles(directory='frontend/styles'), name="styles")
templates = Jinja2Templates(directory='frontend')


@app.get('/', response_class=HTMLResponse)
def run_page(request: Request):
    return templates.TemplateResponse(
        name='run_script.html',
        request=request
    )


@app.post('/run-script')
def run_script( 
    request: Request,
    script_name: str = Form(...), 
    interval: int = Form(...),
):
    request.app.state.runner.add_task(script_name, interval)
    return {"script_name": script_name}
