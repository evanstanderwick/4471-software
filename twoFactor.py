#Authors: Drew DeLap and Evan Standerwick
#Purpose: This program should provide Zoom with a 2-factor identification plug-in that allows the user to select their preferred 2-factor software (google vs duo) through a GUI

import sqlite3
import tkinter as tk

def create_connection(db):
    conn = sqlite3.connect(db)
    return conn


def insert_user(conn, username, password, auth_type, auth_username):
    # inserts a new user into the db
    cur = conn.cursor()
    cur.execute("INSERT INTO users VALUES (?, ?, ?, ?);", (username, password, auth_type, auth_username))
    conn.commit()


def search_for_user(conn, username):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?;", [username]) # this is probably insecure to SQLi, but that isn't really important for this demo
    user = cur.fetchone()
    return user # returns the first found tuple w/ desired username, or None if none found

def sign_in(conn):
    success = False
    username = input("Zoom username: ")
    password = input("(Fake) Zoom password: ")

    # check if in db
    user = search_for_user(conn, username)
    if user == None or user[1] != password:
        print("Access denied: incorrect username or password")
    else:
        # check w/ associated 2-factor account
        if True: # 2-factor success. Just true right now for testing
            success = True
        else:
            print("Access denied by authenticator")

    return success

def sign_up(conn):
    success = False
    username = str(input("Zoom username: "))
    password = str(input("(Fake) Zoom password: "))
    authenticator_type = int(input("Authenticator type: Input 0 for Duo and 1 for Google Authenticator: "))
    while authenticator_type != 0 and authenticator_type != 1:
        authenticator_type = input("Enter either 0 for Duo or 1 for Google Authenticator: ")
    if authenticator_type == 0:
        authenticator_type = "duo"
    elif authenticator_type == 1:
        authenticator_type = "google"
    authenticator_username = input("Enter your authenticator account username: ")

    user = search_for_user(conn, username)
    if user == None:
        insert_user(conn, username, password, authenticator_type, authenticator_username)
        # add one of the 2-factor accounts
        # if that goes well, set success = true
        success = 1 # here right now for testing
    else:
        print("Error: That username already exists")

    return success

def main():
    db_filename = "users.db" # will be in format [username,password,authenticator_type,authenticator_account_identifier]
    conn = create_connection(db_filename)

    #GUI construction
    window = tk.Tk()
    greeting = tk.Label(text="Welcome to Zoom 2 Factor Login")

    window.rowconfigure(0, minsize=100, weight=1)
    window.columnconfigure([0,1], minsize=100, weight = 1)

    btn_signIn = tk.Button(master=window, text="Sign In", command=sign_in(conn))
    btn_signIn.grid(row=0, column=0, sticky="nsew")
    btn_signUp = tk.Button(master=window, text="Sign Up", command=sign_up(conn))
    btn_signUp.grid(row=0, column=1, sticky="nsew")

    window.mainloop()
    

    run = True
    while run: # right now, just loops for ease of use. Maybe adjust this once the GUI goes in?
        choice = int(input("Enter 0 to sign in, or 1 to sign up: "))
        while (choice != 0) and (choice != 1):
            choice = input("Error: Enter either 0 or 1: ")
        if choice == 0:
            success = sign_in(conn)
        else: # choice = "1"
            success = sign_up(conn)

        if success:
            print("Access granted")
        else:
            print("Access denied")
        
        run = input("Run again? (y/n): ")
        if run != "y":
            run = False

    conn.close()

if __name__ == '__main__':
    main()
