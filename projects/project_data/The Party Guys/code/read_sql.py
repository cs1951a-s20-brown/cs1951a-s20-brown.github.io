import sqlite3
import json


PATH_TO_DATABASE = "../Final-Database-Backups/AllNewspapers.db"

conn = sqlite3.connect(PATH_TO_DATABASE)
c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")

## MIGHT WANT To CHANGE the 25 (min friend count) and 1500 (amount to pull per paper) at some point

GET_NEWSPAPER_FOLLOWERS = '''
With subquery As (SELECT * 
FROM followers f 
JOIN newspaper_following nf ON f.handle = nf.follower_handle),
sub2 AS (SELECT * 
FROM (
    SELECT *, ROW_NUMBER() 
      OVER (Partition BY s.newspaper_handle
            ORDER BY random() ) AS Rank
    FROM subquery s
    ) s2 WHERE Rank <= 1500)
	
SELECT f.name, f.handle, f.newspaper_handle, f.num_friends
FROM sub2 as f
LEFT OUTER JOIN words AS w ON ((f.name LIKE '% ' || w.words || ' %') OR (f.name LIKE w.words || ' %') OR (f.name LIKE '% ' || w.words) OR (f.name LIKE w.words))
WHERE w.words IS NULL 

AND f.protected = 0
AND f.verified = 0 AND f.num_friends > 25;'''

# AND f.name NOT REGEXP '.*[0-9\_\#\@\!\^\&\*\(\)\<\>\~].*'
# AND f.name NOT REGEXP '.*[A-H|J-L|N-Z]+[A-Z]+.*'



def sql_search():
    c.execute(GET_NEWSPAPER_FOLLOWERS)
    result = c.fetchall()
    return result


    # for a in paper_handles:
    #     small = []
    #     large = []
    #     count = 0
    #     for r in result:
    #         if r[2] == a:
    #             if not re.search("[0-9\_\#\@\!\^\&\*\(\)\<\>\~]", r[0]) and not re.search("[A-H|J-L|N-Z]+[A-Z]", r[0]): #r.name?
    #                 if count < max_count:
    #                     if r[3] > 200:
    #                         large.append(r[1])
    #                     else:
    #                         small.append(r[1])
    #                     count += 1



# for r in result:
#     # parsed_json = json.loads(r[0])
#     # name = parsed_json.get('name')
#     # handle = parsed_json.get('screen_name')
#     # id_name = id_name + [(handle, name)]
#     print(r)

# print(id_name)
# print(json.dumps(parsed_json, indent=4, sort_keys=True))
