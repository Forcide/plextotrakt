import os, trakt.core
from trakt import init, core, movies

def checkAuthFile():
    home = os.path.expanduser("~")
    if os.path.isfile(home + "\.pytrakt.json"):
        return True
    else:
        return False

def checkTrakt():
    try:
        movies.trending_movies()
        return True
    except:
        print("Connecting to Trakt could not have been established!")
        os.remove(home + "\.pytrakt.json")
        return False

def connectTrakt():
    print("Trying (first) authentication, user input required ...")
    core.AUTH_METHOD = trakt.core.OAUTH_AUTH
    init(usernameTrakt, client_id = clientID, client_secret = clientSecret, store = True)

def startAuth():
    loop = 0
    while loop != 3:
        loop =+ 1
        if checkAuthFile() == True:
            if checkTrakt() == True:
                return True
            else:
                connectTrakt()
        else:
            connectTrakt()

usernameTrakt = ""
clientID = ""
clientSecret = ""

if __name__== "__main__":
    startAuth()