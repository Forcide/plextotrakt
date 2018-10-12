#!/bin/bash
if [ "$(whoami)" != "root" ]; then
  echo "Sorry, you are not root."
  exit 1
fi

python3 traktapi.py
ret=$?
if [ $ret -ne 0 ]; then
  echo "Error with Trakt auth"
  exit 1
fi

screen -S webhook -dm python3 webhook.py
