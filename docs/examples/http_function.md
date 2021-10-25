# Http function (locally)

1. Create a new http function directory. 

```
functions new http http-function --dir ~/test/
```

Expected output:
```
Added a new http function to -> /home/{user}/test/http-function
```

1. Build the newly created http function (This may take a little bit of time).

```
functions build ~/test/http-function/
```

**Note** - You can add `--show-logs` to see preview the build process.

Expected output: 
```
Successfully build a function's image. The name of the functions is -> http-function
```


1. Running `http-function`.

```
functions run http-function
```

Expected output: 
```
Function (http-function) has started. Visit -> http://localhost:8080
```

1. Work validation. 

```
functions list
```

Expected output: 
```
Function - http-function | Status - Running
```

You should be able to view the newly created functions running by going to  `http://localhost:8080`. 
TODO: Insert screenshot. 

1. Cleaning up. 

Once you done with the function, it is a practice to remove unused.

```
functions stop http-function
```

to stop the running function. 


```
functions remove http-function
```

to remove the `http-function` from the local registry.