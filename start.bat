@ECHO OFF
python .\timezone.py 1
TIMEOUT /T 5 /NOBREAK
START python .\plextotrakt.py
TIMEOUT /T 5 /NOBREAK
python .\timezone.py 2
