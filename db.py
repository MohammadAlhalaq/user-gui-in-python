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
        identification,
        sex,
        date_for_cbc,
        test_id,
        wbc,
        "ly%",
        "mo%",
        "gr%",
        ly,
        mo,
        gr,
        rbc,
        hgb,
        hct,
        mcv,
        mch,
        mchc,
        rdw,
        plt,
        pct,
        mpv,
        pdw
    )
        VALUES(? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,?) '''
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
                  "identification" = ?,
                  "sex" = ?,
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
                  "hgb" = ?,
                  "hct" = ?,
                  "mcv" = ?,
                  "mch" = ?,
                  "mchc" = ?,
                  "rdw" = ?,
                  "plt" = ?,
                  "pct" = ?,
                  "mpv" = ?,
                  "pdw" = ?,
              WHERE test_id = ?'''
    cur = conn.cursor()
    cur.execute(sql, userTest)
    conn.commit()


def main():
    database = "pythonsqlitek.db"
    # {
    #      3:  date_for_cbc,
    #      4:  test_id,
    #      5:  wbc,
    #      6:  ly%,
    #      7:  mo%,
    #      8:  gr%,
    #      9: ly,
    #      10: mo,
    #      11: gr,
    #      12: rbc,
    #      13: hgb,
    #      14: hct,
    #      15: mcv,
    #      16: mch,
    #      17: mchc,
    #      18: rdw,
    #      19: plt,
    #      20: pct,
    #      21: mpv,
    #      22: pdw
    # }

    sql_create_user_tests_table = """ CREATE TABLE IF NOT EXISTS user_tests (
                                        id INTEGER PRIMARY KEY,
                                        name text NOT NULL,
                                        birthday TEXT,
                                        address TEXT,
                                        identification TEXT,
                                        sex TEXT,
                                        date_for_cbc TEXT,
                                        test_id INTEGER,
                                        wbc TEXT,
                                        "ly%" TEXT,
                                        "mo%" TEXT,
                                        "gr%" TEXT,
                                        ly TEXT,
                                        mo TEXT,
                                        gr TEXT,
                                        rbc TEXT, 
                                        hgb TEXT,
                                        hct TEXT,
                                        mcv TEXT,
                                        mch TEXT,
                                        mchc TEXT,
                                        rdw TEXT,
                                        plt TEXT,
                                        pct TEXT,
                                        mpv TEXT,
                                        pdw TEXT
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create user_tests table
        create_table(conn, sql_create_user_tests_table)
        #user_test_1 = ('', '', '', "21-12-1", "11", "22", "33",
        #           "44", "55", "66", "77", "88", "99", "10", "11", "12", "13", "14", "15", "14", "15")
        #create_user_test(conn, user_test_1)
        user_2 = ('hassan', '22-01-1999', 'Khaniuones', "7847347893478", "male", "21-12-1", "211","11",  "22", "22", "33","44", "55", "66", "77", "88", "10", "11", "12", "13", "14", "15", "16", "33", "44")
        user_3 = ('hassan', '22-01-1999', 'Khaniuones', "7847347893478", "male", "21-12-1", "2112","11",  "22","22",  "33","44", "55", "66", "77", "88", "10", "11", "12", "13", "14", "15", "16", "33", "44")

        user_4 = ('hassan', '22-01-1999', 'Khaniuones', "7847347893478", "male", "21-12-1", "21113","11",  "22", "33","44", "55", "66", "77", "88", "10", "11", "12", "13", "14", "15", "16", "22", "33", "44")

        user_5 = ('hassan', '22-01-1999', 'Khaniuones', "7847347893478", "male", "21-12-1", "299","11",  "22", "33","44", "55", "66", "77", "88", "10", "11", "12", "13", "14", "15", "16", "33", "22", "44")

        user_6 = ('hassan', '22-01-1999', 'Khaniuones', "7847347893478", "male", "21-12-1", "212","11",  "22","22", "33","44", "55", "66", "77", "88", "10", "11", "12", "13", "14", "15", "16", "33", "44")

        user_7 = ('hassan', '22-01-1999', 'Khaniuones', "7847347893478", "male", "21-12-1", "2110","11",  "22","22", "33","44", "55", "66", "77", "88", "10", "11", "12", "13", "14", "15", "16", "33", "44")

        user_8 = ('hassan', '22-01-1999', 'Khaniuones', "7847347893478", "male", "21-12-1", "2111","11",  "22", "22","33","44", "55", "66", "77", "88", "10", "11", "12", "13", "14", "15", "16", "33", "44")

        user_9 = ('hassan', '22-01-1999', 'Khaniuones', "7847347893478", "male", "21-12-1", "2119","11",  "22", "22","33","44", "55", "66", "77", "88", "10", "11", "12", "13", "14", "15", "16", "33", "44")

        user_10 = ('hassan', '22-01-1999', 'Khaniuones', "7847347893478", "male", "21-12-1", "2118","11",  "22", "22","33","44", "55", "66", "77", "88", "10", "11", "12", "13", "14", "15", "16", "33", "44")

        #create users(
        create_user_test(conn, user_2)
        create_user_test(conn, user_3)
        create_user_test(conn, user_4)
        create_user_test(conn, user_5)
        create_user_test(conn, user_6)
        create_user_test(conn, user_7)
        create_user_test(conn, user_8)
        create_user_test(conn, user_9)
        create_user_test(conn, user_10)
    else:
        print("Error! cannot create the database connection.")

     # user_test
    

     


if __name__ == '__main__':
    main()
