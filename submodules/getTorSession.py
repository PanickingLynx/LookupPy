import requests
from termcolor import colored

#Get a new tor Proxy session
def newTorSession():
    #Create a session
    newProxy = requests.session()
    #Define the session
    newProxy.proxies = { 'http': 'socks5h://localhost:9050',
                        'https': 'socks5h://localhost:9050'}
    print(colored("Starting a new Tor proxy session....", "magenta"))
    return newProxy