from . import mod_b
from . import mod_a as hi # allows a90210.hi.hello() afte import of a90210
# from a90210 import mod_b # this also works but is tied to the package name
# from . import mod_a # this is not necessary as mod_b imports mod_a