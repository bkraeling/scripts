import requests
from bs4 import BeautifulSoup

categories = [
    'Best Picture',
    'Best Director',
    'Best Actor',
    'Best Actress',
    'Best Supporting Actor',
    'Best Supporting Actress',
    'Best Original Screenplay',
    'Best Adapted Screenplay'
]
def getMovieInfo(wikiUrl):
    urlBase = 'https://en.wikipedia.org/{0}'
    movieResponse = requests.get(
        url=urlBase.format(wikiUrl)
    )
    movieSoup = BeautifulSoup(movieResponse.content, 'html.parser')

    info = movieSoup.select_one('table.infobox.vevent')

    print(info)
    info.find("th", string="Directed by").find_next_sibling()

def getName(e):
  return e['name']

def scrapeEventPage(url):
    response = requests.get(
        url=url,
    )

    movies = list()


    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find(id="Awards").parent.find_next_sibling("table")
    table_rows = table.find_all("td")
    for table_row in table_rows:
        category = table_row.select_one("div b a").get_text()
        if category not in categories:
            continue

        movie_list = table_row.select_one("li")

        # Get category winner
        winner = movie_list.select_one("b")
        winner_movie = { "name": winner.i.a.get_text(), "link": winner.i.a['href'] }
        if winner_movie not in movies:
            movies.append(winner_movie)
        other_movies = movie_list.select("li")

        for movie in other_movies:
            nominee_movie = { "name": movie.i.a.get_text(), "link": movie.i.a['href'] }
            if nominee_movie not in movies:
                movies.append(nominee_movie)
    movies.sort(key=getName)
    getMovieInfo(movies[0]['link'])





scrapeEventPage("https://en.wikipedia.org/wiki/83rd_Academy_Awards")
