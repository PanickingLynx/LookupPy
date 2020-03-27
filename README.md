# AkumaPy / Forensic Search

![Main Logo](https://github.com/PanickingLynx/AkumaPy/blob/master/mainicon.png)

### Table of Contents
- What is AkumaPy?
- Is this tool ispired by Sherlock?
- Why would you want to use AkumaPy?
- Why was this created?
- How do I set it up?
- How does it work?
- What is the JSON Output Syntax?
- Which Modules were used?
- Features and planned features.

### What is AkumaPy?

AkumaPy is a forensic search tool, designed to find people via username across multiple Social Networks and other sites.

### Is this tool inspired by Sherlock?

Yes, most definitely. Sherlock is one of the tools that made me get into developing OSINT tools and I am really thankful for it.
You can find this awesome tool here: https://github.com/sherlock-project/sherlock

### Why would you want to use AkumaPy?

AkumaPy is designed to be easy to use for people in forensics.
It can ease tracking people just by recieving a username on one platform and hunting it across other sites.

### Why was this created?

AkumaPy was created for a final school project at the [BBS-Betzdorf-Kirchen Technical College](https://www.bbs-betzdorf-kirchen.de "School Homepage").
It contains multiple areas of programming like Databases, GUI Design and Web-Developement.

### How do I set it up?

To setup AkumaPy, you must have Tor installed and the SOCKS Port must be configured.
You can do this like so:
```
sudo apt install tor
sudo service tor start
sudo nano /etc/tor/torrc
```

In here we uncomment the Lines:
```
SOCKSPort 9050
CookieAuthentication 1
```

Ctrl+X Y and Enter to save
Now we will install the MongoDB Server.
Get it from [mongodb.com](https://www.mongodb.com/ "MongoDB")
Find the server and run (as root):
```
sudo dpkg -i ./the_downloaded_deb
sudo service mongod start
```
If there are errors restart your machine.

Next run (as root):
```
sudo service tor restart
cd /where_you_saved_the_tool/
sudo pip3 install -r ./requirements.txt
sudo python3 ./akuma.py
```
Then you are done.
Warning! The Tool will only work under Linux and with sudo! (For some reason there are errors when run directly from root)
If there are errors with my instructions let me know!

### How does it work?

The software connects to a local or remote MongoDB database. The database contains all the information about the links which would be searched in the run.
- Where is the Username placed?
- What is the link?
- Is it safe for work?

The following text is example JSON for what a document would look like:

```
{
    "name" : "ExampleSite",
    "link" : "https://example.com/{}/",
    "type" : "0"
}
```

name: The sites name

link: The link syntax ({} is the placeholder for the username and will be switched automatically)

type: Site type (0 = SFW / 1 = NSFW)

After reading out the contents of each database entry, the script will send a HTTP Request to the corresponding link and get its status code.
Then the html of the page will be checked if there is any sign of the profile not existing.

The user can choose to get a plain output, output to a .txt document or JSON format.

### What is the JSON Output syntax?

```
{
    "username" : examplename,
    "link" : https://example.com/examplename,
    "site_status" : 404,
    "hit" : bad
}
```

username: Account owners name.

link: Link to Website / Social Network.

site_status: HTTP Status Code recieved.

hit: Something was found = good, Nothing was found = bad, Errors occured = error.

### Which modules were used?

- json
- re
- sys
- os
- requests
- pymongo
- bs4 
- PyQt5
- qdarkstyle
- pysocks

### Planned features

- ~~JSON Output~~ [Finished]
- ~~Automatic name variation~~ [Finished]
- ~~Site html search to get a more specific output~~ [Finished]
- ~~Integrating database insertion into GUI~~ [Finished]
- ~~Adding credits to hotbar on the top of the GUI~~ [Finished]
- ~~Adding Tor routing and privacy options~~ [Finished]
- ~~Colored terminal output by type~~ [Finished]
- ~~OS detection so the tool only runs on Linux and as root~~ [Finished]


### Additional Credits

- Maze aka. Black_eks for creating the tools icon. [Instagram](https://www.instagram.com/black_eks/)
- Doelicious for letting me use her username extensively for testing purposes. [Twitter](https://www.twitter.com/Doelici0us/)
