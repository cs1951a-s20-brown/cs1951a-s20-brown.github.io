Data Spec:

Our combined data is stored in a SQLite database. All fields are required, and there were no missing values in rows of the original datasets. No other assumptions were made about the keys and cross-references. Explanations of what each column represents are listed below.

location_name (TEXT): name of the geographic unit this data point is from, which could be place name, county name, region name, or state name

location_type (TEXT): type of geographic unit described by location name. PL=Place (includes cities, towns, and census designated places); CO=County; RE=region; CA=State.

region_name (TEXT): name of Metropolitan Planning Organizations (MPO) region as reported in the 2010 California Regional Progress Report

race_eth (TEXT): name of race/ethnic group (AIAN; Asian; AfricanAm; Latino; NHOPI; White; Multiple; Other; Total)

pop_trans_acc (INTEGER): Population count (at census block level) within 1/2 mile of high quality transit stop (<15 min waiting time at peak commute hours)

pop2010 (INTEGER): total population in 2010

p_trans_acc (REAL): Percent of the specified population (at census block level) within 1/2 mile of high quality transit stop (<15 min waiting time at peak commute hours)
 
mode (TEXT): short name for mode of transportation to work. ATHOME = worked at home; BICYCLE = bicycle; PUBLICTR= public transportation; WALK = walk to work; CAR = car, truck or van: Drove Alone; CARPOOL = car, truck or van: carpooled; CARTOTAL= car, truck or van

pop_total (INTEGER): total number of workers 16 years old or older in specified population from 2000

pop_mode  (INTEGER): number of workers in specified population who use this mode of transportation for work

percent  (REAL): percent of residents mode of transportation to work from population aged 16 years and older
