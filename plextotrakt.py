import json
from flask import Flask, request
from trakt import tv, movies

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
                traktEpisode = tv.TVEpisode(showTitle, showSeason, showEpisode)
                try:
                    traktEpisode.mark_as_seen()
                    print("SEND SCROBBLE TO TRAKT FOR: " + str(traktEpisode)[13:])
                except:
                    print("COULD NOT SEND DATA TO TRAKT")
            elif payload["Metadata"]["librarySectionType"] == "movie":
                movieTitle = payload["Metadata"]["title"]
                movieYear = int(payload["Metadata"]["year"])
                traktMovie = movies.Movie(movieTitle, movieYear)
                try:
                    traktMovie.mark_as_seen()
                    print("SEND SCROBBLE TO TRAKT FOR: " + str(traktMovie)[9:])
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

if __name__ == "__main__":
    app.run(host="0.0.0.0")
