from pathlib import Path

sql_dir = Path(__file__).parent
sql_display_dir = sql_dir / "sql_display"
sql_download_dir = sql_dir / "sql_download"


def read_query_file(filename, /, download=False) -> str:
    if download:
        dir = sql_download_dir
    else:
        dir = sql_display_dir
    with open(dir / filename, mode="r", encoding="utf-8") as f:
        query = f.read()
    return query
