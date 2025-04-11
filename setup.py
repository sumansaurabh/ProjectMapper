from setuptools import setup, find_packages

setup(
    name="projectmapper",
    version="0.1.6",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "pydantic>=2.11.3",
        "graphviz>=0.20.3",
    ],
    description="A library for mapping FastAPI project structure and connections",
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
