# ProjectMapper for FastAPI

ProjectMapper is a Python library that helps you visualize and understand the structure of your FastAPI application. It analyzes routes, dependencies, models, and their relationships to provide a comprehensive view of your project architecture.

## Installation

```bash
pip install git+https://github.com/sumansaurabh/ProjectMapper.git
```

## Usage

Simply import the library at the start of your FastAPI application:

```python
from fastapi import FastAPI
from projectmapper import map_project

app = FastAPI()

# Initialize the project mapper
mapper = map_project(app)

# Your FastAPI routes and code below
@app.get("/")
def read_root():
    return {"Hello": "World"}
```

## Features

- Automatically maps all routes in your FastAPI application
- Identifies Pydantic models used in your application
- Analyzes dependencies between components
- Provides interactive visualization via web interface
- Available at `/_project_map` and `/_project_visualization` endpoints

## Example

After initializing ProjectMapper with your FastAPI application, you can:

1. Access `http://localhost:8000/_project_map` to see a JSON representation of your project structure
2. Access `http://localhost:8000/_project_visualization` to see a visual representation of your project

## License

MIT
