import inspect
from typing import Dict, List, Any, Callable, Set
from fastapi import FastAPI, APIRouter, Depends
from fastapi.routing import APIRoute


class RouteScanner:
    def __init__(self, app: FastAPI):
        self.app = app
        
    def scan_routes(self) -> List[Dict[str, Any]]:
        """Scan all routes in the FastAPI application."""
        routes = []
        self._process_routes(self.app.routes, routes)
        return routes
    
    def _process_routes(self, app_routes: List[Any], results: List[Dict[str, Any]], prefix: str = ""):
        """Process routes and nested routers."""
        for route in app_routes:
            if isinstance(route, APIRoute):
                route_info = self._extract_route_info(route, prefix)
                results.append(route_info)
            
            # Handle mounted APIRouters
            elif hasattr(route, "routes"):
                router_prefix = prefix + (route.prefix if hasattr(route, "prefix") else "")
                self._process_routes(route.routes, results, router_prefix)
    
    def _extract_route_info(self, route: APIRoute, prefix: str = "") -> Dict[str, Any]:
        """Extract information from a single route."""
        path = prefix + route.path
        endpoint_func = route.endpoint
        
        # Get dependencies
        dependencies = []
        if hasattr(route, "dependencies"):
            dependencies = self._extract_dependencies(route.dependencies)
        
        # Get endpoint signature and docstring
        signature = str(inspect.signature(endpoint_func))
        docstring = inspect.getdoc(endpoint_func) or ""
        
        # Get source file and line number
        try:
            source_file = inspect.getfile(endpoint_func)
            source_line = inspect.getsourcelines(endpoint_func)[1]
        except (TypeError, OSError):
            source_file = "Unknown"
            source_line = 0
        
        # Extract function parameters that might be models
        parameters = []
        for param_name, param in inspect.signature(endpoint_func).parameters.items():
            if param_name != "self" and param_name != "cls":
                parameters.append({
                    "name": param_name,
                    "annotation": str(param.annotation),
                    "default": str(param.default) if param.default is not inspect.Parameter.empty else None
                })
        
        return {
            "path": path,
            "methods": route.methods,
            "name": route.name,
            "endpoint": endpoint_func.__name__,
            "signature": signature,
            "docstring": docstring,
            "parameters": parameters,
            "dependencies": dependencies,
            "source_file": source_file,
            "source_line": source_line,
            "response_model": str(route.response_model) if route.response_model else None,
        }
    
    def _extract_dependencies(self, dependencies: List[Any]) -> List[Dict[str, Any]]:
        """Extract information about dependencies."""
        results = []
        for dep in dependencies:
            if hasattr(dep, "dependency"):
                dependency_callable = dep.dependency
                results.append({
                    "name": dependency_callable.__name__ if hasattr(dependency_callable, "__name__") else str(dependency_callable),
                    "callable": str(dependency_callable)
                })
        return results
