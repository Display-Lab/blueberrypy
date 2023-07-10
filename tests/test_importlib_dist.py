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
    foo = importlib.import_module(".mod_b",spec.name)

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
    mod_b = importlib.import_module(".mod_b",a90210.__name__)

    assert a90210.mod_a.hello().startswith("Hi there!")
    assert mod_b.sup().startswith("Sup... Hi there!")

    # clean up
    completed_process = subprocess.run(
        ["python", "-m", "pip", "uninstall", "-y", "a90210"]
    )


def test_venv_with_install():
    wheel = Wheel("etc/90210-v.6/dist/a90210-0.1.0-py3-none-any.whl")
    sdist = SDist("etc/90210-v.6/dist/a90210-0.1.0.tar.gz")

    assert wheel.name == sdist.name

    sys.path.append("etc/targ")
    # venv_process = venv.create(env_dir="etc/venv", clear=True)
    os.environ['WORKON_HOME'] = "etc/venv"
    os.environ['PIPENV_IGNORE_VIRTUALENVS'] = "True"

    # pip_process = subprocess.run(
    #     [
    #         "python",
    #         "-m",
    #         "pip",
    #         "install",
    #         "--target",
    #         "etc/targ",
    #         wheel.filename,
    #         "--force-reinstall",
    #     ],
    #     capture_output=True
    # )

    pip_process = subprocess.run(
        [
            "pipenv",
            "install",
            wheel.filename,
        ],
        capture_output=True
    )

    a90210 = importlib.import_module("a90210")
    mod_b = importlib.import_module(".mod_b",a90210.__name__)

    assert a90210.mod_a.hello().startswith("Hi there!")
    assert mod_b.sup().startswith("Sup... Hi there!")

    pass

'''
b"Installing etc/90210-v.6/dist/a90210-0.1.0-py3-none-any.whl...\nResolving etc/90210-v.6/dist/a90210-0.1.0-py3-none-any.whl...\nAdding a90210 to Pipfile's [packages] ...\n\xe2\x9c\x94 Installation Succeeded\nInstalling dependencies from Pipfile.lock (11d2a4)...\nTo activate this project's virtualenv, run pipenv shell.\nAlternatively, run a command inside the virtualenv with pipenv run.\n"'''