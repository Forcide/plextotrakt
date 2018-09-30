import time, os, sys, configparser

def setTimezone(id):
    config = configparser.ConfigParser()
    config.read("config.ini")
    if id == 1:
        if config["timezone"]["localtimezone"] == "":
            localTimezone = time.tzname[0]
            configLines = open("config.ini").readlines()
            localTimezoneIndex = configLines.index("localtimezone =\n")
            configLines[localTimezoneIndex] = "localtimezone = " + localTimezone + "\n"
            configWrite = open("config.ini", "w")
            configWrite.writelines(configLines)
            configWrite.close()
    elif id == 2:
        configTimezone = config["timezone"]["localtimezone"]
    traktTimezone = "UTC"
    operatingSystem = os.name
    if "nt" in operatingSystem:
        if id == 1:
            os.system("tzutil /s \"%s\"" % (traktTimezone,))
        elif id == 2:
            os.system("tzutil /s \"%s\"" % (configTimezone,))
    elif "posix" in operatingSystem:
        if id == 1:
            os.environ["TZ"] = traktTimezone
            time.tzset()
        elif id == 2:
            timezone = time.tzname[0]
            os.environ["TZ"] = configTimezone
            time.tzset()

if __name__== "__main__":
    setTimezone(int(sys.argv[1]))
