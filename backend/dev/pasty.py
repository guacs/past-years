"""The CLI for the dev tools for the website."""

import os
from pathlib import Path
from typing import Iterable

import click
import msgspec
from index import create_questions_index, create_whoosh_index

from dev.db import delete_table, reset_user_table
from dev.random_data import RandomQuestionGenerator
from past_years.configuration import _Config, _LogLevel
from past_years.errors import InvalidConfigFileError
from past_years.utils import configure_logger

# ----- Global Values -----
logger_configured: bool = False

# ----- Commands -----


@click.group()
@click.pass_context
@click.option("--config", "-c", help="The path to the config file.")
@click.option(
    "-v",
    "--verbosity",
    count=True,
    help="The verbosity level. This can be repeated for increased verbosity.",
)
def run(ctx: click.Context, config: str, verbosity: int):
    """Dev tools for the Past Years website."""

    config_fp = None
    if config:
        config_fp = Path(config)
        if not config_fp.exists():
            click.secho("ERROR: Config file not found", fg="red")
            ctx.abort()

    try:
        config_obj = _Config.load_config(config_fp)
        _configure_logger(verbosity, config_obj)
        ctx.obj = config_obj
    except InvalidConfigFileError as ex:
        click.secho(f"ERROR: {ex.msg}", fg="red")
        ctx.abort()


# ----- Index related commands -----


@run.group()
@click.option(
    "-v",
    "--verbosity",
    count=True,
    help="The verbosity level. This can be repeated for increased verbosity.",
)
def index(verbosity: int):
    """Indexes the questions."""

    _configure_logger(verbosity)


@index.command()
@click.option(
    "--questions-fp", help="The path to the file/directory with the questions."
)
@click.option("--index-fp", help="The filepath to where the index is stored.")
@click.option(
    "-v",
    "--verbosity",
    count=True,
    help="The verbosity level. This can be repeated for increased verbosity.",
)
def questions(verbosity: int, questions_fp: str | Path, index_fp: str | Path):
    """Indexes the questions (NOT Whoosh)."""

    _configure_logger(verbosity)

    config = _get_config()
    questions_config = config.get_questions_config()
    questions_fp = questions_fp or questions_config.questions_fp
    index_fp = index_fp or questions_config.questions_index_fp
    create_questions_index(questions_fp, index_fp)
    click.secho("Indexed questions successfully!", fg="green")


@index.command()
@click.option(
    "--questions-fp", help="The path to the file/directory with the questions."
)
@click.option("--index-fp", help="The filepath to where the index is stored.")
@click.option("--index-name", help="The name to give the index.")
@click.option("-r", "--reset", is_flag=True)
@click.option(
    "-v",
    "--verbosity",
    count=True,
    help="The verbosity level. This can be repeated for increased verbosity.",
)
def whoosh(
    questions_fp: str | Path,
    index_fp: str | Path,
    index_name: str,
    reset: bool,
    verbosity: int,
):
    """Indexes the questions with Whoosh."""

    _configure_logger(verbosity)

    config = _get_config()
    questions_config = config.get_questions_config()

    questions_fp = questions_fp or questions_config.questions_fp
    index_fp = index_fp or questions_config.whoosh_index_dir
    index_name = index_name or questions_config.whoosh_questions_index_name

    create_whoosh_index(index_fp, questions_fp, index_name, reset)
    click.secho("Created the index successfully!", fg="green")


# ----- Database related commands -----
@run.group
@click.option("--username", "-u", help="The username to connect to the database.")
@click.option("--password", "-p", help="The password to connect to the database.")
def db(username: str | None, password: str | None):
    """All commands related to the MySQL database."""

    if username:
        os.environ.setdefault("PAST_YEARS_DB_USERNAME", username)
    if password:
        os.environ.setdefault("PAST_YEARS_DB_PWD", password)


@db.command(name="reset")
@click.argument("table-name", type=click.Choice(("users",)))
def reset_table(table_name: str):
    """Resets the given table."""

    if table_name == "users":
        reset_user_table()

    click.secho(f"Reset the `{table_name}` table :)", fg="green")


@db.command
@click.argument("table-names", nargs=-1)
@click.confirmation_option("--yes", "-y")
def drop(table_names: Iterable[str]):
    """Drops the table for all the given tables."""

    for name in table_names:
        delete_table(name)
        click.secho(f"Deleted the `{name}` table", fg="magenta")

    click.secho("Deleted all the tables :)", fg="green")


# ----- Miscellaneous -----


@run.command(name="random")
@click.option("--total-questions", "-t", type=int, default=1000)
@click.option(
    "--population",
    "-p",
    help="The JSON file that holds the data to be used for making random questions.",
)
def random_data(total_questions: int, population: str | None):
    population = population or ""
    question_generator = RandomQuestionGenerator(total_questions, population)
    questions_bytes = msgspec.json.encode(list(question_generator.create_questions()))

    # Saving the questions
    config = _get_config().get_questions_config()
    questions_fp = Path(config.questions_fp)
    questions_fp.write_bytes(questions_bytes)

    click.secho("Created and saved the questions!", fg="green")


# ----- Helpers -----
def _get_config() -> _Config:
    """Returns the configuration from the current context."""

    config = click.get_current_context().obj

    assert isinstance(config, _Config)
    return config


def _configure_logger(log_level: int, config: _Config | None = None):
    """A helper to configure the logger.

    This is required as a workaround to the following issue:
    https://github.com/pallets/click/issues/108
    """

    global logger_configured

    if not log_level:
        # This is to ensure that the logger is configured only
        # once
        if logger_configured:
            return
        logger_configured = True

    config = config or _get_config()
    log_config = config.get_logs_config()
    log_config.log_level = _get_log_level(log_level)
    configure_logger(log_config)


def _get_log_level(log_level: int) -> _LogLevel:
    """Returns the log level as a string based on the given
    log level."""

    if log_level >= 3:
        return "trace"
    if log_level == 2:
        return "debug"
    return "info"


if __name__ == "__main__":
    run()
