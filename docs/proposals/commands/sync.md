# `sync` command

* Status: Proposed
* Deciders: [Piotr]
* Date: [2021-12-24]

## Context and Problem Statement

App components like `docker` or `gcp` have their own sources of truth. For technical reasons we cannot avoid that (docker images managed by `docker` etc...). We can and should however make sure we know the last versions state of each of the components.

Currently we experience unlinked docker images that dangle, because they are not present in the registry or ghost functions in registry that have been deleted in a cloud resource.

This is a complex problem to automate, which is why we will rely on a user to let us help to keep this data in sync.

### Details

We are trying to figure out how to efficiently sync different components with in the state of the registry.

We will add a `sync` command that can be called to update registry information for a specific component. Valid options for the command will be limited to the scope of components available.

Update of the registry will be done by running sub-commands like

```bash
functions sync docker
```

that will update the registry against the currently built and running `docker` containers.

Similarly a cloud component can be synced by running

```bash
functions sync gcp
```

which will query the provider for the list of matching components and update the local state accordingly.

Different components will have different ways of handling the differences.

For cloud it makes sense to take the cloud truth as being the correct one, but specifics should referenced to a specific case.

### Potential problems

* We need to find a way to handle conflicts and that may be an issue. It is important to note in here that even in case of a conflict the external components hold the truth and registry is only a place where we store information to combines them.

## Benefits

Once implemented we will be able to keep registry information in sync with component source of truth.

<!-- Identifiers, in alphabetical order -->

[Piotr]: https://github.com/Katolus
