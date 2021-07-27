from os import name, path
import webbrowser
import sqlite3
from sqlite3 import Error
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
database = r"C:\sqlite\db\pythonsqlite.db"


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

# get all userData from DB


def select_all_users(conn):
    """
    Query users by id
    :param conn: the Connection object
    :param id:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    return rows


def getAllUsers(conn):
    users = select_all_users(conn)  # from db
    resevedusers = users[0]
    # {1: "id", 2: "name", 3: "birthday", 4: "address", 5: "age"}
    userArray = []
    for key in users:
        user = str(key).split(", ")
        index = 0
        for item in user:
            newitem = item.strip("(")
            newitem = newitem.strip(")")
            user[index] = newitem.strip("'")
            index += 1
        id = user[0]
        user.pop(0)
        user.append(id)
        trv.insert('', 'end', values=user)
        userArray.append(user)


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


# ----------------------------------------------- Code to add widgets will go here...
window = Tk()

wrapper1 = LabelFrame(
    window,
    text="user List",
)

wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)

trv = Treeview(wrapper1, columns=(1, 2, 3, 4, 5), show="headings")
trv.pack()


trv.heading(1, text="name")
trv.heading(2, text="birthday")
trv.heading(3, text="address")
trv.heading(4, text="age")
trv.heading(5, text="User Id")
getAllUsers(create_connection(database))


def getrow(event):
    rowid = trv.identify_row(event.y)
    item = trv.item(trv.focus())["values"]

    update_window(item)


def refresh():
    trv.delete(*trv.get_children())
    getAllUsers(create_connection(database))


window.title("admin pannale")
window.geometry("800x500")
trv.bind('<Double 1>', getrow)


def update_window(item):
    # { 0: "name", 1: "birthday", 2: "address", 3: "age",4: "id"}
    window1 = Tk()
    name_input = StringVar(window1)
    birthday_input = StringVar(window1)
    address_input = StringVar(window1)
    age_input = StringVar(window1)
    id_input = StringVar(window1)
    name_input.set(item[0])
    birthday_input.set(item[1])
    address_input.set(item[2])
    age_input.set(item[3])
    id_input.set(item[4])

    def clickDelete():
        id = id_input.get()
        if messagebox.askyesno("Confirm Delete?", "Are you dure you want to delete this User?"):
            deleteUser(create_connection(database), id)
            refresh()
        else:
            return True

    def clickPrint():
        header = "mr. "+name_input.get() + " details"
        f = open('UserInfo.html', 'w')
        message = """<html>
        <head>
            <link rel="icon" type="image/jpg" href="browser.jpg"/>
            <title>User Informaition</title>
            <style>
                .container {
                    width: 50%;
                    text-align: center;
                    margin: 100px auto;
                    background-color: #BEB7A4;
                    border-radius: 3px;
                    border: 2px solid #FF3F00;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>The company header</h1>
                <h2>"""+header+"""</h2>
                <h3>Age: """+age_input.get()+"""<h3/>
                <h3>Address: """+address_input.get()+"""<h3/>
                <h3>Birthday: """+birthday_input.get()+"""<h3/>
                <h4>The company footer</h4>
            <div/>
        </body>
        </html>"""

        f.write(message)
        f.close()
        webbrowser.open('UserInfo.html')

    def validation():
        birthday = birthday_input.get().split("-")
        errorState = False
        errorMessage = ''
        if name_input.get().isnumeric() == True:
            errorMessage += "- name must be String and the tall bettween 4 and 25 character\n"
            errorState = True
        elif len(name_input.get()) > 25 and len(age_input.get()) < 4:
            errorMessage += "-lentgh name must be bettween 4 and 25 character\n"
            errorState = True
        if len(birthday) != 3:
            errorMessage += "- birthday must be in the date format eg: 22-12-1999\n"
            errorState = True
        elif birthday[0].isnumeric() != True and birthday[1].isnumeric() != True and birthday[2].isnumeric() != True:
            errorMessage += "- birthday must be in the date format eg: 22-12-1999\n"
            errorState = True
        if address_input.get().isnumeric() == True:
            errorMessage += "- address must be text not a number\n"
            errorState = True
        if age_input.get().isnumeric() == False:
            errorMessage += "- age must be number Not string\n"
            errorState = True
        print("error " + str(errorState)+errorMessage)
        return errorState, errorMessage

    def clickUpdate():
        if messagebox.askyesno("Confirm Update?", "Are you dure you want to Update this User?"):
            errorState = False
            errorMessage = ''
            userDict = {
                "id": '0',
                "name": '',
                "birthday": '',
                "address": '',
                "age": '0'
            }
            isValid = validation()
            errorState = isValid[0]
            errorMessage = isValid[1]
            print(errorState)
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
            if errorState == False:
                updateAndCheckIsUpdatedSuccessfully(
                    userDict,
                    userDict["id"],
                    create_connection(database)
                )
                refresh()
                messagebox.showinfo("Update User Data", "Done")
            else:
                messagebox.showwarning("Wrong", errorMessage)
    label = Label(window1, text="This is a update window")
    label.grid(row=0, column=0)

    Label(
        window1,
        text="Username",
        foreground="white",
        background="#34A2FE",
        width=10,
    ).grid(row=1, column=0)

    Entry(
        window1,
        textvariable=name_input,
        width=50,
    ).grid(row=1, column=3)

    Label(
        window1,
        text="Birthday",
        foreground="white",
        background="#34A2FE",
        width=10,
    ).grid(row=2, column=0)

    Entry(
        window1,
        textvariable=birthday_input,
        width=50,
    ).grid(row=2, column=3)

    Label(
        window1,
        text="Address",
        foreground="white",
        background="#34A2FE",
        width=10,
    ).grid(row=3, column=0)

    Entry(
        window1,
        textvariable=address_input,
        width=50,
    ).grid(row=3, column=3)

    Label(
        window1,
        text="Age",
        foreground="white",
        background="#34A2FE",
        width=10,
    ).grid(row=4, column=0)

    Entry(
        window1,
        textvariable=age_input,
        width=50,
    ).grid(row=4, column=3)
    updateBtn = Button(
        window1, text="Update User", command=clickUpdate)
    updateBtn.grid(row=6, column=0, padx=5, pady=3)

    deleteBtn = Button(
        window1, text="delete User", command=clickDelete)
    deleteBtn.grid(row=6, column=1, padx=5, pady=3)

    printBtn = Button(
        window1, text="Print User Data", command=clickPrint)
    printBtn.grid(row=6, column=2, padx=5, pady=3)

# ------------------------------------------------


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


# execute update taple user
# updateUser("keyInDB", "newvalue")
def updateUser(newUser, user):
    newDictUser = dict()
    if newUser["id"] == 0:
        return newDictUser, False
    # copy and update
    for key in user:
        if newUser[key] != '' and newUser[key] != '0':
            newDictUser[key] = newUser[key]
        else:
            newDictUser[key] = user[key]

    isSuccess = newDictUser != user
    return newDictUser, isSuccess


# checkIsUpdate("keyInDB", "newvalue", connection)
def updateAndCheckIsUpdatedSuccessfully(updateUserData, id, connection):

    userData = updateUser(updateUserData, getUserData(connection, id))
    if userData[1] == False:
        messagebox.showwarning(
            "Wrong", "Problem in update, enter the new data in the forms")
    else:
        update_user(connection, (userData[0]["name"], userData[0]["address"],
                                 userData[0]["age"], userData[0]["birthday"], userData[0]["id"]))
        UserDataFromDatabase = getUserData(connection, userData[0]["id"])
        isUpdated = UserDataFromDatabase == userData[0]
        if isUpdated:
            messagebox.showinfo("Success", "Done Done :)")
        else:
            messagebox.showwarning(
                "Wrong", "Problem in update, enter the new data in the forms")


# -------------------------------------------------------------


def main():

    # create a database connection
    conn = create_connection(database)
    with conn:
        window.mainloop()


if __name__ == '__main__':
    main()
