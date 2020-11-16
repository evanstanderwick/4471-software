#Authors: Drew DeLap and Evan Standerwick
#Purpose: This program should provide Zoom with a 2-factor identification plug-in that allows the user to select their preferred 2-factor software (google vs duo) through a GUI
from functools import partial
from tkinter import *
import os

signInWindow = None
welcomeWindow = None
usernameCheck = None
passwordCheck = None
signInUser = None
signInPass = None
signUpWindow = None
signUpUsername = None
signUpPass = None
username = None
password = None
duoScreen = None
invalidPassWindow = None 
invalidUserWindow = None

#sign in window
def signIn():
    global signInWindow
    signInWindow = Toplevel(welcomeWindow)
    signInWindow.title("Sign In")

    global usernameCheck, passwordCheck, signInUser, signInPass
    usernameCheck = StringVar()
    passwordCheck = StringVar()

    Label(signInWindow, text="Username: ").grid(row=0, column=0)
    signInUser = Entry(signInWindow, textvariable=usernameCheck).grid(row=0,column=1)

    Label(signInWindow, text="Password: ").grid(row=1, column=0)
    signInPass = Entry(signInWindow, show='*', textvariable=passwordCheck).grid(row=1,column=1)

    Button(signInWindow, text="Sign In", command=signInCheck).grid(row=2,column=0)

#sign up window
def signUp():
    global signUpWindow
    signUpWindow = Toplevel(welcomeWindow)
    signUpWindow.title("Sign Up")

    global signUpUsername, signUpPass, username, password
    username = StringVar()
    password = StringVar()

    Label(signUpWindow, text="Username: ").grid(row=0, column=0)
    signUpUsername = Entry(signUpWindow, textvariable=username).grid(row=0,column=1)

    Label(signUpWindow, text="Password: ").grid(row=1, column=0)
    signUpPass = Entry(signUpWindow, show='*', textvariable=password).grid(row=1,column=1)

    Button(signUpWindow, text="Sign Up", command=signUpUser).grid(row=2,column=0)

#check if username and password are logged in file system
def signInCheck():
    user = usernameCheck.get()
    passW = passwordCheck.get()
    #signInUser.delete(0,END)
    #signInPass.delete(0,END)

    files = os.listdir()
    if user in files:
        userFile = open(user, "r")
        validityCheck = userFile.read().splitlines()
        if passW in validityCheck:
            duoAuthentication()
        else:
            invalidPassword()
    else:
        invalidUser()
    
#create file with username and password saved for future reference in the system
def signUpUser():
    user1 = username.get()
    passW1 = password.get()

    file = open(user1, "w")
    file.write(user1 + "\n")
    file.write(passW1)
    file.close()

    #signUpUsername.delete(0,END)
    #signUpPass.delete(0,END)

    Button(signUpWindow, text="Next", command=duoAuthentication).grid(row=3, column=0)

#PLEASE SETUP DUO APPLICATION IN THIS PORTAL IF GUI HELP NECESSARY SLACK ME
def duoAuthentication():
    #Please display duo window here
    global duoScreen
    duoScreen = Toplevel(welcomeWindow)
    duoScreen.title("Duo Authentication")
    Label(duoScreen, text="Duo HERE").grid(row=0,column=0)

#Popup screen for when the password is wrong
def invalidPassword():
    global invalidPassWindow
    invalidPassWindow = Toplevel(signInWindow)
    invalidPassWindow.title("ERROR")
    Label(invalidPassWindow, text="INCORRECT PASSWORD").grid(row=0,column=0)
    Button(invalidPassWindow, text="Retry", command=signIn).grid(row=1,column=0)
    Button(invalidPassWindow, text="Sign Up", command=signUp).grid(row=1,column=1)

#Popup screen for when the password is wrong
def invalidUser():
    global invalidUserWindow
    invalidUserWindow = Toplevel(signInWindow)
    invalidUserWindow.title("ERROR")
    Label(invalidUserWindow, text="INCORRECT USERNAME").grid(row=0,column=0)
    Button(invalidUserWindow, text="Retry", command=signIn).grid(row=1,column=0)
    Button(invalidUserWindow, text="Sign Up", command=signUp).grid(row=1,column=1)

def main():
    global welcomeWindow
    welcomeWindow = Tk()
    welcomeWindow.title("Acount Login")
    Button(text="Sign In", command=signIn).grid(row=0, column=0)
    Button(text="Sign Up", command=signUp).grid(row=0, column=1)
    welcomeWindow.mainloop()

if __name__ == "__main__":
    main()
