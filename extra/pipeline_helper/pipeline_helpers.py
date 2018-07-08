import importlib
from django.conf import settings
from django.apps import apps
import os
from glob import glob

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
        apppath = apps.get_app_config(app).path
        assetpath = f"{apppath}/static/pipeline"
        css_assetpath = f"{assetpath}/css"
        js_assetpath = f"{assetpath}/js"
        outputpath = f"{apppath}/static/min"
        css_outputpath = f"{outputpath}/css"
        js_outputpath = f"{outputpath}/js"

        def compile_css_dir(directory):
            path, dirs, files = next(os.walk(directory))
            if path.endswith('.css'):
                filepath = os.path.relpath(path, css_assetpath)
                key = f"{app}:{filepath}/{file[:len(key.split('.')[-1])]}".replace("/",":")
                _css.update({key:{
                    'source_filenames': tuple(glob(f"{path}/**/*.css", recursive=True)),
                    'output_filename': f"{css_outputpath}/{filepath}/{path}",
                    }})
            else:
                for file in files:
                    if file.endswith('.css') or (file.endswith(('.sass', '.scss')) and not file.startswith('_')):
                        filepath = os.path.relpath(path, css_assetpath)
                        key = f"{app}:{filepath}/{file[:len(key.split('.')[-1])]}"
                        _css.update({key:{
                            'source_filenames': (f"{path}/{file}",),
                            'output_filename': f"{css_outputpath}/{filepath}/{file}",
                            }})
                for nextdir in dirs:
                    compile_css_dir(nextdir)

        def compile_js_dir(directory):
            path, dirs, files = next(os.walk(directory))
            if path.endswith('.js'):
                filepath = os.path.relpath(path, js_assetpath)
                key = f"{app}:{filepath}/{file[:len(key.split('.')[-1])]}".replace("/",":")
                _js.update({key:{
                    'source_filenames': tuple(glob(f"{path}/**/*.js", recursive=True)),
                    'output_filename': f"{js_outputpath}/{filepath}/{path}",
                    }})
            else:
                for file in files:
                    if file.endswith('.js'):
                        filepath = os.path.relpath(path, js_assetpath)
                        filepath.replace('/',':')
                        key = f"{app}:{filepath}/{file[:len(key.split('.')[-1])]}"
                        _css.update({key:{
                            'source_filenames': (f"{path}/{file}",),
                            'output_filename': f"{js_outputpath}/{filepath}/{file}",
                            }})
                for nextdir in dirs:
                    compile_js_dir(nextdir)

        try:
            compile_css_dir(css_assetpath)
            compile_js_dir(js_assetpath)
        except:
            continue

if not cached:
    _assets_from_apps()
    cached = True

def find_js():
    return _js

def find_css():
    return _css
