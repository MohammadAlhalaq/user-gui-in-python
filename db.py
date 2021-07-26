import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_user(conn, user):
    """
    Create a new user
    :param conn:
    :param user:
    :return:
    """

    sql = ''' INSERT INTO users(name, birthday, address, age)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid


def main():
    database = r"C:\sqlite\db\pythonsqlite.db"

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        birthday text,
                                        address text,
                                        age integer
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create users table
        create_table(conn, sql_create_users_table)

    else:
        print("Error! cannot create the database connection.")

     # users
    user_1 = ('mohammad', '2015-01-01', 'Gaza', 15)
    user_2 = ('Ahmed', '2015-01-03', 'Khaniuones', 16)

    # create users
    create_user(conn, user_1)
    create_user(conn, user_2)


if __name__ == '__main__':
    main()
