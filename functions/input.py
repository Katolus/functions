"""Holds functions that ask a user for input"""
import typer

def ask(question: str) -> str:
    typer.prompt()

def confirm(question: str) -> str:
    typer.confirm()