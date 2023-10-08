from analysis.base import DefaultLanguage

# TODO: support import {...} on new line


class JSProcessor(DefaultLanguage):
    def __init__(self, DEBUG: bool = False, critical_threshold: int = 70) -> None:
        super().__init__(DEBUG, critical_threshold)
        self.skip_import = ['import']

    # sample: /* ...
    # sample: ... */
    def line_contains_notes_symbol(self, line):
        return line.find('/*') > -1 or line.find('*/') > -1

    # sample: /* ...
    # sample: // ...
    def line_is_single_comment(self, line):
        return line.startswith('//') or\
            self.line_starts_with_note(line) and self.line_ends_with_note(line)

    # sample: /* ...
    def line_starts_with_note(self, line):
        return line.startswith('/*')

    # sample: ...*/
    def line_ends_with_note(self, line):
        return line.endswith('*/') and line.rfind('*/') > 0

    def line_starts_multiline_text(self, line):
        return False
