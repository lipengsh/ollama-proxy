# ollama-proxy
ollama runs as a proxy

## PyPI Upload
```bash
twine upload --repository testpypi dist/*
```

## Using pipx to Upload Distribution Packages

This section describes how to install twine using pipx and upload distribution packages to PyPI or TestPyPI.

### Install twine

First, install twine using pipx:

```bash
pipx install twine
```

### Upload Distribution Packages

1. Build the distribution package: 

```bash
poetry build
```

2. Upload the distribution package to TestPyPI:

```bash
twine upload --repository testpypi dist/*
```

3. Upload the distribution package to PyPI:

```bash
twine upload dist/*
```

### Notes

- Make sure to update the version number before each upload.
- Using TestPyPI for testing can avoid affecting the official version.
- Consider using a `.pypirc` file to store credentials, simplifying the upload process.
