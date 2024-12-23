from typing import Any

from sqlalchemy import URL, Column, Table
from sqlalchemy.sql.sqltypes import NullType
from sqlmodel import MetaData, create_engine


def lower_camel(s: str):
    if s == "date":
        return "date_"
    return s[0] + "".join([i.capitalize() for i in s.split("_")])[1:]


def upper_camel(s: str):
    return "".join([i.capitalize() for i in s.split("_")])


def define_import():
    print("from datetime import date, datetime")
    print("from decimal import Decimal")
    print("from typing import Optional")
    print()
    print(
        "from sqlalchemy import DATE, INTEGER, NUMERIC, TIMESTAMP, VARCHAR, Column, MetaData"
    )
    print("from sqlmodel import Field, SQLModel")
    print()


def define_class(table: Table):
    print(f"class {upper_camel(table.name)}(SQLModel, table=True):")
    print(f'    metadata = MetaData("{schema}")')
    print(f'    __tablename__ = "{table.name}"')


def define_field(column: Column[Any]):
    print(
        f"    {lower_camel(column.name)} : {define_field_type(column)} = {define_field_value(column)}"
    )


def define_field_type(column: Column[Any]):
    if type(column.type) == NullType:
        return f"Optional[str]"
    else:
        return f"Optional[{column.type.python_type.__name__}]"


def define_field_value(column: Column[Any]):
    if column.primary_key:
        return f'Field(sa_column=Column("{column.name}", {column.type}, default={column.default}, nullable={column.nullable}, primary_key={column.primary_key}, comment="{column.comment}"))'
    else:
        return f'Field(sa_column=Column("{column.name}", {column.type}, default={column.default}, nullable={column.nullable}, comment="{column.comment}"))'


url = URL.create("postgresql+psycopg", database="your_database")

engine = create_engine(
    url,
    echo=False,
)

schema = "public"

meta_data = MetaData(schema)

meta_data.reflect(engine, schema)

define_import()
for _, table in meta_data.tables.items():
    define_class(table)
    for column in table.columns:
        define_field(column)
