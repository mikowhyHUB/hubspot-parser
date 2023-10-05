import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional


class LandingPageParser:
    '''
    Landing page parsing class
    '''
    def __init__(self, url: str):
        self.url = url

    def parse_blog_post(self, url: str) -> Optional[datetime]:
        '''
        Parse a blog post page and extract the publication date

        Args:
        url - The URL of the blog post
        Returns:
        The publication date if found, None otherwise
        '''
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

    def latest_hubspot_articles(self, articles_num: int) -> List[Dict[str, Union[str, Optional[datetime]]]]:
        '''
        Method giving latest HubSpot articles from the landing page

        Args:
        articles_num - Numbers of latest articles to parse
        Returns:
        List of dicts containig links and publish date
        '''
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")
        article_sections = soup.find_all("li", class_="blog-categories-post -visible")

        articles = []
        for section in article_sections:
            article_link = section.find("h3", class_="blog-categories-card-title").find(
                "a"
            )["href"]
            date_published = self.parse_blog_post(article_link)
            articles.append({"link": article_link, "date_published": date_published})

        articles.sort(key=lambda x: x["date_published"], reverse=True)

        return articles[:articles_num]
