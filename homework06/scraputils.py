import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    news_list = []
    athing = parser.find_all(class_="athing")
    subtext = parser.find_all(class_="subtext")

    for i in range(len(athing)):
        author = subtext[i].find(class_="hnuser")
        comments = subtext[i].find_all("a")[-1].text[:-9]
        points = subtext[i].find(class_="score")
        title = athing[i].find(class_="titlelink").text
        url = athing[i].find(class_="titlelink")["href"]
        news_list.append(
            {
                "author": author.text if author else "None",
                "comments": int(comments) if comments else 0,
                "points": int(points.string.split()[0]) if points else 0,
                "title": title,
                "url": url if "http" in url else "https://news.ycombinator.com/" + url,
            }
        )
    return news_list


def extract_next_page(parser):
    """Extract next page URL"""
    if not parser.find(class_="morelink"):
        return None
    return parser.find(class_="morelink")["href"]


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        if not next_page:
            next_page = url[29:36] + str(int(url[36:]) + 1)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
