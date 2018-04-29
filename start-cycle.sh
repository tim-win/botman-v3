#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

echo "Kicking off initial Run"
./build-prod.sh >> /var/log/botman-v3/botman.log 2>&1 &

echo "Daemonized, exiting initial script."
exit 0