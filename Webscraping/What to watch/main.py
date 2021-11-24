from bs4 import BeautifulSoup
import requests
import random
import os

def main():
    # To do:
    
    # -> fix for tv shows
    # -> De 300 filmes/series da categoria escolhida, obter o id de cada filme e meter numa lista, escolher um random
    # e apresentar o Titulo, Imagem, Breve Resumo, Rating, e url para o trailer 
    # -> add rating minimo, ano minimo e diversos genres (?)
    # -> checkar se a choice é valida (ano <= 2021)
    # -> fazer um \n no resumo passado determinados caracters
    

    l=[]
    clear = lambda: os.system('cls')
    doc = get_doc('https://www.imdb.com/feature/genre/?ref_=nv_ch_gr')
    genre,target = get_input(doc)
    watch = ""
    if target == '1': watch = "movie"
    else: watch = "tv show"
    for i in range(1,5): #chooses 200 movies/shows
        doc = get_doc(get_list_url(genre,target,(i-1)*50+1))
        l = add_ids_to_list(doc,l)
    url = get_choice_url(random.choice(l))
    doc = get_doc(url)
    title,year,duration,plot,rating,trailer = get_choice_info(doc)
    clear()
    print(f"The {watch} you have to watch is: \n")
    print(f'{title} {year}\nDuration: {duration}\nRating: {rating}/10\n\n{plot}\nTrailer: {trailer}\n')

def get_choice_info(doc):
    title = doc.h1.string
    info = doc.findAll("li",role="presentation",class_="ipc-inline-list__item")
    year = info[0].span.string
    duration = info[2].text
    plot = doc.find("span",role="presentation",class_='GenresAndPlot__TextContainerBreakpointXL-cum89p-2 gCtawA').text
    rating = doc.find("span",class_="AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV").text
    trailer = doc.find("a",class_="ipc-lockup-overlay Slatestyles__SlateOverlay-sc-1t1hgxj-2 fAkXoJ hero-media__slate-overlay ipc-focusable",href=True)
    trailer = f'https://www.imdb.com{trailer["href"]}'
    return title,year,duration,plot,rating,trailer

def add_ids_to_list(doc,l):
    divs = doc.findAll("div", class_="lister-item-image float-left")
    for div in divs:
        anchor = div.find('a',href=True)
        l.append(str(anchor['href']))
    return l

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

def get_choice_url(choice):
    print(f'https://www.imdb.com{choice}?ref_=adv_li_tt')
    return f'https://www.imdb.com{choice}?ref_=adv_li_tt'

def get_list_url(genre,target,page='1'):
    if target=="1":
        new_url = str(f'https://www.imdb.com/search/title/?title_type=feature&genres={genre.lower().replace(" ","-")}&start={page}&explore=genres&ref_=adv_nxt')
    else:
        new_url = str(f'https://www.imdb.com/search/title/?title_type=tv_series,tv_miniseries&genres={genre.lower().replace(" ","-")}&start={page}&explore=genres&ref_=adv_nxt')
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