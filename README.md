# plextotrakt
Simple but useful script(s) to scrobble watched shows and movies to Trakt from Plex via webhooks. It catches Plex webhooks and converts them to be send to Trakt.

The code highly depends on the PyTrakt project from moogar0880 and the Flask project from Pallets.

PLEASE NOTE: I am absolutely not a programmer, use the code at your own risk. The code is made for my exact needs.

## Install
Download and extract the folder to any location.

Install the needed python modules (admin user):
  * trakt
  * flask

## Configure
To enable webhooks (Plex Pass required) in Plex go to *Account* - *Webhooks* and set the *URL* to the correct URL, eq `http://192.168.0.100:5000`.

Fill out the included [config.ini](config.ini), find instructions in the file.

At the first run you will be ask to copy and paste an URL in a browser and copy the PIN back in the script window.

## Run
To run the program on Linux:
```
sudo bash start.sh
```

To run the program on Windows:
```
.\start.bat
```

## License
This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.
