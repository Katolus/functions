#!/usr/bin/env bash

set -e

echo "Deploying docs to Github pages..."

poetry run mkdocs gh-deploy

echo "Deploy finished..."
