import os, sys
import praw
from pprint import pprint
import settings
from getpass import getpass

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
def migrate_all(origin_account: praw.Reddit, destination_account: praw.Reddit, limit: int = None, verbose: bool = False):
    """
    A global method to call all migration methods
    """
    migrate_subreddits(origin_account, destination_account, limit, verbose)
    migrate_upvoted(origin_account, destination_account, limit, verbose)
    migrate_saved(origin_account, destination_account, limit, verbose)
    migrate_friends(origin_account, destination_account, limit, verbose)

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

def migrate_saved(origin_account: praw.Reddit, destination_account: praw.Reddit, posts: list, verbose: bool = True):
    """
    Migrates saved posts from one reddit account to another
    """    
    if utils.is_null_or_empty(posts):
        print(f"Posts list is empty or was not found.")
        return

    print(f"Total items: {len(posts)}")

    for index, post in enumerate(posts):
        try:
            print(f"Migrating post #{index + 1} with id: {post.id}")

            # Remove from origin account
            origin_account.submission(id=post.id).unsave()

            # Add to destination account
            if type(post) == praw.models.Submission:
                submission = destination_account.submission(id=post.id)

                if submission.saved == False:
                    submission.save()
            elif type(post) == praw.models.Comment:
                comment = destination_account.comment(id=post.id)

                if comment.saved == False:
                    comment.save()
        except Exception as ex:
            log.error(ex, f"An error occurred while migrating the post id {post.id}.")

def migrate_upvoted(origin_account: praw.Reddit, destination_account: praw.Reddit, posts: list, verbose: bool = True):
    """
    Migrates a friend list from one reddit account to another
    """    
    if utils.is_null_or_empty(posts):
        print(f"Friends list is empty or was not found.")
        return

    for post in posts:
        try:
            # Remove from origin account
            origin_account.submission(id=post.id).clear_vote()
            
            # Add to destination account
            if type(post) == praw.models.Submission:
                submission = destination_account.submission(id=post.id)

                if submission.likes is None:
                    submission.upvote()
            elif type(post) == praw.models.Comment:
                comment = destination_account.comment(id=post.id)

                if submission.likes is None:
                    comment.upvote()
        except Exception as ex:
            log.error(ex, f"An error occurred while migrating the post id {post.id}.")

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
            log.error(ex, f"An error occurred while migrating the subreddit '{subreddit_name}'.")

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

    for post in posts:
        try:
            print(f"==================================================")
            print(f"Title: {post.title}")
            print(f"Subreddit Name: {post.subreddit_name_prefixed}")
            print(f"Subreddit Type: {post.subreddit_type}")
            print(f"Is NSFW?: {post.over_18}")
            print(f"Permalink: {post.permalink}")
            print(f"Url: {post.url}")
        except Exception as ex:
            log.error(ex, f"An error occurred while reading saved post information for id {post.id}.")

def list_upvoted(posts: list):
    """
    Lists upvoted posts information from the given account
    """
    if utils.is_null_or_empty(posts):
        return

    for post in posts:
        try:
            print(f"==================================================")
            print(f"Title: {post.title}")
            print(f"Subreddit Name: {post.subreddit_name_prefixed}")
            print(f"Subreddit Type: {post.subreddit_type}")
            print(f"Is NSFW?: {post.over_18}")
            print(f"Url: {post.url}")
        except Exception as ex:
            log.error(ex, f"An error occurred while reading post information for id {post.id}.")

    print(f"Total Items: {len(posts)}")

def list_subreddits(subreddits: list):
    """
    Lists subreddits information from the given account
    """
    if utils.is_null_or_empty(subreddits):
        return

    for subreddit in subreddits:
        try:
            print(f"==================================================")
            print(f"Display Name: {subreddit.display_name_prefixed}")
            print(f"Subreddit Type: {subreddit.subreddit_type}")
            print(f"Is NSFW?: {subreddit.over18}")
        except Exception as ex:
            log.error(ex, f"An error occurred while reading subreddit information for id {subreddit.id}.")

# Get methods
def get_friends(reddit: praw.Reddit, limit: int = None):
    """
    Gets a list of friends from the given reddit account

    :returns: list<praw.models.Redditor>
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

def get_saved(reddit: praw.Reddit, limit: int = None, type: str = None, is_nsfw: bool = None):
    """
    Gets a list of saved posts from the given reddit account

    :returns: list<praw.models.Subreddit>
    """
    posts = None

    if reddit is None:
        print("No reddit instance defined.")
        return posts

    try:
        posts = list(reddit.user.me().saved(limit=limit))

        if not utils.is_null_or_empty(type):
            posts = [post for post in posts if post.subreddit_type == type]

        if is_nsfw is not None:
            posts = [post for post in posts if post.over_18 == is_nsfw]
    except Exception as ex:
        log.error(ex, "An error occurred while reading saved posts information.")
    
    return posts

def get_upvoted(reddit: praw.Reddit, limit: int = None, type: str = None, is_nsfw: bool = None):
    """
    Gets a list of saved posts from the given reddit account

    :returns: list<praw.models.Subreddit>
    """
    posts = None

    if reddit is None:
        print("No reddit instance defined.")
        return posts

    try:
        posts = list(reddit.user.me().upvoted(limit=limit))

        if not utils.is_null_or_empty(type):
            posts = [post for post in posts if post.subreddit_type == type]

        if is_nsfw is not None:
            posts = [post for post in posts if post.over_18 == is_nsfw]
    except Exception as ex:
        log.error(ex, "An error occurred while reading upvoted posts information.")
    
    return posts

def get_subreddits(reddit: praw.Reddit, limit: int = None, type: str = None, is_nsfw: bool = None):
    """
    Gets a list of subreddits subscribed from the given reddit account

    :returns: list<praw.models.Subreddit>
    """
    subreddits = None

    if reddit is None:
        print("No reddit instance defined.")
        return subreddits

    try:
        subreddits = list(reddit.user.subreddits(limit=limit))

        if not utils.is_null_or_empty(type):
            subreddits = [subreddit for subreddit in subreddits if subreddit.subreddit_type == type]
        
        if is_nsfw is not None:
            subreddits = [subreddit for subreddit in subreddits if subreddit.over18 == is_nsfw]
    except Exception as ex:
        log.error(ex, "An error occurred while reading subreddits information.")
    
    return subreddits

def get_account_input():
    """
    """
    username = input("Username: ")
    password = getpass(prompt="Password: ")
    client_id = input("Client ID: ")
    client_secret = input("Client Secret: ")
    user_agent = input("User Agent: ")

    if utils.is_null_or_empty(user_agent) and not utils.is_null_or_empty(username):
        user_agent = f"migrate by /u/{username}"

    return get_reddit_instance(client_id, client_secret, user_agent, username, password)

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

    #upvoted = get_upvoted(reddit=reddit, is_nsfw=True)
    #list_upvoted(posts=upvoted)
    # migrate_upvoted(origin_account=reddit, destination_account=get_account_input(), posts=upvoted)

    #saved = get_saved(reddit=reddit, is_nsfw=True)
    #list_saved(posts=saved)
    #migrate_saved(origin_account=reddit, destination_account=get_account_input(), posts=saved)

    # migrate_subreddits(origin_account=reddit, destination_account=get_account_input(), limit=1)
    # migrate_friends(origin_account=reddit, destination_account=get_account_input(), limit=1)

if __name__ == "__main__":
    main()