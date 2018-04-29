#!/bin/bash
# Is this confusing? That's because bash is confusing.
#
# This is a CI script- it regularly pulls / merges from master
# (as this is intended to be run on a production branch), and
# if there are changes it will do the needful. 
#
# Couple of cases for needful here.
#
# First- if master has changed, then build the image, kill the
# running container, and launch a new one. Downtime is trivial,
# even on a very tiny server.
#
# Second- if this script has been updated, then exec the new one
# and pass it a parameter so we know this is the initial run.
# Basically we check git history to see if this script has changed,
# so we could fall into an endless loop where that is always true
# if we aren't careful.
set -euo pipefail
IFS=$"\n\t"

# Flag to avoid endless loops when re-initializing the script.
LOG_FILE=/var/log/botman-v3/botman.log
INITIAL_RUN=1
TIME=15

function update_this() {
    # If this script needs updating, exec the new one.

    echo "Not an initial run- execing new script."
    exec ./build-prod.sh >> "$LOG_FILE" 2>&1
    exit $?
}

function rebuild_app() {
    # Rebuild and relaunch the application.

    echo "Rebuilding the app..."
    docker build -t botman-v3:${GIT_SHA} .
    echo "Removing the existing docker container..."
    docker rm -f botman-v3
    echo "Launching new docker container..."
    docker run \
        -d --name=botman-v3 \
        -v /opt/botman-v3/:/opt/botman-v3 \
        botman-v3:${GIT_SHA}
}

function log_vars_and_stuff() {
    # Echo the important stuff.
    echo $(date)
    echo "GIT_PULL_RC       =    $GIT_PULL_RC"
    echo "UPDATE_SCRIPT     =    $UPDATE_SCRIPT"
    echo "INITIAL_RUN       =    $INITIAL_RUN"
    echo "GIT_SHA           =    $GIT_SHA"
    
}

function maybe_update_script() {
    # Update script if necessary.
    if [ "$UPDATE_SCRIPT" == "0" ]; then
        echo 'Changes to this script found in last git reference.'
        echo "UPDATE_SCRIPT reason found- checking if initial run."
        if [ "$INITIAL_RUN" == "0" ]; then
            update_this
        else
            echo "Initial run. Ignore."
            echo "No endless loops here!"
        fi
    fi
}

function unflag_initial_run() {
    # Flag off initial run- we're looping here.
    if [ $INITIAL_RUN == "1" ]; then
        echo "Turning off initial run."
        INITIAL_RUN=0
    fi
}

function clean_up_old_dockers() {
    echo "Cleaning up all the old/stopped docker images and containers"
    docker rmi $(docker images -q) || true
    docker rm $(docker ps -aq) || true
}

function wait_a_bit() {
    echo "Waiting for $TIME"
    sleep $TIME
}

function main() {
    # Primary while loop
    while true; do
        # Only supports latest commit, so use branches and merge you animal.

        # $GIT_PULL_RC is 0 when no changes from master. 1 when new changes exist.
        GIT_PULL_RC=$(git pull origin master 2>&1 | grep 'Already up-to-date.' > /dev/null; echo $?)

        # $UPDATE_SCRIPT is 0 when this script has changes in the last commit to HEAD.
        # $UPDATE_SCRIPT is 1 when this script is unchanged.
        UPDATE_SCRIPT=$(git diff --name-only HEAD^ | grep 'build-prod.sh' > /dev/null; echo $?)

        # GIT SHA is the current HEAD on the current branch. Expected to be on `production` branch.
        GIT_SHA=$(git rev-parse --short HEAD)

        if [ $INITIAL_RUN == "1" ]; then
            echo "This is the first pass, so lets update the code anyway."
            echo "Forcing GIT_PULL_RC to 1"
            GIT_PULL_RC=1
            echo "GIT_PULL_RC       =    $GIT_PULL_RC"
        fi

        # output
        log_vars_and_stuff

        if [ "$GIT_PULL_RC" != "0" ]; then
            echo '#### Something has changed.'

            # only update script if its a good idea.
            maybe_update_script

            # rebuild the app- that's what we're here for.
            rebuild_app
        fi

        # Flag off initial run- we're looping here.
        unflag_initial_run

        # Clean up all the old/stopped docker images and containers
        clean_up_old_dockers

        wait_a_bit
    done
}

main

