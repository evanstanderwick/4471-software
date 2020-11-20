# 4471-software
CSE 4471 Zoom Security Plan Software Component
Authors: Drew DeLap and Evan Standerwick

This repository contains a DUO 2-factor authentication plugin that would theoretically be used on top of another applications sign in to add an extra layer of security

Files:

.vscode - python interpreter
backend_authentication - files pertaining to the command line based two factor authentication
duo_universal_python-1.0.1 - DUO download including necessary files to integrate the software
README.md - relevant repository information
twoFactor.py - python register/sign in GUI, NOT integrated with command line dual factor authentication
users.db - basic databasse for users
users.txt - text file equivalent of users.db

backend_authentication:
.vscode
__pycache__
app.py - backend authentication server, built using duo.com, background of main.py
main.py - user interface for dual factor authentication, works through command line
main2.y - copy of main, intended to house a GUI to go on top of the main but encountered technical issues and is not complete at this point
session.txt
users.db - database to house user information and help with lookup
