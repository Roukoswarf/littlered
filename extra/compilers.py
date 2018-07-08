"""Libsass compiler for django-pipeline.
Speedups development and/or production when compiling sass assets. No need of
ruby sass anymore.
"""

import sass
import codecs
from pipeline.compilers import CompilerBase
from django.conf import settings


class LibSassCompiler(CompilerBase):
    """Compiler that uses libsass."""

    output_extension = 'css'

    def match_file(self, filename):
        """Check files extension to use them."""
        return filename.endswith(('.scss', '.sass'))

    def compile_file(self, infile, outfile, outdated=False, force=False):
        """Process sass file."""
        myfile = codecs.open(outfile, 'w', 'utf-8')

        myfile.write(sass.compile(filename=infile,
                                  output_style='compressed' if settings.DEBUG else 'nested',
                                  include_paths=settings.PIPELINE['SASS_LIBS'],
                                  source_comments=settings.DEBUG,
                                  custom_functions=settings.PIPELINE['SASS_FUNCS'],
                                 ))
        
        return myfile.close()