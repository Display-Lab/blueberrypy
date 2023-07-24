
import pathlib
import urllib.parse
import urllib.request

import os

import pytest

@pytest.mark.skip("")
def test_is_path():
    resource = None
    
    assert os.path.isabs("/boo") == True
    
    url = urllib.parse.urlparse("boo")
    assert url.geturl() == "boo"
    
    assert  urllib.request.pathname2url("boo") == "boo"
    
    try: 
        resource = urllib.request.urlopen("boo")
    except ValueError as e:
        e.add_note("Can't open as url")
        file = pathlib.Path("boo").resolve()
        url = file.as_uri()

    try:
        resource = urllib.request.urlopen(url)
    except Exception as e:
        pass

    assert resource == ""