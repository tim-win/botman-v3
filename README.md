# Botman V3
For fun slack bot markov chain bot.

Reads 100% of channels it is present in, adding to a sqlite3 db stored both as raw messages and counts of n-grams following other n-grams. Then generates messages randomly with start words, chooses up-to-4 grams one at a time to generate text, and then finishes once it hits a stop words.

The goal here was to get back into natural language processing, and to rewrite a

# Structure
A python3 bot built on the [lins05/slackbot](https://github.com/lins05/slackbot) core, using a sqlite3 file for persistent data.

The `./run.py` entrypoint kicks off the bot, and contains all handlers. Handlers kick off threads that run asynchronously, so long database calls (the prod version of this is running off a no-shit usb thumb drive as root disk, so sometimes it gets slow) do not block additional tasks. This is also why timeouts for working with the sqlite3 backend are... generous.

## Requirements
docker>=17, lolz

## Deployment
Built for deployment on an RPi3- if you need to run a docker container on another system update the `FROM` line in the dockerfile to remove arm achitecture preface.

To run this on a rpi, just clone to disk, make an /opt/botman-v3/ folder, a /var/log/botman-v3/ folder, add a slackbot_settings.py file (see [underlying bot architecture for details](https://github.com/lins05/slackbot)), and run `./start-cycle.sh`.

This jacky hack of a CI script will check github for any changes and automatically cycle out the exsisting container for a new one if any changes are present. Logrotate will break your logs if you don't set up copy/truncate style log rotation.

## Dev Installation
Can be run / developed natively, with different requirements. Dev requirements include virtualenv, virtualenvwrapper, and a recent version of python (3.5 or newer).

Run the following commands to set up a dev environment:

    mkvirtualenv botman-v3 --python=$(which python3)
    pip install -r requirements.txt

Do also include your slackbot_settings.py file (see [underlying bot architecture for details](https://github.com/lins05/slackbot)).
