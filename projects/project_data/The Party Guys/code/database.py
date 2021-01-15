import sqlite3

PATH_TO_DATABASE = "./data/sql.db"

conn = sqlite3.connect(PATH_TO_DATABASE)
c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")

DROP_NEWSPAPERS_QUERY = '''DROP TABLE IF EXISTS "newspapers";'''
DROP_FOLLOWERS_QUERY = '''DROP TABLE IF EXISTS "followers";'''
DROP_FOLLOWED_QUERY = '''DROP TABLE IF EXISTS "followeds";'''
DROP_NEWSPAPER_FOLLOWING_QUERY = '''DROP TABLE IF EXISTS "newspaper_following";'''
DROP_ACCOUNT_FOLLOWING_QUERY = '''DROP TABLE IF EXISTS "account_following";'''
DROP_POLITICIANS_QUERY = '''DROP TABLE IF EXISTS "politicians";'''

CREATE_NEWSPAPERS_QUERY = '''CREATE TABLE IF NOT EXISTS newspapers (
    handle VARCHAR(15) PRIMARY KEY NOT NULL,
    name VARCHAR(50)
);'''

CREATE_FOLLOWERS_QUERY = '''CREATE TABLE IF NOT EXISTS followers (
    id VARCHAR(30),
    handle VARCHAR(15) PRIMARY KEY NOT NULL,
    name VARCHAR(50),
    location VARCHAR(50),
    url VARCHAR(100),
    num_friends INT,
    num_followers INT,
    num_lists INT,
    num_favorites INT,
    num_statuses INT,
    created_at DATETIME,
    protected INT,
    verified INT,
    description VARCHAR(200)
);'''

CREATE_FOLLOWED_QUERY = '''CREATE TABLE IF NOT EXISTS followeds (
    handle VARCHAR(15) PRIMARY KEY NOT NULL
);'''

CREATE_NEWSPAPER_FOLLOWING_QUERY = '''CREATE TABLE IF NOT EXISTS newspaper_following (
    newspaper_handle VARCHAR(15) NOT NULL,
    follower_handle VARCHAR(15) NOT NULL,
    FOREIGN KEY (newspaper_handle) REFERENCES newspapers(handle),
    FOREIGN KEY (follower_handle) REFERENCES followers(handle),
    PRIMARY KEY (newspaper_handle, follower_handle)
);'''

CREATE_ACCOUNT_FOLLOWING_QUERY = '''CREATE TABLE IF NOT EXISTS account_following (
    followed_handle VARCHAR(15) NOT NULL,
    follower_handle VARCHAR(15) NOT NULL,
    FOREIGN KEY (followed_handle) REFERENCES followeds(handle),
    FOREIGN KEY (follower_handle) REFERENCES followers(handle),
    PRIMARY KEY (followed_handle, follower_handle)
);'''

CREATE_POLITICIANS_QUERY = '''CREATE TABLE IF NOT EXISTS politicians (
    handle VARCHAR(15) PRIMARY KEY NOT NULL,
    name VARCHAR(50),
    score REAL
);'''

INSERT_NEWSPAPER = '''INSERT OR IGNORE INTO newspapers VALUES (?, ?);'''
INSERT_FOLLOWER = '''INSERT OR IGNORE INTO followers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
INSERT_FOLLOWED = '''INSERT OR IGNORE INTO followeds VALUES (?);'''
INSERT_NEWSPAPER_FOLLOWING = '''INSERT OR IGNORE INTO newspaper_following VALUES (?, ?)'''
INSERT_ACCOUNT_FOLLOWING = '''INSERT OR IGNORE INTO account_following VALUES (?, ?)'''
INSERT_POLITICIANS_FOLLOWING = '''INSERT OR IGNORE INTO politicians VALUES (?, ?, ?)'''


# def drop_existing():
#     """Deletes existing tables."""
#     c.execute(DROP_NEWSPAPER_FOLLOWING_QUERY)
#     c.execute(DROP_POLITICAL_FOLLOWING_QUERY)
#     c.execute(DROP_FOLLOWED_QUERY)
#     c.execute(DROP_FOLLOWERS_QUERY)
#     c.execute(DROP_NEWSPAPERS_QUERY)
#     c.execute(DROP_POLITICIANS_QUERY)


def insert_newspapers(newspapers):
    for newspaper in newspapers:
        c.execute(INSERT_NEWSPAPER, newspaper)
    conn.commit()


def insert_followers(followers):
    for follower in followers:
        c.execute(INSERT_FOLLOWER, follower)
    conn.commit()


def insert_followeds(followeds):
    for followed in followeds:
        c.execute(INSERT_FOLLOWED, followed)
    conn.commit()


def insert_newspaper_followings(followings):
    for following in followings:
        c.execute(INSERT_NEWSPAPER_FOLLOWING, following)
    conn.commit()


def insert_account_followings(followings):
    for following in followings:
        c.execute(INSERT_ACCOUNT_FOLLOWING, following)
    conn.commit()


def insert_politicians(politicians):
    for politician in politicians:
        c.execute(INSERT_POLITICIANS_FOLLOWING, politician)
    conn.commit()


def create_tables():
    """Creates three new SQL tables and overwrites old tables.

    1. accounts: handle, account name, int 0 to 2 where 0 = newspaper, 1 = RI politician, 2 = national politician
    2. newspaper_following: handle, account name (all accounts that follow newspapers in accounts table)
    3. political_following: handle, account name (all newspaper followers that follow politicians)"""


    c.execute(CREATE_NEWSPAPERS_QUERY)
    c.execute(CREATE_FOLLOWED_QUERY)
    c.execute(CREATE_FOLLOWERS_QUERY)
    c.execute(CREATE_NEWSPAPER_FOLLOWING_QUERY)
    c.execute(CREATE_ACCOUNT_FOLLOWING_QUERY)
    c.execute(CREATE_POLITICIANS_QUERY)
    conn.commit()
