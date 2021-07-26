from os import path
import sqlite3
from sqlite3 import Error
from tkinter import *


def select_user_by_id(conn, id):
    """
    Query users by id
    :param conn: the Connection object
    :param id:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (id,))
    rows = cur.fetchall()
    return rows

# get userData from DB


def getUserData(connection, id):
    userData = {}
    userSchema = {1: "id", 2: "name", 3: "birthday", 4: "address", 5: "age"}
    if id == 0:
        return "fail"
    else:
        reseveduserData = str(select_user_by_id(connection, id)[0]).split(", ")
        index = 1
        for item in reseveduserData:
            newitem = item.strip("(")
            newitem = newitem.strip(")")
            newitem = newitem.strip("'")
            userData[userSchema[index]] = newitem
            index += 1
        return userData


window = Tk()
# Code to add widgets will go here...

# 2: "name", 3: "birthday", 4: "address", 5: "age"

name_input = StringVar(window)
birthday_input = StringVar(window)
address_input = StringVar(window)
age_input = StringVar(window)
id_input = StringVar(window)
Label(
    window,
    text="Username",
    foreground="white",
    background="#34A2FE",
    width=10,
    height=3
).grid(row=0, column=0)

Entry(
    window,
    textvariable=name_input,
    width=50,
    borderwidth=5,
).grid(row=0, column=1)

Label(
    window,
    text="Birthday",
    foreground="white",
    background="#34A2FE",
    width=10,
    height=3
).grid(row=0, column=2)

Entry(
    window,
    textvariable=birthday_input,
    width=50,
    borderwidth=5,
).grid(row=0, column=3)

Label(
    window,
    text="Address",
    foreground="white",
    background="#34A2FE",
    width=10,
    height=3
).grid(row=1, column=0)

Entry(
    window,
    textvariable=address_input,
    width=50,
    borderwidth=5,
).grid(row=1, column=1)

Label(
    window,
    text="Age",
    foreground="white",
    background="#34A2FE",
    width=10,
    height=3
).grid(row=1, column=2)

Entry(
    window,
    textvariable=age_input,
    width=50,
    borderwidth=5,
).grid(row=1, column=3)

Label(
    window,
    text="User ID",
    foreground="white",
    background="#34A2FE",
    width=10,
    height=3
).grid(row=2, column=0)


Entry(
    window,
    textvariable=id_input,
    borderwidth=5,
).grid(row=2, column=1)


# ------------------------------------------------


def create_connection(db_file):
    # connection with db
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

# query for update user data


def update_user(conn, user):
    """
    update name, birthday, address and age of a user
    :param conn:
    :param user:
    :return: project id
    """
    sql = ''' UPDATE users
              SET name = ? ,
                  address = ? ,
                  age = ? ,
                  birthday = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()


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


# execute update taple user
# updateUser("keyInDB", "newvalue")
def updateUser(newUser, user):
    newDictUser = dict()
    if newUser["id"] == 0:
        return newDictUser, False
    # copy and update
    for key in user:
        if newUser[key] != '':
            newDictUser[key] = newUser[key]
        else:
            newDictUser[key] = user[key]

    isSuccess = newDictUser != user
    return newDictUser, isSuccess


# checkIsUpdate("keyInDB", "newvalue", connection)
def updateAndCheckIsUpdatedSuccessfully(updateUserData, id, connection):

    userData = updateUser(updateUserData, getUserData(connection, id))
    if userData[1] == False:
        print("Problem in update, enter the new data in the forms")
    else:
        update_user(connection, (userData[0]["name"], userData[0]["address"],
                                 userData[0]["age"], userData[0]["birthday"], userData[0]["id"]))
        UserDataFromDatabase = getUserData(connection, userData[0]["id"])
        isUpdated = UserDataFromDatabase == userData[0]
        print(userData[0])
        print(UserDataFromDatabase)
        if isUpdated:
            print("Done Done")
        else:
            print("unfortinatly Problem in update")


def deleteUser(conn, id):
    """
    Delete a user by user id
    :param conn:  Connection to the SQLite database
    :param id: id of the user
    :return:
    """
    sql = 'DELETE FROM users WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

# -------------------------------------------------------------


def main():
    database = r"C:\sqlite\db\pythonsqlite.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # checkIsUpdate("keyInDB", "newvalue", connection)
        # checkIsUpdate("name", "nll", conn)

        def insertUser():
            create_user(conn, (
                name_input.get(),
                birthday_input.get(),
                address_input.get(),
                age_input.get()
            ))

        def getUser():
            user = getUserData(conn, id_input.get())
            Label(
                window,
                text="name is "+user["name"]+",    birthday is " +
                user["birthday"]+",    Address is " +
                user["address"]+",    age is "+user["age"],
                foreground="white",
                background="#34A2FE",
                height=3
            ).grid(row=2, column=3)

        def clickDelete():
            deleteUser(conn, id_input.get())

        def clickUpdate():
            userDict = {
                "id": '0',
                "name": '',
                "birthday": '',
                "address": '',
                "age": '0'
            }

            if name_input.get() != '':
                userDict["name"] = name_input.get()
            if birthday_input.get() != '':
                userDict["birthday"] = birthday_input.get()
            if address_input.get() != '':
                userDict["address"] = address_input.get()
            if age_input.get() != '':
                userDict["age"] = age_input.get()
            if id_input.get() != '':
                userDict["id"] = id_input.get()
            updateAndCheckIsUpdatedSuccessfully(
                userDict,
                userDict["id"],
                conn
            )
        # Button
        Button(window, text="add user",
               command=insertUser).grid(row=1, column=4)
        Button(window, text="Update User",
               command=clickUpdate).grid(row=4, column=1)
        Button(window, text="Delete User",
               command=clickDelete).grid(row=2, column=5)
        Button(window, text="Click to get user",
               command=getUser).grid(row=2, column=4)

        window.mainloop()


if __name__ == '__main__':
    main()
