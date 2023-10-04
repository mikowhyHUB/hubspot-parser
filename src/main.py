from landingpage import LandingPageParser
from blogposts import BlogPostParser

if __name__ == "__main__":
    hubspot_url = "https://blog.hubspot.com/"
    latest_articles_num = 3
    lp_parser = LandingPageParser(hubspot_url)
    article_links = lp_parser.latest_hubspot_articles(latest_articles_num)

    for article_link in article_links:
        print('\n')
        bp_parser = BlogPostParser(article_link)
        bp_parser.display_article_info()
        print("\n", "-"*50)
   

    
