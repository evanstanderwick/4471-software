# backend authentication server. Keep this running while using main.py
# built using guide at https://duo.com/docs/duoweb-v4#wait-for-the-redirect-from-duo-back-to-your-redirect-uri, with some minor changes


import sqlite3
import os.path
import duo_universal
from flask import Flask, request, redirect, session, render_template
import time


app = Flask(__name__)
INTEGRATION_KEY = "DIEBUIRO2SBPFPB9PHGL"
SECRET_KEY = "68YJU5BwiMgMEHEFqf7CfM4fXcrMxztBLTKSxL1d"
API_HOSTNAME = "api-97033195.duosecurity.com"
REDIRECT_URL = "http://localhost:8080/duo-callback" # just loopback, since we don't have a real network-accessible server set up
DUO_CLIENT = duo_universal.Client(INTEGRATION_KEY, SECRET_KEY, API_HOSTNAME, REDIRECT_URL)


@app.route("/", methods=['POST'])
def login_post(conn):
    # here we post the login attempt w/ username and password to the server, or just deny the attempt locally if credentials are incorrect
    success = False
    username = input("Zoom username: ")
    password = input("(Fake) Zoom password: ")

    # check if in db
    user = search_for_user(conn, username)
    if user == None or user[1] != password:
        print("Access denied: incorrect username or password")
    else:
        success = True
    try:
        DUO_CLIENT.health_check()
    except:
        print("Duo servers are inaccessible. Try again later.")
    
    if success:
        # send user to 2FA with duo
        state = DUO_CLIENT.generate_state()
        session = open("session.txt", 'w', 1) # used to move data between authentication server and user-facing program.
        # if we had a network-accessible server set up, we could probably use sockets instead. But this will do for the demo.
        session.write(username)
        session.close()
        prompt_uri = DUO_CLIENT.create_auth_url(username, state)
        print("You have 30 seconds to go to this URL to complete authentication: " + prompt_uri)
        redirect(prompt_uri)
        time.sleep(30) # wait 30 seconds for user to authenticate, then continue
        session = open("session.txt", 'r', 1) # authentication server should have replaced session data w/ the 2FA "success" or "failure"
        session_data = session.readline()
        session.close()
        if session_data == "success":
            auth_success = True
        else:
            auth_success = False
        return auth_success and success
    else:
        # user failed initial login attempt, no need for 2FA.
        return success


@app.route("/duo-callback")
def duo_callback():
    # check w/ Duo. This is the code the server will run once it gets the POST from login_post()
    authenticated_message = "Access denied"
    authenticated = False

    code = request.args.get('duo_code')

    session = open("session.txt", "r+", 1)
    username = session.readline()
    print(username)
    session.close()

    try:
        DUO_CLIENT.exchange_authorization_code_for_2fa_result(code, username) # this exchange is where the 2FA "Allow/Deny" is used
        authenticated = True
    except Exception as e:
        # this runs if anything goes wrong with the exchange, including if "Deny" is pressed
        print(e)

    if authenticated:
        # 2-factor success
        session = open("session.txt", 'w', 1)
        session.write("success")
        authenticated_message = "Access granted"
        print(authenticated_message)
    else:
        # 2-factor denial or backend failure
        session = open("session.txt", 'w', 1)
        session.write("failure")
        print("Access denied by authenticator")

    session.close()
    return authenticated_message


def search_for_user(conn, username):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?;", [username]) # this is probably insecure to SQLi, but that isn't really important for this demo
    user = cur.fetchone()
    return user # returns the first found tuple w/ desired username, or None if none found


if __name__ == '__main__':
    app.run(host="localhost", port=8080)