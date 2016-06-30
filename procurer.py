from urllib.parse import quote

from bs4 import BeautifulSoup
from pylast import LastFMNetwork, Track
from requests import get

try:
    from secret import API_KEY, API_SECRET
except:
    API_KEY = ""  # this is a sample key
    API_SECRET = ""


def ultimate_guitar(url):
    content = get(url).content
    soup = BeautifulSoup(content, "html.parser")
    return soup.find("div", {"class": "t_autor"}).a.text, soup.h1.text, soup.find_all("pre")[-1].text


def lastfm(keyword):
    network = LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
    suggestion = network.search_for_track("", keyword).get_next_page()[0]
    artist, title = suggestion.artist.get_name(), suggestion.title
    print(artist, "-", title)
    return artist, title


def postulate_url(artist, title):
    artist = artist.lower().replace(" ", "_").replace("'","_")
    title = title.lower().replace(" ", "_").replace("'","")
    if title.startswith("the"):
        title = title.lstrip("the").strip("_")
    return 'https://tabs.ultimate-guitar.com/' + artist[0] + '/' + artist + '/' + title + '_ver2_crd.htm'
