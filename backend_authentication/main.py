# main user-facing authentication program. Handles everything except the login stuff, which happens in app.py.


import sqlite3
import os.path
import duo_universal
from flask import Flask, request, redirect, session, render_template
import app


def main():
    db_filename = "users.db" # will be in format [username,password]
    conn = create_connection(db_filename)
    print("")

    run = True
    while run: # right now, just loops for ease of use. Maybe adjust this once the GUI goes in?
        choice = input("Enter 0 to sign in, or 1 to sign up: ")
        while (choice != "0") and (choice != "1"):
            choice = input("Error: Enter either 0 or 1: ")
        if choice == "0":
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


def sign_in(conn):
    # all sign in stuff is done in app.py. Returns True if access granted, False if access denied.
    success = app.login_post(conn)
    return success


def sign_up(conn):
    # just adds username and password to the database. The duo admin must add users to duo using the online admin panel.
    # admin must make sure that the username online matches the username in our database here.
    success = False
    username = input("Zoom username: ")
    password = input("(Fake) Zoom password: ")

    user = search_for_user(conn, username)
    if user == None:
        insert_user(conn, username, password)
        success = True
    else:
        print("Error: That username already exists")

    return success


def create_connection(db):
    # connects to the database
    conn = sqlite3.connect(db)
    return conn


def insert_user(conn, username, password):
    # inserts a new user into the db
    cur = conn.cursor()
    cur.execute("INSERT INTO users VALUES (?, ?);", (username, password))
    conn.commit()


def search_for_user(conn, username):
    # looks for a user in the database.
    # returns the first found tuple with specified username, or None if none found.
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?;", [username]) # this is probably insecure to SQLi, but that isn't really important for this demo
    user = cur.fetchone()
    return user


if __name__ == '__main__':
    #app.run(host="localhost", port=8080)
    main()