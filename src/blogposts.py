import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
from typing import Tuple, List


class BlogPostParser:
    '''
    Parsing blog post content class
    '''
    def __init__(self, url: str):
        self.url = url

    def fetch_article_text(self) -> str | None:
        '''
        Fetch the text content of the blog post.

        Returns:
        The text content of the blof post
        '''
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            article_body = soup.find("div", class_="hsg-rich-text blog-post-body")

            return article_body.get_text()

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the page: {e}")

    def count_words_and_letters(self, text: str) -> Tuple[int, int]:
        '''
        Count the number of words and letters in the given text.

        Args:
        Text to analyze
        Returns:
        A tuple containing the word count and letter count
        '''
        words = re.findall(r"\b\w+\b", text)
        word_count = len(words)
        letter_count = sum(len(word) for word in words)

        return word_count, letter_count

    def find_top_keywords(self, text: str, num_keywords: int=5) -> List[Tuple[str, int]]:
        '''
        Find the op keywords in the given text

        Args:
        text - teh text to analyze
        num_keywords (default 5) - numbeer of top keywords to find
        Returns:
        List of tuple containing the top keywords and their counts
        '''
        words = re.findall(r"\b\w+\b", text)
        keywords = [word.lower() for word in words if len(word) >= 2]
        keyword_count = Counter(keywords)

        return keyword_count.most_common(num_keywords)

    def display_article_info(self) -> None:
        '''
        Display information about the blog post
        '''
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
