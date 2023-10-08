import os

dir_skip_list = ['__pycache__', 'env', 'venv']
skip_import = ['import', 'from']

DEBUG = False
VERBOSE = False
RED_THRESHOLD = 70
ORANGE_THRESHOLD = 50
ONLY_CRITICAL = False

errors_found = False

# TODO: extract Python analysis into separate class

def perform_python_analysis(file_name: str, silent: bool = False):
    global errors_found
    if not ONLY_CRITICAL and not silent and not DEBUG: print(f'analyze {file_name}', end=' ')
    if DEBUG: print(f'analyze {file_name}')

    file_obj = open(file_name, 'r')
    counter = 0
    ignore_mode = False
    multiline_mode = False

    while line := file_obj.readline():
        line = line.strip()
        if DEBUG: print(f'>>> {line}')

        if ignore_mode:
            if line_contains_notes_symbol(line):
                ignore_mode = False
        elif line:
            if multiline_mode and line_contains_notes_symbol(line):
                multiline_mode = False
                counter = process_py_line(counter, line, ignore_mode)
            elif not line_is_single_comment(line):
                if not multiline_mode and line_starts_with_note(line):
                    if line_starts_multiline_text(line):
                        multiline_mode = True
                    else:
                        ignore_mode = True
                        continue
                elif line_starts_multiline_text(line):
                    multiline_mode = True

                counter = process_py_line(counter, line, ignore_mode)

    if not errors_found and counter >= RED_THRESHOLD:
        errors_found = True

    if not silent:
        if counter >= RED_THRESHOLD:
            if ONLY_CRITICAL:
                print(f'analyze {file_name}', end = ' ')
            print(f'- \033[91m{counter}\033[00m')
        elif not ONLY_CRITICAL and counter >= ORANGE_THRESHOLD:
            print(f'- \033[93m{counter}\033[00m')
        elif not ONLY_CRITICAL:
            print(f'- \033[92m {counter}\033[00m')
    file_obj.close()

    return counter

def analyze_single_file(file_name: str):
    if file_name.endswith('.py'):
        return perform_python_analysis(file_name)
    elif VERBOSE:
        print(f'...skip {file_name}')

def analyze(path: str):
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
                    analyze(path + os.path.sep + item)

        elif VERBOSE:
            print(f'..dir {cur_dir_name} is skipped')
    else:
        print(f"The path '{path}' does not exist.")

# sample: """ ...
# sample: ... """
def line_contains_notes_symbol(line):
    return line.find('"""') > -1 or line.find('\'\'\'') > -1

# sample: """ ...
# sample: # ...
def line_is_single_comment(line):
    return line.startswith('#') or\
        line_starts_with_note(line) and line_ends_with_note(line)

# sample: """ ...
def line_starts_with_note(line):
    return line.startswith('"""') or line.startswith('\'\'\'')

# sample: ..."""
def line_ends_with_note(line):
    return line.endswith('"""') and line.rfind('"""') > 0 or line.endswith('\'\'\'') \
        and line.rfind('\'\'\'') > 0

# sample: print( """ ...
def line_starts_multiline_text(line):
    line = line.replace(' ', '')
    return line.find('(\'\'\'') > -1 or line.find('("""') > -1 or \
        line.find('[\'\'\'') > -1 or line.find('["""') > -1 or \
        line.find('{\'\'\'') > -1 or line.find('{"""') > -1 or \
        line.find('=\'\'\'') > -1 or line.find('="""') > -1

def process_py_line(counter, line, ignore_mode):
    line_parsed = line.split(' ')
    if not ignore_mode and line_parsed[0] not in skip_import:
        if DEBUG: print('    .')
        counter += 1
    return counter