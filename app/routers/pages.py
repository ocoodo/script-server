from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select

from app.database import DbSession
from app.models import ScriptJob

router = APIRouter()


templates = Jinja2Templates(directory='app/templates')


@router.get('/', response_class=HTMLResponse)
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


@router.get('/run-script', response_class=HTMLResponse)
def run_page(request: Request):
    return templates.TemplateResponse(
        name='run_script.html', 
        request=request
    )

