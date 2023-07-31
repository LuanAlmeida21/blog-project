#!/bin/sh

# The shell will interrupt the script execution when a command fails.
set -e

wait_pqsl.sh
collectstatic.sh
migrate.sh
runserver.sh