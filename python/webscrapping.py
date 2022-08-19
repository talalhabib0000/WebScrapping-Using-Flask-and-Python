import pandas as pd
from bs4 import BeautifulSoup
import requests
import urllib.parse

movieCode="tt0072000"

# Request Page Source from URL

url=f"https://www.imdb.com/title/{movieCode}/reviews/"
pages=requests.get(url)
pages
# ---------------------------------------------------
# Displaying Source code
soup=BeautifulSoup(pages.content,"html.parser")
# print(soup.prettify())
# ---------------------------------------------------

# Parsing Source

scraped_movies=soup.find_all('div',class_="text show-more__control")
scraped_movies

movies=[]
for movie in scraped_movies: 
    movie=movie.get_text().replace('\n',"")
    movie=movie.strip()
    movies.append(movie) 
movies 