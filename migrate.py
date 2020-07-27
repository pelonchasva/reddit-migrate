import os, sys
import praw

# Modules
import utils
from logger import Logger

# Create a log instance
log = Logger(__file__)

def get_reddit_instance(client_id: str, client_secret: str, user_agent: str, username: str, password: str):
    """
    Log in into Reddit using a user account and returns a reddit instance to interact with
    """
    reddit = None

    if utils.is_null_or_empty(username):
        print(f"Username was not provided.")
        return reddit

    if utils.is_null_or_empty(password):
        print(f"Password was not provided.")
        return reddit

    try:
        reddit = praw.Reddit(client_id, client_secret, user_agent, username, password)
    except Exception as ex:
        log.error(ex, "An error occurred while creating a reddit instance.")

    return reddit

def main():
    """
    """
    pass

if __name__ == "__main__":
    main()