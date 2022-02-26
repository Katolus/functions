# `functions` - architecture overview

* Status: Proposed
* Deciders: [Piotr]
* Date: 2022-02-23

## Context and Problem Statement

This document describes all the architectural components used in the layout of the app.

It describe the assumed flow of the app under certain user stories and how different components fall into a full composition.

The architecture of the project has been developed in iterative process of improvement to the base concept (ADR-0001) and this document will formalize the decisions and provide shape and form context.

## Users

We are taking into the account following user stories:

* user has never worked with function as a service
* user has existing functions and wants to use the tool for unification and easy of use
  * locally on the machine of work
  * remotely in a form of a repository
* machine use, as an example being part of a CI/CD

## Goals

### Seamless installation

**Problem**: We want our users to have a single line and minimal complexity installation journey.

In the driver of *simplicity* the installation should be a quick and easy process. This should include all the ways of managing functions.

### Hight modularity

**Problem**: We want to allow user to decide which parts of the package are required and which one's are not.

This means that if the user only needs the local setup, then installing docker should be the only thing required to run those commands.

Some of the questions we need to answer with the solution:

* How do we figure out which components are available?
* How do we store that information?
* How do we change that state?
* Do we remove or update that information?
* Do we run any validation? If so, then when? How often?

### Components sync

**Problem**: We need to have a consistent way of knowing what is happening with various parts of the application at the lowest operational cost.

This means we want to know which functions are currently deployed, but we don't want to run a check every time a script is run, because that is very inefficient in the CLI way.

Some of the questions we need to answer with the solution:

* How and when do we query and store the current state of the `Docker` component? Is a function running, stopped, built?

### Assumptions

Our users are technically skilled individuals or organisation that have necessary skills to operate a CLI tool.

### Constraints

No constrains at the moment.

## Decision Drivers

* Implementation complexity
* Simplicity of use
* Configurability

### App Diagram

*Insert a diagram representing different interactions between components.*

![Functions app diagram](../assets/diagrams/functional_layout.png)


## Decision Impact

| Interested Parties/Groups | Informed |
| ------------------------- | -------- |
| All Users                 | N/A      |

### How will this decision be communicated to the public

There is no need to communicate it to any channels as it is a documentation written prior to any releases. It is bound to the first release.

## Links

* [ADR-0001](0001_initial_setup.md)

<!-- Identifiers, in alphabetical order -->

[Piotr]: https://github.com/Katolus
