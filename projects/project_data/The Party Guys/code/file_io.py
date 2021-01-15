import csv


def get_news_sources():
    """Fetches Rhode Island newspapers' twitter handles from csv file.

    Returns:
        A list of tuples of strings, where each tuple is formatted as:
        ([twitter handle without leading '@'], [Newspaper name], 0)
        where 0 indicates that the account is a newspaper account.
    """
    sources = []
    with open("data/newspapers.csv", newline='') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            sources.append((row[1].strip(), row[0].strip()))
    return sources


def get_national_politicians():
    """Fetches national politicians' twitter handles from csv file.

    Returns:
        A list of tuples of strings, where each tuple is formatted as:
        ([twitter handle without leading '@'], [Politician's account name], 0)
        where 1 indicates that the account is a national political group.
    """
    handles = []
    with open("data/national_political.csv", newline='') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            handles.append((row[2].strip(), row[1].strip(), None))
    return handles


def get_ri_politicians():
    """Fetches Rhode Island politicians' twitter handles from csv file.

     Returns:
         A list of tuples of strings, where each tuple is formatted as:
         ([twitter handle without leading '@'], [Politician's account name], 2)
         where 2 indicates that the account is a rhode island political group.
     """
    handles = []
    with open("data/rhode_island_political.csv", newline='') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            handles.append((row[1].strip("@ "), row[0].strip(), None))
    return handles


def get_scored_politicians():
    handles = []
    with open("data/scored_handles.csv", newline='') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            if row[2] != "Media Outlets":
                handles.append((row[6].strip(), row[3].strip(), row[7]))
    return handles
