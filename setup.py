from setuptools import setup, find_packages

setup(
    name="projectmapper",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "pydantic>=2.11.3",
        "graphviz>=0.20.3",
        "ast-comments>=1.0.1",  # For better AST parsing
    ],
    description="A library for mapping FastAPI project structure, data flow and connections",
    author="Penify",
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
