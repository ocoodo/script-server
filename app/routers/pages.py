from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select

from app.database import DbSession
from app.models import Script

router = APIRouter()


templates = Jinja2Templates(directory='app/templates')


@router.get('/', response_class=HTMLResponse)
async def index_page(
    request: Request,
    db_session: DbSession
):
    query = await db_session.execute(
        select(Script)
    )
    scripts = query.scalars().all()
    return templates.TemplateResponse(
        name='index.html',
        request=request,
        context={
            "scripts": scripts
        }
    )


@router.get('/scripts/{script_name}')
async def script_page(
    script_name: str,
    request: Request,
    db_session: DbSession
):
    response = await db_session.execute(
        select(Script)
        .where(Script.name == script_name)
    )
    script = response.scalar_one_or_none()
    return templates.TemplateResponse(
        name='script-info.html',
        request=request,
        context={
            "script": script
        }
    )


@router.get('/run-script', response_class=HTMLResponse)
def run_page(request: Request):
    return templates.TemplateResponse(
        name='script-run.html', 
        request=request
    )

