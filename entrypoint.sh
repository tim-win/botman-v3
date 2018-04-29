#!/bin/sh

cd /botman-v3/

echo "Some bad assed params right here: $@"
exec "$@"
