from distutils.core import setup
import py2exe, sys, os

import sys
base = None
if sys.platform == "win32":
    base = "Win32GUI"

sys.argv.append('py2exe')

setup(
    options={'py2exe': {'bundle_files': 1, 'compressed': True}},
    windows=[{'script': "main.py"}],
    zipfile=None,
)
