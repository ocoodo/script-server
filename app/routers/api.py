from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse

from app.models import ScriptJob
from app.database import DbSession

router = APIRouter()


@router.post('/run-script', response_class=RedirectResponse)
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