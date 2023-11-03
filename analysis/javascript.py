from analysis.base import DefaultLanguage

# TODO: support import {...} on new line


class JSProcessor(DefaultLanguage):
    def __init__(self, DEBUG: bool = False, critical_threshold: int = 70) -> None:
        super().__init__(DEBUG, critical_threshold)
        self.skip_import = ['import']

