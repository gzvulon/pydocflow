"""
## Overview

Sample for working with postgress via sqlalchemy

## Links

- https://www.compose.com/articles/using-json-extensions-in-postgresql-from-python-2/
- https://www.a2hosting.com/kb/developer-corner/postgresql/connecting-to-postgresql-using-python
- https://www.postgresqltutorial.com/postgresql-json/
- https://chartio.com/resources/tutorials/how-to-execute-raw-sql-in-sqlalchemy/

"""

import json
import sqlalchemy

from sqlalchemy import Column, Integer, Text, String
from sqlalchemy.dialects.postgresql import JSON, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


connection_string = 'postgresql://postgres:ASDqwe123@35.245.212.10'


db = sqlalchemy.create_engine(connection_string)
engine = db.connect()

def first():
    meta = sqlalchemy.MetaData(engine)

    j_table = sqlalchemy.Table("jsontable", meta,
                    Column('id', Integer),
                    Column('name', Text),
                    Column('email', Text),
                    Column('doc', JSON))
    meta.create_all()

    meta = sqlalchemy.MetaData(engine)
    result = engine.execute("SELECT 1")
    print(result.rowcount)

    statement = j_table.insert().values(
            id=3,
            name="Mr. Params",
            email="use@params.com",
            doc={
                "dialect": "params",
                "address": {"street": "Main St.", "zip": 12345},
            },
        )
    engine.execute(statement)
    print(str(statement))

    find_user = j_table.select().where(j_table.c.name == "Mr. Params")
    one = engine.execute(find_user).fetchone()
    return one

# FROM jsontable
"""
install-postgres-errors:
    url: https://stackoverflow.com/questions/11618898/pg-config-executable-not-found
"""

def second():
    db = sqlalchemy.create_engine(connection_string)
    engine = db.connect()

    Base = declarative_base()
    class User(Base):
        __tablename__ = 'jsontable2'
        id = Column(Integer, primary_key=True)
        # id = Column(Integer, primary_key=True)
        name = Column(Text)
        email = Column(Text)
        doc = Column(JSON)

    Base.metadata.create_all(engine)
    SessionFactory = sessionmaker(engine)

    session = SessionFactory()
    u = User(
        id=3,
        name="Oscar ORM",
        email="me@orms.com",
        doc={"address": {"zip": 5678, "street": "Cross St."}})
    session.add(u)
    session.commit()

    uu = session.query(User).filter(User.id == 3).one()
    return uu

def third():
    _q = """
    SELECT doc -> 'dialect' as dialect FROM jsontable WHERE
        CAST (
            doc -> 'address' ->> 'zip' AS INTEGER
        ) = 12345
    """
    with engine.connect() as con:
        rs = con.execute(_q)
    return list(str(r) for r in rs)



