import inspect
import sys
import os
from typing import Dict, List, Any, Type, Set, Optional
from pydantic import BaseModel


class ModelAnalyzer:
    def __init__(self, project_root: Optional[str] = None):
        self.discovered_models = set()
        self.project_root = project_root
        
    def extract_models_from_routes(self, routes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract Pydantic models from route parameters and responses."""
        # First, collect all potential model references
        model_references = set()
        
        # Check route parameters and response models
        for route in routes:
            # Check response model
            if route["response_model"]:
                self._add_model_from_string(route["response_model"], model_references)
            
            # Check parameters for potential models
            for param in route["parameters"]:
                self._add_model_from_string(param["annotation"], model_references)
        
        # Now analyze the actual models
        return self._analyze_models(model_references)
    
    def _add_model_from_string(self, type_str: str, model_references: Set[str]):
        """Parse a type string and add potential model references."""
        # This is a simplified version; a more robust parser would be needed
        # for complex type annotations
        for potential_model in type_str.split(','):
            # Clean up the string
            model_name = potential_model.strip().split('[')[0].split('.')[-1]
            if model_name:
                model_references.add(model_name)
    
    def _is_project_module(self, module) -> bool:
        """Check if a module is part of the project."""
        # Skip known problematic modules and packages
        if hasattr(module, "__name__"):
            module_name = module.__name__
            # Skip OpenAI modules and other common external libraries
            if any(module_name.startswith(prefix) for prefix in [
                'openai', 'numpy', 'pandas', 'tensorflow', 'torch', 'sklearn', 
                'matplotlib', 'requests', 'boto3', 'flask', 'django', 'fastapi.', 
                'pydantic.', 'starlette', 'sqlalchemy', 'pytest'
            ]):
                return False
        
        if not self.project_root:
            # If project_root is not specified, we'll consider internal modules only
            return not (hasattr(module, '__file__') and 
                      (module.__file__ is None or 
                       'site-packages' in str(module.__file__) or
                       'dist-packages' in str(module.__file__)))
        
        try:
            if not hasattr(module, '__file__') or module.__file__ is None:
                return False
                
            # Get normalized absolute paths
            module_path = os.path.normpath(os.path.abspath(module.__file__))
            project_path = os.path.normpath(os.path.abspath(self.project_root))
            
            # Simple path prefix check
            return module_path.startswith(project_path)
        except Exception:
            # If we can't determine the module's file, treat it as external
            return False
    
    def _analyze_models(self, model_references: Set[str]) -> List[Dict[str, Any]]:
        """Analyze models found in the project."""
        models = []
        
        # Create a copy of sys.modules to prevent "dictionary changed size during iteration" error
        modules_items = list(sys.modules.items())
        
        # Find all Pydantic models in loaded modules
        for module_name, module in modules_items:
            # Skip modules with underscore prefix and empty modules
            if module_name.startswith('_') or not module:
                continue
                
            # Skip external modules/dependencies earlier in the process
            if not self._is_project_module(module):
                continue
            
            try:
                # Define a safe get_members function to avoid problematic attribute access
                def safe_getmembers(module):
                    try:
                        # Only return members that can be accessed without triggering lazy loading
                        for name in dir(module):
                            try:
                                obj = getattr(module, name)
                                yield name, obj
                            except (AttributeError, ImportError, Exception):
                                continue
                    except Exception:
                        return []
                
                for name, obj in safe_getmembers(module):
                    try:
                        if (inspect.isclass(obj) and issubclass(obj, BaseModel) and 
                            obj.__module__ == module.__name__ and 
                            obj != BaseModel):
                            
                            # Skip if we've already processed this model
                            if obj in self.discovered_models:
                                continue
                                
                            self.discovered_models.add(obj)
                            
                            # Extract model fields
                            fields = []
                            for field_name, field_info in obj.__fields__.items():
                                fields.append({
                                    "name": field_name,
                                    "type": str(field_info.outer_type_),
                                    "required": field_info.required,
                                    "default": str(field_info.default) if not field_info.required else None
                                })
                            
                            models.append({
                                "name": obj.__name__,
                                "module": obj.__module__,
                                "fields": fields
                            })
                    except (TypeError, AttributeError, Exception):
                        # Skip any class that can't be properly analyzed
                        continue
            except Exception:
                # Skip any modules that can't be inspected
                continue
        
        return models
