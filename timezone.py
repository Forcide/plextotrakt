import time, os, sys

def setTimezone(id):
    configTimezone = "W. Europe Standard Time"
    timezone = "UTC"
    operatingSystem = os.name
    if "nt" in operatingSystem:
        if id == 1:
            os.system("tzutil /s \"%s\"" % (timezone,))
        elif id == 2:
            os.system("tzutil /s \"%s\"" % (configTimezone,))
    elif "posix" in operatingSystem:
        if id == 1:
            os.environ["TZ"] = timezone
            time.tzset()
        elif id == 2:
            timezone = time.tzname[0]
            os.environ["TZ"] = configTimezone
            time.tzset()

if __name__== "__main__":
    setTimezone(int(sys.argv[1]))
