import os
from pathlib import Path

import duckdb

# Path constants.
PATH_ROOT = Path(os.path.dirname(__file__)) / ".." / ".."
PATH_DATA = PATH_ROOT / "data"


def initialise_db():
    duckdb.read_csv(PATH_DATA / "marketing.csv").create_view("marketing")
