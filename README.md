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
- Deep data flow analysis between components
- Database operation detection and visualization
- Complete execution flow tracking

## Endpoints

ProjectMapper adds these endpoints to your FastAPI application:

| Endpoint | Description |
|----------|-------------|
| `/_project/json` | JSON representation of your project structure |
| `/_project/html` | Visual representation of your project structure |
| `/_project/dataflow/json` | JSON representation of your project's data flow |
| `/_project/dataflow/html` | Interactive visualization of your project's data flow |

You can customize the base path by passing it to the `map_project` function:

```python
mapper = map_project(app, base_path="/api/internal/project")
```

## Data Flow Analysis

The data flow analysis provides:

- Function call chains for each route
- Data references and transformations
- Database operation detection
- Complete execution flow visualization

This helps you understand:

- How data flows from requests to responses
- Which functions are called during request processing
- What database operations are triggered
- How dependencies interact with each other

## License

MIT
