from . import mod_a
# from test_module import hello

def sup():
    return "Sup... " + mod_a.hello()

if __name__ == '__main__':
    print(sup())