import importlib
import pkgutil
from typing import List
from app.modules.base import BaseModule
import app.modules as modules_package

class ModuleLoader:
    def __init__(self):
        self.loaded_modules: List[BaseModule] = []
    
    def discover_and_load_modules(self):
        """Dynamically discover and load all modules"""
        for _, name, _ in pkgutil.iter_modules(modules_package.__path__):
            try:
                # Import the module package
                module_package = importlib.import_module(f"app.modules.{name}")
                
                # Import the actual module class
                if hasattr(module_package, 'module'):
                    module_class = getattr(module_package.module, f"{name.title()}Module")
                    module_instance = module_class()
                    self.loaded_modules.append(module_instance)
            except Exception as e:
                print(f"Failed to load module {name}: {str(e)}")
    
    def get_all_routers(self):
        """Return all module routers"""
        return [module.router for module in self.loaded_modules] 