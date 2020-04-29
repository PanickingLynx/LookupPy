import platform
import os
import sys
from termcolor import colored

def osDetection():
    #Get current OS
    currentSystem = platform.system()
    #Exit if either is true
    if currentSystem == "Windows":
        print(colored("WRONG OPERATING SYSTEM! PLEASE USE LINUX!", "red"))
        input("Press RETURN to exit")
        exit()
    elif currentSystem == "Darwin":
        print(colored("WRONG OPERATING SYSTEM! PLEASE USE LINUX!", "red"))
        input("Press RETURN to exit")
        exit()

def rootDetection():
    #Check if the user is root
    if not os.geteuid()==0:
        sys.exit('This script must be run as root!')

def errorListExists():
    #Error list for missing indicators
    try:
        errorList = open("./errorlist.txt")
        #Stringify the List to compare the words on the page with the list 
        errorListString = str(errorList)
        return errorListString
    except FileNotFoundError:
        sys.exit("errorlist.txt has not been found in the cwd, please create it by running the command 'touch ./errorlist.txt'.")

def testAll():
    osDetection()
    rootDetection()
    return errorListExists()
