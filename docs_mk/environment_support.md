Due to limited amount of resources and a narrow development scope, `functions` are available/working on a limited subset of environments (OS + runtime).

## Operating systems

| OS name       | Status    | Was tested?  |
| ------------- | --------- | ------------ |
| Ubuntu(Linux) | Available | Yes          |
| macOS         | Available | Yes - Mildly |
| Windows       | Unknown   | No           |

## Programming languages and runtime versions

There are several places where a language limitation might be enforced by our code.

### Locally

"Functions" managed by the `functions` package are run by `docker` and therefore require correct execution scope. Because of execution scope for various languages requires separate implementations, the current support is limited.

At the moment this is limited to `Python`.

That said, since the scope is defined in the generated `Dockerfile`, there is nothing stopping you from writing your own `Dockerfile` and support your own execution scope.

### GCP

Because cloud functions have a limited runtime [set](https://cloud.google.com/functions/docs/concepts/exec#runtimes), we need to limit these versions as well.

Here is an estimate of what runtimes are available.

| Language  | Version | Value    | Was tested? |
| --------- | ------- | -------- | ----------- |
| Python    | 3.7     | python37 | Yes         |
| Python    | 3.8     | python38 | Yes         |
| Python    | 3.9     | python39 | Yes         |
| Node      | 10      | nodejs10 | No          |
| Node      | 12      | nodejs12 | No          |
| Node      | 14      | nodejs14 | No          |
| Node      | 16      | nodejs16 | No          |
| Java      | 11      | java11   | No          |
| Go        | 1.11    | go111    | No          |
| Go        | 1.13    | go113    | No          |
| Go        | 1.16    | go116    | No          |
| .NET Core | 3.1     | dotnet3  | No          |
| PHP       | 7.4     | php74    | No          |
| Ruby      | 2.6     | ruby26   | No          |
| Ruby      | 2.7     | ruby27   | No          |

Our goal is to find a solution to get this information from an underlying tool, but it is not always possible so we need to bottleneck it at our package level.

We are completely aware that it is not a perfect solution, but are trying to be as transparent as possible.
