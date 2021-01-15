import json
from twitter_api import get_followers, get_following, get_followers_ids, get_following_ids
from file_io import get_news_sources, get_ri_politicians, get_national_politicians, get_scored_politicians
from database import create_tables, insert_newspapers, insert_followers, insert_followeds, insert_newspaper_followings, insert_account_followings, insert_politicians
from read_sql import sql_search
import re

MAX_NEWSPAPER_FOLLOWERS = 800000
MAX_FOLLOWING = 5000
MAX_FOLLOWING_SMALL = 200
MAX_FOLLOWING_EXAMINE = 200
NEW_DATABASE = False


def toBit(input):
    t_f = str(input)
    if t_f == "True":
        return 1
    elif t_f == "False":
        return 0
    else:
        return -1


def get_newspaper_followings(news_sources):
    """Gets the followers of newspaper accounts.

    Retrieves up to MAX_NEWSPAPER_FOLLOWERS followers of each paper.
    Args:
        news_sources: A list of tuples formatted as: ([twitter handle without leading '@'], [Newspaper name], 0)

    Returns:
        followings: List of tuples where each tuple is a newspaper and a single follower of that newspaper.
            Formatted as: ([newspaper handle], [person handle])
        people: Account names of people following newspapers for accounts table.
            Formatted as: ([person handle], None (no name for privacy reasons), 3 (because account is normal person)
    """
    newspaper_handles = [sources[0] for sources in news_sources]
    # newspaper_handles = [newspaper_handles[0]] #only running on Boston Globe
    followings = []
    followers = []
    for newspaper_handle in newspaper_handles:
        for follower in get_followers_ids(newspaper_handle, MAX_NEWSPAPER_FOLLOWERS):
            followers.append((follower.id_str, follower.screen_name, follower.name, follower.location, follower.url,
                              int(follower.friends_count), int(follower.followers_count), int(follower.listed_count),
                              int(follower.favourites_count), int(follower.statuses_count),
                              follower.created_at,
                              toBit(follower.protected), toBit(follower.verified), follower.description))
            followings.append((newspaper_handle, follower.screen_name))
    return followers, followings




def get_account_followings(handles, big):
    """Gets the accounts that follow political twitter accounts.

    Queries up to MAX_FOLLOWING friends of each user when checking if they follow political accounts.
    Args:
        people: Account names of people following newspapers for accounts table.
            Formatted as: ([person handle], None (no name for privacy reasons), 3 (because account is normal person)
        political_handles: A list of tuples formatted as: ([twitter handle without leading '@'], [Account name], ENUM)

    Returns: A list of tuples where each tuple is a pair of political account and person that
        follows said account.
        """
    followings = []
    followeds = []
    for handle in handles:
        if big:
            for followed in get_following_ids(handle, MAX_FOLLOWING):
                followeds.append([followed.screen_name])
                followings.append((followed.screen_name, handle))
        else:
            for followed in get_following(handle, MAX_FOLLOWING_SMALL):
                followeds.append([followed.screen_name])
                followings.append((followed.screen_name, handle))
    return followeds, followings



def filter_followers(news_sources):
    result = sql_search()
    newspaper_handles = [sources[0] for sources in news_sources]
    newspaper_handles = [newspaper_handles[4], newspaper_handles[5], newspaper_handles[6]] #only running on Boston Globe


    followings_all = []
    followeds_all = []

    for a in newspaper_handles:
        small = []
        large = []
        count = 0

        for r in result:
            if r[2] == a:
                if not re.search("[0-9\_\#\@\!\^\&\*\(\)\<\>\~]", r[0]) and not re.search("[A-H|J-L|N-Z]+[A-Z]",
                                                                                          r[0]):  # r.name?
                    if count < MAX_FOLLOWING_EXAMINE:
                        if r[3] > 200:
                            large.append(r[1])
                        else:
                            small.append(r[1])
                    count += 1

        # Comment out one or the other to divide up work between computers
        i = 0
        followedsL = []
        followingsL = []
        followedsS = []
        followingsS = []
        top = max(len(large), len(small))

        while (i < top):
            print(a + ": " + str(i) + "/" + str(top))
            if i < len(large):
                followedsL, followingsL = get_account_followings([large[i]], True)
            if i < len(small):
                followedsS, followingsS = get_account_followings([small[i]], False)
            followeds_all += followedsL
            followings_all += followingsL
            followeds_all += followedsS
            followings_all += followingsS
            i += 1

    return followeds_all, followings_all




def add_politicians():
    politicians = {}
    all_politicians = get_ri_politicians() + get_national_politicians() + get_scored_politicians()
    for politician in all_politicians:
        politicians[politician[0]] = politician
    insert_politicians(politicians.values())


def main():
    # Create tables
    create_tables()

    newspapers = get_news_sources()

    if NEW_DATABASE:
        add_politicians()
        # Insert newpapers
        insert_newspapers(newspapers)

    # Insert followers
    # followers, newspaper_followings = get_newspaper_followings(newspapers)
    # insert_followers(followers)
    # insert_newspaper_followings(newspaper_followings)

    #
    # # Insert followed
    followed, account_following = filter_followers(newspapers)
    # followed, account_followings = get_account_followings(followers)

    # print(len(followed))
    # print(followed[0])
    # print(followed)
    # print(len(account_following))
    # print(account_following[0])

    insert_followeds(followed)
    insert_account_followings(account_following)



if __name__ == "__main__":
    main()
