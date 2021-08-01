from os import name, path
import webbrowser
import sqlite3
import serial
import time
import traceback
import datetime
import requests
from sqlite3 import Error
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from threading import Thread
database = r"pythonsqlitek.db"
#port = '/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller_D-if00-port0'
port = '/dev/ttyUSB0'
baud = 9600


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
        test_id,
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
        pdw
    )
        VALUES(? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,?) '''
    cur = conn.cursor()
    cur.execute(sql, userTest)
    conn.commit()
    return cur.lastrowid


def select_user_test_by_test_id(conn, id):
    """
    Query test_users by test_id
    :param conn: the Connection object
    :param test_id:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_tests WHERE test_id=?", (id,))
    rows = cur.fetchall()
    return rows

# get all userTestData from DB


def select_all_user_tests(conn):
    """
    Query user_tests by test_id
    :param conn: the Connection object
    :param test_id:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_tests")
    rows = cur.fetchall()
    return rows


def getAllTestUsers(conn):
    test_users = select_all_user_tests(conn)  # from db
    # {1: "test_id", 2: "name", 3: "birthday", 4: "address"}
    userTestArray = []
    for key in test_users:
        testUser = str(key).split(", ")
        index = 0
        for item in testUser:
            newitem = item.strip("(")
            newitem = newitem.strip(")")
            testUser[index] = newitem.strip("'")
            index += 1
        id = testUser[4]
        testUser.pop(4)
        testUser.append(id)
        trv.insert('', 'end', values=testUser)
        userTestArray.append(testUser)


def getUserTestData(connection, id):
    userTestData = {}
    userTestSchema = {
        1: "name", 2: "birthday", 3: "address", 4: "date_for_cbc",
        5:  "test_id",
        6:  "wbc",
        7:  "ly%",
        8:  "mo%",
        9:  "gr%",
        10: "ly",
        11: "mo",
        12: "gr",
        13: "rbc",
        14: "hbg",
        15: "gct",
        16: "mcv",
        17: "mch",
        18: "mchc",
        19: "plt",
        20: "pct",
        21: "mpv",
        22: "pdw"
    }
    if id == 0:
        return "fail"
    else:
        reseveduserData = str(select_user_test_by_test_id(
            connection, id)[0]).split(", ")
        index = 1
        for item in reseveduserData:
            newitem = item.strip("(")
            newitem = newitem.strip(")")
            newitem = newitem.strip("'")
            userTestData[userTestSchema[index]] = newitem
            index += 1
        return userTestData


def deleteUserTest(conn, id):
    """
    Delete a user_test by user_test test_id
    :param conn:  Connection to the SQLite database
    :param test_id: test_id of the user_test
    :return:
    """
    sql = 'DELETE FROM user_tests WHERE test_id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()


# ----------------------------------------------- Code to add widgets will go here...
window = Tk()

wrapper1 = LabelFrame(
    window,
    text="user_test List",
)

wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)

trv = Treeview(wrapper1, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
               12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24), show="headings")
trv.pack()


trv.heading(1, text="name")
trv.heading(2, text="birthday")
trv.heading(3, text="address")
trv.heading(4, text="date_for_cbc")
trv.heading(5, text="wbc")
trv.heading(6, text="ly%")
trv.heading(7, text="mo%")
trv.heading(8, text="gr%")
trv.heading(9, text="ly")
trv.heading(10, text="mo")
trv.heading(11, text="gr")
trv.heading(12, text="rbc")
trv.heading(13, text="hbg")
trv.heading(14, text="gct")
trv.heading(15, text="mcv")
trv.heading(16, text="mch")
trv.heading(17, text="mchc")
trv.heading(18, text="plt")
trv.heading(19, text="pct")
trv.heading(20, text="mpv")
trv.heading(21, text="pdw")
trv.heading(22, text="user_test Id")
getAllTestUsers(create_connection(database))


def getrow(event):
    item = trv.item(trv.focus())["values"]
    update_window(item)


def refresh():
    trv.delete(*trv.get_children())
    getAllTestUsers(create_connection(database))


def add_user_test_from_CBC():
    ser = serial.Serial(port, baud, timeout=1)
    ser.flushInput()

    print("name" + ser.name)

    attrib_CBC = ["Date", "ID", "WBC", "LY%", "MO%", "GR%", "LY", "MO", "GR",
                  "RBC", "HBG", "HCT", "MCV", "MCH", "MCHC", "PLT", "PCT", "MPV", "PDW"]
    print(len(attrib_CBC))

    oldline = []
    a = 0
    while (a == 0):
        try:
            i = 0
            line = ser.readline()                 # read bytes until line-ending
            line = line.decode('UTF-8', 'ignore')  # convert to string
            # remove line-ending characters
            line = line.rstrip('\r\n')

            split_line = line.splitlines()
            user_test = ['DClick to edit the user test', 'data', '']
            if oldline != split_line:
                for item in split_line:
                    if i < 19:
                        item = item.strip(" ")
                        item = item.strip("\x02")
                        item = item.strip("\x03")
                        print("i " + item)
                        user_test.append(item)
                        i += 1
                print(split_line)
                print("userT" + str(tuple(user_test)))
                print(create_user_test(create_connection(database),  user_test))
                refresh()
    #'', '', '', '21/07/05', '0005', '0.1L', '', '', '', '', '', '', '0.01L', '0.3L', '0.1L', '100', 'OVER', 'OVER', '',
                # '5L', '', '')

        except Exception:
            traceback.print_exc()
            print("exiting")
            #print("Keyboard Interrupt")
            # break doesn't quit now on error.


def threaded_function():
    add_user_test_from_CBC()


window.title("admin pannale")
window.geometry("1200x500")
trv.bind('<Double 1>', getrow)


def update_window(item):
    print(item)
    # { 0: "name", 1: "birthday", 2: "address", 3: "test_id"}
    window1 = Tk()
    name_input = StringVar(window1)
    birthday_input = StringVar(window1)
    address_input = StringVar(window1)
    id_input = StringVar(window1)
    date_for_cbc = StringVar(window1)
    wbc = StringVar(window1)
    ly = StringVar(window1)
    mo = StringVar(window1)
    gr = StringVar(window1)
    ly = StringVar(window1)
    mo = StringVar(window1)
    gr = StringVar(window1)
    rbc = StringVar(window1)
    hbg = StringVar(window1)
    gct = StringVar(window1)
    mcv = StringVar(window1)
    mch = StringVar(window1)
    mchc = StringVar(window1)
    plt = StringVar(window1)
    pct = StringVar(window1)
    mpv = StringVar(window1)
    pdw = StringVar(window1)

    name_input.set(item[0])
    birthday_input.set(item[1])
    address_input.set(item[2])
    id_input.set(item[21])

    date_for_cbc.set(item[3])
    wbc.set(item[4])
    ly.set(item[5])
    mo.set(item[6])
    gr.set(item[7])
    ly.set(item[8])
    mo.set(item[9])
    gr.set(item[10])
    rbc.set(item[11])
    hbg.set(item[12])
    gct.set(item[13])
    mcv.set(item[14])
    mch.set(item[15])
    mchc.set(item[16])
    plt.set(item[17])
    pct.set(item[18])
    mpv.set(item[19])
    pdw.set(item[20])

    def clickDelete():
        id = id_input.get()
        if messagebox.askyesno("Confirm Delete?", "Are you dure you want to delete this user_test?"):
            deleteUserTest(create_connection(database), id)
            refresh()
            window1.destroy()
        else:
            return True

    def clickPrint():
        header = "mr. "+name_input.get() + " details"
        f = open('UserInfo.html', 'w')
        message = """<html>
        <head>
            <link rel="icon" type="image/jpg" href="browser.jpg"/>
            <title>User Test Informaition</title>
            <style>
                .container {
                    width: 50%;
                    text-align: center;
                    margin: 100px auto;
                    background-color: #BEB7A4;
                    border-radius: 3px;
                    border: 2px solid #FF3F00;
                }
                h3 {
                    text-transform: uppercase;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>The company header</h1>
                <h2>"""+header+"""</h2>
                <h3>Address: """+address_input.get()+"""<h3/>
                <h3>Birthday: """+birthday_input.get()+"""<h3/>
                <h3>date_for_cbc: """+date_for_cbc.get()+"""<h3/>
                <h3>wbc: """+wbc.get()+"""<h3/>
                <h3>ly: """+ly.get()+"""<h3/>
                <h3>mo: """+mo.get()+"""<h3/>
                <h3>gr: """+gr.get()+"""<h3/>
                <h3>ly: """+ly.get()+"""<h3/>
                <h3>mo: """+mo.get()+"""<h3/>
                <h3>gr: """+gr.get()+"""<h3/>
                <h3>rbc: """+rbc.get()+"""<h3/>
                <h3>hbg: """+hbg.get()+"""<h3/>
                <h3>gct: """+gct.get()+"""<h3/>
                <h3>mcv: """+mcv.get()+"""<h3/>
                <h3>mch: """+mch.get()+"""<h3/>
                <h3>mchc: """+mchc.get()+"""<h3/>
                <h3>plt: """+plt.get()+"""<h3/>
                <h3>pct: """+pct.get()+"""<h3/>
                <h3>mpv: """+mpv.get()+"""<h3/>
                <h3>pdw: """+pdw.get()+"""<h3/>

                <h4>The company footer</h4>
            <div/>
        </body>
        </html>"""

        f.write(message)
        f.close()
        webbrowser.open('UserInfo.html')
        window1.destroy()

    def validation():
        birthday = birthday_input.get().split("-")
        errorState = False
        errorMessage = ''
        if name_input.get().isnumeric() != True:
            if len(name_input.get()) < 25 and len(name_input.get()) > 4:
                if len(birthday) == 3:
                    if birthday[0].isnumeric() == True and birthday[1].isnumeric() == True and birthday[2].isnumeric() == True:
                        if int(birthday[0]) < 32 and int(birthday[0]) > 0:
                            if int(birthday[1]) < 13 and int(birthday[1]) > 0:
                                if int(birthday[2]) > 1860 and int(birthday[2]) < 2014:
                                    if address_input.get().isnumeric() != True:
                                        messagebox.showinfo(
                                            "Done", "Verifed with no error")
                                    else:
                                        return True, "- address must be text not a number\n"
                                else:
                                    return True, "- birthday days must be bettween 1860 and 2015\n"
                            else:
                                return True, "- birthday months must be bettween 0 and 12\n"
                        else:
                            return True, "- birthday days must be bettween 0 and 30\n"
                    else:
                        return True, "- birthday must be in the date format eg: 22-12-1999\n"
                else:
                    return True, "- birthday must be in the date format eg: 22-12-1999\n"
            else:
                return True, "-lentgh name must be bettween 4 and 25 character\n"
        else:
            return True, "- name must be String\n"
        return errorState, errorMessage

    def clickUpdate():
        if messagebox.askyesno("Confirm Update?", "Are you dure you want to Update this User Test?"):
            errorState = False
            errorMessage = ''
            userTestDict = {
                "test_id": '0',
                "name": '',
                "birthday": '',
                "address": '',
            }
            isValid = validation()
            errorState = isValid[0]
            errorMessage = isValid[1]
            if name_input.get() != '':
                userTestDict["name"] = name_input.get()
            if birthday_input.get() != '':
                userTestDict["birthday"] = birthday_input.get()
            if address_input.get() != '':
                userTestDict["address"] = address_input.get()
            if id_input.get() != '':
                userTestDict["test_id"] = id_input.get()
            if errorState == False:
                updateAndCheckIsUpdatedSuccessfully(
                    userTestDict,
                    userTestDict["test_id"],
                    create_connection(database)
                )
                refresh()
                window1.destroy()
            else:
                messagebox.showwarning("Wrong", errorMessage)
    label = Label(window1, text="This is a update window")
    label.grid(row=0, column=0)
    Label(
        window1,
        text="Test Id: " + id_input.get(),
        foreground="white",
        background="#34A2FE",
        width=10,
    ).grid(row=1, column=0)
    Label(
        window1,
        text="Username",
        foreground="white",
        background="#34A2FE",
        width=10,
    ).grid(row=2, column=0)

    Entry(
        window1,
        textvariable=name_input,
        width=50,
    ).grid(row=2, column=3)

    Label(
        window1,
        text="Birthday",
        foreground="white",
        background="#34A2FE",
        width=10,
    ).grid(row=3, column=0)

    Entry(
        window1,
        textvariable=birthday_input,
        width=50,
    ).grid(row=3, column=3)

    Label(
        window1,
        text="Address",
        foreground="white",
        background="#34A2FE",
        width=10,
    ).grid(row=4, column=0)

    Entry(
        window1,
        textvariable=address_input,
        width=50,
    ).grid(row=4, column=3)

    updateBtn = Button(
        window1, text="Update user_test", command=clickUpdate)
    updateBtn.grid(row=6, column=0, padx=5, pady=3)

    deleteBtn = Button(
        window1, text="delete user_test", command=clickDelete)
    deleteBtn.grid(row=6, column=1, padx=5, pady=3)

    printBtn = Button(
        window1, text="Print user_test Data", command=clickPrint)
    printBtn.grid(row=6, column=2, padx=5, pady=3)

# ------------------------------------------------


# query for update user_test data
def update_user_test(conn, user_test):
    """
    update name and birthday address of a user_test
    :param conn:
    :param user_test:
    :return: project test_id
    """
    sql = ''' UPDATE user_tests
              SET "name" = ? ,
                  "address" = ? ,
                  "birthday" = ?
              WHERE test_id = ?'''
    cur = conn.cursor()
    cur.execute(sql, user_test)

    conn.commit()


# execute update taple user_test
def updateUserTest(newUserTest, user_tests):
    newDictUserTest = dict()
    if newUserTest["test_id"] == 0:
        return newDictUserTest, False
    # copy and update
    for key in user_tests:
        if key == "test_id" or key == "name" or key == "birthday" or key == "address":
            if newUserTest[key] != '' and newUserTest[key] != '0':
                newDictUserTest[key] = newUserTest[key]
            else:
                newDictUserTest[key] = user_tests[key]

    isSuccess = newDictUserTest["test_id"] != user_tests["test_id"] or newDictUserTest["name"] != user_tests["name"] or newDictUserTest[
        "birthday"] != user_tests["birthday"] or newDictUserTest["address"] != user_tests["address"]
    print(isSuccess)
    return newDictUserTest, isSuccess


# checkIsUpdate("keyInDB", "newvalue", connection)
def updateAndCheckIsUpdatedSuccessfully(updateUserTestData, id, connection):

    userTestData = updateUserTest(
        updateUserTestData, getUserTestData(connection, id))
    if userTestData[1] == False:
        messagebox.showwarning(
            "Wrong", "Problem in update, enter the new data in the forms")
    else:
        update_user_test(connection, (userTestData[0]["name"], userTestData[0]["address"],
                                      userTestData[0]["birthday"], userTestData[0]["test_id"]))
        messagebox.showinfo("Succzess", "Done Done :)")


# -------------------------------------------------------------


def main():
    thread = Thread(target=threaded_function, args=[])
    thread.start()
    # create a database connection
    conn = create_connection(database)
    with conn:
        window.mainloop()


if __name__ == '__main__':
    main()
