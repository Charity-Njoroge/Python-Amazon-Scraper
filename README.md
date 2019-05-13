# Python-Amazon-Scraper
In this project, I scrape data from Amazon website and return it into csv files.
In the project that returns the prices, I am pulling data from one page but
you can however use this technique to extract data from multiple pages,
if you have all the ASIN numbers listed for the products that you are intending
to scrape inside a csv file. (asin_list.csv)
To begin with, every Amazon product has a unique ASIN or
Amazon Standard Identification Number. beginning the link with
– https://www.amazon.com/dp/
and ending with ASIN number after dp/
Now we will note down the ASIN numbers of 5 products in a spreadsheet
and then access the prices for those five products. But wait, extracting
the ASIN number from the URL might be a bit difficult and it would be easier
if I showed you how to just keep the URLs in a spreadsheet, extract the
ASIN number from them (between dp/.../,
and then use those ASIN numbers to get the product prices.


