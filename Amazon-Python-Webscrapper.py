"""
A Python Script to return products from Amazon that are under 100$.
The data is represented using Pandas
"""
from bs4 import BeautifulSoup
import requests
from time import gmtime, strftime

a = []

# User input for the category they want to search
url_str = input("Enter the product category you wish to search for : ")
url = []

# split the product category into individual words and add to the amazon url
words = url_str.split()  # list of individual words
var = len(words)

# loop through the list of words and add the product category to the amazon url
if var == 1:
    url = \
        "https://www.amazon.com/s/ref=nb_sb_noss_1?url=" \
        "search-alias%3Daps&field-keywords=" + words[0]
if var == 2:
    url = \
        "https://www.amazon.com/s/ref=nb_sb_noss_1?url=" \
        "search-alias%3Daps&field-keywords=" + words[0] + "+" + words[1]
if var == 3:
    url = \
        "https://www.amazon.com/s/ref=nb_sb_noss_1?url=" \
        "search-alias%3Daps&field-keywords=" + words[0] + "+" + words[1] \
        + "+" + words[2]

elif var == 4:
    url = \
        "https://www.amazon.com/s/ref=nb_sb_noss_1?url=" \
        "search-alias%3Daps&field-keywords=" + words[0] + "+" + words[1] \
        + words[2] + "+" + words[3]

# use a user-agent to avoid getting
#  a generic anti-crawling response for every request Amazon.
headers = {"User-Agent":
               "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0)"
               " Gecko/20100101 Firefox/66.0"}

response = requests.get(url, headers=headers, verify=False)
soup = BeautifulSoup(response.content, 'html.parser')
# print(response)

# csv writing setup
filename = "products.csv"
fp = open(filename, "w", encoding="utf-8")

# grab time and format strings
strftime("%Y-%m-%d %H:%M:%S", gmtime())

headers = "ASIN, Name" + "price :" + strftime("%Y-%m-%d %H:%M:%S",
                                                   gmtime()) + ", Number " \
                                                                     "of " \
                                                                     "Reviews" \
                                                                     "\n"
fp.write(headers)

# Style 1 of Amazon's product display
containers1 = soup.findAll("li",
                           {"class":
                                "s-result-item s-result-card-for-container "
                                "a-declarative celwidget "})
print("containers style 1: ", len(containers1))

# page could be styled different, invoke query second style
containers2 = soup.findAll("li",
                           {"class":
                                "s-result-item s-result-card-for-container"
                                " s-carded-grid celwidget "})
print("containers style 2: ", len(containers2))

# check for sponsored containers
sponsored_containers = soup.findAll("li",
                                    {"class":
                                         "s-result-item celwidget AdHolder"})
print("containers style 3 sponsored: ", len(sponsored_containers))

# check for the most common style
common_containers = soup.findAll("li", {"class":"s-result-item celwidget "})
print("containers style 4 common: ", len(common_containers))

# check for special style
containers3 = soup.findAll("li", {"class"
                                   :"s-result-item s-col-span-12 celwidget "})
print("containers style 5 special", len(containers3))

for container in sponsored_containers:
    # product ASIN
    asin = container["data_asin"]

    # product name
    try:
        title_container = container.findall({"li" :
                                                 {"class" :
                                                         "a-link-normal "
                                                         "s-access-detail-page "
                                                         "s-color-twister-\
                                                         title-link a-text- \
                                                         normal"}})
        name = title_container[0]["title"]

    except:
        name = "N/A"

        # Product Price # span class="a-offscreen"
        price_container = container.findAll("span", {"class": "a-offscreen"})
        price = price_container[1].text

        # Number of reviews
        num_review_container = container.findAll("a", {
            "class": "a-size-small a-link-normal a-text-normal"})
        try:
            if len(num_review_container) > 1:
                num_reviews = num_review_container[1].text
            else:
                num_reviews = num_review_container[0].text
        except:
            num_reviews = "0"

        fp.write(asin + ',' + name.replace(",", "|") + ',' + price.replace("$",
                                                                           "") +
                 "," + num_reviews.replace(",", "") + "\n")
        # + ',' + name.replace(",", "|") + ',' + price + ","
        # + num_reviews + "\n")

for container in common_containers:
        # Product Asin
        asin = (container["data-asin"])

        # Product Name
        try:
            title_container = container.findAll("a", {
                "class":
                    "a-link-normal s-access-detail-page "
                    "s-color-twister-title-link a-text-normal"})
            name = title_container[0]["title"]
        except:
            name = "N/A"

        # Product Price # span class="a-offscreen"
        price_container = container.findAll("span", {"class": "a-offscreen"})
        # print(price_container)
        try:
            price = price_container[0].text
        except:
            price = "N/A"

        # Number of reviews
        num_review_container = container.findAll("a", {
            "class": "a-size-small a-link-normal a-text-normal"})
        try:
            if (len(num_review_container) > 1):
                num_reviews = num_review_container[1].text
            else:
                num_reviews = num_review_container[0].text
        except:
            num_reviews = "0"

        # try:
        #	num_review2 = num_review_container[1].text.strip()
        #	print(num_review2)
        # except list index out of range:
        #	num_review2 = 0;
        fp.write(asin + ',' + name.replace(",", "|") + ',' +
                 price.replace("$", "") + "," +
                 num_reviews.replace(",", "") + "\n")

        fp.close()


