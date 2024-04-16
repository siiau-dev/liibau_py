from os import path
from setuptools import setup

info = {}
curdir = path.abspath(path.dirname(__file__))
with open(path.join(curdir, "src", "siiaulib_py", "__info__.py"), "r") as f:
    exec(f.read(), info)

with open('README.md', 'r') as f:
    readme = f.read()

with open('requirements.txt', 'r') as f:
    requires = f.readlines()

setup(
    name = info['__title__'],
    version = info['__version__'],
    description = info['__description__'],
    long_description = readme,
    long_description_content_type="text/markdown",
    url = info['__url__'],
    author = info['__author__'],
    author_email = info['__author_email__'],
    license = info['__license__'],
    package_dir = {'': 'src'},
    packages = ['siiaulib_py'],
    include_package_data = True,
    python_requires = ">=3.8",
    install_requires = requires,
    classifiers = [
        "Development Status :: 1 - Planning",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Spanish",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    project_urls = {
        "Página principal": info['__url__'],
        "Repositorio": info['__github__']
    }
)
