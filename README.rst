.. Start

============
Example app
============

=================
For developers
=================

This project was created using ``poetry``. The ``--src`` flag tells it to use a top-level layout with a  ``src`` directory instead or the module name itself.

``poetry`` also creates a ``pyproject.toml`` file for configuring the project.

``poetry`` sets up ``pytest`` for testing, and that is set up automatically by ``poetry new``. We do need to tell tooling that runs ``pytest`` outside of ``poetry`` (like **VSCode**) that Python modules used in test are found in the ``src`` directory. This happens in the ``[tool.pytest.ini_options]`` section in ``pyproject.toml``.

``poetry`` will find or setup a virtual enviroment on first run. Using ``poetry install`` instead of ``pip install`` will setup the virtual environment. ``poetry`` tries to guess the version of ``python`` to install so there are interactiopns with ``pyenv`` (which I use) and the specific versions of ``python`` mentioned in the ``[tool.poetry.dependencies]`` section of ``pyproject.toml``. See ``pyenv`` and ``poetry`` docs for more info. 

Here's the sequence I followed starting from my dev directory::

    poetry new --src blueberrypy
    cd blueberrypy

Make sure that the ``python`` version is set::
    
    # pyproject.toml
    [tool.poetry.dependencies]
    python = "^3.10"

And to keep the regular command line session using the same version as poetry::

  pyenv local 3.10.4
  poetry env use python

Here's how I set up ``pytest`` to use a current version and recognize the source modules::
    
    # pyproject.toml 
    [tool.pytest.ini_options]
    testpaths = ["tests"]
    # in case tooling running pytest will not resolve modules
    pythonpath = ["src"]

There's lots more config to come. Using ``tox`` maybe. Adding ``./docs`` powered by ``sphinx``. Using ``poetry`` or ``tox``'s build capability. 

And then adding in *FastAPI* (plus a *CLI* interface for batch).





