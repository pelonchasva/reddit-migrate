def is_null_or_empty(obj):
    """
    Returns True if the object is either null or an empty object, False otherwise
    """
    validations = []

    validations.append(obj is None)
    validations.append(obj == "")

    if isinstance(obj, list) or isinstance(obj, dict):
        validations.append(len(obj) == 0)

    return any(validations)

def get_env_value_by_key(key: str):
    """
    Returns the value from an environment variable if exists
    """
    pass