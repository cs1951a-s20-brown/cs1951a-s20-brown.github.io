The dataset is combined with two parts, quantified data and news data.

 ---------------------------------------------------------------------

I. Where the data comes from

The quantified data is from "Yahoo!Finance" and processed to change two columns of it.
The news data is from "marketwatch" and "Reuters" these two websites

II. Format of the data

For each stock, in the quantified data file, there are 8 columns. Below is an example:

Date="2016-01-04", Open=102.61, High=105.37, Low=102, Close=105.35, price-change=0.089, p-change=0.09, label=1

a. Date - every trading day from 2016 to 2017 in the format "yyyy-mm-dd"

b. Open - Opening price of the stock in the specific day

c. High - Highest price of the stock in the specific day

d. Low - Lowest price of the stock in the specific day

e. Close - Closing price of the stock in the specific day

f. Price-change - Changing of price on adjacent trading days

g. P-change - the percent of change of price on adjacent trading days

h. Label - 1(up) or -1(down)

In the news data file, there are 2 columns. Below is an example:

Date="2016-01-02", title="'acquisition', 'idea', 'alphabet', 'amazon', 'tech', 'giant'"

a. Date - every day that has news of this stock published from 2016 to 2017

b. Title - key words after data cleaning which could represent the information of this news

-----------------------------------------------------------------------------

Yiyin Zhang
03/10/2020




