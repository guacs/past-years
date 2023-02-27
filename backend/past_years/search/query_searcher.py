from __future__ import annotations

from typing import Protocol
from whoosh.index import open_dir
from whoosh.qparser import QueryParser, OrGroup, MultifieldParser
from whoosh import qparser


class QuerySearcherProtocol(Protocol):
    """Searcher that searches through documents
    based on user queries."""

    def search(self, query: str) -> set[str]:
        """Returns the IDs of the documents that satisfy
        the query."""
        ...


class WhooshSearcher(QuerySearcherProtocol):
    """A searcher that uses Whoosh as the underlying query
    search engine."""

    def __init__(
        self, index_dir: str, index_name: str, field_name: str | list[str]
    ) -> None:
        self._idx = open_dir(index_dir, index_name)

        if isinstance(field_name, str):
            parser = QueryParser
        else:
            parser = MultifieldParser

        self._qparser = parser(
            field_name, schema=self._idx.schema, group=OrGroup  # type: ignore
        )

        # Configuring the query parser
        self._qparser.add_plugin(
            qparser.WildcardPlugin(),
        )
        self._qparser.replace_plugin(qparser.OperatorsPlugin())

        self._total_docs = self._idx.doc_count()

    def search(self, query: str) -> set[str]:
        parsed_query = self._qparser.parse(query)

        with self._idx.searcher() as searcher:
            results = searcher.search(parsed_query, limit=self._total_docs)
            return {hit["id"] for hit in results}
