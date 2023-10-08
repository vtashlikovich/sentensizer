import pytest
import analyzer as az

PATH = 'test_files/python/'

# @pytest.mark.skip
@pytest.mark.parametrize("file_name, result",[
    (PATH + 'comments.py', 6),
    (PATH + 'class.py', 11),
    (PATH + 'main.py', 4),
    (PATH + 'dict.py', 23),
    (PATH + 'loggingconf.py', 36),
    (PATH + 'print.py', 4),
    (PATH + 'model.py', 40),
    ])
def test_python(file_name, result):
    az.DEBUG = True
    statements = az.perform_python_analysis(file_name, silent=True)
    assert statements == result