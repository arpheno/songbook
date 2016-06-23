from bs4 import BeautifulSoup
from requests import get


def ultimate_guitar(url):
    content = get(url).content
    soup = BeautifulSoup(content, "html.parser")
    return soup.h1.text, soup.find("div", {"class": "t_autor"}).a.text, soup.find_all("pre")[-1].text