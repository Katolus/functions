#!/usr/bin/env bash

set -e

# Go to the root of the github repository
cd $(git rev-parse --show-toplevel)

# Export .env variables to be in shell execution scope
export $(cat .env | xargs)

exec $@
