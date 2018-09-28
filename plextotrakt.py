from flask import Flask, request
import json, os, trakt.core
from trakt import init
from trakt.tv import TVEpisode
from trakt.movies import Movie

def checkAuth():
    if os.path.isfile(configOauthPath):
        return
    else:
        print("Authentication File not found!\n Trying first authentication, user input required ...")
        print(init(usernameTrakt, client_id = clientID, client_secret = clientSecret, store = True))

app = Flask(__name__)
@app.route("/",methods=["POST"])
def plexWebhook():
    data = request.form
    try:
        payload = json.loads(data["payload"])
    except:
        print("ERROR WITH PAYLOAD")
    if payload["Account"]["title"] == usernamePlex:
        if payload["event"] == "media.scrobble":
            if payload["Metadata"]["librarySectionType"] == "show":
                showTitle = payload["Metadata"]["grandparentTitle"]
                showSeason = int(payload["Metadata"]["parentIndex"])
                showEpisode = int(payload["Metadata"]["index"])
                traktEpisode = TVEpisode(showTitle, showSeason, showEpisode)
                print(traktEpisode)
                try:
                    traktEpisode.mark_as_seen()
                    print("SEND SCROBBLE TO TRAKT")
                except:
                    print("COULD NOT SEND DATA TO TRAKT")
            elif payload["Metadata"]["librarySectionType"] == "movie":
                movieTitle = payload["Metadata"]["title"]
                movieYear = payload["Metadata"]["year"]
                traktMovie = Movie(movieTitle, movieYear)
                try:
                    traktMovie.mark_as_seen()
                    print("SEND SCROBBLE TO TRAKT")
                except:
                    print("COULD NOT SEND DATA TO TRAKT")
            else:
                print("WRONG MEDIA TYPE")
        else:
            print("NO SCROBBLE")
    else:
        print("WRONG USER")
    return "OK"

usernamePlex = "" # Plex Username
usernameTrakt = "" # Trakt Username
clientID = "" # Trakt App Client ID
clientSecret = "" # Trakt App Client Secret
configOauthPath = "oauth_trakt.json"
trakt.core.AUTH_METHOD = trakt.core.OAUTH_AUTH
trakt.core.CONFIG_PATH = configOauthPath

checkAuth()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
