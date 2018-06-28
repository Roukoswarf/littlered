import importlib
from django.conf import settings

# Assets with be cached the first
# time module is imported.

_js = {}
_css = {}
cached = False

def _assets_from_apps():
    """
    Search the INSTALLED_APPS for assets.py files,
    and fill the js/css with its contents. Namespace
    bundles with their app's name.
    """
    for app in settings.INSTALLED_APPS:
        try:
            assets = importlib.import_module(f'{app}.assets')
        except ImportError:
            continue

        js = getattr(assets, "PIPELINE_JS", {})
        css = getattr(assets, "PIPELINE_CSS", {})

        js = { f'{app}:{k}': v for k, v in js.items() }
        css = { f'{app}:{k}': v for k, v in css.items() }
        _js.update(js)
        _css.update(css)

if not cached:
    _assets_from_apps()
    cached = True

def find_js():
    return _js

def find_css():
    return _css
