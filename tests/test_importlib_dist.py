import importlib.util
import subprocess
from sys import modules
import sys
from pkginfo import Wheel, SDist
import os
import venv


def test_hello_works():
    spec = importlib.util.spec_from_file_location(
        "hello", "etc/90210-v.6/src/a90210/mod_a.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert module.hello().startswith("Hi there!")


def test_basic_relative_import_works():
    spec = importlib.util.spec_from_file_location(
        "mod42", "etc/90210-v.6/src/a90210/__init__.py"
    )
    module = importlib.util.module_from_spec(spec)
    modules[spec.name] = module
    foo = importlib.import_module(".mod_b", spec.name)

    # spec.loader.exec_module(module)

    assert module.mod_b.sup().startswith("Sup... Hi there!")
    assert foo.sup().startswith("Sup... Hi there!")

    del modules[spec.name]  # cleanup


def test_pip_install_for_package():
    subprocess.run(["python", "--version"], capture_output=True)

    completed_process = subprocess.run(
        [
            "python",
            "-m",
            "pip",
            "install",
            "etc/90210-v.6/dist/a90210-0.1.0-py3-none-any.whl",
            "--force-reinstall",
        ],
        capture_output=True,
    )

    a90210 = importlib.import_module("a90210")
    mod_b = importlib.import_module(".mod_b", a90210.__name__)

    assert a90210.mod_a.hello().startswith("Hi there!")
    assert mod_b.sup().startswith("Sup... Hi there!")

    # clean up
    completed_process = subprocess.run(
        ["python", "-m", "pip", "uninstall", "-y", "a90210"]
    )


import site


def test_venv_with_install():
    """--target is simply an instruction of where to dump the files that would normally go into the python site-packages folder.
    THere are three ways to do this:
    * Let pipenv use the python-activator's environment (virtual, system, whatever). This does not require any update to sys.path
    * Set PIPENV_IGNORE_VIRTUALENVS and provide a location via fully qualified PIPENV_CUSTOM_VENV_NAME. Requires
    adding the 'site-packages' path in the custom virtual env to sys.path, which is a little os dependant
    * Set a "target" on install using '--extra-pip-args "--target etc/targ"'. This path gets added to sys.paths.
    DOesn't allow multiple python versions"""
    wheel = Wheel("etc/90210-v.6/dist/a90210-0.1.0-py3-none-any.whl")
    sdist = SDist("etc/90210-v.6/dist/a90210-0.1.0.tar.gz")

    assert wheel.name == sdist.name

    os.environ["PIPENV_IGNORE_VIRTUALENVS"] = "True"

    """This uses a custom venv location with 'site-packages' but is os dependent."""
    # os.environ[
    #     "PIPENV_CUSTOM_VENV_NAME"
    # ] = "/Users/pboisver/dev/code-red/blueberrypy_test/etc/pyshelf"
    # pip_process = subprocess.run(["pipenv", "--python", "3.11"], capture_output="True")
    # sys.path.append("etc/pyshelf/lib/python3.11/site-packages")

    sys.path.append("etc/targ")  # works with '--target etc/targ'

    pip_process = subprocess.run(["pipenv", "--venv"], capture_output="True")

    pip_process = subprocess.run(
        ["pipenv", "install", wheel.filename, "--extra-pip-args", "--target etc/targ"],
        capture_output=True,
    )

    a90210 = importlib.import_module("a90210")
    mod_b = importlib.import_module(".mod_b", a90210.__name__)

    assert a90210.mod_a.hello().startswith("Hi there!")
    assert mod_b.sup().startswith("Sup... Hi there!")

    # subprocess.run(["pipenv", "uninstall", "--all"])

    pass
