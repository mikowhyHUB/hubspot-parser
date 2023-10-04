import requests
from bs4 import BeautifulSoup
from datetime import datetime

class LandingPageParser:
    def __init__(self, url):
        self.url = url

    def parse_blog_post(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.find("script", {"type": "application/ld+json"})
        date_published = None
        if script_tag:
            script_data = script_tag.text
            try:
                date_published = datetime.fromisoformat(
                    script_data.split('"datePublished": "')[1].split('"')[0]
                )
            except IndexError:
                pass
        return date_published

    def latest_hubspot_articles(self, articles_num):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        article_sections = soup.find_all("li", class_="blog-categories-post -visible")
        articles = [
            section.find("h3", class_="blog-categories-card-title").find("a")["href"]
            for section in article_sections
        ]
        articles.sort(reverse=True)
        for article_link in articles[:articles_num]:
            date_published = self.parse_blog_post(article_link)
            print(article_link, date_published)
        return articles[:articles_num]
