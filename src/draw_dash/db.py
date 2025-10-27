import os

import duckdb

from draw_dash.constant import PATH_ROOT

# Path constants.
PATH_DATA = PATH_ROOT / "data"


def initialise_db():
    duckdb.read_csv(PATH_DATA / "marketing.csv").create_view("marketing")
