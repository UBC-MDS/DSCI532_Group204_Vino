# DSCI 532 - Group 204 - Milestone 1 Proposal


## Section 1: Motivation and Purpose

Which specific regions in the United States produce the best wines? Which regions provide the best value? What grape varieties consistently get high ratings? There are so many different wines and wineries that it can be difficult for the average person to choose a good quality bottle of wine at a particular price point. 

To address this issue, we propose building a data visualization app that allows a wine shopper to visually explore geographic trends from a large set of wine reviews and compare the qualities of different grapes, wineries, and regions. With the help of our app, shoppers should easily be able to pick out the best wine for their budget. We will illustrate how the price, ratings, and value of wines compare across different regions and varieties of grapes in North America.


## Section 2: Description of the Data

We will be visualizing a dataset of 54,504 reviews for wines from the United States. The full data set contains 130,000 reviews for wines around the world, and was scraped from Wine Enthusiast on November 22nd, 2017. This data set was not used by any of our group members for DSCI 531, but we recieved approval from TA Kate Sedivy-Haley to proceed with this new dataset for DSCI 532.

Each observation has 14 associated variables describing the wine. Our analysis focuses on details from the following columns: information about the specific bottle of wine (```variety```,  ```description```, ```title``` , ```points```, and ```price```), as well as geographic information about the winery it comes from (```country```, ```province```, and  ```winery```). Using this data we will also derive a new variable, which is a ```value``` score for the wine calculated as a ratio of ```points``` (quality or rating) to ```price```.


## Section 3: Research Questions and Usage Scenarios

The **research questions** we plan to answer using this dashboard include: which regions, wineries, and grape varieties in North America consistently produce the best rated, priced, and/or valued wine? Does variability exist in which regions produce the best rated, priced, and/or valued wine, and if so, does this variability depend on winery or grape variety?

Additionally, one goal of this app is to help the average person make wine-related decisions in their daily lives. 

For instance, Jerry wants to buy a bottle of wine for his dinner party to impress his guests, but he has a limited budget. How will he decide which wine to buy? When Jerry visits the “V is for Vino” app he will find a comprehensive overview of wines grown throughout North America, where he can [explore] and [compare] the ratings, prices, and values of these wines. Using the app, he can use an interactive drop down menu to rank all wines by his choice of rating, price, or the overall value to [identify] the perfect wine to impress his dinner guests. 

Alice is going down to Napa Valley on vacation and wants to buy a nice bottle of wine to take home. How will she [identify] which bottle is the best to buy in this particular region? When Alice visits the “V is for Vino” app, she can use the interactive chloropleth map on the app to display wineries in different regions within North America. She can filter by region(s) by directly clicking on the map, allowing her to [summarize] the price, rating, and value of all wines within that region. Included in this summary are graphs displaying the distribution of a selected metric (rating, price, or value), a comparison of price and quality with points for the selected region highlighted, and a ranking of all the best wines in that region based on a selected metric (rating, price, or value). 

Heather works as a wine merchant and wants to buy a selection of local wines to supply her wine store. She would like to [identify] highly rated local wineries and [compare] different wine varieties between these wineries to make here selection. Using the "V is for Vino" app, she can filter the dataset to see which regions are close to her by selecting nearby regions on the chloropleth map. She can use a dropdown menu to compare grape varieties across all wineries within only the selected regions. 


