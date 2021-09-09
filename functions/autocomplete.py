from functions.validation import valid_function_dirs


def complete_services():
    return ["cloud_function", "cloud_run"]


def complete_function_dir(incomplete: str):
    for name in valid_function_dirs().keys():
        if name.startswith(incomplete):
            yield name


def autocomplete_function_names(incomplete: str):
    # for name 
    ...