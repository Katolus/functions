# How do we handle exceptions?

* Status: Proposed
* Deciders: [Piotr]
* Date: 2021-02-23

## Work context

We want to be smart about how we use exceptions in the app. We want to use them as indicators that something has gone wrong or unexpected in the code. For example, if the functions registry could be loaded we want to throw and error specific to that case and handle it with an appropriate message.

## Proposal

We know that exceptions in python can be subclassed and caught accordingly to a level of ancestory.

We suggest using this pattern to throw case specific exceptions grouped in by type and handle the most generic case in case nothing matched.

In order to make this happen and support this feature out of the box without having to remember about handling errors, we want to use a decorator that will wrap each respective command.

The decorator needs to handle each implemented error which is why creating a common base class to inherit exceptions from may save some code.

When implemented, the way for handling an unexpected behavior should be a simple as created a class that inherits from a base error class.

```python
class DocumentationQualityError(FunctionBaseError):
    code = "documentation.not_yet_the_quality"
    msg_template = 'Message to return to the user on error'
```

### Implementation

Error subclasses are included in files named `errors.py`.

Their base classes takes any key argument passed into the classes and saves it on an instance so that it is available for the templated message and stringifying - `msg_template` variable.

This means that you can pass any key argument without the necessity of defining the arguments on a base class.

```python
class IsNotAValidDirectory(FunctionBaseError):
    code = "path.invalid_directory"
    msg_template = "Path '{path}' is not a valid function directory"

...

raise IsNotAValidDirectory(path='/home/paris/')
```

This however means that if you do not pass the reference variable, an error class will throw an error.

All `FunctionBaseError` derived error classes are handled per default handlers defined in the `error_handlers.py` script. If you need to make a default case for handling any errors, use the `error_handler` decorator as per examples in the script file.

The `error_handler` decorator stores references to errors in a `ERROR_REGISTRY` that is used to capture and handle expected errors in the `handle_error` decorator.

`handle_error` decorator handles or all core functionalities by default through a wrapper definition in the `FTyper` class. It is defined on the core class to avoid having to define it on all of the resources.

You can also use `@handle_error` decorator to capture a specific class to be handle in the context of the decorator.

```python
@handle_error(error_class=CaptureErrorOnlyHere)
def some_edge_case_method(): ...
```

<!-- Identifiers, in alphabetical order -->

[Piotr]: https://github.com/Katolus
