import os, configparser, time, logging
from trakt import init, core, movies
from datetime import timezone, timedelta

def checkAuthFile():
    operatingSystem = os.name
    if "nt" in operatingSystem:
        logger.debug("WINDOWS DETECTED")
        pytraktPath = "\.pytrakt.json"
    elif "posix" in operatingSystem:
        logger.debug("UNIX DETECTED")
        pytraktPath = "/.pytrakt.json"
    else:
        logger.debug("UNKNOWN OS DETECTED, SKIPPING")
        exit(1)
    homePath = os.path.expanduser("~")
    if os.path.isfile(homePath + pytraktPath):
        return True
    else:
        return False

def checkTrakt():
    try:
        movies.trending_movies()
        return True
    except:
        if checkAuthFile == True:
            os.remove(home + "\.pytrakt.json")
            logger.debug("AUTH FILE DELETED")
        return False

def connectTrakt():
    print("Trying (first) authentication, user input required ...")
    core.AUTH_METHOD = core.OAUTH_AUTH
    try:
        init(usernameTrakt, client_id = clientID, client_secret = clientSecret, store = True)
        return True
    except:
        return False

def startAuth(count):
    if checkAuthFile() == True:
        logger.debug("TRAKT AUTH FILE FOUND")
        if checkTrakt() == True:
            logger.info("CONNECTION TO TRAKT WAS SUCCESSFUL")
            exit(0)
        else:
            logger.debug("CONNECTION TO TRAKT WAS NOT SUCCESSFUL")
            if count == 1:
                exit(1)
            else:
                logger.info("TRYING NEW AUTH FOR USER: " + usernameTrakt)
                if connectTrakt() == True:
                    startAuth(1)
                else:
                    logger.info("AUTH NOT SUCCESSFUL")
                    exit(1)
    else:
        logger.debug("TRAKT AUTH FILE NOT FOUND")
        if count == 1:
            exit(1)
        else:
            logger.info("TRYING NEW AUTH FOR USER: " + usernameTrakt)
            if connectTrakt() == True:
                startAuth(1)
            else:
                logger.info("AUTH NOT SUCCESSFUL")
                exit(1)

if __name__== "__main__":
    tzOff = time.localtime().tm_gmtoff
    tzInfo = str(timezone(timedelta(0, tzOff)))
    logging.basicConfig(
        filename = "plextotrakt.log",
        filemode = "a",
        format = "%(asctime)s " + tzInfo + ", %(name)s, %(levelname)s, %(message)s",
        datefmt = "%d-%m-%Y %H:%M:%S",
    )
    config = configparser.ConfigParser()
    config.read("config.ini")
    logLevel = config["general"]["logging"]
    logger = logging.getLogger("traktapi")
    if logLevel == "DEBUG":
        logger.setLevel(logging.DEBUG)
    elif logLevel == "INFO":
        logger.setLevel(logging.INFO)
    elif logLevel == "ERROR":
        logger.setLevel(logging.ERROR)
    else:
        logger.setLevel(logging.NOTSET)
    usernameTrakt = config["trakt"]["username"]
    clientID = config["trakt"]["clientid"]
    clientSecret = config["trakt"]["clientsecret"]
    startAuth(0)
