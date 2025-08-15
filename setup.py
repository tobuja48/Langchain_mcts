"""Setup script for langchain-mcts package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="langchain-mcts",
    version="0.1.0",
    author="Tu Nombre",
    author_email="tu@email.com",
    description="Monte Carlo Tree Search integration for LangChain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tu-usuario/langchain-mcts",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain>=0.1.0",
        "numpy>=1.20.0",
    ],
    extras_require={
        "dev": ["pytest>=6.0", "black", "flake8", "mypy"],
    },
    project_urls={
        "Bug Reports": "https://github.com/tu-usuario/langchain-mcts/issues",
        "Source": "https://github.com/tu-usuario/langchain-mcts",
        "Documentation": "https://langchain-mcts.readthedocs.io/",
    },
)