import os
from analysis.java import JavaProcessor
from analysis.python import PythonProcessor
from analysis.javascript import JSProcessor

# TODO: make this list configurable
dir_skip_list = ['__pycache__', 'env', 'venv', 'node_modules']

DEBUG = False
VERBOSE = False

# TODO: make it configurable
RED_THRESHOLD = 70
ORANGE_THRESHOLD = 50
ONLY_CRITICAL = False
errors_found = False
files_analyzed_num = 0
total_sentences_num = 0
critical_files = 0

python_processor = PythonProcessor(DEBUG=DEBUG, critical_threshold=RED_THRESHOLD)
js_processor = JSProcessor(DEBUG=DEBUG, critical_threshold=RED_THRESHOLD)
java_processor = JavaProcessor(DEBUG=DEBUG, critical_threshold=RED_THRESHOLD)


def analyze_single_file(file_name: str):
    global errors_found, files_analyzed_num, total_sentences_num, critical_files

    sentences_count = 0
    if file_name.endswith('.py'):
        sentences_count = python_processor.process_file(file_name)
        errors_found = not errors_found and python_processor.errors_found
        total_sentences_num += sentences_count
        files_analyzed_num += 1
    elif file_name.endswith('.js') or file_name.endswith('.ts'):
        sentences_count = js_processor.process_file(file_name)
        errors_found = not errors_found and js_processor.errors_found
        total_sentences_num += sentences_count
        files_analyzed_num += 1
    elif file_name.endswith('.java'):
        sentences_count = java_processor.process_file(file_name)
        errors_found = not errors_found and java_processor.errors_found
        total_sentences_num += sentences_count
        files_analyzed_num += 1
    else:
        if VERBOSE: print(f'...skip {file_name}')
        return None

    if not ONLY_CRITICAL: print(f'{file_name}', end=' ')
    if sentences_count >= RED_THRESHOLD:
        critical_files += 1
        if ONLY_CRITICAL: print(f'{file_name}', end=' ')
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
                file_path = os.path.join(path, item)
                if os.path.isfile(file_path):
                    analyze_single_file(file_path)
                else:
                    analyze_path(file_path)
        elif VERBOSE:
            print(f'..dir {cur_dir_name} is skipped')
    else:
        print(f"The path '{path}' does not exist.")
