"""
This program is designed to generate a random password with a certain number of characters. It also stores login data,
such as a email or login name, along with the password and the account this data belongs to, such as, Netflix or Hulu.
"""

from tkinter import *
from tkinter import ttk
import random
import string
import mysql.connector

# Connects to MySQL DBMS
# Enter your own MySQL username and password
mydb = mysql.connector.connect(
    host="localhost",
    user="",
    password=""
)

# Create cursor object
mycursor = mydb.cursor(buffered=True)

# Create and select database
mycursor.execute("CREATE DATABASE IF NOT EXISTS database1")
mycursor.execute("USE database1")


# Function that displays a frame
def raise_frame(frame):
    frame.tkraise()


# Function that brings you back to the beginning frame
def home(*args):
    raise_frame(mainframe)


# Function deletes an entry from the databases
def delete(*args):
    # Converts StringVar() variable to a string variable
    strcom = company4.get()

    # Select the record in the table that needs to be deleted depending on the attribute in the 'strcom' variable
    sql = "SELECT * FROM logindata WHERE company = %s"
    val1 = (strcom,)

    # Execute SQL command
    mycursor.execute(sql, val1)

    # Try to fetch record that was selected in previous command
    record = mycursor.fetchone()

    # If the record does not exist, start creating error frame
    if record is None:
        # Create an error frame
        failframe = ttk.Frame(root, padding="3 3 12 12")
        failframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Create a display message for error frame
        ttk.Label(failframe, text=f"The account name {strcom} does not exist. Nothing was done. Please try again.") \
            .grid(column=2, row=1)

        # Create Home button for error frame
        ttk.Button(failframe, text="Home", command=home).grid(column=2, row=2)

        # Set padding between the widgets in the frame
        for child1 in failframe.winfo_children():
            child1.grid_configure(padx=10, pady=10)

        # Display error frame
        raise_frame(failframe)
    # If the record does exist, start creating success frame
    else:
        # Set DELETE command for record depending on attribute in 'strcom' variable
        sql = "DELETE FROM logindata WHERE company = %s"
        val = (strcom,)

        # Execute DELETE command
        mycursor.execute(sql, val)
        mydb.commit()

        # Create success frame
        successframe = ttk.Frame(root, padding="3 3 12 12")
        successframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Create message on success frame
        ttk.Label(successframe, text=f"The login name and password related to your {strcom} account has been deleted.") \
            .grid(column=2, row=1)

        # Create Home button on success frame
        ttk.Button(successframe, text="Home", command=home).grid(column=2, row=2)

        # Set padding for widgets in success frame
        for child1 in successframe.winfo_children():
            child1.grid_configure(padx=10, pady=10)

        # Display success frame
        raise_frame(successframe)


# Function to update password in existing record
def update(*args):
    # Create string of characters for password generator
    letters = string.ascii_letters
    nums = '0123456789'
    spe = '-+*%&$!_'
    symbols = letters + nums + spe

    # convert StringVar() variables to string and int variables
    strcom = company2.get()
    strlen = length2.get()
    intlen = int(strlen)

    # Generate random password
    password = ''.join(random.sample(symbols, intlen))

    # Set SELECT command for record depending on attribute in 'strcom' variable
    sql = "SELECT * FROM logindata WHERE company = %s"
    val1 = (strcom,)

    # Execute SELECT command
    mycursor.execute(sql, val1)

    # Try to fetch record that was selected in previous command
    record = mycursor.fetchone()

    # If record does not exist, start creating error frame
    if record is None:
        # Create error frame
        failframe = ttk.Frame(root, padding="3 3 12 12")
        failframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Create message in error frame
        ttk.Label(failframe, text=f"The account name {strcom} does not exist. Nothing was done. Please try again.") \
            .grid(column=2, row=1)

        # Create Home button in error frame
        ttk.Button(failframe, text="Home", command=home).grid(column=2, row=2)

        # Set padding for widgets in error frame
        for child1 in failframe.winfo_children():
            child1.grid_configure(padx=10, pady=10)

        # Display error frame
        raise_frame(failframe)
    # If record does exist, start creating success frame
    else:
        # Set UPDATE command for record using data in 'strcom' and 'password' variables
        sql = "UPDATE logindata SET password = %s WHERE company = %s"
        val = (password, strcom)

        # Execute UPDATE command
        mycursor.execute(sql, val)
        mydb.commit()

        # Create success frame
        successframe = ttk.Frame(root, padding="3 3 12 12")
        successframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Create message in success frame
        ttk.Label(successframe, text=f"Password successfully updated and stored. Your new password is {password}") \
            .grid(column=2, row=1)

        # Create button in success frame
        ttk.Button(successframe, text="Home", command=home).grid(column=2, row=2)

        # Set padding for widgets in success frame
        for child1 in successframe.winfo_children():
            child1.grid_configure(padx=10, pady=10)

        # Display success frame
        raise_frame(successframe)


