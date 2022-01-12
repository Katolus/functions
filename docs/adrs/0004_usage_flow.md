# `functions` high level flow

* Status: Proposed
* Deciders: [Piotr] <!-- optional -->
* Date: 2021-12-23

## Context and Problem Statement

We need to document the technical assumptions around the way this software can be used. Describe user stories through the app flow and how different components fall into full composition.

The project has been based on iterations of improvement to the base concept, however at this point there is a need of formalizing the decisions makings to add a shape and form the way the project is developed.

## Details <!-- optional -->

We want to define the design of the app from different points of perspective and propose a plan of how different components will interact with each other.

Decisions made to the flow should take into the account a user stories of:

* user has never worked with function as a service
* user has existing functions and wants to use the tool for unification and easy of use
  * locally on the machine of work
  * remotely in a form of a repository
* machine use, as an example being part of a CI/CD

## Goals

### Seamless installation

TBU

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

### Assumptions <!-- optional -->

Our users are technically skilled individuals or organisation that have necessary skills to operate a CLI tool.

### Constraints <!-- optional -->

No constrains at the moment.

## Decision Drivers <!-- optional -->

* implementation complexity
* simplicity of use
* configurability

## Considered Options

[Can be either a list of options or in complicated scenarios, a reference to sub documents]

* subcommand components
* sync subcommand
* `init` command

## Decision Outcome

Chosen option: "[option 1]", because [justification. e.g., only option, which meets k.o. criterion decision driver | which resolves force force | … | comes out best (see below)].

### App Diagram

*Insert a diagram representing different interactions between components.*

### Positive Consequences <!-- optional -->

* [e.g., improvement of quality attribute satisfaction, follow-up decisions required, …]
* …

### Negative Consequences <!-- optional -->

* [e.g., compromising quality attribute, follow-up decisions required, …]
* …

## Pros and Cons of the Options <!-- optional -->

### [option 1]

[example | description | pointer to more information | …] <!-- optional -->

* Good, because [argument a]
* Good, because [argument b]
* Bad, because [argument c]
* … <!-- numbers of pros and cons can vary -->

### [option 2]

[example | description | pointer to more information | …] <!-- optional -->

* Good, because [argument a]
* Good, because [argument b]
* Bad, because [argument c]
* … <!-- numbers of pros and cons can vary -->

### [option 3]

[example | description | pointer to more information | …] <!-- optional -->

* Good, because [argument a]
* Good, because [argument b]
* Bad, because [argument c]
* … <!-- numbers of pros and cons can vary -->

## Decision Impact

[Who may be impacted by this decision]

| Interested Parties/Groups | Informed |
| ------------------------- | -------- |
|           N/A             |    N/A   |

### How will this decision be communicated to the public

It is bound to the first release.

## Links <!-- optional -->

* [Link type] [Link to ADR] <!-- example: Refined by [ADR-0005](0005-example.md) -->
* … <!-- numbers of links can vary -->

<!-- Identifiers, in alphabetical order -->

[Piotr]: https://github.com/Katolus
