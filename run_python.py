import webbrowser
import traceback
import sqlite3
import serial
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
        RDW,
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


def select_user_test_by_test_id(conn, id):
    """
    Query test_users by id
    :param conn: the Connection object
    :param id:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_tests WHERE id=?", (id,))
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
    for key in test_users:
        testUser = str(key).split(", ")
        index = 0
        for item in testUser:
            newitem = item.strip("(")
            newitem = newitem.strip(")")
            testUser[index] = newitem.strip("'")
            index += 1

        _id = testUser.pop(0)
        user_test_id = testUser[6]
        testUser.pop(6)
        testUser.insert(0, user_test_id)
        testUser.append(str(_id))
        trv.insert('', 'end', values=testUser)


def getUserTestData(connection, id):
    userTestData = {}
    userTestSchema = {
        1: "id",
        2: "name", 3: "birthday", 4: "address", 5: "identification", 6: "sex",
        7: "date_for_cbc",
        8:  "test_id",
        9:  "wbc",
        10:  "ly%",
        11:  "mo%",
        12:  "gr%",
        13: "ly",
        14: "mo",
        15: "gr",
        16: "rbc",
        17: "hgb",
        18: "hct",
        19: "mcv",
        20: "mch",
        21: "mchc",
        22: "rdw",
        23: "plt",
        24: "pct",
        25: "mpv",
        26: "pdw"
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
    sql = 'DELETE FROM user_tests WHERE id=?'
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
               12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25), show="headings", selectmode='browse')
trv.pack()

# ----------- scrollbar
vsbx = Scrollbar(wrapper1, orient="horizontal", command=trv.xview)
vsbx.place(x=1, y=223, width=1155)
trv.configure(xscrollcommand=vsbx.set)

vsby = Scrollbar(wrapper1, orient="vertical", command=trv.yview)
vsby.place(x=1140, y=23, height=195)
trv.configure(yscrollcommand=vsby.set)
trv.heading(1, text="User_Test Id")
trv.heading(2, text="Name")
trv.heading(3, text="Birthday")
trv.heading(4, text="Address")
trv.heading(5, text="Identification")
trv.heading(6, text="Sex")
trv.heading(7, text="Date_For_CBC")
trv.heading(8, text="WBC")
trv.heading(9, text="LY%")
trv.heading(10, text="MO%")
trv.heading(11, text="GR%")
trv.heading(12, text="LY")
trv.heading(13, text="MO")
trv.heading(14, text="GR")
trv.heading(15, text="RBC")
trv.heading(16, text="HGB")
trv.heading(17, text="HCT")
trv.heading(18, text="MCV")
trv.heading(19, text="MCH")
trv.heading(20, text="MCHC")
trv.heading(21, text="RDW")
trv.heading(22, text="PLT")
trv.heading(23, text="PCT")
trv.heading(24, text="MPV")
trv.heading(25, text="PDW")

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

    attrib_CBC = ["Date", "ID", "WBC", "LY%", "MO%", "GR%", "LY", "MO", "GR",
                  "RBC", "HGB", "HCT", "MCV", "MCH", "MCHC", "RDW", "PLT", "PCT", "MPV", "PDW"]

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
            user_test = ['DClick to edit the user test', 'data', '', '', '']
            if oldline != split_line:
                for item in split_line:
                    if i < 20:
                        item = item.strip(" ").strip("\x02").strip("\x03")
                        user_test.append(item)
                        i += 1
                create_user_test(create_connection(database), tuple(user_test))
                refresh()

        except Exception:
            traceback.print_exc()
            # break doesn't quit now on error.


def threaded_function():
    add_user_test_from_CBC()


window.title("admin pannale")
window.geometry("1200x500")
trv.bind('<Double 1>', getrow)


def update_window(item):
    window1 = Tk()
    name_input = StringVar(window1)
    birthday_input = StringVar(window1)
    address_input = StringVar(window1)
    identification_input = StringVar(window1)
    sex_input = StringVar(window1)
    id__auto = StringVar(window1)
    id_input = StringVar(window1)
    date_for_cbc = StringVar(window1)
    wbc = StringVar(window1)
    ly = StringVar(window1)
    mo = StringVar(window1)
    gr = StringVar(window1)
    ly1 = StringVar(window1)
    mo1 = StringVar(window1)
    gr1 = StringVar(window1)
    rbc = StringVar(window1)
    hgb = StringVar(window1)
    hct = StringVar(window1)
    mcv = StringVar(window1)
    mch = StringVar(window1)
    mchc = StringVar(window1)
    rdw = StringVar(window1)
    plt = StringVar(window1)
    pct = StringVar(window1)
    mpv = StringVar(window1)
    pdw = StringVar(window1)

    id_input.set(item[0])  # {"id_input": 7, }
    name_input.set(item[1])
    birthday_input.set(item[2])
    address_input.set(item[3])
    identification_input.set(item[4])
    sex_input.set(item[5])
    date_for_cbc.set(item[6])
    wbc.set(item[7])
    ly.set(item[8])
    mo.set(item[9])
    gr.set(item[10])
    ly1.set(item[11])
    mo1.set(item[12])
    gr1.set(item[13])
    rbc.set(item[14])
    hgb.set(item[15])
    hct.set(item[16])
    mcv.set(item[17])
    mch.set(item[18])
    mchc.set(item[19])
    rdw.set(item[20])
    plt.set(item[21])
    pct.set(item[22])
    mpv.set(item[23])
    pdw.set(item[24])
    id__auto.set(item[25])

    def clickDelete():
        if messagebox.askyesno("Confirm Delete?", "Are you sure you want to delete this user_test?"):
            deleteUserTest(create_connection(database), id__auto.get())
            refresh()
            window1.destroy()
        else:
            return True
    CBC_dict = {
        7: {"name": "WBC", "unit": "10^3/ul", "normal_limits": [4, 12]},
        8:  {"name": "LY%", "unit": "%", "normal_limits": [25, 50]},
        9:  {"name": "MO%", "unit": "%", "normal_limits": [2, 10]},
        10: {"name": "GR%", "unit": "%", "normal_limits": [42, 85]},
        11: {"name": "LY", "unit": "10^3/ul", "normal_limits": [1, 5]},
        12: {"name": "MO", "unit": "10^3/ul", "normal_limits": [0.1, 1]},
        13: {"name": "GR", "unit": "10^3/ul", "normal_limits": [2.30, 7.70]},
        14: {"name": "RBC", "unit": "10^6/ul", "normal_limits": [4, 6.20]},
        15: {"name": "HGB", "unit": "g/dl", "normal_limits": [11, 17]},
        16: {"name": "HCT", "unit": "%", "normal_limits": [35, 55]},
        17: {"name": "MCV", "unit": "um^3", "normal_limits": [80, 100]},
        18: {"name": "MCH", "unit": "pg", "normal_limits": [26, 34]},
        19: {"name": "MCHC", "unit": "g/dl", "normal_limits": [31, 35]},
        20: {"name": "RDW", "unit": "%", "normal_limits": [10, 16]},
        21: {"name": "PLT", "unit": "10^3/ul", "normal_limits": [150, 400]},
        22: {"name": "PCT", "unit": "%", "normal_limits": [0.200, 0.500]},
        23: {"name": "MPV", "unit": "um^3", "normal_limits": [7, 11]},
        24: {"name": "PDW", "unit": "um^3", "normal_limits": [10, 18]}
    }
    html_cbc = ""
    for element in CBC_dict:
        html_cbc += '''
            <tr>
                <th>
                    '''+CBC_dict[element]["name"]+'''
                </th>
                <td>
                    '''+str(item[element])+'''
                </td>
                <td>
                    '''+CBC_dict[element]["unit"]+'''
                </td>
                <td>
                    '''+str(CBC_dict[element]["normal_limits"][0])+'''
                </td>
                <td>
                    '''+str(CBC_dict[element]["normal_limits"][1])+'''
                </td>
                
            </tr>
            '''

    def clickPrint():
        header = "mr. "+name_input.get()
        f = open('UserInfo.html', 'w')
        message = """
        <html>
            <head>
                <link rel="icon" type="image/jpg" href="browser.jpg"/>
                <title>User Test Informaition</title>
                <style>
                    .container {
                        width: 70%;
                        margin: 100px auto;
                        border-radius: 3px;
                        border: 2px solid #FF3F00;
                    }
                    h3 {
                        text-transform: uppercase;
                    }

                    table {
                    font-family: arial, sans-serif;
                    border-collapse: collapse;
                    width: 100%;
                    }

                    td, th {
                    border: 1px solid #BEB7A4;
                    text-align: left;
                    padding: 8px;
                    }

                    tr:nth-child(even) {
                    background-color: #BEB7A4;
                    }

                </style>
            </head>
            <body>
                <div class="container">
                    <table>
                        <tr>
                            <th>Patient Name</th>
                            <th>Patient ID</th>
                            <th>Address</th>
                            <th>birthday</th>
                            <th>identification</th>
                            <th>Gender</th>
                            
                        </tr>
                        <tr>
                            <td>"""+header+"""</td>
                            <td>"""+id_input.get()+"""</td>
                            <td>"""+address_input.get()+"""</td>
                            <td>"""+birthday_input.get()+"""</td>
                            <td>"""+identification_input.get()+"""</td>
                            <td>"""+sex_input.get()+"""</td>
                        </tr>
                    </table>
                    </br>
                    <table>
                        <tr>
                            <th>CBC Date</th>
                            <td>"""+date_for_cbc.get()+"""</td>
                        </tr>
                    </table>
                    </br>
                    <table>
                            
                            <tr>
                                    <th>titles</th>
                                    <th>Results</th>
                                    <th>Units</th>
                                    <th>Normal</th>
                                    <th>Limits</th>
                            </tr>
                        """+html_cbc+"""
                    </table> 
                </div>      
            </body>
        </html>"""

        f.write(message)
        f.close()
        webbrowser.open('UserInfo.html')
        window1.destroy()

    def validation():
        birthday = birthday_input.get().split("-")
        if name_input.get().isnumeric() != True or len(name_input.get()) == 0:
            if len(name_input.get()) < 25 and len(name_input.get()) > 4:
                if len(birthday_input.get()) == 0:
                    if address_input.get().isnumeric() != True or len(address_input.get()) == 0:
                        if identification_input.get().isnumeric() == True or len(identification_input.get()) == 0:
                            messagebox.showinfo(
                                "Done", "Verifed")
                            return False, "nice"
                        else:
                            return True, "- identification must to be number\n"
                    else:
                        return True, "- address must be text not a number\n"
                elif len(birthday) == 3:
                    if birthday[0].isnumeric() == True and birthday[1].isnumeric() == True and birthday[2].isnumeric() == True:
                        if int(birthday[0]) < 32 and int(birthday[0]) > 0:
                            if int(birthday[1]) < 13 and int(birthday[1]) > 0:
                                if int(birthday[2]) > 1860 and int(birthday[2]) < 2014:
                                    if address_input.get().isnumeric() != True or len(address_input.get()) == 0:
                                        if identification_input.get().isnumeric() == True or len(identification_input.get()) == 0:
                                            messagebox.showinfo(
                                                "Done", "Verifed")
                                            return False, "- nice\n"
                                        else:
                                            return True, "- identification must to be number\n"
                                    else:
                                        return True, "- address must be text not a number\n"
                                else:
                                    return True, "- birthday days must be bettween 1860 and 2015\n"
                            else:
                                return True, "- birthday monthes must be bettween 0 and 12\n"
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

    def clickUpdate():
        if messagebox.askyesno("Confirm Update?", "Are you dure you want to Update this User Test?"):
            errorState = False
            errorMessage = ''
            userTestDict = {
                "test_id": '0',
                "name": '',
                "birthday": '',
                "address": '',
                "identification": '',
                "sex": ''
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
            if identification_input.get() != '':
                userTestDict["identification"] = identification_input.get()
            if sex_input.get() != '':
                userTestDict["sex"] = sex_input.get()
            if errorState == False:
                updateAndCheckIsUpdatedSuccessfully(
                    userTestDict,
                    id__auto.get(),
                    create_connection(database)
                )
                refresh()
                window1.destroy()
            else:
                messagebox.showwarning("Wrong", errorMessage)

    def sel():
        selection = "You selected the option " + sex_input.get()
        sex_label.config(text=selection)

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

    Label(
        window1,
        text="identification",
        foreground="white",
        background="#34A2FE",
        width=10,
    ).grid(row=5, column=0)

    Entry(
        window1,
        textvariable=identification_input,
        width=50,
    ).grid(row=5, column=3)
    Label(
        window1,
        text="Select Sex",
        foreground="white",
        background="#34A2FE",
        width=10,
    ).grid(row=6, column=0)
    sex_label = Label(window1)
    sex_label.grid(row=6, column=2)
    male = Radiobutton(window1, text="Male", variable=sex_input, value="male",
                       command=sel)
    male.grid(row=6, column=3)

    fmale = Radiobutton(window1, width=10, text="Fmale", variable=sex_input, value="fmale",
                        command=sel)
    fmale.grid(row=6, column=4)

    updateBtn = Button(
        window1, text="Update user_test", command=clickUpdate)
    updateBtn.grid(row=8, column=0, padx=5, pady=3)

    deleteBtn = Button(
        window1, text="delete user_test", command=clickDelete)

    male.grid(row=6, column=3)

    fmale = Radiobutton(window1, width=10, text="Fmale", variable=sex_input, value="fmale",
                        command=sel)
    fmale.grid(row=6, column=4)

    updateBtn = Button(
        window1, text="Update user_test", command=clickUpdate)
    updateBtn.grid(row=8, column=0, padx=5, pady=3)

    deleteBtn = Button(
        window1, text="delete user_test", command=clickDelete)
    deleteBtn.grid(row=8, column=1, padx=5, pady=3)

    printBtn = Button(
        window1, text="Print user_test Data", command=clickPrint)
    printBtn.grid(row=8, column=2, padx=5, pady=3)

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
                  "birthday" = ?,
                  "address" = ? ,
                  "identification" = ?,
                  "sex" = ?
              WHERE id = ?'''
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
        if key == "test_id" or key == "name" or key == "birthday" or key == "address" or key == "identification" or key == "sex":
            if newUserTest[key] != '0':
                newDictUserTest[key] = newUserTest[key]
            else:
                newDictUserTest[key] = user_tests[key]

    isSuccess = newDictUserTest["test_id"] != user_tests["test_id"] or newDictUserTest["name"] != user_tests["name"] or newDictUserTest["birthday"] != user_tests[
        "birthday"] or newDictUserTest["address"] != user_tests["address"] or newDictUserTest["identification"] != user_tests["identification"] or newDictUserTest["sex"] != user_tests["sex"]
    return newDictUserTest, isSuccess


# checkIsUpdate("keyInDB", "newvalue", connection)
def updateAndCheckIsUpdatedSuccessfully(updateUserTestData, id, connection):

    userTestData = updateUserTest(
        updateUserTestData, getUserTestData(connection, id))
    if userTestData[1] == False:
        messagebox.showwarning(
            "Wrong", "Problem in update, enter the new data in the forms")
    else:
        update_user_test(connection, (userTestData[0]["name"], userTestData[0]["birthday"],
                         userTestData[0]["address"], userTestData[0]["identification"], userTestData[0]["sex"],  id))
        messagebox.showinfo("Succzess", "Done Done, The Data Is Saved:)")


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
