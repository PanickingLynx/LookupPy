import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["AkumaPy"]
mycol = mydb["links"]

def main():
    name = input("Insert a fitting name for the social network you wanna add: ")
    print("Please Insert the link you wanna add, make sure to add a WILDCARD into the link whereever the Username would be: ")
    link = input("Insert the link here: ")
    print("")
    isNSFW = input("Is this a NSFW link? If yes, put a 1, if no put a 0: ")
    print(name, isNSFW, link)
    if "http://" or "https://" not in link:
        print("INVALID URL, MISSING HTTP OR HTTPS!!!")
        input("PRESS ENTER TO RESET!")
        main()
    elif "WILDCARD" not in link:
        print("PLEASE PUT THE 'WILDCARD' STRING INTO A VALID PLACE IN THE LINK")
        input("PRESS ENTER TO RESET!")
        main()
    if 1 or 0 not in isNSFW:
        print("NO isNSFW ASSIGNED! ENTER A 1 OR A 0")
        input("PRESS ENTER TO RESET!")
        main()
    if name or link or isNSFW == "":
        print("MISSING PARAMETER! PLEASE RETRY!")
        input("PRESS ENTER TO RESET!")
        main()
        
    print("Inserting....")
    mydoc = { "name": name, "link": link, "isNSFW": isNSFW}

    mycol.insert_one(mydoc)

    print("Done!")
    input("Press ENTER to exit the program!")
    exit()

main()
