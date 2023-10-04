import requests
from bs4 import BeautifulSoup
from datetime import datetime


# MVP
def latest_hubspot_articles(url, articles_num):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    article_sections = soup.find_all("li", class_="blog-categories-post -visible")

    articles = []
    for section in article_sections:
        link = section.find("h3", class_="blog-categories-card-title").find("a")["href"]
        date_str = (
            section.find("div", class_="blog-categories-card-footer")
            .find_all("p")[1]
            .text.strip()
        )

        date_obj = datetime.strptime(date_str, "%m/%d/%y")

        articles.append(
            {"date": date_obj, "link": link}
        )

    articles.sort(key=lambda x: x["date"], reverse=True)

    for article in articles[:articles_num]:
        print(article['link'])


if __name__ == "__main__":
    hubspot_url = "https://blog.hubspot.com/"
    latest_articles_num = 3
    latest_hubspot_articles(hubspot_url, latest_articles_num)
