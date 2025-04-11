import ast
import inspect
import os.path
from typing import Dict, List, Any, Set, Optional, Tuple

class FunctionCall(ast.NodeVisitor):
    """AST visitor that finds function calls within a function."""
    
    def __init__(self):
        self.calls = []
        
    def visit_Call(self, node):
        """Visit a function call node."""
        if isinstance(node.func, ast.Name):
            # Direct function call like function_name()
            self.calls.append(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            # Method call like object.method()
            self.calls.append(f"{self.get_attribute_chain(node.func)}")
        
        # Continue visiting child nodes
        self.generic_visit(node)
    
    def get_attribute_chain(self, node):
        """Get full attribute chain like a.b.c."""
        if isinstance(node, ast.Attribute):
            return f"{self.get_attribute_chain(node.value)}.{node.attr}"
        elif isinstance(node, ast.Name):
            return node.id
        return "unknown"


class CodeFlowAnalyzer:
    """Analyzes code flow by tracking function calls and data flow."""
    
    def __init__(self):
        self.call_graph = {}  # Maps function names to the functions they call
        self.data_flow = {}   # Maps function names to data they access/modify
    
    def analyze_function(self, func_obj, source_file: str) -> Dict[str, Any]:
        """Analyze a function's code flow including called functions and data accesses."""
        if not source_file or source_file == "Unknown" or not os.path.exists(source_file):
            return {"calls": [], "data_references": [], "db_operations": []}
            
        try:
            # Get function source
            source_lines, start_line = inspect.getsourcelines(func_obj)
            source_code = "".join(source_lines)
            
            # Parse the source code
            tree = ast.parse(source_code)
            
            # Find all function calls
            visitor = FunctionCall()
            visitor.visit(tree)
            
            # Analyze for database operations
            db_operations = self.detect_database_operations(tree)
            
            # Track data references
            data_references = self.detect_data_references(tree)
            
            flow_info = {
                "calls": visitor.calls,
                "data_references": data_references,
                "db_operations": db_operations
            }
            
            # Store in call graph
            self.call_graph[func_obj.__name__] = flow_info
            
            return flow_info
            
        except Exception as e:
            # Return empty result if analysis fails
            return {"calls": [], "data_references": [], "db_operations": [], "error": str(e)}
    
    def detect_database_operations(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Detect database operations in the AST."""
        db_operations = []
        
        class DBOperationVisitor(ast.NodeVisitor):
            def visit_Call(self, node):
                # Common database operation patterns
                
                # SQLAlchemy: session.query(), session.add(), Model.query, etc.
                if isinstance(node.func, ast.Attribute):
                    attr_chain = self.get_attribute_chain(node.func)
                    
                    # SQLAlchemy patterns
                    if any(pattern in attr_chain for pattern in [
                        ".query", ".add", ".commit", ".delete", ".filter", 
                        ".all", ".first", ".get", ".update", ".execute"
                    ]):
                        db_operations.append({
                            "type": "sqlalchemy",
                            "operation": attr_chain,
                            "line": node.lineno
                        })
                    
                    # Tortoise-ORM patterns
                    elif any(pattern in attr_chain for pattern in [
                        ".filter", ".get", ".create", ".delete", ".update", 
                        ".all", ".first", ".save", ".values"
                    ]):
                        if attr_chain.startswith("Model") or "models." in attr_chain:
                            db_operations.append({
                                "type": "tortoise-orm",
                                "operation": attr_chain,
                                "line": node.lineno
                            })
                    
                    # MongoDB with Motor or PyMongo
                    elif any(pattern in attr_chain for pattern in [
                        ".find", ".insert", ".update", ".delete", ".aggregate"
                    ]):
                        if "collection" in attr_chain or "db." in attr_chain:
                            db_operations.append({
                                "type": "mongodb",
                                "operation": attr_chain,
                                "line": node.lineno
                            })
                
                # Continue visiting child nodes
                self.generic_visit(node)
            
            def get_attribute_chain(self, node):
                """Get full attribute chain like a.b.c."""
                if isinstance(node, ast.Attribute):
                    return f"{self.get_attribute_chain(node.value)}.{node.attr}"
                elif isinstance(node, ast.Name):
                    return node.id
                return "unknown"
        
        db_visitor = DBOperationVisitor()
        db_visitor.visit(tree)
        
        return db_operations
    
    def detect_data_references(self, tree: ast.AST) -> List[str]:
        """Detect data references (variables used) in the AST."""
        data_refs = set()
        
        class VarRefVisitor(ast.NodeVisitor):
            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Load):
                    data_refs.add(node.id)
                self.generic_visit(node)
                
            def visit_arg(self, node):
                data_refs.add(node.arg)
                self.generic_visit(node)
        
        var_visitor = VarRefVisitor()
        var_visitor.visit(tree)
        
        return list(data_refs)
    
    def build_execution_flow(self, routes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build complete execution flow graph for each route."""
        route_flows = {}
        
        for route in routes:
            endpoint_name = route["endpoint"]
            route_flow = {
                "endpoint": endpoint_name,
                "path": route["path"],
                "methods": route["methods"],
                "call_chain": self.build_call_chain(endpoint_name),
                "data_flow": self.trace_data_flow(endpoint_name),
                "db_operations": self.extract_db_operations(endpoint_name)
            }
            route_flows[endpoint_name] = route_flow
            
        return route_flows
    
    def build_call_chain(self, func_name: str, visited: Set[str] = None) -> List[Dict[str, Any]]:
        """Recursively build the chain of function calls."""
        if visited is None:
            visited = set()
            
        if func_name in visited:
            return []  # Prevent cycles
            
        visited.add(func_name)
        
        if func_name not in self.call_graph:
            return []
            
        call_chain = []
        for called_func in self.call_graph[func_name].get("calls", []):
            call_chain.append({
                "function": called_func,
                "calls": self.build_call_chain(called_func, visited.copy())
            })
            
        return call_chain
    
    def trace_data_flow(self, func_name: str) -> Dict[str, Any]:
        """Trace how data flows through a function and its called functions."""
        if func_name not in self.call_graph:
            return {}
            
        # Get data references for this function
        data_refs = self.call_graph[func_name].get("data_references", [])
        
        # Get data flows for called functions
        called_funcs_data = {}
        for called_func in self.call_graph[func_name].get("calls", []):
            called_funcs_data[called_func] = self.trace_data_flow(called_func)
            
        return {
            "references": data_refs,
            "called_functions": called_funcs_data
        }
    
    def extract_db_operations(self, func_name: str) -> List[Dict[str, Any]]:
        """Extract database operations from a function and its called functions."""
        if func_name not in self.call_graph:
            return []
            
        # Get direct DB operations
        db_ops = self.call_graph[func_name].get("db_operations", [])
        
        # Get DB operations from called functions
        for called_func in self.call_graph[func_name].get("calls", []):
            db_ops.extend(self.extract_db_operations(called_func))
            
        return db_ops
