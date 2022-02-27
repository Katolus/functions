# What are we using as our main development branch?

* Status: Accepted
* Deciders: [Piotr]
* Date: 2021-11-23

## Context and Problem Statement

[Describe the context and problem statement, e.g., in free form using two to three sentences. You may want to articulate the problem in form of a question.]

## Details


### Constraints

* Adhere to an understandable standard.

## Decision Drivers

* Keep it simple.
* Keep it flexible.
* Keep it cheap.
* Keep it safe.

## Considered Options

* `master`/`main`
* `development`

## Decision Outcome

Chosen option: `development`, because we think that it will be the easiest branch names to drive ongoing development efforts. It semantically separate from `master` or `main` and has a clear commitment.

The idea behind this decision is a attempt to create a more accessible development stream.

The vision being that the `master` branch should be focused on the valuable releases associate with package versions releases.

All the tooling that needs to be run to enforce quality should be associated with the `master` branch.

The `master` branch should be protected.

All this should enable a more flexible work around smaller issues in a singular pool of developer(s).

All the PRs should target the `development` branch as base and a release PR should be a combination of sub PRs on a per ready basis.

This means that the tests for various python versions of the package and other heavy duty actions will only be trigger on merges to master.

### Positive Consequences

* low-cost of ongoing work.
* faster development.
* more control over release stages.

### Negative Consequences

* untested changes in `development` might be hard to discover prior to `master` merges.
* slightly more complicated contribution process.

## Pros and Cons of the Options

### `master` / `main`

Use `master` or `main` as the main development branch.

* Good, because it is a well understand pattern.
* Bad, because it will cost us more to run all the check in every merge event.

### `development`

Use `development` as the main development branch.

* Good, because it separates development actions from main tooling branch.
* Good, because it has a clear meaning.
* Good, because it should allow for making quick changes.
* Bad, because it might be a bit confusing.
* Bad, because it might lead untested changes into the main `development` branch.

## Decision Impact

| Interested Parties/Groups | Informed |
| ------------------------- | -------- |
| Contributors              | Yes      |

### How will this decision be communicated to the public

This information is communication via the `CONTRIBUTING.md` document.

<!-- Identifiers, in alphabetical order -->

[Piotr]: https://github.com/Katolus
