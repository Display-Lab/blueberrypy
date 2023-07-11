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

    # importlib.import_module(spec.name)
    # importlib.import_module(".hello_with_import",spec.name) 
    spec.loader.exec_module(module)

    assert module.hello_with_import.sup() == "Sup... Hi there!"
    assert module.hello.hello() == "Hi there!"

    del modules[spec.name] # cleanup

def test_loading_parent_package_works():
    pspec = importlib.util.spec_from_file_location(
        "pack29", "etc/test_module/__init__.py"
    )
    pack = importlib.util.module_from_spec(pspec)
    modules[pspec.name] = pack
    pspec.loader.exec_module(pack)

    spec = importlib.util.spec_from_file_location(
        "pack29.mod42", "etc/test_module/hello_with_import.py"
    )
    module = importlib.util.module_from_spec(spec)
    modules[spec.name] = module
    spec.loader.exec_module(module)

    assert module.sup() == "Sup... Hi there!"
    assert pack.hello_with_import.sup() == "Sup... Hi there!"

    s = importlib.import_module("pack29.mod42")

    del modules[spec.name] # cleanup



def test_package_folder_name_not_matching():
    spec = importlib.util.spec_from_file_location("90210", "etc/pack_a/__init__.py")
    module = importlib.util.module_from_spec(spec)
    modules[spec.name] = module
    spec.loader.exec_module(module) # module='pack_a', this works; imports submodules declaratively
    # importlib.import_module('pack_a') # does not work
    # importlib.import_module('.mod_b',module.__name__) # works, also imports 'mod_a' transitively
    # importlib.import_module('pack_a.mod_b') # works the same, also imports 'mod_a'
    # importlib.import_module('pack_a.mod_a') # does not work, get 'mod_a' but not 'mod_b'

    assert module.mod_b.sup() == "Sup... Hi there!"
    assert module.mod_a.hello() == "Hi there!"

    importlib.reload(modules["90210.mod_b"])
    importlib.reload(modules["90210.mod_a"])

    assert module.mod_b.sup() == "Sup... Hi there!"
    assert module.mod_a.hello() == "Hi there!"

    del modules[spec.name] # cleanup


def test_package_folder_name_with_dots():
    spec = importlib.util.spec_from_file_location("pack_a", "etc/1.2.3/__init__.py")
    module = importlib.util.module_from_spec(spec)
    modules[spec.name] = module
    # spec.loader.exec_module(module) # module='pack_a', this works; imports submodules declaratively
    # importlib.import_module('pack_a') # does not work
    # importlib.import_module('.mod_b',module.__name__) # works, also imports 'mod_a' transitively
    foo = importlib.import_module('pack_a.mod_b') # works, same as above. 'foo' is a local alias for 'mod_b'
    # importlib.import_module('pack_a.mod_a') # does not work, gets 'mod_a' but not 'mod_b'

    assert module.mod_b.sup() == "Sup... Hi there!"
    assert module.mod_a.hello() == "Hi there!"
    assert foo.sup() == "Sup... Hi there!"

    importlib.reload(modules["pack_a.mod_b"])
    importlib.reload(modules["pack_a.mod_a"])

    assert module.mod_b.sup() == "Sup... Hi there!"
    assert module.mod_a.hello() == "Hi there!"

    del modules[spec.name] # cleanup
