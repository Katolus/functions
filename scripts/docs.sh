#!/usr/bin/env bash

set -e

poetry run typer functions/main.py utils docs --name functions --output docs/cli.md
