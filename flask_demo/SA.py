from sqlalchemy import *
import sqlalchemy.util as util
import string,sys
from sqlalchemy.databases import mysql

mysql_engine = create_engine("mysql://root:root@localhost/ryan")
#"mysql://username:passwd@host/database_name"
metadata = MetaData()
user_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(20), nullable=False),
    Column("passwd", String(20), nullable=False),
    mysql_engine = "InnoDB"
)
metadata.create_all(mysql_engine)
