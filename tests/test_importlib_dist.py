import importlib.util
import os
import shutil
import subprocess
import sys
from sys import modules

from pkginfo import SDist, Wheel
import pytest


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


"""Using pipenv to install packages at runtime into an isolated environment ()
As long as the location used by pipenv is on syspath, the code can be invoked from the app (python-activator) even if the the package was installed in a different location than the site-packages for the app. Modules loaded at runtime *do not* run in the pipenv virtual env; there are simply made available by sys.path.append('path/to/pipenv/installed/packages')
There are three ways to do this:
    1. Let pipenv use the app's (python-activator) environment (virtual, system, whatever). This does not require any update to sys.path. Distribution packages will be installed into the os dependent 'site-packages' location. (same as 'pip install <package>' and respects the virtual enviroment.)
    2. Set PIPENV_IGNORE_VIRTUALENVS='True' and provide a location via fully qualified path for PIPENV_CUSTOM_VENV_NAME. Requires adding the custom environment's 'site-packages' path to sys.path, which is a little os dependent. Allows for separate envs for diffent python versions (even on a per install basis, I think.)
    3. Set a "target" location for each install using '--extra-pip-args "--target etc/targ"'. This path should be added to sys.paths. Installs can all use the same target or specifiy separate targets. Creates or uses an existing virtual environment for /bin and /lib. Doesn't allow multiple python versions, just uses the python version of the apps enviroment.
Notes:
    * Some techniques can be combined
    * Sometimes 'pip' is enough
    * Haven't tested much with installing for different python versions. Can be done using:
        * 'subprocess.run(["pipenv", "--python", "3.11"]) which will add a new virtual environment, or 
        * at the time of install with 'subprocess.run(["pipenv","install","<package>","--python","3.6"])
    * I looked hard for a way to identify the os specific site-packages path programmatically; still not there
    """


def test_pipenv_with_application_env():
    wheel = Wheel("etc/90210-v.6/dist/a90210-0.1.0-py3-none-any.whl")
    sdist = SDist("etc/90210-v.6/dist/a90210-0.1.0.tar.gz")

    assert wheel.name == sdist.name

    """pipenv will respect any existing virtual env"""
    subprocess.run(["pipenv", "install", wheel.filename])

    a90210 = importlib.import_module(wheel.name)
    mod_b = importlib.import_module(".mod_b", a90210.__name__)

    assert a90210.mod_a.hello().startswith("Hi there!")
    assert mod_b.sup().startswith("Sup... Hi there!")

    subprocess.run(["pipenv", "uninstall", a90210.__name__])

    pass


def test_pipenv_with_custom_virtual_env():
    """Set PIPENV_IGNORE_VIRTUALENVS and provide a location via fully qualified PIPENV_CUSTOM_VENV_NAME. Requires
    adding the 'site-packages' path in the custom virtual env to sys.path, which is a little os dependent; here we use the *nix style.
    """
    wheel = Wheel("etc/90210-v.6/dist/a90210-0.1.0-py3-none-any.whl")
    sdist = SDist("etc/90210-v.6/dist/a90210-0.1.0.tar.gz")

    assert wheel.name == sdist.name

    os.environ["PIPENV_IGNORE_VIRTUALENVS"] = "True"  # don't use existing env

    os.environ[
        "PIPENV_CUSTOM_VENV_NAME"
    ] = "/Users/pboisver/dev/code-red/blueberrypy_test/etc/pyshelf"
    sys.path.append("etc/pyshelf/lib/python3.10/site-packages")

    subprocess.run(["pipenv", "install", wheel.filename])

    a90210 = importlib.import_module("a90210")
    mod_b = importlib.import_module(".mod_b", a90210.__name__)

    assert a90210.mod_a.hello().startswith("Hi there!")
    assert mod_b.sup().startswith("Sup... Hi there!")

    subprocess.run(["pipenv", "--rm"])  # Entirely remove custom virtual environment

    pass


def test_pipenv_with_per_install_target():
    """Set a "target" on install using '--extra-pip-args "--target etc/targ"'. This path gets added to sys.paths.
    Doesn't (might?) allow multiple python versions
    """
    wheel = Wheel("etc/90210-v.6/dist/a90210-0.1.0-py3-none-any.whl")
    sdist = SDist("etc/90210-v.6/dist/a90210-0.1.0.tar.gz")

    assert wheel.name == sdist.name

    sys.path.append("etc/targ")  # works with '--target etc/targ'

    """Using '--target' for pip is a one way thing; neither pip not pipenv will be able to uninstall it completely. They may remove it from the Pipfile but not memory or the tartget folder which is on the sys.path. See manual cleanup below"""
    pip_process = subprocess.run(
        ["pipenv", "install", wheel.filename, "--extra-pip-args", "--target etc/targ"]
    )

    a90210 = importlib.import_module("a90210")
    mod_b = importlib.import_module(".mod_b", a90210.__name__)

    assert a90210.mod_a.hello().startswith("Hi there!")
    assert mod_b.sup().startswith("Sup... Hi there!")

    subprocess.run(["pipenv", "uninstall", wheel.name])  # try to uninstall

    assert importlib.reload(a90210)  # still works

    sys.path.remove("etc/targ")  # stop looking in target
    shutil.rmtree("etc/targ")  # delete the target folder

    with pytest.raises(ModuleNotFoundError):  # should throw exception now
        importlib.reload(a90210)

    pass
