# Deploying a function to GCP

A prerequisite to this tutorial is a requirement that you have an existing function in your registry. We will use a function from the `http` tutorial.

As you will see it is very straightforward to deploy a resources to GCP using `functions`.

Additional assumptions include:

* you have a valid GCP account in `gcloud` scope capable of deploying cloud function resources.
* you have `GCP` available as your component.
* internet connection!

## Run the deployment

It is a simple as running

```console
> functions gcp deploy http-function

'http-function' functions has been deployed to GCP!
```

## Validate the deployment

To validate the state of all of the functions run

```console
> functions list

Function - http-function | Local - STOPPED | GCP - DEPLOYED
```

## Remove a cloud function resource

To remove a cloud function resource run

```console
> functions gcp delete http-function

'http-function' has been removed from GCP!
```

**Note**: You will not be able to remove resources not deployed with `functions`.
