from bs4 import BeautifulSoup
import requests

def main():
    doc = get_doc('https://www.imdb.com/feature/genre/?ref_=nv_ch_gr')
    genre,target = get_input(doc)
    doc = get_doc(get_new_url(genre,target))

def get_doc(url):
    result = requests.get(url).text
    return BeautifulSoup(result,"html.parser")

def get_movies_genres(doc):
    movies = []
    table = doc.find("div",class_="full-table")
    for col in table.findChildren("a"):
        movies.append(col.string.strip())
    return movies

def get_shows_genres(doc):
    shows = []
    table = doc.findAll("div",class_="full-table")[5]
    for col in table.findChildren("a"):
        shows.append(col.string.strip())
    return shows

def get_new_url(genre,target):
    if target=="1":
        new_url = str(f'https://www.imdb.com/search/title?genres={genre.lower().replace(" ","-")}&amp;title_type=feature&amp;explore=genres')
    else:
        new_url = str(f'https://www.imdb.com/search/title/?genres={genre.lower().replace(" ","-")}&title_type=tv_series,mini_series&explore=genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=b4e1d6fb-9821-4c7d-ad14-31ed10854442&pf_rd_r=0WMG35NH4V150ASTGKQG&pf_rd_s=center-7&pf_rd_t=15051&pf_rd_i=genre')
    return new_url

def get_input(doc):
    print("\n1. Movies\t2. TV Shows\n")
    target = input("What do you pretend to watch? (Type the number):\n> ")
    if target=="1":
        MOVIES_GENRES = get_movies_genres(doc)
        rang = len(MOVIES_GENRES)
        list = MOVIES_GENRES
    elif target=="2":
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
    return genre,target

if __name__ == '__main__':
     main()