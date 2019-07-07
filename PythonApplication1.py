import requests
from bs4 import BeautifulSoup

for i in range(0, 980, 20):
    url = "https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start=" + "%d&type=T"%i
    
    douban_data = requests.get(url)
    soup = BeautifulSoup(douban_data.text, "lxml")

    titles = soup.select("#subject_list > ul > li > div.info > h2 > a")
    prices = soup.select("div.pub")
    stars = soup.select("#subject_list > ul > li > div.info > div.star.clearfix > span.rating_nums")

    for title, price, star in zip(titles, prices, stars):
        data = {
                "title" : title.get_text().strip().split()[0], 
                "price" : price.get_text().strip().split("/")[-1], 
                "star"  : star.get_text()
            }

        print(data)
