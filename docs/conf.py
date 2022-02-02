import datetime
import markdown
import os
import sys

sys.path.insert(0, os.path.abspath('..'))

def getversion():
    with open(os.path.join('..', 'dhbw', '__init__.py')) as file:
        lines = file.read().split('\n')
        for line in lines:
            if line.startswith('__version__'):
                return line.split('=')[-1].strip('\' \"')
    return '0'

def getyear():
    return datetime.datetime.now().year

release = f'{getversion()}'
project = f'dhbw-python {release}'
author = f'Juergen Hock'
copyright = f'{getyear()} by {author}'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx_rtd_theme',
    'numpydoc',
]

autodoc_mock_imports = [
    'click',
    'matplotlib',
    'numpy',
    'scipy',
]

exclude_patterns = [
    'doctrees',
    'html',
    'Thumbs.db',
    '.DS_Store',
]

autodoc_member_order = 'groupwise'
numpydoc_show_class_members = False

html_title = f'{project} docs'
html_theme = 'sphinx_rtd_theme'

with open(os.path.join('..', 'README.md'), 'r') as file:
    text = file.read()
    html = markdown.markdown(text)

with open(os.path.join('..', 'index.html'), 'w') as file:
    file.write(html)
