import tweepy
import time
import datetime

CONSUMER_KEY = "CVoJM7rGjSg8fx1rqQVm4qAkr"
CONSUMER_SECRET = "O7bKdkmENOFuK1Dom9Pu2YvzE5PFjd3qC7p2G0gAGxFtzXS0GM"
ACCESS_TOKEN = "1214920708884709383-dFWeFZBzJ93dcFKs67eDBMQx1eVDeT"
ACCESS_TOKEN_SECRET = "uY8w402iU0ZWpotDSLkXluDiACCDbCqr6fE8nyxFpsyTy"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


def print_rate_limit_exceeded():
    """Prints a message to the screen noting the time when the rate limit was exceeded."""
    current = datetime.datetime.now()
    print("Rate Limit Exceeded: %d:%d:%d" % (current.hour, current.minute, current.second))


def handle_rate_limit(cursor):
    """Sleeps for 15 minutes when the Twitter rate limit is triggered.

    Iterates over the cursor object. When the iterator has no more objects, it
    triggers a StopIteration exception and the function returns.
    """
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            print_rate_limit_exceeded()
            time.sleep(1 * 60)
        except tweepy.TweepError:
            print("NOT AUTHORIZED: SKIPPING")
        except StopIteration:
            return


def handle_lookup_error(user_ids):
    """Sleeps for 15 minutes when the Twitter rate limit is triggered.

    Iterates over the cursor object. When the iterator has no more objects, it
    triggers a StopIteration exception and the function returns.
    """
    try:
        return api.lookup_users(user_ids)
    except tweepy.RateLimitError:
        print_rate_limit_exceeded()
        time.sleep(1 * 60)
    except tweepy.TweepError:
        print("NOT AUTHORIZED: SKIPPING")




def get_followers(handle, count):
    """Returns the followers of a Twitter user as a list of Twitter handles.

    Args:
        handle: String containing the twitter handle to find followers of.
        count: The max number of followers to return.
    """
    toReturn = []
    follower_gen = handle_rate_limit(tweepy.Cursor(api.followers, id=handle, count=min(200, count)).items(count))
    for follower in follower_gen:
        toReturn.append(follower)
    print("200 followers Generated")
    return toReturn

def get_followers_ids(handle, count):
    """Returns the followers of a Twitter user as a list of Twitter handles.

    Args:
        handle: String containing the twitter handle to find followers of.
        count: The max number of followers to return.
    """
    current = 1
    pace = 1
    followers = []
    user_ids = []
    for user_id in handle_rate_limit(tweepy.Cursor(api.followers_ids, id=handle, count=min(5000, count)).items(count)):
        if current == 100:
            print("users: " + str(current*pace))
            pace += 1
            user_ids.append(user_id)
            followers += handle_lookup_error(user_ids)
            current = 1
            user_ids = []
        else:
            user_ids.append(user_id)
            current += 1
    if len(user_ids) != 0:
        followers += handle_lookup_error(user_ids)

    return followers


def get_following_ids(handle, count):
    """Returns the followers of a Twitter user as a list of Twitter handles.

    Args:
        handle: String containing the twitter handle to find followers of.
        count: The max number of followers to return.
    """
    current = 1
    pace = 1
    following = []
    user_ids = []
    for user_id in handle_rate_limit(tweepy.Cursor(api.friends_ids, id=handle, count=min(5000, count)).items(count)):
        if current == 100:
            print("users: " + str(current * pace))
            pace += 1
            user_ids.append(user_id)
            following += handle_lookup_error(user_ids)
            current = 1
            user_ids = []
        else:
            user_ids.append(user_id)
            current += 1
    if len(user_ids) != 0:
        following += handle_lookup_error(user_ids)

    return following



def get_following(handle, count):
    """Returns the accounts a Twitter user is following as a list of Twitter handles.

        Args:
            handle: String containing the twitter handle to find friends of.
            count: The max number of friends to return.
        """
    toReturn = []
    follower_gen = handle_rate_limit(tweepy.Cursor(api.friends, id=handle, count=min(200, count)).items(count))
    for follower in follower_gen:
        toReturn.append(follower)
    print("200 followers Generated")
    return toReturn
