# DSCI 532 - Group 204 - Milestone 1 Proposal


## Section 1: Motivation and Purpose

Which specific regions in the United States produce the best wines? Which regions provide the best value? What grape varieties consistently get high ratings? There are so many different wines and wineries that it can be difficult for the average person to choose a good quality bottle of wine at a particular price point. 

To address this issue, we propose building a data visualization app that allows a wine shopper to visually explore geographic trends from a large set of wine reviews and compare the qualities of different grapes, wineries, and regions. This should help shoppers pick out the best wine for their budget. We will illustrate how the price, ratings, and value of wines compare across different regions and varieties of grapes in the USA.


## Section 2: Description of the Data

We will be visualizing a dataset of 54,504 reviews for wines from the United States. The full data set contains 130,000 reviews for wines around the world, and was scraped from Wine Enthusiast on November 22nd, 2017. 

Each observation has 14 associated variables describing the wine and our analysis is focusing on the details from the following columns: information about the specific bottle of wine (```variety```,  ```description```, ```title``` , ```points```, and ```price```), as well as geographic information about the winery it comes from (```country```, ```province```, and  ```winery```). Using this data we will also derive a new variable, which is a ```value``` score for the wine calculated as a ratio of ```points``` (quality) to ```price```.


## Section 3: Research Questions and Usage Scenarios



