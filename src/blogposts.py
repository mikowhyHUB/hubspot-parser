import requests
from bs4 import BeautifulSoup
import re
from collections import Counter


class BlogPostParser:
    def __init__(self, url):
        self.url = url

    def fetch_article_text(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            article_body = soup.find("div", class_="hsg-rich-text blog-post-body")

            return article_body.get_text()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the page: {e}")

    def count_words_and_letters(self, text):
        words = re.findall(r"\b\w+\b", text)
        word_count = len(words)
        letter_count = sum(len(word) for word in words)

        return word_count, letter_count

    def find_top_keywords(self, text, num_keywords=5):
        words = re.findall(r"\b\w+\b", text)
        keywords = [word.lower() for word in words if len(word) >= 2]
        keyword_count = Counter(keywords)

        return keyword_count.most_common(num_keywords)

    def display_article_info(self):
        article_text = self.fetch_article_text()

        if article_text is not None:
            word_count, letter_count = self.count_words_and_letters(article_text)
            top_keywords = self.find_top_keywords(article_text)
            print(
                f"Liczba słów użytych w aartykule: {word_count}\n"
                f"Liczba liter użytych w artykule: {letter_count}\n"
                "Pięć najczęściej używanych fraz kluczowych w artykule:"
            )
            for keyword, count in top_keywords:
                print(f"{keyword}: {count}")
