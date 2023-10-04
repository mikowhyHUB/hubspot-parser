import requests
from bs4 import BeautifulSoup
from datetime import datetime

# MVP


def parse_blog_post(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    date_published = None

    script_tag = soup.find("script", {"type": "application/ld+json"})
    if script_tag:
        script_data = script_tag.text
        try:
            date_published = datetime.fromisoformat(
                script_data.split('"datePublished": "')[1].split('"')[0]
            )
        except IndexError:
            pass

    return date_published


def latest_hubspot_articles(url, articles_num):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    article_sections = soup.find_all("li", class_="blog-categories-post -visible")

    articles = [
        section.find("h3", class_="blog-categories-card-title").find("a")["href"]
        for section in article_sections
    ]

    articles.sort(reverse=True)

    return articles[:articles_num]
