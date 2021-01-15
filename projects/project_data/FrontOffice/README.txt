README

Complete Data Spec: 

I. Describe full data format
   We have data for the NBA, MLB, NFL. For each sport there are two csv files: team_performance and salary. 
   So, in all have have six csv files: "nba_team_performance.csv", "mlb_team_performance.csv", "nfl_team_performance.csv", 
   "nba_salary.csv", "mlb_salary.csv", "nfl_salary.csv".
   
   The team_performance tables for each sport include the following columns (excluding "nba_team_performance.csv"):
   a. abv (string): the abbreviation of the team name 
   b. year (int): the year of the season (i.e. if the season is 2000-2001, the year here is 2000) 
   c. name (string): the full name of the team 
   d. points (float): metric used to judge team's performance 
       - for NBA, the total number of points the team has scored during the season
       - for MLB, the average number of runs scored per game by the team
       - for NFL, the total number of points scored during the season
   e. opp_points (float): metric used to judge team's performance 
       - for NBA, the total number of points the team has been scored on during the season
       - for MLB, the average number of runs scored per game by the opponent
       - for NFL, the total number of points allowed during the season
   f. rank (int): metric used to judge team's performance 
       - for NBA, the team’s rank based on the number of points they score per game
       - for MLB, the team’s rank based on their win percentage
       - for NFL, the team’s rank based on the number of points they scored during the season
   g. win_ratio (float): number of wins divided by the number of games played during the season
   
       For "nba_team_performance.csv", we have the following schema: 
       a. conf (string): conference of team, either east or west
       b. rank (int): final rank within conference
       c. winrate: same as win_ratio 
       d. points_scored: same as points
       e. points_conceded: same as opp_points 
       f. srs: simple rating system, combined team performance metric 

   The salary tables for each sport include the following columns (excluding "nba_salary.csv"):
   a. id (string): the unique player id 
   b. year (int): the year of the season (i.e. if the season is 2000-2001, the year here is 2000) 
   c. team (string): the abbreviation of the team name
   d. name (string): the name of the player 
   e. position (string): the position of the player (not for NBA)
   f. salary: the annual salary of the player 
   
   For "nba_salary.csv", we have the same schema but excluding position. 


II. Assumptions about data types and other notes 
    - Only None/missing objects in the data is in the position column in the salary tables 
    - All data is from the past 20 seasons with one exception: NFL salary table only has data from 2001 to 2009
    - Metrics to be used to judge teams' performance are not consistent across sports 
    
    
III. Assumptions about keys and cross-references 
    - For cross referencing between salary and team_performance tables, we use (year, team abbreviation) tuple  
    - Our primary key in our team_performance table is the (year, team abbreviation) tuple, which will also be used as the foriegn 
      key in the salaries table
    
    
IV. "Required" vs. optional fields 
    - The only "required" fields are the keys refereneced above. Other fields are optional. 

