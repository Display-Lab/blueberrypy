import importlib.util
from sys import modules


def test_hello_works():
    module_spec = importlib.util.spec_from_file_location(
        "hello", "etc/test_module/hello.py"
    )
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)

    assert module.hello() == "Hi there!"


def test_basic_relative_import_works():
    spec = importlib.util.spec_from_file_location(
        "mod42", "etc/test_module/__init__.py"
    )
    module = importlib.util.module_from_spec(spec)
    modules[spec.name] = module
    importlib.import_module(spec.name)

    spec.loader.exec_module(module)

    assert module.hello_with_import.sup() == "Sup... Hi there!"


