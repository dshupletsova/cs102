from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)
from homework06.scraputils import get_news


def create_db(news_list):
    s = session()
    for dic in news_list:
        new = News(
            title=dic["title"],
            author=dic["author"],
            url=dic["url"],
            comments=dic["comments"],
            points=dic["points"],
        )
        s.add(new)
        s.commit()


class News(Base):  # type: ignore
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


Base.metadata.create_all(bind=engine)

if __name__ == "__main__":

    the_list = get_news("https://news.ycombinator.com/", n_pages=34)
    create_db(the_list)
