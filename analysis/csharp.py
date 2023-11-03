from analysis.base import DefaultLanguage


class CSharpProcessor(DefaultLanguage):
    def __init__(self, DEBUG: bool = False, critical_threshold: int = 70) -> None:
        super().__init__(DEBUG, critical_threshold)
        self.skip_import = ['using']

