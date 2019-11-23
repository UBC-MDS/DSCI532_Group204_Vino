# DSCI 532 - Group 204 - Milestone 1 Proposal


## Section 1: Motivation and Purpose

Which specific regions in the United States produce the best wines? Which regions provide the best value? What grape varieties consistently get high ratings? There are so many different wines and wineries that it can be difficult for the average person to choose a good quality bottle of wine at a particular price point. 

To address this issue, we propose building a data visualization app that allows a wine shopper to visually explore geographic trends from a large set of wine reviews and compare the qualities of different grapes, wineries, and regions. With the help of our app, shoppers should easily be able to pick out the best wine for their budget. We will illustrate how the price, ratings, and value of wines compare across different regions and varieties of grapes in North America.


## Section 2: Description of the Data

We will be visualizing a dataset of 50,500 reviews for wines from the United States. The full data set contains 130,000 reviews for wines around the world, and was scraped from Wine Enthusiast on November 22nd, 2017. This data set was not used by any of our group members for DSCI 531, but we recieved approval from TA Kate Sedivy-Haley to proceed with this new dataset for DSCI 532.

Each observation has 14 associated variables describing the wine. Our analysis focuses on information about the specific bottle of wine (`variety`, `description`, `title` , `points`, and `price`), and geographic information about the winery that it comes from (`country`, `province`, and `winery`).

Using this data we will also derive two new variables:
- A `value` score for the wine, calculated as a ratio of `points` (quality or rating) to `price`.
- A `county` location value for each obersvation, derived from its `winery`, and corresponding id's labelled as `state_id` and `county_id` derived from the [FIPS](https://en.wikipedia.org/wiki/Federal_Information_Processing_Standard_state_code) state and county codes accessed from the [us-atlas](https://github.com/topojson/us-atlas) repository. The county and state mappings will allow us to display data broken down by county and state on a choropleth map.

The resulting variables and their types associated with our analysis are summarised below:

| Variables      | Types  |
|-------------|--------|
| description | Text   |
| country     | Text   |
| province    | Text   |
| winery      | Text   |
| title       | Text   |
| variety     | Text   |
| points      | Number |
| price       | Number |
| value       | Number |
| county      | Text   |
| state_id    | Number |
| county_id   | Number |



## Section 3: Research Questions and Usage Scenarios

The **research questions** we plan to answer using this dashboard include: which regions, wineries, and grape varieties in the United States consistently produce the best rated, priced, and/or valued wines? Does variability exist in which regions produce the best rated, priced, and/or valued wine, and if so, does this variability depend on winery or grape variety?

Additionally, one goal of this app is to help the average person make wine-related decisions in their daily lives. 

For instance, Jerry wants to buy a bottle of wine for his dinner party to impress his guests, but he has a limited budget. How will he decide which wine to buy? When Jerry visits the “V is for Vino” app he will find a comprehensive overview of wines grown throughout the United States, where he can [explore] and [compare] the ratings, prices, and values of these wines. Using the app, he can use an interactive drop down menu to rank all wines by his choice of rating, price, or the overall value to [identify] the perfect wine to impress his dinner guests. 

 Alice is a wine merchant and wants to buy a selection of wines from a variety of regions across the US to supply a new wine store she's helping open. She would like to [identify] wineries that tend to get high ratings for their wines and also [compare] different grape varieties at these wineries while making her stock selections. Her goal is to ensure the new shop has a balanced selection of high value wines to offer customers. Using the "V is for Vino" app, she can use the interactive chloropleth map to explore wines from these different regions. Clicking directly on the map to filter for summary statistics at specific regions or wineries would allow her to [summarize] the price, rating, and value of those wines and effectively select bottles to stock at her shop.
  
In both cases, it's clear that this app has the potential to empower users to make more effective data-driven decisions than they would have been able to otherwise.