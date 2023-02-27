from pathlib import Path


class IndexExistsError(Exception):
    def __init__(self, index_name: str, fp: str | Path):
        self.msg = f"Whoosh index, {index_name}, already exists at '{fp}'"
        super().__init__(self.msg)
