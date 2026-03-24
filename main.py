from contextlib import asynccontextmanager

from sqlalchemy import select
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

from database import init_db, DbSession
from models import ScriptJob
from engine import RunnerEngine


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.runner = RunnerEngine()
    app.state.runner.scheduler.start()
    await init_db()
    yield
    app.state.runner.scheduler.shutdown() 


app = FastAPI(lifespan=lifespan)


app.mount('/styles', StaticFiles(directory='frontend/styles'), name="styles")
templates = Jinja2Templates(directory='frontend')


@app.get('/', response_class=HTMLResponse)
async def index_page(
    request: Request,
    db_session: DbSession
):
    query = await db_session.execute(
        select(ScriptJob)
    )
    scripts = query.scalars().all()
    return templates.TemplateResponse(
        name='index.html', 
        request=request,
        context={
            "scripts": scripts
        }
    )


@app.get('/run-script', response_class=HTMLResponse)
def run_page(request: Request):
    return templates.TemplateResponse(
        name='run_script.html', 
        request=request
    )


@app.post('/run-script', response_class=RedirectResponse)
async def run_handler( 
    request: Request,
    db_session: DbSession,
    script_name: str = Form(...),
    interval: int = Form(...)
):
    request.app.state.runner.add_task(script_name, interval)
    new_script = ScriptJob(
        name=script_name,
        interval=interval
    )
    db_session.add(new_script)
    await db_session.commit()
    return RedirectResponse(
        url='/', 
        status_code=303
    )


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
