from bs4 import BeautifulSoup
from datetime import date as d
import requests
import random
from re import sub
import os

def get_doc(url):
    """get_doc: str -> BeautifulSoup
    
    Given an url, returns a BeautifulSoup object with html parser 
    """
    result = requests.get(url).text
    return BeautifulSoup(result,"html.parser")
def get_input(doc):
    """get_input: BeautifulSoup -> str x str
    
    Given a BeautifulSoup object, read the website to create a list of the
    available genres returning the one chosen by the user and the target
    ("1"->movies ; "2"->TV Shows)
    """

    def get_movies_genres(doc):
        """get_movies_genres: BeautifulSoup -> List

        Webscrapes imdb website and returns a list with the available genres for
        movies.
        """
        movies = []
        table = doc.find("div",class_="full-table")
        for col in table.findChildren("a"):
            movies.append(col.string.strip())
        return movies
    def get_shows_genres(doc):
        """get_shows_genres: BeautifulSoup -> List

        Webscrapes imdb website and returns a list with the available genres for
        TV Shows.
        """
        shows = []
        table = doc.findAll("div",class_="full-table")[5]
        for col in table.findChildren("a"):
            shows.append(col.string.strip())
        return shows

    print("\n1. Movies\t2. TV Shows\n")
    target = input("What do you pretend to watch? (Type the number):\n> ")
    if target=="1": #Movies
        MOVIES_GENRES = get_movies_genres(doc)
        rang = len(MOVIES_GENRES)
        list = MOVIES_GENRES
    elif target=="2": #TV Shows
        TV_SHOWS_GENRES = get_shows_genres(doc)
        rang = len(TV_SHOWS_GENRES)
        list = TV_SHOWS_GENRES
    else:
        print("Invalid Input.")
        exit()
    print()
    for genre in range(1,rang+1):
            if genre==rang:
                print(f"{genre}. {list[genre-1]}\n")
            elif genre%4!=0:
                print(f"{genre}. {list[genre-1]} ",end="\t")
            else:
                print(f"{genre}. {list[genre-1]}")
    genre_index = input("Select the number of the genre you pretend to watch:\n> ")
    try:
        if 1<=int(genre_index)<=rang:
            genre_index=int(genre_index)-1
        genre = list[genre_index]
    except:
        print("You should input a number from the list")
        exit()
def get_list_url(genre,target,page='1'):
    """get_lis_url: str x str x str -> str
    
    Given a genre and a target (Movie or TV Show), returns the url of top 50 
    movies/shows by popularity on imdb starting on the 'page'.
    """
    if target=="1":
        new_url = str(f'https://www.imdb.com/search/title/?title_type=feature&genres={genre.lower().replace(" ","-")}&start={page}&explore=genres&ref_=adv_nxt')
    else:
        new_url = str(f'https://www.imdb.com/search/title/?title_type=tv_series,tv_miniseries&genres={genre.lower().replace(" ","-")}&start={page}&explore=genres&ref_=adv_nxt')
    return new_url
    return genre,target
def add_ids_to_list(doc,l):
    """add_ids_to_list: BeautifulSoup x List -> List
    
    Adds all available movie/show from a specific genre to a list and returns it
    """

    def is_id_valid(parent):
        """is_id_valid: BeautifulSoup -> bool
        
        Only returns true if movie/show selected has been already released
        """
        date = parent.find("span",class_="lister-item-year text-muted unbold")
        date = date.string
        try:
            date = sub("[^0-9]", "", date)
            date = int(date[:4])
        except TypeError:
            return False
        if date > system_year: return False
        return True

    
    system_year = d.today().year
    divs = doc.findAll("div", class_="lister-item-image float-left")
    for div in divs:
        anchor = div.find('a',href=True)
        if is_id_valid(anchor.parent.parent):
            l.append(str(anchor['href']))
    return l
def get_choice_url(choice):
    """get_choice_url: str -> str
    
    Returns the imdb url of the choice
    """
    return f'https://www.imdb.com{choice}?ref_=adv_li_tt'
def get_choice_info(doc,movie_or_show):
    """get_choice_info: BeautifulSoup x str -> str x str x str x str x str x str
    
    Given an BeautifulSoup object, scraps the information about the movie:
                [title,year,duration,plot,rating,trailer]
    """
    title = doc.h1.string
    info = doc.findAll("li",role="presentation",class_="ipc-inline-list__item")
    if movie_or_show == 'movie': year = info[0].span.string
    else: year = info[1].span.string
    if movie_or_show == 'movie': duration = info[2].text
    else: duration = info[3].text
    plot = doc.find("span",role="presentation",class_='GenresAndPlot__TextContainerBreakpointXL-cum89p-2 gCtawA').text
    rating = doc.find("span",class_="AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV").text
    try:
        trailer = doc.find("a",class_="ipc-lockup-overlay Slatestyles__SlateOverlay-sc-1t1hgxj-2 fAkXoJ hero-media__slate-overlay ipc-focusable",href=True)
        trailer = f'https://www.imdb.com{trailer["href"]}'
    except:
        trailer = ""
    return title,year,duration,plot,rating,trailer

def main():
    # To do:
    # GUI with tinkers
    
    l=[]
    clear = lambda: os.system('cls') #Clear the console function
    doc = get_doc('https://www.imdb.com/feature/genre/?ref_=nv_ch_gr')
    genre,target = get_input(doc)
    watch = ""
    if target == '1': watch = "movie"
    else: watch = "TV show"
    #chooses 200 movies/shows
    for i in range(1,5):
        doc = get_doc(get_list_url(genre,target,(i-1)*50+1))
        l = add_ids_to_list(doc,l)
    
    url = get_choice_url(random.choice(l))
    doc = get_doc(url)
    title,year,duration,plot,rating,trailer = get_choice_info(doc,watch)
    clear()
    print(f"The {watch} you have to watch is: \n")
    if watch == 'movie': print(f'{title} - {year}\nDuration: {duration}\nRating: {rating}/10\n\n{plot}\nTrailer: {trailer}\n')
    else: print(f'{title} ({year})\nDuration: {duration}\nRating: {rating}/10\n\n{plot}\nTrailer: {trailer}\n')

if __name__ == '__main__':
     main()