from pymysql import connect, cursors
import os


def database(database_name, user, passwd, host, port=3306):
    return connect(
        db=database_name,
        user=user,
        passwd=passwd,
        host=host,
        port=port,
        cursorclass=cursors.DictCursor)


def query(connection, statement, params=None):
    with connection.cursor() as c:
        if params is not None:
            c.execute(statement, params)
        else:
            c.execute(statement)
        for row in c:
            yield row


def execute(connection, statement, params=None):
    with connection.cursor() as c:
        if params is not None:
            c.execute(statement, params)
        else:
            c.execute(statement)
        connection.commit()


def factory_conexao():
    return database(
        os.environ.get("DB"),
        os.environ.get("USERDB"),
        os.environ.get("PASS"),
        os.environ.get("HOST"),
    )
