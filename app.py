import sys


import os
from dotenv import load_dotenv
load_dotenv()
from database import conn, createTable

# Add password to the database

def submitPassword(webStr, userStr, pswdStr, emailStr):
    try:
        with conn.cursor() as cursor:
            sql = f"INSERT INTO `passwords` (`website`, `username`, `password`, `email`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (f"{webStr}", f"{userStr}", f"{pswdStr}", f"{emailStr}"))

            conn.commit()
    
    finally:
        pass


def interpretResponse(inp):
    # Check for command validity
    # If False, notify user and return to starting prompt
    # If True, continue
    if not checkForValidRes(inp):
        print("Please enter a valid response.\n")
        runStartPrompt()
    
    checkIfQuitOrStart(inp)
    
    match inp.lower():
        
        case "ls":
            printCommandList()

        case "c":
            # Ask user for master password before continuing; if wrong return to start prompt
            # If master password matches ask user for website, then username, then email, then password
            # If at any point a string is empty, then notify user and exit and return to start prompt
            # If all fields are entered properly, ask for confirmation (display data) then add to database if yes
            # If no, then send user back to create command

            #askMasterPassword()
            createPassword()
        case "d":
            # Ask user for master password before continuing; if wrong return to start prompt
            # If master password matches ask user for website
            # Confirm if website exists in db, if not notify user and re-ask
            # Confirm if they selected the right website; if yes, continue, if no allow to reenter
            # Ask user if they want to delete password and display password [Prompt: 'password']
            # Ask for second confirmation, if no at any point, return to start prompt
            # If yes, print all related data, then remove from database and send confirmation message, return to start prompt
            askMasterPassword()
            deletePassword()

        case "s":
            # Ask user what website they are searching for
            # If the password exists for that website, send conformation message
            # If the password does not exist for that website ask if they would like to create one
            # If yes run createPassword(), if no return to start
            searchPassword()
        
        case _:
            # How????
            print("How'd you get here????\n")

# Check for command validity
# If not valid, return False
# If valid, return True
def checkForValidRes(inp):
    for command in commandList:
        #print(input.lower())
        if (inp.lower() == command):
            #print("Entered valid response.")
            return True
    
    return False

# Place creation logic here
def createPassword():
    resArray = []

    website = input("\nWhat is the website? ")
    resArray.append(str(website))

    username = input("\nWhat is the username? ")
    resArray.append(str(username))

    email = input("\nWhat is the email? ")
    resArray.append(str(email))

    password = input("\nWhat is the password? ")
    resArray.append(str(password))

    # Checks to see if any of the above inputs were empty; if so, go back to beginning of program
    for response in resArray:
        if response == "":
            print("\nYou cannot send an empty response.\n")
            runStartPrompt()

    # Confirm if user entered correct data
    confirmData(f"\n Create Website: {resArray[0]}\n Create Username: {resArray[1]}\n Create Email: {resArray[2]}\n Create Password: {resArray[3]}\n", createPassword)

    # Send confirmed response to database and send success message, then go back to start
    submitPassword(resArray[0], resArray[1], resArray[2], resArray[3])
    print(f"Password successfully submitted!\n Website: {resArray[0]}\n Username: {resArray[1]}\n Password: {resArray[2]}\n Email: {resArray[3]}\n")
    runStartPrompt()

# Place deletion logic here
def deletePassword():
    websiteName = str(input("\nWhat is the website you would like to delete? "))
    dbEntry = findPassword(websiteName, deletePassword)

    # Checks to make sure that dbEntry is not an empty string
    if not type (dbEntry) == None:
        confirmData(f"Delete Website: {dbEntry.get("website")}\n Delete Username: {dbEntry.get("username")}\n Delete Password: {dbEntry.get("password")}\n Delete Email: {dbEntry.get("email")}\n", deletePassword)
        doubleConfirm = input(f"\nAre you sure you want to delete password '{dbEntry.get("password")}' from '{dbEntry.get("website")}' (y/n)? ")

        if not doubleConfirm == "y":
            print("\nCommand execution stopped. Redirecting to start propmpt.\n")
            runStartPrompt()

    try:
        with conn.cursor() as cursor:
            sql = f"DELETE FROM passwords WHERE website = %s;"
            cursor.execute(sql, (f"{websiteName}"))

            conn.commit()
    
    finally:
        print("\nDeletion successful.")
        runStartPrompt()

# Place search logic here
def searchPassword():
    website = input("\nWhat is the website? ")
    dbEntry = findPassword(website, searchPassword)
    print(f"A password for '{website}' does exist!")
    runStartPrompt()
    # displayPassword = input(f"\nWould you like to see the password for '{website}'? (y/n):")

    # if not displayPassword == "y"

# Query the database to see if the website exists
# If the password does not exist then the function that this was called in is restarted or the user may create a password for that website
def findPassword(websiteName, restartFunction):
    checkIfQuitOrStart(websiteName)
    try:
        with conn.cursor() as cursor:
            sql = f"SELECT * FROM passwords WHERE website = %s;"
            cursor.execute(sql, (f"{websiteName}"))
            dbEntry = cursor.fetchall()
            if len(dbEntry) > 0:
                return dbEntry[0]
            else:
                print(f"The website '{websiteName}' does not have an entry in the database. Try again, create the password, or type 'start' to go back to the start.\n")

                create = input(f"Would you like to create a password for '{websiteName}'? (y/n):")

                if create == "y":
                    createPassword()

                restartFunction()
    
    finally:
        pass


# Print the list of commands
def printCommandList():
    print("Printing command list.\n")

    for i in range(0, len(commandList)-1):
        print(f"{commandList[i]}: {commandDescriptions[i]}")

    print("\n")
    runStartPrompt()

# Use the filepath in a .env to find the masterkey and if user inputs correctly, move on
# Otherwise, return to the start
def askMasterPassword():
    masterLocation = open(os.getenv('FILEPATH'), 'r')
    masterKey = masterLocation.readline()


    pswdEntry = input("What is the master password? ")

    if pswdEntry == masterKey:
        print("Correct!\n")
        return

    print("The master password you entered was wrong. Returning to start prompt.\n")
    runStartPrompt()

# Check if an input contains either 'q' or 'start'
def checkIfQuitOrStart(inp):
    if inp == "q":
        conn.close()
        sys.exit()
    elif inp == "start":
        runStartPrompt()

# Run the starting prompt
def runStartPrompt():
    res = input("\nWhat would you like to do? (Type 'ls' for a list of commands) ")
    interpretResponse(res)

# Ask user for confimation on the data being submitted, if not restart a command
def confirmData(data, restartFunction):
    confirmation = input(f"Would you like to submit the following data:\n {data}\n(y/n): ")

    checkIfQuitOrStart(confirmation)

    if not confirmation == "y":
        print("Sending you back to original prompt.\n")
        restartFunction()



# PROGRAM INITILIZERS (OR HOWEVER YOU SPELL IT)



# list of valid commands
commandList = ['q', 'ls', 'c', 'd', 'start', 's', 'how do you even know about this']

commandDescriptions = ["Quits the program.", 
                       "Prints list of all commands and their descriptions.", 
                       "Creates a password.", 
                       "Deletes a password by website name or id.", 
                       "Returns back to starting prompt (Usable at any point).", 
                       "Seraches the database for password that matches a specfied website"
                       "Dude, how?"]

# Title Line
print("\n---PASSWORD MANAGER---")

# UNCOMMENT THE BELOW COMMAND TO CREATE THE DATABASE TABLE EASILY
#createTable("passwords", ["website", "username", "password", "email"])
# Start the program initially
runStartPrompt()
