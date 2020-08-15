from decouple import config
from pprint import pprint
from logger import Logger

log = Logger(__file__)


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
    value = None

    if is_null_or_empty(key):
        print("Key was not specified.")
        return value

    try:
        value = config(key)
    except Exception as ex:
        log.error(ex, f"An error occurred while retrieving the value for the environment variable '{key}'")

    return value


def print_schema(obj):
    """
    Prints the schema from a given object by using vars() method and pprint to display it nicely on the console
    """
    if is_null_or_empty(obj):
        print("Object is not defined.")
        return

    try:
        pprint(vars(obj))
    except Exception as ex:
        log.error(ex, "An error ocurred while parsing the object.")
