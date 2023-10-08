import os
from analysis.python import PythonProcessor

dir_skip_list = ['__pycache__', 'env', 'venv']
skip_import = ['import', 'from']

DEBUG = False
VERBOSE = False

RED_THRESHOLD = 70
ORANGE_THRESHOLD = 50
ONLY_CRITICAL = False
errors_found = False

python_processor = PythonProcessor(DEBUG=DEBUG, critical_threshold=RED_THRESHOLD)

def analyze_single_file(file_name: str):
    global errors_found

    sentences_count = 0
    if file_name.endswith('.py'):
        sentences_count = python_processor.process_file(file_name)
        errors_found = not errors_found and python_processor.errors_found
    elif VERBOSE:
        print(f'...skip {file_name}')
        return None

    if not ONLY_CRITICAL: print(f'{file_name}', end = ' ')
    if sentences_count >= RED_THRESHOLD:
        if ONLY_CRITICAL: print(f'{file_name}', end = ' ')
        print(f'- \033[91m{sentences_count}\033[00m')
    elif not ONLY_CRITICAL:
        if sentences_count >= ORANGE_THRESHOLD:
            print(f'- \033[93m{sentences_count}\033[00m')
        else:
            print(f'- \033[92m {sentences_count}\033[00m')

    return sentences_count

def analyze_path(path: str):
    if os.path.isfile(path):
        analyze_single_file(path)
    elif os.path.exists(path):
        cur_dir_name = os.path.dirname(path).split(os.path.sep)[-1]
        if cur_dir_name not in dir_skip_list and not cur_dir_name.startswith('.'):
            if VERBOSE: print(f'dir {cur_dir_name}')

            for item in os.listdir(path):
                if os.path.isfile(os.path.join(path, item)):
                    analyze_single_file(path + os.path.sep + item)
                else:
                    analyze_path(path + os.path.sep + item)
        elif VERBOSE:
            print(f'..dir {cur_dir_name} is skipped')
    else:
        print(f"The path '{path}' does not exist.")