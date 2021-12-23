# Add a `sync` subcommand

We are trying to figure out how to efficiently sync different components with in the state of the registry.

Update the registry will be done by running sub-commands like

```bash
functions sync local
```

that will update the registry against the currently built and running `docker` components.

Similarly a cloud component can be synced by running

```bash
functions sync gcp
```

which will query the provider for the list of matching components and update the local state accordingly.

Different components will have different ways of handling the differences.

For cloud it makes sense to take the cloud truth as being the correct one.

Locally it might be up to a user to decide what to do with an image that is built but not present in the registry (strong edge case).
