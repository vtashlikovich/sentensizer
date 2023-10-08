class DefaultLanguage:
    def __init__(self, DEBUG: bool = False, critical_threshold: int = 70) -> None:
        self.errors_found = False
        self.DEBUG = DEBUG
        self.critical_threshold = critical_threshold
        self.skip_import = []

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

    def process_line(self, counter, line, ignore_mode):
        line_parsed = line.split(' ')
        if not ignore_mode and line_parsed[0] not in self.skip_import:
            if self.DEBUG: print('    .')
            counter += 1
        return counter
