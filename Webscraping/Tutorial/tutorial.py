from bs4 import BeautifulSoup
import re
import requests

# with open("index2.html",'r') as f:
#     doc = BeautifulSoup(f,"html.parser")

"""find the dollar str in file + everything that comes next"""
# tags = doc.find_all(text=re.compile("\$.*"),limit=1)
# for tag in tags:
#     print(tag.strip())

"""modify the html file and save onto a new one"""
# tags = doc.find_all("input",type="text")
# for tag in tags:
#     tag["placeholder"] = "I changed u!"

# with open("index.html","w") as file:
#     file.write(str(doc))

"""read the coinamrketcap.com to get the name and price of the top 10 cryptocurrencys"""
url = "https://coinmarketcap.com"
result = requests.get(url).text
doc = BeautifulSoup(result,"html.parser")
tbody = doc.tbody
trs = tbody.contents #list of the table rows of html file

prices = {}
for tr in trs[:10]:
    name,price = tr.contents[2:4]
    print(name)
    print()
    fixed_name = name.p.string
    fixed_price = price.a.string
    prices[fixed_name] = fixed_price

for tr in trs[10:]:
    name,price = tr.contents[2:4]
    fixed_name = name.span.next_sibling
    fixed_price = price.span.text
    fixed_tag = fixed_name.next_sibling.string
    prices[fixed_name.string] = fixed_price

for crypto in prices:
    print(crypto,"->",prices.get(crypto))
