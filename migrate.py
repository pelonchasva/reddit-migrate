import os, sys
import praw
from pprint import pprint
import settings

# Modules
import utils
from logger import Logger

# Create a log instance
log = Logger(__file__)

def get_reddit_instance(client_id: str, client_secret: str, user_agent: str, username: str, password: str):
    """
    Logs into Reddit using a user account and returns a reddit instance to interact with
    """
    reddit = None

    if utils.is_null_or_empty(client_id):
        print(f"Client ID was not provided.")
        return reddit

    if utils.is_null_or_empty(client_secret):
        print(f"Client Secret was not provided.")
        return reddit

    if utils.is_null_or_empty(user_agent):
        print(f"User agent was not provided.")
        return reddit
    
    if utils.is_null_or_empty(username):
        print(f"Username was not provided.")
        return reddit

    if utils.is_null_or_empty(password):
        print(f"Password was not provided.")
        return reddit

    try:
        reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent, username=username, password=password)
    except Exception as ex:
        log.error(ex, "An error occurred while creating a reddit instance.")

    return reddit

def get_account_preferences(reddit: praw.Reddit):
    """
    """
    pass

# Remove methods
def remove_all(reddit: praw.Reddit, verbose: bool = False):
    """
    A global method to call all removal methods
    """
    pass

def remove_friends(friends: list, verbose: bool = False):
    """
    Removes friends in the given account
    """
    if utils.is_null_or_empty(friends):
        return

    try:
        for friend in friends:
            if verbose:
                print(f"Removing friend => {friend.name}")
            
            friend.unfriend()
    except Exception as ex:
        log.error(ex, "An error occurred while removing friends.")

def remove_saved(posts: list, verbose: bool = False):
    """
    Removes saved submissions in the given account
    """
    if utils.is_null_or_empty(posts):
        return

    try:
        for post in posts:
            if verbose:
                print(f"Removing save post => {post.title}")
            
            post.unsave()
    except Exception as ex:
        log.error(ex, "An error occurred while removing saved posts.")

def remove_upvoted(posts: list, verbose: bool = False):
    """
    Removes upvoted posts in the given account
    """
    if utils.is_null_or_empty(posts):
        return

    try:
        for post in posts:
            if verbose:
                print(f"Removing upvoted post => {post.title}")
            
            post.downvote()
    except Exception as ex:
        log.error(ex, "An error occurred while removing upvoted posts.")

def remove_subreddits(subreddits: list, verbose: bool = False):
    """
    Removes subreddits from the given account
    """
    if utils.is_null_or_empty(subreddits):
        return

    try:
        for subreddit in subreddits:
            if verbose:
                print(f"Removing subrredit => {subreddit.title}")

            subreddit.unsubscribe()
    except Exception as ex:
        log.error(ex, "An error occurred while removing subscribed subrredits.")

# Account migration methods
def migrate_all():
    """
    A global method to call all migration methods
    """
    pass

def migrate_friends(origin_account: praw.Reddit, destination_account: praw.Reddit, limit: int = None, verbose: bool = False):
    """
    Migrates a friend list from one reddit account to another
    """
    friends = get_friends(reddit=origin_account, limit=limit)
    
    if utils.is_null_or_empty(friends):
        print(f"Friends list is empty or was not found.")
        return

    for friend in friends:
        redditor_name = friend.name

        try:
            # Add to destination account
            destination_account.redditor(redditor_name).friend()

            # Remove from origin account
            origin_account.redditor(redditor_name).unfriend()
        except Exception as ex:
            log.error(ex, "An error occurred while migrating the redditor '{redditor_name}'.")

def migrate_saved(origin_account: praw.Reddit, destination_account: praw.Reddit, limit: int = None, verbose: bool = False):
    """
    Migrates saved posts from one reddit account to another
    """
    posts = get_saved(reddit=origin_account, limit=limit)
    
    if utils.is_null_or_empty(posts):
        print(f"Posts list is empty or was not found.")
        return

    for post in posts:
        try:
            # Add to destination account
            

            # Remove from origin account
            
            
        except Exception as ex:
            log.error(ex, "An error occurred while migrating the post.")

def migrate_upvoted(origin_account: praw.Reddit, destination_account: praw.Reddit, limit: int = None, verbose: bool = False):
    """
    Migrates a friend list from one reddit account to another
    """
    posts = get_upvoted(reddit=origin_account, limit=limit)
    
    if utils.is_null_or_empty(posts):
        print(f"Friends list is empty or was not found.")
        return

    for post in posts:
        try:
            # Add to destination account
            

            # Remove from origin account
            
        except Exception as ex:
            log.error(ex, "An error occurred while migrating the post.")

