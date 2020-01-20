# AkumaPy / Forensic Search

### Table of Contents
- What is AkumaPy?
- Why would you want to use AkumaPy?
- Why was this created?
- How does it work?
- Which Modules were used?
- Features and planned features.

### What is AkumaPy?

AkumaPy is a forensic search tool, designed to find people via username across multiple Social Networks and other sites.

### Why would you want to use AkumaPy?

AkumaPy is designed to be easy to use for people in forensics.
It can ease tracking people just by recieving a username on one platform and hunting it across other sites.

### Why was this created?

AkumaPy was created for a final school project at the [BBS-Betzdorf-Kirchen Technical College](https://www.bbs-betzdorf-kirchen.de "School Homepage").
It contains multiple areas of programming like Databases, GUI Design and Web-Developement.

### How does it work?

The software connects to a local or remote MongoDB database. The database contains all the information about the links which would be searched in the run.
- Where is the Username placed?
- What is the link?
- Is it safe for work?

The following text is example JSON for what a document would look like:

```
{
    "name" : "ExampleSite",
    "link" : "https://example.com/WILDCARD/",
    "type" : "0"
}
```

name: The sites name

link: The link syntax (WILDCARD is the placeholder for the username and will be switched automatically)

type: Site type (0 = SFW / 1 = NSFW)

After reading out the contents of each database entry, the script will send a HTTP Request to the corresponding link and get its status code.
Then the html of the page will be checked if there is any sign of the profile not existing.

The user can choose to get a plain output, output to a .txt document or JSON format.

### Which modules were used?

- json
- re
- sys
- requests
- pymongo
- bs4 
- PyQt5
- qdarkstyle

### Planned features

- ~~JSON Output~~ [Finished]
- ~~Automatic name variation~~ [Finished]
- ~~Site html search to get a more specific output~~ [Finished]
- ~~Integrating database insertion into GUI~~ [Finished]
- ~~Adding credits to hotbar on the top of the GUI~~ [Finished]

### Additional Credits

- Maze aka. Black_eks for creating the tools icon. [Instagram](https://www.instagram.com/black_eks/)
- Doelicious for letting me use her username extensively for testing purposes. [Twitter](https://www.twitter.com/Doelici0us/)
