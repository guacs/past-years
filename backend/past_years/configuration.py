"""Holds the config related items."""
from __future__ import annotations
from copy import copy
import os
from pathlib import Path

from typing import Any, Generator, Literal, Type
from msgspec import Struct
import msgspec

from past_years.errors import ConfigNotFoundError, InvalidConfigFileError

_LogLevel = Literal["trace", "debug", "info", "success", "warning", "error", "critical"]

# ----- Config classes -----


class _APIConfig(Struct):
    """The configuration related to the API."""

    gh_repo_name: str
    gh_repo_owner: str
    allow_origins: list[str] = []


class _QuestionsConfig(Struct):
    """The configurations related to the questions."""

    whoosh_index_dir: Path
    """The path to the directory with the Whoosh index for the questions."""

    questions_fp: Path
    """The path to the directory/file with the PYQs."""

    questions_index_fp: Path
    """The path to the file with the questions index."""

    whoosh_questions_index_name: str = "questions"
    """The name of the Whoosh questions index."""

    whoosh_questions_field_name: str = "question"
    """The name of the field that's indexed in Whoosh."""

    def normalize_paths(self, fp: Path):
        """Normalizes all the relative paths into absolute paths."""

        self.questions_fp = _get_full_path(fp, self.questions_fp)
        self.questions_index_fp = _get_full_path(fp, self.questions_index_fp)
        self.whoosh_index_dir = _get_full_path(fp, self.whoosh_index_dir)


class _LogConfig(Struct):
    """The configurations related to logging."""

    format: str
    """The format of the log messge."""

    log_level: _LogLevel = "debug"
    """The log level. The levels are those found in Loguru."""

    serialize: bool = False
    """Indicates whether to serialize the logs to JSON or not."""

    sink: Path = Path(".")
    """The sink to which the logs are written to in addition to the
    stdout."""

    def normalize_path(self, fp: Path):
        """Normalizes all the relative paths into absolute paths."""

        self.sink = _get_full_path(fp, self.sink)


class _CommonConfig(Struct):
    """Common configurations in dev, test and prod modes."""

    questions: _QuestionsConfig
    logs: _LogConfig
    api: _APIConfig

    def normalize_paths(self, fp: Path):
        """Normalizes all the relative paths into absolute paths."""

        self.questions.normalize_paths(fp)
        self.logs.normalize_path(fp)


class _DevConfig(_CommonConfig):
    """The configurations for development."""


class _TestConfig(_CommonConfig):
    """The configurations for testing."""


class _ProdConfig(_CommonConfig):
    """The configurations for production."""


class _Config(Struct):
    """The configuration for the entire application.

    NOTE: This does NOT contain secrets such as API keys.
    """

    mode: Literal["dev", "test", "prod"]
    dev: _DevConfig
    prod: _ProdConfig
    test: _TestConfig

    def normalize_paths(self, fp: Path):
        self.dev.normalize_paths(fp)
        self.prod.normalize_paths(fp)
        self.test.normalize_paths(fp)

    def get_questions_config(self) -> _QuestionsConfig:
        """Returns the questions config based on the current mode."""

        return self._get_config().questions

    def get_logs_config(self) -> _LogConfig:
        """Returns the logs config based on the current mode."""

        return self._get_config().logs

    def get_api_config(self) -> _APIConfig:
        """Returns the API config based on the current mode."""

        return self._get_config().api

    def _get_config(self) -> _DevConfig | _ProdConfig | _TestConfig:
        """Gets the dev/prod/test config based on the current mode."""

        if self.mode == "dev":
            return self.dev
        if self.mode == "test":
            return self.test
        return self.prod

    @classmethod
    def load_config(
        cls: Type[_Config], file_path: Path | None = None, starting_path: str = __file__
    ) -> _Config:
        """Loads the configuration from the given file path.

        Args:
            file_path: The path to the configuration file.
                If the file path is not provided, a config file with the
                name `.config.toml` is searched for recursively upwards
                starting from the directory this file is in.

            starting_path: The path from which to start recursively
                looking for the config file.

        Returns:
            The configuration object.
        """

        file_path = file_path or _get_config_fp(starting_path=starting_path)
        file_bytes = file_path.read_bytes()
        try:
            config = msgspec.toml.decode(
                file_bytes, type=_Config, dec_hook=_path_dec_hook
            )
            config.normalize_paths(file_path.absolute())
            return config
        except msgspec.ValidationError as ex:
            raise InvalidConfigFileError(str(ex), file_path) from ex


# ----- Helpers -----


def _get_config_fp(
    config_file_name: str = ".config.toml", starting_path: str = __file__
) -> Path:
    """Gets the file path for the configuration file with the
    given filename.

    Args:
        config_file_name: The name of the configuration file.
        starting_path: The path from which to start recursively
            looking for the config file.
    """

    for fp in _walk_to_root(Path(starting_path)):
        for file_name in os.listdir(fp):
            if file_name == config_file_name:
                return fp / file_name

    raise ConfigNotFoundError(config_file_name)


def _walk_to_root(path: Path) -> Generator[Path, None, None]:
    """Recursively walks upto the root directory."""

    path = path if path.is_dir() else path.parent
    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist")

    curr_dir: Path = path
    root_dir: Path = Path(os.path.abspath(os.sep))
    while curr_dir != root_dir:
        yield curr_dir
        curr_dir = curr_dir.parent

    yield root_dir


def _get_full_path(absolute: Path, relative: Path) -> Path:
    """Returns the full path of the relative path based on the
    assumption that the relative path is relative to the
    given absolute path.

    Arguments:
        absolute: The absolute path used as the starting point
            in normalizing the relative path.
        relative: The path to normalize. If this is already
            a relative path, then no normalization is done
            and instead it is simply returned.

    Example:
        absolute = "/path/to/absolute/file"
        relative = "../relative/file"

        get_full_path(absolute, relative) # /path/to/relative/file
    """

    if relative.is_absolute():
        return relative

    assert absolute.is_absolute(), f"{absolute} must be absolute"

    full_path = copy(absolute)
    for fp in reversed(relative.parents):
        full_path /= fp.name
    full_path /= relative.name

    return full_path.resolve()


# ----- Msgspec Hooks -----


def _path_dec_hook(type: Type, obj: Any) -> Any:
    """A hook to convert strings into Path objects when decoding
    with Msgspec."""

    if type is Path and isinstance(obj, str):
        return Path(obj)

    raise TypeError(f"Objects of type {type} are not supported")


# The "singleton" configuration object
config = _Config.load_config()
