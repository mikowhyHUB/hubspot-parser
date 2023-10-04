import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
from landingpage import latest_hubspot_articles

# MVP


def fetch_article_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        article_body = soup.find("div", class_="hsg-rich-text blog-post-body")

        return article_body.get_text()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the page: {e}")


def count_words_and_letters(text):
    words = re.findall(r"\b\w+\b", text)
    word_count = len(words)
    letter_count = sum(len(word) for word in words)

    return word_count, letter_count


def find_top_keywords(text, num_keywords=5):
    words = re.findall(r"\b\w+\b", text)
    keywords = [word.lower() for word in words if len(word) >= 2]
    keyword_count = Counter(keywords)

    return keyword_count.most_common(num_keywords)


def display_article_info(url):
    article_text = fetch_article_text(url)

    if article_text is not None:
        word_count, letter_count = count_words_and_letters(article_text)
        top_keywords = find_top_keywords(article_text)

        print(
            f"Number of words used in the article: {word_count}\n"
            f"Number of letters used in the article: {letter_count}\n"
            "Five most frequently used keywords in the article:"
        )
        for keyword, count in top_keywords:
            print(f"{keyword}: {count}")


if __name__ == "__main__":
    hubspot_url = "https://blog.hubspot.com/"
    latest_articles_num = 3
    article_links = latest_hubspot_articles(hubspot_url, latest_articles_num)

    for article_link in article_links:
        print('\n')
        display_article_info(article_link)
        print("\n", "-"*50)
