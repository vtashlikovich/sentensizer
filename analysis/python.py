from analysis.base import DefaultLanguage


class PythonProcessor(DefaultLanguage):
    def __init__(self, DEBUG: bool = False, critical_threshold: int = 70) -> None:
        super().__init__(DEBUG, critical_threshold)
        self.skip_import = ['import', 'from']

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
