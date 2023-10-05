from landingpage import LandingPageParser
from blogposts import BlogPostParser
from typing import List, Dict


def main() -> None:
    hubspot_url: str = "https://blog.hubspot.com/"
    latest_articles_num: int = 3
    lp_parser = LandingPageParser(hubspot_url)
    article_links: List[Dict[str, str]] = lp_parser.latest_hubspot_articles(
        latest_articles_num
    )

    for article_link in article_links:
        print("\n")
        print(f"URL: {article_link['link']}")
        bp_parser = BlogPostParser(article_link["link"])
        bp_parser.display_article_info()
        print("\n", "-" * 50)


if __name__ == "__main__":
    main()
