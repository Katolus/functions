# How do we store information about the managed functions?

* Status: Accepted
* Deciders: [Piotr] <!-- optional -->
* Date: 2021-11-23

## Problem statement

In order to keep track and managed the functions we need a place to store information about said functions. Something that holds the name of the functions, required variables and settings.

This time information usually is being held in databases, but for the purpose of a command line tool we want to find a way on how to hold this data with the most minimalistic approach. A solution that can be easily coupled with the package and hence removed without any issue. Updates, need to be quick and no palalerilzm is to be expected.

## Proposal

We suggest a simple file based registry which stores the data in a JSON format.

There will be a single json file called `functions.json` and will stored withing the `config` module's path. Inside that file each of the function will be represent as instance of a Python class. This python class will define variables that need to be defined about each of the functions that is to be considered valid.

Things to consider:

* multiple functions
* functions with the same name may overwrite each other, therefore it would be a idea to enforce a uniqueness and enable adding previously "damaged" functions

Each time a CLI is triggered a file will be read and loaded into the memory so that the data about interacted functions is available in the scope of the program. The marshalling and un-marshalling will be performed in a JSON format.

## Outcomes

The truth is that is not the most stable solution, but it offers transparency in viewing the saved information in a file as well as direct modification as needed.

In a `user` scenario this file should be accessed and edited.

<!-- Identifiers, in alphabetical order -->

[Piotr]: https://github.com/Katolus
