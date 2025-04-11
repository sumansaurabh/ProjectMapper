import json
from typing import Dict, Any, List


class SetEncoder(json.JSONEncoder):
    """Custom JSON encoder that converts sets to lists."""
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def generate_html_visualization(project_map: Dict[str, Any]) -> str:
    """Generate an HTML visualization of the project map."""
    routes_html = _generate_routes_html(project_map["routes"])
    models_html = _generate_models_html(project_map["models"])
    dependencies_html = _generate_dependencies_html(project_map["dependencies"])
    
    # Generate project map JSON for JavaScript visualization
    project_map_json = json.dumps(project_map, cls=SetEncoder)
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI Project Map</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://d3js.org/d3.v7.min.js"></script>
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
            #visualization {{ height: 700px; border: 1px solid #ddd; border-radius: 4px; overflow: hidden; position: relative; }}
            #graph-container {{ width: 100%; height: 100%; }}
            
            /* D3 Visualization Styles */
            .node {{ cursor: pointer; }}
            .node text {{ font-size: 12px; }}
            .node circle {{ stroke-width: 2px; }}
            .node-route circle {{ fill: #61affe; }}
            .node-model circle {{ fill: #fca130; }}
            .node-dependency circle {{ fill: #49cc90; }}
            .link {{ stroke: #999; stroke-opacity: 0.6; stroke-width: 1.5px; }}
            
            .tooltip {{ 
                position: absolute; 
                padding: 10px; 
                background: white; 
                border-radius: 4px; 
                border: 1px solid #ddd;
                pointer-events: none;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                max-width: 300px;
                z-index: 1000;
            }}
            
            .legend {{ 
                position: absolute; 
                top: 10px; 
                right: 10px; 
                background: white; 
                padding: 10px; 
                border: 1px solid #ddd; 
                border-radius: 4px; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            
            .legend-item {{ 
                display: flex; 
                align-items: center; 
                margin-bottom: 5px; 
            }}
            
            .legend-color {{ 
                width: 15px; 
                height: 15px; 
                margin-right: 8px; 
                border-radius: 50%; 
                display: inline-block; 
            }}
            
            .controls {{
                position: absolute;
                bottom: 10px;
                left: 10px;
                background: white;
                padding: 5px 10px;
                border-radius: 4px;
                border: 1px solid #ddd;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            
            button {{
                border: none;
                background: #f1f1f1;
                padding: 5px 10px;
                border-radius: 4px;
                margin: 0 5px;
                cursor: pointer;
            }}
            
            button:hover {{
                background: #ddd;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>FastAPI Project Map</h1>
            
            <div class="tab-container">
                <div class="tabs">
                    <div class="tab active" onclick="openTab(event, 'visualization-tab')">Visualization</div>
                    <div class="tab" onclick="openTab(event, 'routes-tab')">Routes</div>
                    <div class="tab" onclick="openTab(event, 'models-tab')">Models</div>
                    <div class="tab" onclick="openTab(event, 'dependencies-tab')">Dependencies</div>
                </div>
                
                <div id="visualization-tab" class="tab-content active">
                    <h2>Interactive Visualization</h2>
                    <div id="visualization">
                        <div id="graph-container"></div>
                        <div class="legend">
                            <h3>Legend</h3>
                            <div class="legend-item">
                                <span class="legend-color" style="background-color: #61affe;"></span>
                                <span>Routes</span>
                            </div>
                            <div class="legend-item">
                                <span class="legend-color" style="background-color: #fca130;"></span>
                                <span>Models</span>
                            </div>
                            <div class="legend-item">
                                <span class="legend-color" style="background-color: #49cc90;"></span>
                                <span>Dependencies</span>
                            </div>
                        </div>
                        <div class="controls">
                            <button id="zoom-in">+ Zoom In</button>
                            <button id="zoom-out">- Zoom Out</button>
                            <button id="reset">Reset</button>
                        </div>
                    </div>
                </div>
                
                <div id="routes-tab" class="tab-content">
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
            
            // Transform the project map into a format suitable for D3
            function transformProjectData(projectMap) {{
                const nodes = [];
                const links = [];
                const nodeMap = new Map();
                let nodeId = 0;
                
                // Add routes as nodes
                projectMap.routes.forEach(route => {{
                    const id = nodeId++;
                    const methodString = Array.isArray(route.methods) ? 
                        route.methods.join(', ') : route.methods;
                        
                    const node = {{
                        id: id,
                        name: `${{methodString}} ${{route.path}}`,
                        type: 'route',
                        details: route,
                        endpoint: route.endpoint
                    }};
                    
                    nodes.push(node);
                    nodeMap.set(route.endpoint, id);
                }});
                
                // Add models as nodes
                projectMap.models.forEach(model => {{
                    const id = nodeId++;
                    const node = {{
                        id: id,
                        name: model.name,
                        type: 'model',
                        details: model
                    }};
                    
                    nodes.push(node);
                    nodeMap.set(model.name, id);
                }});
                
                // Add dependencies as nodes if they aren't routes
                const allDeps = new Set();
                Object.values(projectMap.dependencies).forEach(deps => {{
                    deps.forEach(dep => allDeps.add(dep));
                }});
                
                allDeps.forEach(dep => {{
                    if (!nodeMap.has(dep)) {{
                        const id = nodeId++;
                        const node = {{
                            id: id,
                            name: dep,
                            type: 'dependency',
                            details: {{ name: dep }}
                        }};
                        
                        nodes.push(node);
                        nodeMap.set(dep, id);
                    }}
                }});
                
                // Create links from routes to models
                projectMap.routes.forEach(route => {{
                    // Link to response model if any
                    if (route.response_model) {{
                        const modelName = route.response_model.split('[')[0].split('.')[-1];
                        if (nodeMap.has(modelName)) {{
                            links.push({{
                                source: nodeMap.get(route.endpoint),
                                target: nodeMap.get(modelName),
                                type: 'returns'
                            }});
                        }}
                    }}
                    
                    // Link to parameter models
                    route.parameters.forEach(param => {{
                        const paramType = param.annotation.split('[')[0].split('.')[-1];
                        if (nodeMap.has(paramType)) {{
                            links.push({{
                                source: nodeMap.get(paramType),
                                target: nodeMap.get(route.endpoint),
                                type: 'parameter'
                            }});
                        }}
                    }});
                    
                    // Link to dependencies
                    route.dependencies.forEach(dep => {{
                        const depName = dep.name;
                        if (nodeMap.has(depName)) {{
                            links.push({{
                                source: nodeMap.get(route.endpoint),
                                target: nodeMap.get(depName),
                                type: 'depends_on'
                            }});
                        }}
                    }});
                }});
                
                // Create links from route endpoint to dependencies
                Object.entries(projectMap.dependencies).forEach(([endpoint, deps]) => {{
                    if (nodeMap.has(endpoint)) {{
                        deps.forEach(dep => {{
                            if (nodeMap.has(dep)) {{
                                links.push({{
                                    source: nodeMap.get(endpoint),
                                    target: nodeMap.get(dep),
                                    type: 'depends_on'
                                }});
                            }}
                        }});
                    }}
                }});
                
                return {{ nodes, links }};
            }}
            
            function renderVisualization() {{
                const container = document.getElementById('graph-container');
                
                // Clear any previous visualization
                container.innerHTML = '';
                
                // Get container dimensions
                const width = container.clientWidth;
                const height = container.clientHeight;
                
                // Transform project data for D3
                const graphData = transformProjectData(projectMap);
                
                // Create SVG
                const svg = d3.select('#graph-container')
                    .append('svg')
                    .attr('width', width)
                    .attr('height', height)
                    .attr('viewBox', [0, 0, width, height])
                    .call(d3.zoom().on('zoom', (event) => {{
                        g.attr('transform', event.transform);
                    }}));
                
                const g = svg.append('g');
                
                // Create tooltip
                const tooltip = d3.select('#visualization')
                    .append('div')
                    .attr('class', 'tooltip')
                    .style('opacity', 0);
                
                // Create links
                const link = g.append('g')
                    .selectAll('line')
                    .data(graphData.links)
                    .enter()
                    .append('line')
                    .attr('class', 'link')
                    .attr('stroke-dasharray', d => d.type === 'parameter' ? '5,5' : 'none');
                
                // Define different node types
                const node = g.append('g')
                    .selectAll('.node')
                    .data(graphData.nodes)
                    .enter()
                    .append('g')
                    .attr('class', d => `node node-${{d.type}}`)
                    .call(d3.drag()
                        .on('start', dragStarted)
                        .on('drag', dragged)
                        .on('end', dragEnded));
                
                // Add circles to nodes
                node.append('circle')
                    .attr('r', d => d.type === 'route' ? 10 : (d.type === 'model' ? 8 : 6))
                    .attr('stroke', '#fff');
                
                // Add text labels to nodes
                node.append('text')
                    .attr('dy', 20)
                    .attr('text-anchor', 'middle')
                    .text(d => d.name)
                    .each(function(d) {{
                        const self = d3.select(this);
                        const textLength = self.node().getComputedTextLength();
                        
                        // If text is too long, truncate it
                        if (textLength > 100) {{
                            self.text(d.name.substring(0, 20) + '...');
                        }}
                    }});
                
                // Add hover behavior
                node.on('mouseover', function(event, d) {{
                    // Highlight connected links and nodes
                    link.style('stroke-opacity', l => {{
                        if (l.source.id === d.id || l.target.id === d.id) {{
                            return 1;
                        }} else {{
                            return 0.2;
                        }}
                    }})
                    .style('stroke-width', l => {{
                        if (l.source.id === d.id || l.target.id === d.id) {{
                            return 3;
                        }} else {{
                            return 1.5;
                        }}
                    }});
                    
                    node.style('opacity', n => {{
                        return isConnected(d, n) ? 1 : 0.2;
                    }});
                    
                    // Show tooltip with details
                    tooltip.transition()
                        .duration(200)
                        .style('opacity', 0.9);
                    
                    let tooltipContent = `<strong>${{d.name}}</strong><br/>Type: ${{d.type}}<br/>`;
                    
                    if (d.type === 'route') {{
                        tooltipContent += `
                            Path: ${{d.details.path}}<br/>
                            Methods: ${{Array.isArray(d.details.methods) ? d.details.methods.join(', ') : d.details.methods}}<br/>
                            Handler: ${{d.details.endpoint}}<br/>
                            ${{d.details.response_model ? `Response Model: ${{d.details.response_model}}<br/>` : ''}}
                        `;
                    }} else if (d.type === 'model') {{
                        tooltipContent += `
                            Module: ${{d.details.module}}<br/>
                            Fields: ${{d.details.fields.length}}<br/>
                        `;
                    }}
                    
                    tooltip.html(tooltipContent)
                        .style('left', (event.pageX + 10) + 'px')
                        .style('top', (event.pageY - 28) + 'px');
                }})
                .on('mouseout', function() {{
                    // Restore original appearance
                    link.style('stroke-opacity', 0.6).style('stroke-width', 1.5);
                    node.style('opacity', 1);
                    
                    // Hide tooltip
                    tooltip.transition()
                        .duration(500)
                        .style('opacity', 0);
                }});
                
                // Check if two nodes are connected
                function isConnected(a, b) {{
                    if (a.id === b.id) return true;
                    
                    return graphData.links.some(l => {{
                        return (l.source.id === a.id && l.target.id === b.id) ||
                               (l.source.id === b.id && l.target.id === a.id);
                    }});
                }}
                
                // Initialize force simulation
                const simulation = d3.forceSimulation(graphData.nodes)
                    .force('link', d3.forceLink(graphData.links).id(d => d.id).distance(100))
                    .force('charge', d3.forceManyBody().strength(-300))
                    .force('center', d3.forceCenter(width / 2, height / 2))
                    .force('collide', d3.forceCollide().radius(40))
                    .on('tick', ticked);
                
                // Update positions on each tick
                function ticked() {{
                    link
                        .attr('x1', d => d.source.x)
                        .attr('y1', d => d.source.y)
                        .attr('x2', d => d.target.x)
                        .attr('y2', d => d.target.y);
                    
                    node.attr('transform', d => `translate(${{d.x}},${{d.y}})`);
                }}
                
                // Drag functions
                function dragStarted(event, d) {{
                    if (!event.active) simulation.alphaTarget(0.3).restart();
                    d.fx = d.x;
                    d.fy = d.y;
                }}
                
                function dragged(event, d) {{
                    d.fx = event.x;
                    d.fy = event.y;
                }}
                
                function dragEnded(event, d) {{
                    if (!event.active) simulation.alphaTarget(0);
                    d.fx = null;
                    d.fy = null;
                }}
                
                // Zoom controls
                document.getElementById('zoom-in').addEventListener('click', function() {{
                    const currentTransform = d3.zoomTransform(svg.node());
                    svg.transition().duration(500).call(
                        d3.zoom().on('zoom', event => g.attr('transform', event.transform))
                            .transform, 
                        d3.zoomIdentity.translate(currentTransform.x, currentTransform.y).scale(currentTransform.k * 1.5)
                    );
                }});
                
                document.getElementById('zoom-out').addEventListener('click', function() {{
                    const currentTransform = d3.zoomTransform(svg.node());
                    svg.transition().duration(500).call(
                        d3.zoom().on('zoom', event => g.attr('transform', event.transform))
                            .transform, 
                        d3.zoomIdentity.translate(currentTransform.x, currentTransform.y).scale(currentTransform.k / 1.5)
                    );
                }});
                
                document.getElementById('reset').addEventListener('click', function() {{
                    svg.transition().duration(500).call(
                        d3.zoom().on('zoom', event => g.attr('transform', event.transform))
                            .transform, 
                        d3.zoomIdentity
                    );
                }});
            }}
            
            // Initialize the visualization
            window.addEventListener('load', function() {{
                renderVisualization();
            }});
            
            // Handle window resize
            window.addEventListener('resize', function() {{
                renderVisualization();
            }});
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

def generate_data_flow_visualization(data_flow_map: Dict[str, Any]) -> str:
    """Generate an HTML visualization of the data flow map."""
    # Convert data flow map to JSON for JavaScript visualization
    data_flow_json = json.dumps(data_flow_map, cls=SetEncoder)
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI Data Flow Analysis</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://d3js.org/d3.v7.min.js"></script>
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
            
            #data-flow-visualization {{ height: 800px; border: 1px solid #ddd; border-radius: 4px; overflow: hidden; position: relative; }}
            
            .node rect {{ stroke: #333; fill: #fff; }}
            .node text {{ font-size: 12px; }}
            .node.route rect {{ fill: #61affe; }}
            .node.function rect {{ fill: #fca130; }}
            .node.database rect {{ fill: #49cc90; }}
            .node.model rect {{ fill: #f93e3e; }}
            
            .edgePath path {{ stroke: #333; stroke-width: 1.5px; fill: none; }}
            .edgePath.data-flow path {{ stroke: #f93e3e; }}
            .edgePath.function-call path {{ stroke: #fca130; }}
            .edgePath.db-operation path {{ stroke: #49cc90; }}
            
            .tooltip {{ 
                position: absolute; 
                padding: 10px; 
                background: white; 
                border-radius: 4px; 
                border: 1px solid #ddd;
                pointer-events: none;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                max-width: 300px;
                z-index: 1000;
            }}
            
            .route-details {{
                margin-bottom: 20px;
                padding: 15px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }}
            
            .route-details h3 {{
                margin-top: 0;
                border-bottom: 1px solid #eee;
                padding-bottom: 10px;
            }}
            
            .function-call {{
                padding: 8px;
                margin: 5px 0;
                background-color: #f8f9fa;
                border-radius: 4px;
                border-left: 4px solid #fca130;
            }}
            
            .db-operation {{
                padding: 8px;
                margin: 5px 0;
                background-color: #f8f9fa;
                border-radius: 4px;
                border-left: 4px solid #49cc90;
            }}
            
            .data-reference {{
                padding: 8px;
                margin: 5px 0;
                background-color: #f8f9fa;
                border-radius: 4px;
                border-left: 4px solid #f93e3e;
            }}
            
            .legend {{ 
                position: absolute; 
                top: 10px; 
                right: 10px; 
                background: white; 
                padding: 10px; 
                border: 1px solid #ddd; 
                border-radius: 4px; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            
            .legend-item {{ 
                display: flex; 
                align-items: center; 
                margin-bottom: 5px; 
            }}
            
            .legend-color {{ 
                width: 15px; 
                height: 15px; 
                margin-right: 8px; 
                border-radius: 3px; 
                display: inline-block; 
            }}
            
            pre.code {{
                background: #f6f8fa;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>FastAPI Data Flow Analysis</h1>
            
            <div class="tab-container">
                <div class="tabs">
                    <div class="tab active" onclick="openTab(event, 'visualization-tab')">Flow Visualization</div>
                    <div class="tab" onclick="openTab(event, 'details-tab')">Route Details</div>
                </div>
                
                <div id="visualization-tab" class="tab-content active">
                    <h2>Data Flow Visualization</h2>
                    <p>This diagram shows how data flows through your FastAPI application, including function calls, database operations, and data transformations.</p>
                    
                    <div id="data-flow-visualization">
                        <div class="legend">
                            <h3>Legend</h3>
                            <div class="legend-item">
                                <span class="legend-color" style="background-color: #61affe;"></span>
                                <span>Routes</span>
                            </div>
                            <div class="legend-item">
                                <span class="legend-color" style="background-color: #fca130;"></span>
                                <span>Functions</span>
                            </div>
                            <div class="legend-item">
                                <span class="legend-color" style="background-color: #49cc90;"></span>
                                <span>Database Operations</span>
                            </div>
                            <div class="legend-item">
                                <span class="legend-color" style="background-color: #f93e3e;"></span>
                                <span>Models/Data</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div id="details-tab" class="tab-content">
                    <h2>Route Data Flow Details</h2>
                    <div id="route-details-container">
                        <!-- Route details will be inserted here -->
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <script src="https://unpkg.com/dagre-d3@0.6.4/dist/dagre-d3.min.js"></script>
        
        <script>
            // Store data flow map
            const dataFlowMap = {data_flow_json};
            
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
                
                if (tabName === 'details-tab') {{
                    renderRouteDetails();
                }}
            }}
            
            function renderGraph() {{
                // Create a new directed graph
                const g = new dagreD3.graphlib.Graph().setGraph({{
                    rankdir: "TB",
                    ranksep: 70,
                    nodesep: 50,
                    edgesep: 10,
                    marginx: 20,
                    marginy: 20
                }});
                
                // Process data flow map to create graph
                const routes = dataFlowMap.data_flow;
                const addedNodes = new Set();
                const addedEdges = new Set();
                
                // Create nodes for each route
                Object.values(routes).forEach(route => {{
                    const routeId = `route_${{route.endpoint}}`;
                    
                    if (!addedNodes.has(routeId)) {{
                        g.setNode(routeId, {{
                            label: `${{route.methods}} ${{route.path}}`,
                            class: "route",
                            rx: 5,
                            ry: 5,
                            padding: 10,
                            shape: "rect"
                        }});
                        addedNodes.add(routeId);
                    }}
                    
                    // Process call chain
                    processCallChain(g, routeId, route.call_chain, addedNodes, addedEdges);
                    
                    // Process DB operations
                    route.db_operations.forEach((op, i) => {{
                        const opId = `db_${{route.endpoint}}_${{i}}`;
                        
                        if (!addedNodes.has(opId)) {{
                            g.setNode(opId, {{
                                label: `${{op.type}}: ${{op.operation}}`,
                                class: "database",
                                rx: 5,
                                ry: 5,
                                padding: 10,
                                shape: "rect"
                            }});
                            addedNodes.add(opId);
                        }}
                        
                        const edgeId = `${{routeId}}_${{opId}}`;
                        if (!addedEdges.has(edgeId)) {{
                            g.setEdge(routeId, opId, {{
                                label: "DB operation",
                                class: "db-operation",
                                curve: d3.curveBasis
                            }});
                            addedEdges.add(edgeId);
                        }}
                    }});
                }});
                
                // Create a renderer and run it
                const render = new dagreD3.render();
                
                // Set up SVG
                const svg = d3.select("#data-flow-visualization").append("svg")
                    .attr("width", "100%")
                    .attr("height", "100%")
                    .attr("style", "background-color: white");
                
                const svgGroup = svg.append("g");
                
                // Add zoom behavior
                const zoom = d3.zoom().on("zoom", (e) => {{
                    svgGroup.attr("transform", e.transform);
                }});
                svg.call(zoom);
                
                // Run the renderer
                render(svgGroup, g);
                
                // Center the graph
                const initialScale = 0.75;
                svg.call(zoom.transform, d3.zoomIdentity
                    .translate((svg.attr("width") - g.graph().width * initialScale) / 2, 20)
                    .scale(initialScale));
                
                // Add tooltips
                svgGroup.selectAll("g.node")
                    .append("title")
                    .text(function(id) {{
                        const node = g.node(id);
                        return node.label;
                    }});
            }}
            
            function processCallChain(g, parentId, callChain, addedNodes, addedEdges) {{
                if (!callChain || !callChain.length) return;
                
                callChain.forEach((call, i) => {{
                    const callId = `func_${{call.function}}_${{i}}`;
                    
                    if (!addedNodes.has(callId)) {{
                        g.setNode(callId, {{
                            label: call.function,
                            class: "function",
                            rx: 5,
                            ry: 5,
                            padding: 10,
                            shape: "rect"
                        }});
                        addedNodes.add(callId);
                    }}
                    
                    const edgeId = `${{parentId}}_${{callId}}`;
                    if (!addedEdges.has(edgeId)) {{
                        g.setEdge(parentId, callId, {{
                            label: "calls",
                            class: "function-call",
                            curve: d3.curveBasis
                        }});
                        addedEdges.add(edgeId);
                    }}
                    
                    // Process nested calls
                    if (call.calls && call.calls.length) {{
                        processCallChain(g, callId, call.calls, addedNodes, addedEdges);
                    }}
                }});
            }}
            
            function renderRouteDetails() {{
                const container = document.getElementById("route-details-container");
                container.innerHTML = "";
                
                const routes = dataFlowMap.data_flow;
                Object.values(routes).forEach(route => {{
                    const routeDiv = document.createElement("div");
                    routeDiv.className = "route-details";
                    
                    // Create route header
                    const title = document.createElement("h3");
                    title.textContent = `${{Array.isArray(route.methods) ? route.methods.join(", ") : route.methods}} ${{route.path}}`;
                    routeDiv.appendChild(title);
                    
                    // Route info
                    const info = document.createElement("p");
                    info.innerHTML = `<strong>Endpoint:</strong> ${{route.endpoint}}`;
                    routeDiv.appendChild(info);
                    
                    // Function calls section
                    if (route.call_chain && route.call_chain.length > 0) {{
                        const callsHeader = document.createElement("h4");
                        callsHeader.textContent = "Function Call Chain:";
                        routeDiv.appendChild(callsHeader);
                        
                        const callsDiv = document.createElement("div");
                        renderCallChain(callsDiv, route.call_chain, 0);
                        routeDiv.appendChild(callsDiv);
                    }}
                    
                    // Database operations section
                    if (route.db_operations && route.db_operations.length > 0) {{
                        const dbHeader = document.createElement("h4");
                        dbHeader.textContent = "Database Operations:";
                        routeDiv.appendChild(dbHeader);
                        
                        route.db_operations.forEach(op => {{
                            const dbOpDiv = document.createElement("div");
                            dbOpDiv.className = "db-operation";
                            dbOpDiv.innerHTML = `<strong>${{op.type}}:</strong> ${{op.operation}} (line ${{op.line}})`;
                            routeDiv.appendChild(dbOpDiv);
                        }});
                    }}
                    
                    // Data flow section
                    const dataFlowHeader = document.createElement("h4");
                    dataFlowHeader.textContent = "Data References:";
                    routeDiv.appendChild(dataFlowHeader);
                    
                    const dataFlow = route.data_flow;
                    if (dataFlow && dataFlow.references && dataFlow.references.length > 0) {{
                        dataFlow.references.forEach(ref => {{
                            const refDiv = document.createElement("div");
                            refDiv.className = "data-reference";
                            refDiv.textContent = ref;
                            routeDiv.appendChild(refDiv);
                        }});
                    }} else {{
                        const noData = document.createElement("p");
                        noData.textContent = "No data references detected.";
                        routeDiv.appendChild(noData);
                    }}
                    
                    container.appendChild(routeDiv);
                }});
            }}
            
            function renderCallChain(container, calls, depth) {{
                if (!calls || !calls.length) return;
                
                calls.forEach(call => {{
                    const callDiv = document.createElement("div");
                    callDiv.className = "function-call";
                    callDiv.style.marginLeft = `${{depth * 20}}px`;
                    callDiv.textContent = call.function;
                    container.appendChild(callDiv);
                    
                    // Render nested calls
                    if (call.calls && call.calls.length) {{
                        renderCallChain(container, call.calls, depth + 1);
                    }}
                }});
            }}
            
            // Initialize visualizations
            window.addEventListener('load', function() {{
                renderGraph();
                
                if (document.getElementById('details-tab').classList.contains('active')) {{
                    renderRouteDetails();
                }}
            }});
        </script>
    </body>
    </html>
    """