# Function that creates a new record entry
def create(event=None, *args):
    # Deletes in any previous entry in Entry widget
    com_entry2.delete(0, "end")

    # Create string of characters for password generator
    letters = string.ascii_letters
    nums = '0123456789'
    spe = '-+*%&$!_'
    symbols = letters + nums + spe

    # Convert StringVar() variables into string and int variables
    strcom = company.get()
    strname = name.get()
    strlen = length.get()
    intlen = int(strlen)

    # Generate random password
    password = ''.join(random.sample(symbols, intlen))

    # Create table, if it doesn't already exist
    mycursor.execute("CREATE TABLE IF NOT EXISTS logindata (company VARCHAR(255), "
                     "login VARCHAR(50), password VARCHAR(50), PRIMARY KEY (company))")

    try:
        # Set INSERT command using values in 'strcom', 'strname', 'password' variables
        sql = "INSERT INTO logindata (company, login, password) VALUES (%s, %s, %s)"
        val = (strcom, strname, password)

        # Execute INSERT command
        mycursor.execute(sql, val)
        mydb.commit()

        # Create success frame
        successframe = ttk.Frame(root, padding="3 3 12 12")
        successframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Create message in success frame
        ttk.Label(successframe, text=f"Password successfully generated and stored. Your new password is {password}") \
            .grid(column=2, row=1)

        # Create Home button in success frame
        ttk.Button(successframe, text="Home", command=home).grid(column=2, row=2)

        # Set padding for widgets in success frame
        for child1 in successframe.winfo_children():
            child1.grid_configure(padx=10, pady=10)

        # Display success frame
        raise_frame(successframe)
    # If record already exists, revert to 'except' block
    except mysql.connector.errors.IntegrityError:
        # Create error frame
        failframe = ttk.Frame(root, padding="3 3 12 12")
        failframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Create message for error frame
        ttk.Label(failframe, text="Account already exists. Either create new account entry or update existing one.") \
            .grid(column=2, row=1)

        # Create buttons for error frame
        ttk.Button(failframe, text="Create new account", command=lambda: raise_frame(newframe)).grid(column=1, row=2)
        ttk.Button(failframe, text="Update existing account", command=lambda: raise_frame(updateframe)).grid(column=2,
                                                                                                             row=2)

        # Set padding for widgets in error frame
        for child1 in failframe.winfo_children():
            child1.grid_configure(padx=10, pady=10)

        # Display error frame
        raise_frame(failframe)


# Function that displays record
def view(*args):
    # Converts StringVar() variable into string variable
    strcom = company3.get()

    # Deletes any previous input in Entry widget
    com_entry2.delete(0, "end")

    # Set SELECT command for record depending on attribute in 'strcom' variable
    sql = "SELECT * FROM logindata WHERE company = %s"
    val1 = (strcom,)

    # Execute SELECT command
    mycursor.execute(sql, val1)

    # Try to fetch record from previous command
    record = mycursor.fetchone()

    # If record doesn't exist, start creating error frame
    if record is None:
        # Create error frame
        failframe = ttk.Frame(root, padding="3 3 12 12")
        failframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Create message in error frame
        ttk.Label(failframe, text=f"The account name {strcom} does not exist. Please try again.") \
            .grid(column=2, row=1)

        # Create Home button in error frame
        ttk.Button(failframe, text="Home", command=home).grid(column=2, row=2)

        # Set padding for widgets in error frame
        for child1 in failframe.winfo_children():
            child1.grid_configure(padx=10, pady=10)

        # Display error frame
        raise_frame(failframe)
    # If record does exist, start crate success frame
    else:
        # Set SELECT command for record depending on attribute in 'strcom' variable
        sql = "SELECT * FROM logindata WHERE company = %s"
        val = (strcom,)

        # Execute SELECT command
        mycursor.execute(sql, val)

        # Fetch all records from previous command
        result = mycursor.fetchall()

        # Create success frame
        successframe = ttk.Frame(root, padding="3 3 12 12")
        successframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Create messages for success frame
        for x in result:
            ttk.Label(successframe, text=f"Your login for {x[0]} is {x[1]} and your password is {x[2]}") \
                .grid(column=2, row=1)
        # Create Home button for success frame
        ttk.Button(successframe, text="Home", command=home).grid(column=2, row=2)

        # Set padding for widgets in success frame
        for child1 in successframe.winfo_children():
            child1.grid_configure(padx=10, pady=10)

        # Display success frame
        raise_frame(successframe)


