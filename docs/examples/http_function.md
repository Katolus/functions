# Http function (locally)

### Create a new http function directory

```console
functions new http http-function --dir ~/test/
```

Expected output:
```
Added a new http function to -> /home/{user}/test/http-function
```

### Build the newly created http function (This may take a little bit of time).

```
functions build ~/test/http-function/
```

**Note** - You can add `--show-logs` to see preview the build process.

Expected output:
```
Successfully build a function's image. The name of the functions is -> http-function
```


### Running `http-function`.

```
functions run http-function
```

Expected output:
```
Function (http-function) has started. Visit -> http://localhost:8080
```

### Work validation.

```
functions list
```

Expected output:
```
Function - http-function | Status - Running
```

You should be able to view the newly created functions running by going to  `http://localhost:8080`.

![Hello world on localhost](https://user-images.githubusercontent.com/20417569/139000266-f596a100-c018-4591-83c5-d131b778a24e.png)

### Cleaning up

Once you done with the function, it is a practice to remove unused.

```
functions stop http-function
```

to stop the running function.


```
functions remove http-function
```

to remove the `http-function` from the local registry.
