# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------

project = "Feluda"
copyright = "2024, Tattle"
author = "Tattle"

# The full version, including alpha/beta/rc tags
release = "0.9.4"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "myst_nb",
    "sphinx_copybutton",
    "sphinx_design",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# -- Options for autodoc ----------------------------------------------------

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

autodoc_mock_imports = [
    # Core dependencies
    "numpy",
    "pillow",
    "pydub",
    "boto3",
    "werkzeug",
    "requests",
    "wget",
    "dacite",
    "pyyaml",
    # Machine learning libraries
    "torch",
    "torchvision",
    "transformers",
    "opencv-python",
    "cv2",
    "scikit-learn",
    "sklearn",
    "matplotlib",
    "seaborn",
    "pandas",
    "tesseract",
    "pytesseract",
    "tqdm",
    # Additional ML/AI libraries
    "umap",
    "umap-learn",
    "scipy",
    "scipy.optimize",
    "scipy.spatial",
    "scipy.stats",
    "numba",
    "faiss",
    "faiss-cpu",
    "faiss-gpu",
    "hdbscan",
    "leidenalg",
    "igraph",
    "networkx",
    "community",
    "python-louvain",
    # Image processing
    "PIL",
    "PIL.Image",
    "PIL.ImageDraw",
    "PIL.ImageFont",
    # Audio processing
    "librosa",
    "soundfile",
    "pydub",
    "pydub.audio_segment",
    # Video processing
    "moviepy",
    "moviepy.editor",
    "ffmpeg",
    "ffmpeg-python",
    # Text processing
    "nltk",
    "spacy",
    "textblob",
    "langdetect",
    "polyglot",
    # Utilities
    "tqdm",
    "joblib",
    "multiprocessing",
    "concurrent.futures",
    "threading",
    "asyncio",
    "aiohttp",
    "httpx",
    "websockets",
    "redis",
    "pymongo",
    "sqlalchemy",
    "psycopg2",
    "mysql-connector-python",
    # Development and testing
    "pytest",
    "pytest-cov",
    "pytest-asyncio",
    "black",
    "flake8",
    "mypy",
    "pre-commit",
    # Jupyter and notebook related
    "ipykernel",
    "jupyter",
    "notebook",
    "jupyterlab",
    "ipywidgets",
    # Visualization
    "plotly",
    "bokeh",
    "altair",
    "holoviews",
    "datashader",
    "bokeh.plotting",
    "plotly.graph_objects",
    "plotly.express",
    # Data science
    "pandas",
    "numpy",
    "scipy",
    "statsmodels",
    "scikit-learn",
    "xgboost",
    "lightgbm",
    "catboost",
    "optuna",
    "hyperopt",
    # Deep learning frameworks
    "tensorflow",
    "tensorflow.keras",
    "keras",
    "mxnet",
    "jax",
    "jax.numpy",
    "flax",
    "haiku",
    "optax",
    # Cloud and deployment
    "docker",
    "kubernetes",
    "helm",
    "terraform",
    "ansible",
    "gunicorn",
    "uvicorn",
    "fastapi",
    "flask",
    "django",
    "celery",
    "redis",
    "rabbitmq",
    # Monitoring and logging
    "prometheus_client",
    "grafana_api",
    "elasticsearch",
    "logstash",
    "kibana",
    "sentry_sdk",
    "structlog",
    "loguru",
    # Configuration and environment
    "python-dotenv",
    "configparser",
    "yaml",
    "toml",
    "json5",
    "jsonschema",
    "pydantic",
    "marshmallow",
    "cerberus",
    # File handling
    "pathlib",
    "shutil",
    "tempfile",
    "zipfile",
    "tarfile",
    "gzip",
    "bz2",
    "lzma",
    "pickle",
    "shelve",
    "sqlite3",
    "csv",
    "json",
    "xml",
    "xml.etree.ElementTree",
    "lxml",
    "beautifulsoup4",
    "bs4",
    "requests_html",
    "selenium",
    "playwright",
    # System and OS
    "os",
    "sys",
    "subprocess",
    "signal",
    "psutil",
    "platform",
    "socket",
    "ssl",
    "hashlib",
    "hmac",
    "base64",
    "uuid",
    "datetime",
    "time",
    "calendar",
    "locale",
    "gettext",
    "argparse",
    "click",
    "typer",
    "fire",
    "docopt",
    # Data formats
    "pickle",
    "cPickle",
    "marshal",
    "shelve",
    "dbm",
    "sqlite3",
    "mysql.connector",
    "psycopg2",
    "pymongo",
    "redis",
    "memcached",
    "cassandra",
    "neo4j",
    "elasticsearch",
    "influxdb",
    "prometheus",
    "graphite",
    "statsd",
    # Web and API
    "requests",
    "urllib3",
    "httpx",
    "aiohttp",
    "websockets",
    "flask",
    "django",
    "fastapi",
    "starlette",
    "uvicorn",
    "gunicorn",
    "tornado",
    "sanic",
    "falcon",
    "bottle",
    "cherrypy",
    "pyramid",
    "web2py",
    "dash",
    "streamlit",
    "gradio",
    "panel",
    "voila",
    "bokeh",
    "plotly",
    "dash",
    "streamlit",
    "gradio",
    "panel",
    "voila",
    "bokeh",
    "plotly",
]

# -- Options for myst-nb ----------------------------------------------------

nb_execution_mode = "off"
nb_execution_timeout = 300

# Suppress highlighting warnings for shell commands in notebooks
suppress_warnings = ["misc.highlighting_failure"]
# -- Options for intersphinx -------------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
}

# -- Options for HTML output -------------------------------------------------

html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "includehidden": True,
    "titles_only": False,
}

# -- Options for copybutton --------------------------------------------------

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True
