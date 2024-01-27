import pymysql as mysql
import sys

from database import db, connect_db, Email, Password

# variable that allows program to run until specified otheriwse by user
running = True

# list of valid commands
commandList = ['q', 'ls', 'c', 'd', 'start', 'how do you even know about this']

# Title Line
print("\n---PASSWORD MANAGER---\n")

conn = mysql.connect(
    host='localhost',
    user='root',
    password='3416SbSp13MS',
    db='pswdmanager',
    charset='utf8mb4',
    cursorclass=mysql.cursors.DictCursor
)

# Add password to the database

def submitPassword(userStr, pswdStr, emailStr):
    try:
        with conn.cursor() as cursor:
            sql = f"INSERT INTO `password` (`username`, `password`, `email`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (f"{userStr}", f"{pswdStr}", f"{emailStr}"))

            conn.commit()
    
    finally:
        conn.close()


def checkResponse(input):
    # Check for command validity
    # If False, notify user and return to starting prompt
    # If True, continue
    if not checkForValidRes(input):
        print("Please enter a valid response.\n")
        return
    
    match input.lower():
        case "q":
            # Exit the program
            sys.exit()
        
        case "ls":
            printCommandList()

        case "c":
            # Ask user for master password before continuing; if wrong return to start prompt
            # If master password matches ask user for website, then username, then email, then password
            # If at any point a string is empty, then notify user and exit and return to start prompt
            # If all fields are entered properly, ask for confirmation (display data) then add to database if yes
            # If no, then send user back to create command
            createPassword()

        case "d":
            # Ask user for master password before continuing; if wrong return to start prompt
            # If master password matches ask user for website
            # Confirm if they selected the right website; if yes, continue, if no allow to reenter
            # Ask user if they want to delete password and display password [Prompt: 'password']
            # Ask for second confirmation, if no at any point, return to start prompt
            # If yes, print all related data, then remove from database and send confirmation message, return to start prompt
            deletePassword()

        case "start":
            # End the case search and return user to the start
            return
        
        case _:
            # How????
            print("How'd you get here????\n")

# Check for command validity
# If not valid, return False
# If valid, return True
def checkForValidRes(input):
    for command in commandList:
        #print(input.lower())
        if (input.lower() == command):
            #print("Entered valid response.")
            return True
    
    return False

# Place creation logic here
def createPassword():
    print("Creating password.\n")

# Place deletion logic here
def deletePassword():
    print("Deleting password.\n")

def printCommandList():
    print("Printing command list.\n")

# Run the starting prompt
def runStartPrompt():
    res = input("What would you like to do? (Type 'ls' for a list of commands) ")
    return str(res)


while running:
    res = runStartPrompt()
    checkResponse(res)