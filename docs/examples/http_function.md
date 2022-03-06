# Create a `http` function and run it locally

HTTP functions can be created to handle HTTP requests.

They are the easiest function to validate working locally.

Follow these steps to get it to work locally.

## Create a new `http` function using the `new` command

```console
functions new http http-function --dir ~/tests/
```

Expected output:

```console
Added a new http function to -> /home/{user}/tests/http-function
```

## Build the newly created http function

In console run

```console
functions build http-function
```

You are building a docker image in the background using the default settings.

**Note**:  You can add `--show-logs` to see preview the build process.

Expected output

```console
Successfully build a function's image. The name of the functions is -> http-function
```

## Running the newly built function`http-function`

To the results and your newly build function, run the following

```console
functions run http-function
```

Expected output

```console
Function (http-function) has started. Visit -> http://localhost:8080
```

### Work validation

To validate that the function is running you can run

```console
functions list
```

Expected output

```console
Function - http-function | Local - RUNNING | GCP - UNKNOWN
```

You should be able to view the newly created functions running by going to `http://localhost:8080`.

![Hello world on localhost](https://user-images.githubusercontent.com/20417569/139000266-f596a100-c018-4591-83c5-d131b778a24e.png)

### Cleaning up

Once you done with the function, it is a practice to remove an unused resource.

```console
functions stop http-function
```

to stop the running function.


```console
functions remove http-function
```

to remove the `http-function` from the local registry

or

```console
functions delete http-function
```

to delete the function with underlying images, containers and even files.
