import json
from textwrap import dedent
from pathlib import Path


def infer_mysql_type(value):
    """
    استراتژی امن برای جلوگیری از Row too large:
    - str -> TEXT (خارج از صفحه)
    - list/dict -> JSON
    - bool -> TINYINT(1)
    - int -> BIGINT
    - float -> DOUBLE
    - None -> TEXT
    """
    if value is None:
        return "TEXT"
    if isinstance(value, bool):
        return "TINYINT(1)"
    if isinstance(value, int):
        return "BIGINT"
    if isinstance(value, float):
        return "DOUBLE"
    if isinstance(value, str):
        return "TEXT"
    if isinstance(value, (list, dict)):
        return "JSON"
    return "TEXT"


def generate_create_table(data: dict, table_name: str = "foodies") -> str:
    """Generate CREATE TABLE statement based on JSON structure."""
    columns = []
    for k, v in data.items():
        col_type = infer_mysql_type(v)
        if k == "id":
            col_def = f"`{k}` {col_type} NOT NULL"
        else:
            col_def = f"`{k}` {col_type} NULL"
        columns.append(col_def)

    create_stmt = (
        f"CREATE TABLE `{table_name}` (\n  "
        + ",\n  ".join(columns)
        + ",\n  PRIMARY KEY (`id`)\n)"
        + " ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"
    )
    return create_stmt


def main(json_file: str, sql_file: str = "create_table.sql"):
    # read JSON input
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # generate create table SQL
    create_stmt = generate_create_table(data)

    # save to .sql file
    Path(sql_file).write_text(create_stmt, encoding="utf-8")

    # print to terminal
    print(create_stmt)


if __name__ == "__main__":
    # Example: python script.py input.json
    import sys

    if len(sys.argv) < 2:
        print("Usage: python script.py <input.json> [output.sql]")
    else:
        json_file = sys.argv[1]
        sql_file = sys.argv[2] if len(sys.argv) > 2 else "create_table.sql"
        main(json_file, sql_file)


