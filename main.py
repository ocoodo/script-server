from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
import uvicorn

from engine import RunnerEngine


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.runner = RunnerEngine()
    app.state.runner.scheduler.start()
    yield
    app.state.runner.scheduler.shutdown()
    


app = FastAPI(lifespan=lifespan)


@app.post('/scripts/run')
def run_script(script_name: str, interval: int, request: Request):
    request.app.state.runner.add_task(script_name, interval)
    return script_name


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0')
