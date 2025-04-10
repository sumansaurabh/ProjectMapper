import inspect
from typing import Any, Dict, List, Optional, Set, Type, Callable
import fastapi
from fastapi import APIRouter, Depends, FastAPI
from pydantic import BaseModel

from .scanner import RouteScanner
from .models import ModelAnalyzer
from .visualization import generate_html_visualization
from .dependencies import DependencyAnalyzer


class ProjectMapper:
    def __init__(self, app: FastAPI):
        self.app = app
        self.route_scanner = RouteScanner(app)
        self.model_analyzer = ModelAnalyzer()
        self.dependency_analyzer = DependencyAnalyzer()
        self._initialized = False
        
    def initialize(self):
        """Initialize the project mapper, analyzing the FastAPI application structure."""
        if self._initialized:
            return
            
        # Add a route to the FastAPI app to view the project map
        @self.app.get("/_project_map", include_in_schema=False)
        async def view_project_map():
            return self.generate_map()
        
        # Add a route to view the project visualization
        @self.app.get("/_project_visualization", include_in_schema=False)
        async def view_project_visualization():
            from fastapi.responses import HTMLResponse
            return HTMLResponse(content=self.generate_visualization(), status_code=200)
        
        self._initialized = True
        
    def generate_map(self) -> Dict[str, Any]:
        """Generate a structured map of the project."""
        routes = self.route_scanner.scan_routes()
        models = self.model_analyzer.extract_models_from_routes(routes)
        dependencies = self.dependency_analyzer.analyze_dependencies(routes)
        
        return {
            "routes": routes,
            "models": models,
            "dependencies": dependencies
        }
    
    def generate_visualization(self) -> str:
        """Generate HTML visualization of the project map."""
        project_map = self.generate_map()
        return generate_html_visualization(project_map)


def map_project(app: FastAPI) -> ProjectMapper:
    """
    Attach ProjectMapper to a FastAPI application.
    
    Usage:
        app = FastAPI()
        mapper = map_project(app)
    """
    mapper = ProjectMapper(app)
    mapper.initialize()
    return mapper
