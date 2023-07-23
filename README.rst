.. Start

============
Example app
============

Illustraing some good python practices

--------------------
For developers
--------------------

This project was created using ``poetry``. The ``--src`` flag tells it to use a top-level layout with a  ``src`` directory instead or the module name itself.

``poetry`` also creates a ``pyproject.toml`` file for configuring the project.

``poetry`` sets up ``pytest`` for testing, and that is set up automatically by ``poetry new``. We may need to tell tooling that runs ``pytest`` outside of ``poetry`` (like **VSCode**) that Python modules used in test are found in the ``src`` directory. This happens in the ``[tool.pytest.ini_options]`` section in ``pyproject.toml``.

``poetry`` will find or setup a virtual enviroment on first run. Using ``poetry install`` instead of ``pip install`` will setup the virtual environment. ``poetry`` tries to guess the version of ``python`` to install so there are interactiopns with ``pyenv`` (which I use) and the specific versions of ``python`` mentioned in the ``[tool.poetry.dependencies]`` section of ``pyproject.toml``. See ``pyenv`` and ``poetry`` docs for more info. 

......................
Getting started
......................

Once you have checked this repo out (using ``git clone https://github.com/Display-Lab/blueberrypy.git``) just make sure that you are using a virtualenv and local fixed version of ``python``. 

The project is configured to use ``poetry`` for dependency management, including managing virtual enviroments. I use ``pyenv`` to manage ``python`` versions so to match the version in pyproject.toml::

  pyenv local 3.10.4
  poetry env use 3.10.4
  poetry install

in the project directory. You should be able to run both ``pytest`` and ``poetry run pytest``

Depending on your IDE youmay want to run in the poetry shell (e.g. VSCode)::

  poetry run code .

You can check ``poetry``'s virtual environment by running ``poetry env info``.  

...............................
How this project was created
...............................

Here's the sequence I followed starting from my dev directory::

    poetry new --src blueberrypy
    cd blueberrypy

Make sure that the ``python`` version is set::
    
    # pyproject.toml
    [tool.poetry.dependencies]
    python = "^3.10"

(or run ``poetry add python@^3.10``)

And to keep the regular command line session using the same version as poetry::

  pyenv local 3.10.4
  poetry env use 3.10.4
  poetry install

Then run your IDE (e.g. VSCode)::

  poetry shell
  code .

Here's how I set up ``pytest`` to use a current version and recognize the source modules::
    
    # pyproject.toml 
    [tool.poetry.dev-dependencies]
    pytest = ">=7.1"

or run ``poetry add --dev pytest@^7.1``

then set::

    [tool.pytest.ini_options]
    testpaths = ["tests"]
    # in case tooling running pytest will not resolve modules
    pythonpath = ["src"]

.............................. 
What's in it
.............................. 

* ``poetry`` for managing dependencies and performing simple builds
* ``pytest`` for testing
* ``FastAPI`` for demoing simple annotation and model driven reactive web API
* ``Typer`` for creating and using a simple CLI 
* ``Sphinx`` for docs
* ``isort``, ``black``, and ``flake8`` for code formatting, linting, and checking
* ``pre-commit`` hooks — NOT YET


...............................
What's next?
...............................

There's lots more good pratcie and config to come. Using ``tox`` maybe. Adding ``./docs`` powered by ``sphinx``. Using ``poetry`` or ``tox``'s build capability. 

And then adding in *FastAPI* (plus a *CLI* interface for batch).


**Note**
This is a note


https://github.com/Display-Lab/blueberrypy/blob/5b7b1d410e8c2724ce83d7da7c5b5972fd387f65/src/blueberrypy/main.py#L14-L16

