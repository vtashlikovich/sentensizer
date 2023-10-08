import pytest
from analysis.python import PythonProcessor

PATH = 'test_files/python/'


@pytest.fixture
def python_processor():
    return PythonProcessor()


# @pytest.mark.skip
@pytest.mark.parametrize("file_name, result", [
    (PATH + 'comments.py', 6),
    (PATH + 'class.py', 11),
    (PATH + 'main.py', 4),
    (PATH + 'dict.py', 23),
    (PATH + 'loggingconf.py', 36),
    (PATH + 'print.py', 4),
    (PATH + 'model.py', 40)])
def test_python(file_name, result, python_processor):
    statements = python_processor.process_file(file_name, silent=True)
    assert statements == result
