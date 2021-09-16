"""Holds functions that ask a user for input"""
import typer


def ask(question: str) -> str:
    return typer.prompt(question)


def confirm(question: str) -> bool:
    return typer.confirm(question)


def confirm_abort(question: str) -> bool:
    return typer.confirm(question, abort=True)
