import json
from typing import Dict, Any


def generate_html_visualization(project_map: Dict[str, Any]) -> str:
    """Generate an HTML visualization of the project map."""
    routes_html = _generate_routes_html(project_map["routes"])
    models_html = _generate_models_html(project_map["models"])
    dependencies_html = _generate_dependencies_html(project_map["dependencies"])
    
    # Generate project map JSON for JavaScript visualization
    project_map_json = json.dumps(project_map)
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI Project Map</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .section {{ margin-bottom: 30px; }}
            h1, h2, h3 {{ color: #333; }}
            .tab-container {{ border: 1px solid #ddd; border-radius: 4px; overflow: hidden; }}
            .tabs {{ display: flex; background: #f1f1f1; }}
            .tab {{ padding: 10px 20px; cursor: pointer; }}
            .tab.active {{ background: #fff; border-bottom: 2px solid #007bff; }}
            .tab-content {{ display: none; padding: 20px; }}
            .tab-content.active {{ display: block; }}
            .route {{ border: 1px solid #ddd; margin-bottom: 10px; padding: 10px; border-radius: 4px; }}
            .model {{ border: 1px solid #ddd; margin-bottom: 10px; padding: 10px; border-radius: 4px; }}
            .method {{ display: inline-block; padding: 2px 6px; border-radius: 4px; font-size: 12px; font-weight: bold; margin-right: 5px; }}
            .method.get {{ background-color: #61affe; color: white; }}
            .method.post {{ background-color: #49cc90; color: white; }}
            .method.put {{ background-color: #fca130; color: white; }}
            .method.delete {{ background-color: #f93e3e; color: white; }}
            .method.patch {{ background-color: #50e3c2; color: white; }}
            #visualization {{ height: 600px; border: 1px solid #ddd; border-radius: 4px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>FastAPI Project Map</h1>
            
            <div class="tab-container">
                <div class="tabs">
                    <div class="tab active" onclick="openTab(event, 'routes-tab')">Routes</div>
                    <div class="tab" onclick="openTab(event, 'models-tab')">Models</div>
                    <div class="tab" onclick="openTab(event, 'dependencies-tab')">Dependencies</div>
                    <div class="tab" onclick="openTab(event, 'visualization-tab')">Visualization</div>
                </div>
                
                <div id="routes-tab" class="tab-content active">
                    <h2>Routes</h2>
                    {routes_html}
                </div>
                
                <div id="models-tab" class="tab-content">
                    <h2>Models</h2>
                    {models_html}
                </div>
                
                <div id="dependencies-tab" class="tab-content">
                    <h2>Dependencies</h2>
                    {dependencies_html}
                </div>
                
                <div id="visualization-tab" class="tab-content">
                    <h2>Interactive Visualization</h2>
                    <div id="visualization"></div>
                </div>
            </div>
        </div>
        
        <script>
            // Store project map data for visualization
            const projectMap = {project_map_json};
            
            function openTab(evt, tabName) {{
                const tabContents = document.getElementsByClassName("tab-content");
                for (let i = 0; i < tabContents.length; i++) {{
                    tabContents[i].classList.remove("active");
                }}
                
                const tabs = document.getElementsByClassName("tab");
                for (let i = 0; i < tabs.length; i++) {{
                    tabs[i].classList.remove("active");
                }}
                
                document.getElementById(tabName).classList.add("active");
                evt.currentTarget.classList.add("active");
                
                if (tabName === 'visualization-tab') {{
                    renderVisualization();
                }}
            }}
            
            function renderVisualization() {{
                // This is where we would integrate a visualization library like D3.js
                // For now, we'll just show a placeholder
                const container = document.getElementById('visualization');
                container.innerHTML = '<div style="padding: 20px; text-align: center;">Interactive visualization would be rendered here using D3.js or a similar library.</div>';
            }}
        </script>
    </body>
    </html>
    """

def _generate_routes_html(routes):
    """Generate HTML for routes section."""
    html = ""
    for route in routes:
        methods_html = ""
        for method in route["methods"]:
            method_lower = method.lower()
            methods_html += f'<span class="method {method_lower}">{method}</span>'
        
        html += f"""
        <div class="route">
            <h3>{methods_html} {route["path"]}</h3>
            <p><strong>Handler:</strong> {route["endpoint"]}</p>
            <p><strong>Signature:</strong> {route["signature"]}</p>
            <p><strong>Source:</strong> {route["source_file"]}:{route["source_line"]}</p>
            <p><strong>Response Model:</strong> {route["response_model"] or "None"}</p>
            <p><strong>Dependencies:</strong> {', '.join([dep["name"] for dep in route["dependencies"]]) or "None"}</p>
            <p><strong>Description:</strong> {route["docstring"]}</p>
        </div>
        """
    return html

def _generate_models_html(models):
    """Generate HTML for models section."""
    html = ""
    for model in models:
        fields_html = ""
        for field in model["fields"]:
            required = "Required" if field["required"] else f"Optional, default: {field['default']}"
            fields_html += f'<li><strong>{field["name"]}</strong>: {field["type"]} ({required})</li>'
        
        html += f"""
        <div class="model">
            <h3>{model["name"]}</h3>
            <p><strong>Module:</strong> {model["module"]}</p>
            <h4>Fields:</h4>
            <ul>
                {fields_html}
            </ul>
        </div>
        """
    return html

def _generate_dependencies_html(dependencies):
    """Generate HTML for dependencies section."""
    html = ""
    for endpoint, deps in dependencies.items():
        deps_html = "<ul>" + "".join([f"<li>{dep}</li>" for dep in deps]) + "</ul>" if deps else "None"
        html += f"""
        <div class="dependency">
            <h3>{endpoint}</h3>
            <h4>Depends on:</h4>
            {deps_html}
        </div>
        """
    return html
