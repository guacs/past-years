from pathlib import Path


class PastYearsError(Exception):
    """The base exception class for the application."""

    def __init__(self, msg: str) -> None:
        self.msg = msg
        super().__init__(msg)


class ConfigNotFoundError(PastYearsError):
    """Raised when the configuration file is not found."""

    def __init__(self, fp: str | Path) -> None:
        msg: str = f"Config file, {fp}, not found"
        super().__init__(msg)


class InvalidConfigFileError(PastYearsError):
    """Raised when the config file is invalid."""

    def __init__(self, msg: str, fp: str | Path) -> None:
        error_msg = f"Invalid config file: '{fp}'\nERROR: {msg}"
        super().__init__(error_msg)


class QuestionNotFoundError(PastYearsError):
    """Raised when a question is not found."""

    def __init__(self, question_id: str) -> None:
        self.question_id = question_id
        super().__init__(f"Question with id `{question_id}` was not found")
