# `add` command

* Status: Proposed
* Deciders: [Piotr]
* Date: 2021-12-28

## Context and Problem Statement

We need to have a way of adding pre-existing functions into the scope of package's registry. If not, the package has a very limited functionality.

We need to keep in mind that the 'folder' added to function's scope need to have a standard structure with some of the files being required and **validation** practices in place.

We need to make sure to **add** the files that are missing, but cannot be present like `Dockerfile` to run these functions locally.

## Proposed Solution

We suggest adding an `add` command that would take a path, run validations, add necessary files and store the new function path in the registry with an appropriate state.

### Details

1. Add function will be component independent, root command that takes a single file path argument and options as find fitted.
2. Ask about details of the functions:
   * name of the function.
   * type of a function.
   * language of execution.
3. Loads the directory given by the path and makes sure that:
   * a `Dockerfile` is not present.
   * a default language can be derived or must be specified.
   * function language is supported.
   * an entry file is present.
   * validate the the name of the function is not already used.
4. If missing the necessary files need to be generated.
5. Add the new function into the registry.

### Potential problems

There are a lot of potential edge cases on what is added into a folder's directory.

`Dockerfile` will be hard to tailor to a specific language.

Picking up a language from set of files will most likely be messy and hard.

A lot of potential problems so got to make sure we support the simplest version and notify about any forseen errors.

## Benefits

If done well, it will enable people adding different sets of functions into their registry from before working with this package. Also if anything goes wrong, this command should be easy enough to add a `function` back to the registry.

<!-- Identifiers, in alphabetical order -->

[Piotr]: https://github.com/Katolus
