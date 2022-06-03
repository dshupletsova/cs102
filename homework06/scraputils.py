import requests
from bs4 import BeautifulSoup


def extract_news(parser1: BeautifulSoup):

    news_list = []

    title_list = []
    url_list = []
    comments_list = []
    point_list = []
    author_list = []

    subtext_line = parser1.select(".subtext")

    all_things = parser1.find_all("tr", {"cl# type: ignore
import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    news_list = []
    posts = parser.findAll("tr")[3]
    news = posts.td.find_all("tr", attrs={"class": "athing"})
    content = posts.td.find_all("td", attrs={"class": "subtext"})
    for i in range(len(news)):
        if content[i].find("a", attrs={"class": "hnuser"}):
            author = content[i].find("a", attrs={"class": "hnuser"}).text.split()[0]
        else:
            author = None
        if content[i].find("span", attrs={"class": "score"}):
            points = int(
                content[i].find("span", attrs={"class": "score"}).text.split()[0]
            )
        else:
            points = 0
        comms = content[i].find_all("a")[-1].text
        if comms == "discuss":
            comms = 0
        else:
            comms = comms.split()[0]
        news_list.append(
            {
                "author": author,
                "comments": comms,
                "points": points,
                "title": news[i].find("a", attrs={"class": "titlelink"}).text,
                "url": news[i].find("a", attrs={"class": "titlelink"})["href"],
            }
        )
    return news_list


def extract_next_page(parser):
    body = parser.findAll("tr")[3]
    return body.td.find_all("td", attrs={"class": "title"})[-1].a["href"]


def get_news(url, n_pages=1):
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

        find_athing = a_thing.find_all("td", {"class": "title"})
        title_list.append(find_athing[1].a.text)
        url_list.append(find_athing[1].a["href"])

    print(url_list)

    for index in range(len(subtext_line)):
        points = subtext_line[index].select(".score")
        if points == []:
            points = 0
        else:
            points = int(points[0].text.split()[0])
        point_list.append(points)

        # сбор для author_list
        author = subtext_line[index].select(".hnuser")
        if author == []:
            author = "Anonymous"
        else:
            author = author[0].text
        author_list.append(author)

        comments = subtext_line[index].find_all("a")[4].text
        if comments == "discuss":
            comments_list.append(0)
        else:
            comments_list.append(int(comments.split()[0]))
    print(comments_list)

    for ind in range(len(title_list)):
        news_list.append(
            [title_list[ind], author_list[ind], url_list[ind], comments_list[ind], point_list[ind]]
        )
    return news_list


def extract_next_page(parser1: BeautifulSoup):
    link = parser1.select(".morelink")[0]["href"]
    # print(str(link))
    return str(link)


def get_news(url, n_pages=1):
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


if __name__ == "__main__":
    print(get_news("https://news.ycombinator.com/newest", n_pages=3))
