# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'flink-cdc'
copyright = '2021, Leonard Xu'
author = 'Leonard Xu'

# The full version, including alpha/beta/rc tags
release = '2.0.0'


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_rtd_theme',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'myst_parser'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

import myst_parser

source_parsers = {
    '.md': myst_parser
}
source_suffix = ['.md']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

try:
   html_context
except NameError:
   html_context = dict()
html_context['display_lower_left'] = True

if 'REPO_NAME' in os.environ:
	REPO_NAME = os.environ['REPO_NAME']
else:
	REPO_NAME = ''

from git import Repo
repo = Repo( search_parent_directories=True )
 
if 'current_version' in os.environ:
   current_version = os.environ['current_version']
else:
   current_version = repo.active_branch.name

html_context['current_version'] = current_version
html_context['version'] = current_version
html_context['versions'] = list()
 
versions = [branch.name for branch in repo.branches]
for version in versions:
   html_context['versions'].append( (version, '/' +REPO_NAME+ '/' +version+ '/') )

html_context['display_github'] = True
html_context['github_repo'] = 'flink-cdc-connectors'
html_context['github_version'] = 'master'
