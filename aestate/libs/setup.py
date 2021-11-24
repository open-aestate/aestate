# -*- utf-8 -*-
import setuptools  # important
from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension

extensions = [Extension('utils', ['utils.py'])]

setup(
    ext_modules=cythonize(extensions, compiler_directives={'language_level': 2}),
)
