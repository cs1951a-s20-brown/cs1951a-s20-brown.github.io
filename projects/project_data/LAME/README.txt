Complete Data Spec:

The data came from joining two csv movie datasets together into a single csv
data set. The primary key for both original datasets was the movie title and
release date for a movie. The two movies were eventually joined using the
primary key match as the joining requirement. The features of the dataset
columns are:


- original title (required): the movie title

- original language (optional): The original language of the movie

- rating (optional): The rating of the movie (e.g. PG, PG-13, R)

- genre (required): Genre of the movie (e.g. drama, comedy)

- budget (required): How much money the movie spent in production in dollars

- revenue (required): How much money the movie made in dollars

- release date (required): When the movie was released in theaters

- runtime (optional): Run time of the movie in minutes

- tomatometer rating (required): the average of all the critic scores

- tomatometer count (optional): the number of reviews used to generate the
critic rating

- audience rating (required); the average of all the audience ratings

- audience count (optional): the number of reviews used to generate the
audience rating


Title, language, rating, and genre are all strings while release date is a
convertible datetime and all other features are integers. Both Tomato and
audience ratings are out of 100. The data we have is publicly available making
it acceptable to use. 
