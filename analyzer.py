import os

dir_skip_list = ['__pycache__', 'env', 'venv']
skip_import = ['import', 'from']

DEBUG = False
VERBOSE = False

def perform_python_analysis(file_name: str):
    if not DEBUG: print(f'analyze {file_name}', end=' ')
    if DEBUG: print(f'analyze {file_name}')
    # loop through file

    file_obj = open(file_name, 'r')
    counter = 0
    ignore_mode = False

    while line := file_obj.readline():
        line = line.strip()
        if DEBUG: print(f'>>> {line}')

        if ignore_mode:
            if line_contains_notes_symbol(line):
                ignore_mode = False
        else:
            if line and not line_is_comment(line):
                if line_starts_with_note(line):
                    if not line_ends_with_note(line):
                        ignore_mode = True
                    continue

                line_parsed = line.split(' ')
                if not ignore_mode and line_parsed[0] not in skip_import:
                    if DEBUG: print('    .')
                    counter += 1

    print(f'- {counter}')
    file_obj.close()

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

def line_contains_notes_symbol(line):
    return line.find('"""') > -1 or line.find('\'\'\'') > -1

def line_is_comment(line):
    return line.startswith('#')

def line_starts_with_note(line):
    return line.startswith('"""') or line.startswith('\'\'\'')

def line_ends_with_note(line):
    return line.endswith('"""') or line.endswith('\'\'\'')