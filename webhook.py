import json, configparser, logging, time, os
from flask import Flask, request
from trakt import tv, movies
from datetime import timezone, timedelta

app = Flask(__name__)
@app.route("/",methods=["POST"])
def plexWebhook():
    data = request.form
    try:
        payload = json.loads(data["payload"])
    except:
        logger.debug("ERROR WITH PAYLOAD")
        return "ERROR"
    if payload["Account"]["title"] == usernamePlex:
        if payload["event"] == "media.scrobble":
            if payload["Metadata"]["librarySectionType"] == "show":
                showTitle = payload["Metadata"]["grandparentTitle"]
                showSeason = int(payload["Metadata"]["parentIndex"])
                showEpisode = int(payload["Metadata"]["index"])
                traktEpisode = tv.TVEpisode(showTitle, showSeason, showEpisode)
                try:
                    traktEpisode.mark_as_seen()
                    logger.info(payload["Account"]["title"] + ": SEND SCROBBLE TO TRAKT FOR, " + str(traktEpisode)[13:])
                except:
                    logger.debug(payload["Account"]["title"] + ": COULD NOT SEND DATA TO TRAKT FOR, " + str(traktEpisode)[13:])
            elif payload["Metadata"]["librarySectionType"] == "movie":
                movieTitle = payload["Metadata"]["title"]
                movieYear = int(payload["Metadata"]["year"])
                traktMovie = movies.Movie(movieTitle, movieYear)
                try:
                    traktMovie.mark_as_seen()
                    logger.info(payload["Account"]["title"] + ": SEND SCROBBLE TO TRAKT FOR, " + str(traktMovie)[9:])
                except:
                    logger.error(payload["Account"]["title"] + ": COULD NOT SEND DATA TO TRAKT FOR, " + str(traktMovie)[9:])
            else:
                logger.debug(payload["Account"]["title"] + ": WRONG MEDIA TYPE, " + payload["Metadata"]["librarySectionType"])
        else:
            logger.debug(payload["Account"]["title"] + ": NO SCROBBLE, " + payload["event"])
    else:
        logger.debug(payload["Account"]["title"] + ": WRONG USER")
    return "OK"

if __name__ == "__main__":
    operatingSystem = os.name
    if "posix" in operatingSystem:
        os.environ['TZ'] = 'UTC'
        time.tzset()
    tzOff = time.localtime().tm_gmtoff
    tzInfo = str(timezone(timedelta(0, tzOff)))
    logging.basicConfig(
        filename = "plextotrakt.log",
        filemode = "a",
        format = "%(asctime)s " + tzInfo + ", %(name)s, %(levelname)s, %(message)s",
        datefmt = "%d-%m-%Y %H:%M:%S",
        level = logging.ERROR
    )
    config = configparser.ConfigParser()
    config.read("config.ini")
    logLevel = config["general"]["logging"]
    logger = logging.getLogger("webhook")
    if logLevel == "DEBUG":
        logger.setLevel(logging.DEBUG)
    elif logLevel == "INFO":
        logger.setLevel(logging.INFO)
    elif logLevel == "ERROR":
        logger.setLevel(logging.ERROR)
    else:
        logger.setLevel(logging.NOTSET)
    if "posix" in operatingSystem:
        logger.debug("LINUX DETECTED, SCRIPT TIMEZONE SET TO UTC")
    usernamePlex = config["plex"]["username"]
    logger.info("FLASK APP GOING TO INITIALIZE NOW")
    app.run(host="0.0.0.0")
