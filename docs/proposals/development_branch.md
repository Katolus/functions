# `development` as default branch

* Status: Proposed
* Deciders: [Piotr] <!-- optional -->
* Date: 2021-11-23

## Proposal

We propose to set up the main branch that the majority work from PRs and contributions are commited to be the `development` branch.

The idea behind this decision is a attempt to create a more accessible development stream.

The vision being that the `master` branch should be focused on the valuable releases associate with package versions releases.

All the tooling that needs to be run to enforce quality should be associated with the `master` branch.

The `master` branch should be protected.

All this should enable a more flexible work around smaller issues in a singular pool of developer(s).

All the PRs should target the `development` branch as base and a release PR should be a combination of sub PRs on a per ready basis.

This means that the tests for various python versions of the package and other heavy duty actions will only be trigger on merges to master.

__The details for this process are yet to be established.__

<!-- Identifiers, in alphabetical order -->

[Piotr]: https://github.com/Katolus