# Create main window for app
root = Tk()
root.title("Password Generator")

# Create the five root frames
mainframe = ttk.Frame(root, padding="3 3 12 12")
newframe = ttk.Frame(root, padding="3 3 12 12")
updateframe = ttk.Frame(root, padding="3 3 12 12")
viewframe = ttk.Frame(root, padding="3 3 12 12")
deleteframe = ttk.Frame(root, padding="3 3 12 12")

# Set dimensions for the five root frames
for frame in (mainframe, newframe, updateframe, viewframe, deleteframe):
    frame.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

# Create message and buttons for the main frame
ttk.Label(mainframe, text="Welcome to Password Generator, please make a selection: ").grid(column=1, row=1)
ttk.Button(mainframe, text="Generate password and save data", command=lambda: raise_frame(newframe)).grid(column=1,
                                                                                                          row=2)
ttk.Button(mainframe, text="Update password and save data", command=lambda: raise_frame(updateframe)).grid(column=2,
                                                                                                           row=2)
ttk.Button(mainframe, text="View data", command=lambda: raise_frame(viewframe)).grid(column=1, row=3)
ttk.Button(mainframe, text="Delete data", command=lambda: raise_frame(deleteframe)).grid(column=2, row=3)

# Set padding for widgets in the main frame
for child in mainframe.winfo_children():
    child.grid_configure(padx=10, pady=10)

# Create entry widget for username or email for create new record frame
name = StringVar()
ttk.Label(newframe, text="ENTER LOGIN NAME OR EMAIL: ").grid(column=1, row=1)
name_entry = ttk.Entry(newframe, width=50, textvariable=name)
name_entry.grid(column=2, row=1)

# Create entry widget for account name for create new record frame
company = StringVar()
ttk.Label(newframe, text="ENTER COMPANY NAME: ").grid(column=1, row=2)
com_entry = ttk.Entry(newframe, width=50, textvariable=company)
com_entry.grid(column=2, row=2)

# Create entry widget for password length for create new record frame
length = StringVar()
ttk.Label(newframe, text="ENTER PASSWORD LENGTH: ").grid(column=1, row=3)
len_entry = ttk.Entry(newframe, width=50, textvariable=length)
len_entry.grid(column=2, row=3)

# Create Generate button for create new record frame
ttk.Button(newframe, text="Generate", command=create)

# Set padding for widgets in the crate new record frame
for child in newframe.winfo_children():
    child.grid_configure(padx=10, pady=10)

# Create entry widget for account name for update existing record frame
company2 = StringVar()
ttk.Label(updateframe, text="ENTER COMPANY NAME: ").grid(column=1, row=2)
com_entry2 = ttk.Entry(updateframe, width=50, textvariable=company2)
com_entry2.grid(column=2, row=2)

# Create entry widget for password length for update existing record frame
length2 = StringVar()
ttk.Label(updateframe, text="ENTER PASSWORD LENGTH: ").grid(column=1, row=3)
len_entry2 = ttk.Entry(updateframe, width=50, textvariable=length2)
len_entry2.grid(column=2, row=3)

# Create Update button for update existing record frame
ttk.Button(updateframe, text="Update", command=update)

# Set padding for widgets in update existing record frame
for child in updateframe.winfo_children():
    child.grid_configure(padx=10, pady=10)

# Create entry widget for account name for view record frame
company3 = StringVar()
ttk.Label(viewframe, text="ENTER COMPANY NAME: ").grid(column=1, row=2)
com_entry2 = ttk.Entry(viewframe, width=50, textvariable=company3)
com_entry2.grid(column=2, row=2)

# Create View button for view record frame
ttk.Button(viewframe, text="View", command=view)

# Set padding for widgets in view record frame
for child in viewframe.winfo_children():
    child.grid_configure(padx=10, pady=10)

# Create entry widget for account name for delete record frame
company4 = StringVar()
ttk.Label(deleteframe, text="ENTER COMPANY NAME: ").grid(column=1, row=2)
com_entry3 = ttk.Entry(deleteframe, width=50, textvariable=company4)
com_entry3.grid(column=2, row=2)

# Create Delete button for delete record frame
ttk.Button(deleteframe, text="Delete", command=delete)

# Set padding for widgets in delete record frame
for child in deleteframe.winfo_children():
    child.grid_configure(padx=10, pady=10)

# Display main frame
raise_frame(mainframe)

# Launch app
root.mainloop()
