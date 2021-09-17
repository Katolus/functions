#!/usr/bin/env bash

set -e

poetry run typer functions/main.py utils docs --name functions-cli --output tmp_README.md