def migrate_subreddits(origin_account: praw.Reddit, destination_account: praw.Reddit, limit: int = None, verbose: bool = False):
    """
    Migrates a list of subreddits from one reddit account to another
    """
    subreddits = get_subreddits(reddit=origin_account, limit=limit)
    
    if utils.is_null_or_empty(subreddits):
        print(f"Subreddits list is empty or was not found.")
        return

    for subreddit in subreddits:
        subreddit_name = subreddit.title

        try:
            # Add to destination account
            destination_account.subreddit(subreddit_name).subscribe()

            # Remove from origin account
            origin_account.subreddit(subreddit_name).unsubscribe()
        except Exception as ex:
            log.error(ex, "An error occurred while migrating the subreddit '{subreddit_name}'.")

# Information methods
def list_friends(friends: list):
    """
    Lists friends information from the given account
    """
    if utils.is_null_or_empty(friends):
        return

    try:
        for friend in friends:
            pprint(vars(friend))
            break
    except Exception as ex:
        log.error(ex, "An error occurred while reading friends information.")

def list_saved(posts: list):
    """
    Lists saved posts information from the given account
    """
    if utils.is_null_or_empty(posts):
        return

    try:
        for post in posts:
            print(f"==================================================")
            print(f"Title: {post.title}")
            print(f"Subreddit Name: {post.subreddit_name_prefixed}")
            print(f"Subreddit Type: {post.subreddit_type}")
            print(f"Is NSFW?: {post.over_18}")
            print(f"Permalink: {post.permalink}")
            print(f"Url: {post.url}")
    except Exception as ex:
        log.error(ex, "An error occurred while reading saved posts information.")

def list_upvoted(posts: list):
    """
    Lists upvoted posts information from the given account
    """
    if utils.is_null_or_empty(posts):
        return

    try:
        for post in posts:
            print(f"==================================================")
            print(f"Title: {post.title}")
            print(f"Subreddit Name: {post.subreddit_name_prefixed}")
            print(f"Subreddit Type: {post.subreddit_type}")
            print(f"Is NSFW?: {post.over_18}")
            print(f"Url: {post.url}")
    except Exception as ex:
        log.error(ex, "An error occurred while reading upvoted posts information.")

def list_subreddits(subreddits: list):
    """
    Lists subreddits information from the given account
    """
    if utils.is_null_or_empty(subreddits):
        return

    try:
        for subreddit in subreddits:
            print(f"==================================================")
            print(f"Display Name: {subreddit.display_name_prefixed}")
            print(f"Subreddit Type: {subreddit.subreddit_type}")
            print(f"Is NSFW?: {subreddit.over18}")
    except Exception as ex:
        log.error(ex, "An error occurred while reading subreddits information.")

# Get methods
def get_friends(reddit: praw.Reddit, limit: int = None):
    """
    Gets a list of friends from the given reddit account

    :returns: list<praw.Redditor>
    """
    friends = None

    if reddit is None:
        print("No reddit instance defined.")
        return friends

    try:
        friends = list(reddit.user.friends(limit=limit))
    except Exception as ex:
        log.error(ex, "An error occurred while fetching friends information.")

    return friends

def get_saved(reddit: praw.Reddit, limit: int = None):
    """
    Gets a list of saved posts from the given reddit account

    :returns: list<praw.Subreddit>
    """
    posts = None

    if reddit is None:
        print("No reddit instance defined.")
        return posts

    try:
        posts = list(reddit.user.me().saved(limit=limit))
    except Exception as ex:
        log.error(ex, "An error occurred while reading saved posts information.")
    
    return posts

def get_upvoted(reddit: praw.Reddit, limit: int = None):
    """
    Gets a list of saved posts from the given reddit account

    :returns: list<praw.Subreddit>
    """
    posts = None

    if reddit is None:
        print("No reddit instance defined.")
        return posts

    try:
        posts = list(reddit.user.me().upvoted(limit=limit))
    except Exception as ex:
        log.error(ex, "An error occurred while reading upvoted posts information.")
    
    return posts

def get_subreddits(reddit: praw.Reddit, limit: int = None):
    """
    Gets a list of subreddits subscribed from the given reddit account

    :returns: list<praw.Subreddit>
    """
    posts = None

    if reddit is None:
        print("No reddit instance defined.")
        return posts

    try:
        posts = list(reddit.user.subreddits(limit=limit))
    except Exception as ex:
        log.error(ex, "An error occurred while reading subreddits information.")
    
    return posts

def main():
    """
    """
    USERNAME = settings.REDDIT_USERNAME
    PASSWORD = settings.REDDIT_PASSWORD
    CLIENT_ID = settings.REDDIT_CLIENT_ID
    CLIENT_SECRET = settings.REDDIT_CLIENT_SECRET
    USER_AGENT = settings.REDDIT_USER_AGENT

    reddit = get_reddit_instance(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT, username=USERNAME, password=PASSWORD)

    if reddit is None:
        return

    #pprint(vars(reddit.config))

    #list_friends(reddit=reddit)
    #list_saved(reddit=reddit)
    #list_upvoted(reddit=reddit)
    #list_subreddits(reddit=reddit)

if __name__ == "__main__":
    main()