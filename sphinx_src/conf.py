




import sys
import os

# import sphinx.environment

import mock

MOCK_MODULES = ['ij', 'ij.measure', 'ij.gui', 'ij.io', 'ij.plugin', 'ij.plugin.frame', 'fiji_utils']
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = mock.Mock()

sys.path.insert(0, os.path.abspath('..'))
print(os.path.abspath('..'))
# sys.path.insert(0, os.path.abspath('../sphinx_src'))
project = 'bob_py'
author = 'Amelia Brown'

# import bob_py
# from bob_py import *


html_theme = 'sphinx_rtd_theme'

html_show_sourcelink = True


html_static_path = ['_static']
# html_css_files = ['custom.css']
html_style = 'custom.css'


# html_theme = 'nature'

# html_theme = 'sphinxdoc'

# html_theme = 'classic'

# html_theme = 'python-docs-theme'


# html_theme = 'sphinx_scipy_theme'
# html_theme_path = [os.path.abspath('../sphinx_src')]

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.mathjax',
    'sphinx.ext.intersphinx',
]




mathjax_path = ('https://cdn.mathjax.org/mathjax/latest/MathJax.js?'
                'config=TeX-AMS-MML_HTMLorMML')



intersphinx_mapping = {
    'numpy': ('http://docs.scipy.org/doc/numpy/', None),
    'scipy': ('http://docs.scipy.org/doc/scipy/reference/', None),
    'python': ('http://docs.python.org/3.7', None)
}



# autodoc_default_flags = [
#     'members',
# ]

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    # 'undoc-members': True,
    # 'exclude-members': '__weakref__'
}

source_suffix = '.rst'
add_module_names = False

master_doc = 'index'


pygments_style = 'sphinx'




# Extensions to theme docs
def setup(app):
    from sphinx.domains.python import PyField
    from sphinx.util.docfields import Field

    app.add_object_type(
        'confval',
        'confval',
        objname='configuration value',
        indextemplate='pair: %s; configuration value',
        doc_field_types=[
            PyField(
                'type',
                label=('Type',),
                has_arg=False,
                names=('type',),
                bodyrolename='class'
            ),
            Field(
                'default',
                label=('Default',),
                has_arg=False,
                names=('default',),
            ),
        ]
    )
