import os

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from past_years.auth.token_service import TokenServiceMySql
from past_years.configuration import config
from past_years.db.db import MySqlDB
from past_years.db.users_db import UsersDBMySql
from past_years.github.gh_client import GithubClient
from past_years.incorrect.incorrect_question import IncorrectQuestionsHandler
from past_years.search.query_searcher import WhooshSearcher
from past_years.search.question_bank import QuestionBank
from past_years.search.search_engine import QuestionSearchEngine


class DepsContainer(DeclarativeContainer):

    wiring_config = WiringConfiguration(modules=["past_years.api.app"])

    # Search Engine dependencies
    question_bank = providers.Singleton(
        QuestionBank,
        questions_fp=config.get_questions_config().questions_fp,
        questions_idx=config.get_questions_config().questions_index_fp,
    )
    query_searcher = providers.Singleton(
        WhooshSearcher,
        config.get_questions_config().whoosh_index_dir,
        config.get_questions_config().whoosh_questions_index_name,
        config.get_questions_config().whoosh_questions_field_name,
    )
    search_engine = providers.Singleton(
        QuestionSearchEngine, question_bank=question_bank, query_searcher=query_searcher
    )

    # Database dependencies
    db = providers.Singleton(
        MySqlDB,
        db_name=config.get_db_config().db_name,
        host=config.get_db_config().host,
    )
    users_db = providers.Singleton(UsersDBMySql, db=db)
    token_service = providers.Singleton(TokenServiceMySql, db=db)

    # Other dependencies
    gh_client = providers.Singleton(
        GithubClient,
        pat=os.environ["GH_ISSUES_PAT"],
        repo=config.get_api_config().gh_repo_name,
        owner=config.get_api_config().gh_repo_owner,
    )
    incorrect_qstn = providers.Singleton(IncorrectQuestionsHandler, gh_client=gh_client)
