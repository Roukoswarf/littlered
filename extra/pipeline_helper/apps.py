import math
from django.apps import AppConfig
from . import pipeline_helpers
import django

class PipelineHelperConfig(AppConfig):
    name = 'pipeline_helper'
    verbose_name = "Pipeline Helper"

    # Settings for the automatic compilation and minification of CSS, JS, SCSS and other
    # types of files.
    def ready(self):
        PIPELINE = {
            'COMPILERS': (
                'pipeline.compilers.es6.ES6Compiler',
                'extra.compilers.LibSassCompiler',
            ),
            # CSS Settings
            'CSS_COMPRESSOR': 'extra.compressors.CssCompressor',
            'STYLESHEETS': pipeline_helpers.find_css(),
            # SASS/SCSS Settings
            'SASS_LIBS': {'.env/lib/sass'},
            'SASS_FUNCS': {math.degrees,
                        math.radians,
                        math.sin,
                        math.cos,
                        math.tan,
                        math.sinh,
                        math.cosh,
                        math.tanh,},
            # Javascript Settings
            'JS_COMPRESSOR': 'pipeline.compressors.uglifyjs.UglifyJSCompressor',
            'JAVASCRIPT': pipeline_helpers.find_js(),
        }
