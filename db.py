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


def create_user_test(conn, userTest):
    """
    Create a new user_test
    :param conn:
    :param user:
    :return:
    """

    sql = ''' INSERT INTO user_tests(
        name, 
        birthday, 
        address, 
        date_for_cbc,
        wbc,
        "ly%",
        "mo%",
        "gr%",
        ly,
        mo,
        gr,
        rbc,
        hbg,
        gct,
        mcv,
        mch,
        mchc,
        plt,
        pct,
        mpv,
        pdw,
        unnoun,
        unnoun2
    )
        VALUES(? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,?) '''
    cur = conn.cursor()
    cur.execute(sql, userTest)
    conn.commit()
    return cur.lastrowid


def update_user_test(conn, userTest):
    """
    update name and birthday address of a userTest
    :param conn:
    :param userTest:
    :return: project id
    """
    sql = ''' UPDATE user_tests
              SET "name" = ? ,
                  "address" = ? ,
                  "birthday" = ?,
                  "date_for_cbc" = ?,
                  "wbc" = ?,
                  "ly%" = ?,
                  "mo%" = ?,
                  "gr%" = ?,
                  "ly" = ?,
                  "mo" = ?,
                  "gr" = ?,
                  "rbc" = ?,
                  "hbg" = ?,
                  "gct" = ?,
                  "mcv" = ?,
                  "mch" = ?,
                  "mchc" = ?,
                  "plt" = ?,
                  "pct" = ?,
                  "mpv" = ?,
                  "pdw" = ?,
                  "unnoun" = ?,
                  "unnoun2" = ?,
              WHERE test_id = ?'''
    cur = conn.cursor()
    cur.execute(sql, userTest)
    conn.commit()


def main():
    database = r"C:\sqlite\db\pythonsqlitek.db"
    # {
    #      1:  test_id,
    #      5:  date_for_cbc,
    #      6:  wbc,
    #      7:  ly%,
    #      8:  mo%,
    #      9:  gr%,
    #      10: ly,
    #      11: mo,
    #      12: gr,
    #      13: rbc,
    #      14: hbg,
    #      15: gct,
    #      16: mcv,
    #      17: mch,
    #      18: mchc,
    #      19: plt,
    #      20: pct,
    #      21: mpv,
    #      22: pdw,
    #      23: unnoun,
    #      24: unnoun2
    # }

    sql_create_user_tests_table = """ CREATE TABLE IF NOT EXISTS user_tests (
                                        test_id INTEGER PRIMARY KEY,
                                        name text NOT NULL,
                                        birthday TEXT,
                                        address TEXT,
                                        date_for_cbc TEXT,
                                        wbc TEXT,
                                        "ly%" TEXT,
                                        "mo%" TEXT,
                                        "gr%" TEXT,
                                        ly TEXT,
                                        mo TEXT,
                                        gr TEXT,
                                        rbc TEXT, 
                                        hbg TEXT,
                                        gct TEXT,
                                        mcv TEXT,
                                        mch TEXT,
                                        mchc TEXT,
                                        plt TEXT,
                                        pct TEXT,
                                        mpv TEXT,
                                        pdw TEXT,
                                        unnoun TEXT,
                                        unnoun2 TEXT
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create user_tests table
        create_table(conn, sql_create_user_tests_table)

    else:
        print("Error! cannot create the database connection.")

     # user_test
    user_test_1 = ('husin', '22-01-1999', 'Gaza', "21-12-1", "11", "22", "33",
                   "44", "55", "66", "77", "88", "99", "10", "11", "12", "13", "14", "15", "16", "33", "44", "44")

    # user_2 = ('hassan', '22-01-1999', 'Khaniuones', "21-12-1", "11", "22", "33",
    #           "44", "55", "66", "77", "88", "99", "10", "11", "12", "13", "14", "15", "16", "33", "44", "44")
    # user_3 = ('husin', '22-01-1999', 'Gaza', "21-12-1", "11", "22", "33",
    #           "44", "55", "66", "77", "88", "99", "10", "11", "12", "13", "14", "15", "16")
    # user_4 = ('hassan', '22-01-1999', 'Khaniuones', "21-12-1", "11", "22", "33",
    #           "44", "55", "66", "77", "88", "99", "10", "11", "12", "13", "14", "15", "16", "33", "44", "44")
    # user_5 = ('husin', '22-01-1999', 'Gaza', "21-12-1", "11", "22", "33",
    #           "44", "55", "66", "77", "88", "99", "10", "11", "12", "13", "14", "15", "16")
    # user_6 = ('hassan', '22-01-1999', 'Khaniuones', "21-12-1", "11", "22", "33",
    #           "44", "55", "66", "77", "88", "99", "10", "11", "12", "13", "14", "15", "16", "33", "44", "44")
    # user_7 = ('husin', '22-01-1999', 'Gaza', "21-12-1", "11", "22", "33",
    #           "44", "55", "66", "77", "88", "99", "10", "11", "12", "13", "14", "15", "16")
    # user_8 = ('hassan', '22-01-1999', 'Khaniuones', "21-12-1", "11", "22", "33",
    #           "44", "55", "66", "77", "88", "99", "10", "11", "12", "13", "14", "15", "16", "33", "44", "44")
    # user_9 = ('husin', '22-01-1999', 'Gaza', "21-12-1", "11", "22", "33",
    #           "44", "55", "66", "77", "88", "99", "10", "11", "12", "13", "14", "15", "16", "33", "44", "44")
    # user_10 = ('hassan', '22-01-1999', 'Khaniuones', "21-12-1", "11", "22", "33",
    #            "44", "55", "66", "77", "88", "99", "10", "11", "12", "13", "14", "15", "16", "33", "44", "44")

    # create users
    create_user_test(conn, user_test_1)
    # create_user_test(conn, user_2)
    # create_user_test(conn, user_3)
    # create_user_test(conn, user_4)
    # create_user_test(conn, user_5)
    # create_user_test(conn, user_6)
    # create_user_test(conn, user_7)
    # create_user_test(conn, user_8)
    # create_user_test(conn, user_9)
    # create_user_test(conn, user_10)


if __name__ == '__main__':
    main()
