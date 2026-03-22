from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec

from apscheduler.schedulers.background import BackgroundScheduler


class RunnerEngine:
    def __init__(self, scripts_path: str = './scripts'):
        self.scheduler = BackgroundScheduler(timezone='UTC')
        self.scripts_path = Path(scripts_path).resolve()
        if not self.scripts_path.is_dir():
            self.scripts_path.mkdir(exist_ok=True, parents=True)
    
    def _load_module(self, location: Path):
        if not location.is_file():
            raise FileNotFoundError(f'module file in {location} not found')
        
        spec = spec_from_file_location('module', location)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    def _load_func(self, module):
        func = getattr(module, 'run', None)
        
        if func and callable(func):
            return func
        raise AttributeError('function run() does not exists')
    
    def run_script(self, name: str):
        location = self.scripts_path / f"{name}.py"
        module = self._load_module(location)
        func = self._load_func(module)
        return func()
    
    def add_task(self, script_name: str, interval_seconds: int):
        self.scheduler.add_job(
            id=script_name,
            func=self.run_script,
            trigger='interval',
            seconds=interval_seconds,
            args=(script_name,),
            replace_existing=True
        )
    

runner = RunnerEngine()
