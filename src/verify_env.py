import sys
import importlib.metadata as md

print('Python:', sys.version)
for pkg in ['optiland', 'numpy', 'scipy', 'matplotlib', 'pandas', 'yaml']:
    try:
        if pkg == 'yaml':
            import yaml  # noqa: F401
            version = md.version('PyYAML')
        else:
            __import__(pkg)
            version = md.version(pkg)
        print(f'{pkg}: {version}')
    except Exception as exc:
        print(f'{pkg}: ERROR: {exc}')
