#!/bin/bash

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r /Ultra-Forward-Bot/requirements.txt

echo "Starting Bot..."
cd /Ultra-Forward-Bot || exit
python3 main.py

#!/bin/bash

#echo "Cloning Repo...."

#if [ -z "$BRANCH" ]; then
 # echo "No BRANCH specified, using 'main'..."
  #git clone https://github.com/AkRao47/AK-T-Ultra-Forward-Bot /Ultra-Forward-Bot
#else
  #echo "Cloning branch: $BRANCH"
  #git clone -b "$BRANCH" https://github.com/AkRao47/AK-T-Ultra-Forward-Bot /Ultra-Forward-Bot
#fi

#cd /Ultra-Forward-Bot || exit
#pip install -U -r requirements.txt

#echo "Starting Bot...."
#python3 main.py
