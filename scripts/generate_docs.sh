#!/usr/bin/env bash

set -e

typer functions/main.py utils docs --name functions --output docs_mk/cli.md
