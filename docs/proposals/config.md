# Cam we have a persistent state for functions?

* Status: Proposed
* Deciders: [Piotr]
* Date: 2021-11-23

## Work context

In order to enable functionalities like `autocomplete`, `logging` or resources management, we need an easy and accessible place to store information about the state.

## Problem

We want to have a way of storing information between function executions.

Our goal is to maintain flexibility and ease of definition for the first implementation.

## Proposal

We look into some of the options considered in building this feature.

### Database

Add a database to background to store or retrieve information about the functions.

Something like a postgres DB?

Pros:

* moderate scalability
* safe

Cons:

* big effort
* weight of the implementation
* difficulty with justifying using a database for a CLI tool

### File storage

Use a file to store the configuration in a unified format - `JSON` / `TOML`.

Pros:

* Easy implementation
* All the control
* `cat` to view the content
* One place to store it all

Cons:

* Questionable consistency
* "Ups I deleted the file. What now?"

## Decision

A `database` system for storing information about the state definitely seems like an overkill.

It much more achievable to handle a single file write and reads. We can manipulate it, remove it, create again very easily which means we can make mistakes and fix them quickly.

We are not worried about any consistency issues at this point in time.

## Implementation

We define a `config` module.

This module will store all `functions` specific files. Current files like log files, config file or the registry files, but any other future files if necessary.

Moreover the `config` module stores said `config.toml` file that holds information about the available components, version information and tool specific configuration.

Module's path will evaluated in another document, but it needs to be saved in a location accessible by multiple operating systems.

**The module is created on the first run of the `functions` terminal interface**.

This is when the components are evaluated and the information is saved on file. If you need to reevaluate it is possible to do by deleting the file.

## Summary

The solution chosen should be a simple way of handling the problem enabling all the derived functionalities. If however this becomes insufficient another way should be easily configurable.

We will continue to monitor its validity in the `Internal Alpha` release and suggest improvements and soon the problems become apparent.

<!-- Identifiers, in alphabetical order -->

[Piotr]: https://github.com/Katolus
