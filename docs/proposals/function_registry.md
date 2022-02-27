# How do we store information about the managed functions?

* Status: Proposed
* Deciders: [Piotr]
* Date: 2021-02-24

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

## Implementation

The core functionality of this feature is defined by the `FunctionRegistry` class.

This class should be used to interact with `registry.json` file. This file holds information about the all the functions in the scope of the tool.

Details of each of the `functions` are defined by an instance of the `FunctionRecord` class and a stored in a JSON format. This class is capable of loading, saving and displaying info about the function in a terminal. It's purpose is to store information about the `name`, `config` and `status`.

### Function vs FunctionRecord

`Function` and `FunctionRecord` can easily be confused so it is important to clearly define their purpose.

`Function` is class that defines variables methods of a instantiated `function` in run time. Use this method to manipulate the function on runtime.

`FunctionRecord` is a class that describes configuration and metadata about the state of the function; as far as registry information is capable. Use this class to handle, pass, update and use function's metadata.

## Outcomes

The truth is that is not the most stable solution, but it offers transparency in viewing the saved information in a file as well as direct modification as needed.

In a `user` scenario this file should not be accessed nor edited.

<!-- Identifiers, in alphabetical order -->

[Piotr]: https://github.com/Katolus
