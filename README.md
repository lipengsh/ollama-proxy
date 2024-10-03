# ollama-proxy
ollama run as a proxy


## Pypi upload
```bash

twine upload --repository testpypi dist/*
```

## 使用pipx上传分发包

本节介绍如何使用pipx安装twine并上传分发包到PyPI或TestPyPI。

### 安装twine

首先，使用pipx安装twine:

```bash
pipx install twine
```

### 上传分发包

1. 构建分发包: 

```bash
poetry build
```

2. 上传分发包到TestPyPI:

```bash
twine upload --repository testpypi dist/*
```

3. 上传分发包到PyPI:

```bash
twine upload dist/*
```

### 注意事项

- 每次上传前，请确保更新版本号。
- 使用TestPyPI进行测试可以避免影响正式版本。
- 考虑使用`.pypirc`文件存储凭证，简化上传过程。





