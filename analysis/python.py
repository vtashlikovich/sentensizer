import os

dir_skip_list = ['__pycache__', 'env', 'venv']
skip_import = ['import', 'from']

class PythonProcessor:
    def __init__(self, DEBUG: bool = False, critical_threshold: int = 70) -> None:
        self.errors_found = False
        self.DEBUG = DEBUG
        self.critical_threshold = critical_threshold
        pass

    def process_file(self, file_name: str, silent: bool = False):
        file_obj = open(file_name, 'r')
        counter = 0
        ignore_mode = False
        multiline_mode = False

        while line := file_obj.readline():
            line = line.strip()
            if self.DEBUG: print(f'>>> {line}')

            if ignore_mode:
                if self.line_contains_notes_symbol(line):
                    ignore_mode = False
            elif line:
                if multiline_mode and self.line_contains_notes_symbol(line):
                    multiline_mode = False
                    counter = self.process_line(counter, line, ignore_mode)
                elif not self.line_is_single_comment(line):
                    if not multiline_mode and self.line_starts_with_note(line):
                        if self.line_starts_multiline_text(line):
                            multiline_mode = True
                        else:
                            ignore_mode = True
                            continue
                    elif self.line_starts_multiline_text(line):
                        multiline_mode = True

                    counter = self.process_line(counter, line, ignore_mode)

        if not self.errors_found and counter >= self.critical_threshold:
            self.errors_found = True

        file_obj.close()

        return counter

    # sample: """ ...
    # sample: ... """
    def line_contains_notes_symbol(self, line):
        return line.find('"""') > -1 or line.find('\'\'\'') > -1

    # sample: """ ...
    # sample: # ...
    def line_is_single_comment(self, line):
        return line.startswith('#') or\
            self.line_starts_with_note(line) and self.line_ends_with_note(line)

    # sample: """ ...
    def line_starts_with_note(self, line):
        return line.startswith('"""') or line.startswith('\'\'\'')

    # sample: ..."""
    def line_ends_with_note(self, line):
        return line.endswith('"""') and line.rfind('"""') > 0 or line.endswith('\'\'\'') \
            and line.rfind('\'\'\'') > 0

    # sample: print( """ ...
    def line_starts_multiline_text(self, line):
        line = line.replace(' ', '')
        return line.find('(\'\'\'') > -1 or line.find('("""') > -1 or \
            line.find('[\'\'\'') > -1 or line.find('["""') > -1 or \
            line.find('{\'\'\'') > -1 or line.find('{"""') > -1 or \
            line.find('=\'\'\'') > -1 or line.find('="""') > -1

    def process_line(self, counter, line, ignore_mode):
        line_parsed = line.split(' ')
        if not ignore_mode and line_parsed[0] not in skip_import:
            if self.DEBUG: print('    .')
            counter += 1
        return counter