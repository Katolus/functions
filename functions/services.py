"""Holds the information about interaction with remote services"""
from functions.gcp import describe_function as gcp_describe_function


def describe_function(function_name: str):
    gcp_describe_function(function_name)
