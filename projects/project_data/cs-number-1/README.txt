Link to complete dataset: https://drive.google.com/open?id=1ZqAqhDke_2B_E-Ht4_wR9IT9ujbMAyKR
A sample of our data can be found in sample.json

Each datafile is named according to the department code it corresponds to.

The fields here are all required:
They have the following keys and values:
	url: The URL of the class on critical review (string)
	title: The name of the class (string)
	review-id: unique ID corresponding to the class and year of reviews (int)
	edition: year of review (string)
	section: semester of class (1 is fall, 2 is spring) (string)
	prof: professor of the class (string)
	frosh: number of freshmen reviewing (int)
	soph: number of sophomore reviewing (int)
	jun: number of juniors reviewing (int)
	sen: number of seniors reviewing (int)
	test-value: review data (dictionary of int arrays)

The structure of test-value is as follows. Notable is that these fields
The fields here are are all optional 1-5 ints except where mentioned.

are the same length, and each index corresponds to a particular student:
	readings: whether the readings were worthwhile
	class-materials: whether class materials were helpful
	difficult: overall class difficulty
	learned: how much a student learned
	loved: how much a student enjoyed the course
	grading-speed: how fast grades were distributed
	grading-fairness: how fair the grades seemed
	non-concs: how much would a student recommend to a non concentrator
	concs: number of concentrators (string 'N' or 'C')
	effective: how effective the presentations were
	efficient: how efficient classes were
	encouraged: whether discussion was encouraged
	passionate: how passionate the teacher was about the material
	receptive: how receptive the teacher was to student needs
	availableFeedback: how available the teacher was to feedback
	requirement: if the class was taken as a requirement
	grade: expected grade (string 'A', 'B', 'C', 'S')
	attendance: proportion of classes attended
	minhours: minimum hours spent per week in preparation (float but unbounded)
	maxhours: maximum hours sptent per week in preparation (float but unbounded)
