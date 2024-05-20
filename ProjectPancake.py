# Assuming you have not changed the general structure of the template no modification is needed in this file.
from . import commands
from .lib import fusionAddInUtils as futil

import adsk.core, adsk.fusion, adsk.cam, traceback
import mysql.connector
import tkinter as tk
from tkinter import simpledialog

app = adsk.core.Application.get()
ui = app.userInterface

connection = None

def show_login_dialog():
    global connection

    root = tk.Tk()
    root.withdraw()  # Hide the root window

    server_ip = simpledialog.askstring("Server IP", "Enter the server IP:")
    db_name = simpledialog.askstring("Database Name", "Enter the database name:")
    user_name = simpledialog.askstring("User Name", "Enter the user name:")
    password = simpledialog.askstring("Password", "Enter the password:", show='*')

    try:
        connection = mysql.connector.connect(
            host=server_ip,
            database=db_name,
            user=user_name,
            password=password
        )
        if connection.is_connected():
            ui.messageBox("Successfully connected to the database")
    except mysql.connector.Error as err:
        ui.messageBox(f"Error: {err}")
        connection = None


def run(context):
    try:
        show_login_dialog()
    except:
        ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    global connection
    try:
        if connection and connection.is_connected():
            connection.close()
            ui.messageBox("Database connection closed")
    except:
        ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))