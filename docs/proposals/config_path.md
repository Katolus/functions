# Where do we store configuration files?

* Status: Proposed
* Deciders: [Piotr] <!-- optional -->
* Date: 2022-01-08

## Work context

We want the app to have a pseudo state in which information about managed functions are stored to enable better management and enhanced development possibilities. In this document want to tackle the problem of storing all the configuration documents and future application specific files in a directory where it can be access by all components that need it. A unified strategy that works well across different operating systems and specific distributions.

## Problem

Unfortunately there is not a single pattern widely approved and implemented by developers working cross systems that instructs an application where to store the config data so that is best for the health of the files and the whole system.

For example linux application developers have a concept of a `SOMETHING` environment variable that usually is empty but if missing they default such actions to the `.config` file on a user's workspace.

This however is unique to Linux and does not apply throughout other systems, hence we need to find a way of tackling the issue and enable usage of this application on Windows and macOS systems.

## Research

To be done...

## Proposal

To be updated...

<!-- Identifiers, in alphabetical order -->

[Piotr]: https://github.com/Katolus

