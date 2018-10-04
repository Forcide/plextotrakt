import time, os, sys, configparser, logging
from datetime import timezone, timedelta

def setTimezone(id):
    if id == 1:
        if config["general"]["localtimezone"] == "":
            logger.debug("NO LOCALTIMEZONE SET IN CONFIG")
            localTimezone = time.tzname[0]
            configLines = open("config.ini").readlines()
            localTimezoneIndex = configLines.index("localtimezone =\n")
            configLines[localTimezoneIndex] = "localtimezone = " + localTimezone + "\n"
            configWrite = open("config.ini", "w")
            configWrite.writelines(configLines)
            configWrite.close()
            logger.debug("WRITING LOCALTIMEZONE TO CONFIG: " + localTimezone)
    elif id == 2:
        configTimezone = config["general"]["localtimezone"]
        logger.debug("LOCALTIMEZONE DETECTED IN CONFIG: " + configTimezone)
    traktTimezone = "UTC"
    operatingSystem = os.name
    if "nt" in operatingSystem:
        logger.debug("WINDOWS DETECTED")
        if id == 1:
            os.system("tzutil /s \"%s\"" % (traktTimezone,))
            logger.info("TIMEZONE SET TO: " + traktTimezone)
        elif id == 2:
            os.system("tzutil /s \"%s\"" % (configTimezone,))
            logger.info("TIMEZONE SET TO: " + configTimezone)
    elif "posix" in operatingSystem:
        logger.debug("UNIX DETECTED")
        if id == 1:
            os.environ["TZ"] = traktTimezone
            time.tzset()
            logger.info("TIMEZONE SET TO: " + traktTimezone)
        elif id == 2:
            timezone = time.tzname[0]
            os.environ["TZ"] = configTimezone
            time.tzset()
            logger.info("TIMEZONE SET TO: " + configTimezone)

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
    logger = logging.getLogger("timezone")
    logLevel = config["general"]["logging"]
    if logLevel == "DEBUG":
        logger.setLevel(logging.DEBUG)
    elif logLevel == "INFO":
        logger.setLevel(logging.INFO)
    elif logLevel == "ERROR":
        logger.setLevel(logging.ERROR)
    setTimezone(int(sys.argv[1]))
