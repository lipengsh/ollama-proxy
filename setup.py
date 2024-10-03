from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ollama-proxy",
    version="0.1.0",
    author="lipi",
    author_email="lipeng.sh@qq.com",
    description="Ollama proxy to cloud service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lipish/ollama-proxy",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "toml",
        # 添加其他
    ],
    entry_points={
        "console_scripts": [
            "ollama-proxy=ollama_proxy.main:app",
        ],
    },
)
