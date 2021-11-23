from bs4 import BeautifulSoup
import requests

URL = 'https://www.google.com/travel/explore?tfs=CBwQAxoaagwIAhIIL20vMHBtbjcSCjIwMjEtMTItMDkaGhIKMjAyMS0xMi0xM3IMCAISCC9tLzBwbW43cAKCAQ0I____________ARABQAFIAZgBAQ&tfu=GgA&hl=pt-PT&tcfs=UgJgAQ'
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
headers = {"user-agent" : USER_AGENT}
cookies = {"CONSENT": "YES+cb.20210720-07-p0.en+FX+410"}
resp = requests.get(URL, headers=headers,cookies=cookies).text

doc = BeautifulSoup(resp,"html.parser")
print(doc.prettify())