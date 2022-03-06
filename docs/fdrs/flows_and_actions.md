# Flow and Actions

* Status: Experimental
* Deciders: [Piotr]
* Date: 2022-02-01

## Context

Throughout the functions interactions there are topics and places where a certain "action" is repeated. Say we want to add a function into the registry, we might want to as well sync the registry with components which will entitle adding sync resources in a similar way to the `add` command mentioned before.

## Problem

We want to ensure there is a standard way of handling user "actions" and "flows".

With this approach we hope to avoid code complexity, edge cases, duplication and handle more cases on a larger scale.

The difficulty comes from properly scoping out said actions and flows. The concept fits wonderfully with the idea of modularity and DRY standards.

## Criteria

* Keep it simple.
* Keep it readable.

## Proposal

We suggest grouping user actions and flows into scripts that can be easily used in other modules.

* `actions.py` - holds logic that includes a user interaction like asking for a function name. We need to know that in more than one place. Once we specify it as an action, we can use the same action in all of the places.
* `flows.py` - holds definitions of procedures that are common throughout the code, like loading a config file, exiting if function name already exists or adding a function to the registry.

## Our worries

We worry that we will eventually come across a circular dependency issue that is hard to tackle without a rewrite of the code. This should be avoidable if the code layout is well structured, but that is a challenge on it's own.

<!-- Identifiers, in alphabetical order -->

[Piotr]: https://github.com/Katolus
