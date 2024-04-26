import requests
from bs4 import BeautifulSoup
import time
import openpyxl

book = openpyxl.Workbook()

headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

link = ["https://www.kisia.or.kr/"]

def get_child(links,i):
    linkss = []
    if not (bool(links)):
        return
    book.active.append(list(f"depth = {i}"))
    for l in links:
        #time.sleep(3)
        print(f"depth = {i}")

        try:
            response = requests.get(l,allow_redirects=True,headers=headers)
            response.close()
        except requests.exceptions.RequestException as err:
            continue
        soup = BeautifulSoup(response.content,"html.parser")
        for a in soup.findAll("a"):
            try:
                href = a["href"]
            except KeyError:
                break
            if href.startswith("#") or href.startswith("javascript:") or len(href) == 0:
                continue

            if "tel:" in href:
                continue
            
            if not ("http" in href):
                if href.startswith("/"):
                    href = href[1:]
                href = l+href
            
            if href not in linkss:
                print(href.encode('utf-8'),len(href))
                linkss.append(href)

            book.active.append(list(href))
    
    i+=1
    get_child(linkss[1:],i)

i = 0
get_child(link,i)

book.save("result.xlsx")
book.close()
