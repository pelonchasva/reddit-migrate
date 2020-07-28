import os, sys
import praw
from pprint import pprint

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

# Remove methods
def remove_friends(reddit: praw.Reddit, limit: int = None, verbose: bool = False):
    """
    Removes friends in the given account
    """
    if reddit is None:
        print("No reddit instance defined.")
        return

    try:
        friends = reddit.user.friends(limit=limit)

        for friend in friends:
            if verbose:
                print(f"Removing friend => {friend.name}")
            
            friend.unfriend()
    except Exception as ex:
        log.error(ex, "An error occurred while removing friends.")

def remove_saved(reddit: praw.Reddit, limit: int = None, verbose: bool = False):
    """
    Removes saved submissions in the given account
    """
    if reddit is None:
        print("No reddit instance defined.")
        return

    try:
        posts = reddit.user.me().saved(limit=limit)

        for post in posts:
            if verbose:
                print(f"Removing save post => {post.title}")
            
            post.unsave()
    except Exception as ex:
        log.error(ex, "An error occurred while removing saved posts.")

def remove_upvoted(reddit: praw.Reddit, limit: int = None, verbose: bool = False):
    """
    Removes upvoted posts in the given account
    """
    if reddit is None:
        print("No reddit instance defined.")
        return

    try:
        posts = reddit.user.me().upvoted(limit=limit)

        for post in posts:
            if verbose:
                print(f"Removing upvoted post => {post.title}")
            
            post.downvote()
    except Exception as ex:
        log.error(ex, "An error occurred while removing upvoted posts.")

def remove_subreddits(reddit: praw.Reddit, limit: int = None, verbose: bool = False):
    """
    Removes subreddits from the given account
    """
    if reddit is None:
        print("No reddit instance defined.")
        return

    try:
        subreddits = reddit.user.subreddits(limit=limit)

        for subreddit in subreddits:
            if verbose:
                print(f"Removing subrredit => {subreddit.name}")
    except Exception as ex:
        log.error(ex, "An error occurred while removing subscribed subrredits.")

# Account migration methods

# Information methods
def list_friends(reddit: praw.Reddit, limit: int = None):
    """
    Lists friends information from the given account
    """
    if reddit is None:
        print("No reddit instance defined.")
        return

    try:
        friends = reddit.user.friends(limit=limit)

        for friend in friends:
            print(f"Name: {friend.name}")
    except Exception as ex:
        log.error(ex, "An error occurred while reading friends information.")

def list_saved(reddit: praw.Reddit, limit: int = None):
    """
    Lists saved posts information from the given account
    """
    if reddit is None:
        print("No reddit instance defined.")
        return

    try:
        posts = reddit.user.me().saved(limit=limit)

        for post in posts:
            pprint(post)
            break
    except Exception as ex:
        log.error(ex, "An error occurred while reading saved posts information.")

def list_upvoted(reddit: praw.Reddit, limit: int = None):
    """
    Lists upvoted posts information from the given account
    """
    if reddit is None:
        print("No reddit instance defined.")
        return

    try:
        posts = reddit.user.me().upvoted(limit=limit)

        for post in posts:
            pprint(post)
            break
    except Exception as ex:
        log.error(ex, "An error occurred while reading upvoted posts information.")

def list_subreddits(reddit: praw.Reddit, limit: int = None):
    """
    Lists subreddits information from the given account
    """
    if reddit is None:
        print("No reddit instance defined.")
        return

    try:
        subreddits = reddit.user.subreddits(limit=limit)

        for subreddit in subreddits:
            pprint(subreddit)
            break
    except Exception as ex:
        log.error(ex, "An error occurred while reading subreddits information.")

def main():
    """
    """
    pass

if __name__ == "__main__":
    main()