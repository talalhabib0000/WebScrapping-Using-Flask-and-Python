from email.message import Message
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import numpy as np
import re  # support regular expressions
from bs4 import BeautifulSoup
import requests
import urllib.parse
from flask import Flask, render_template, request
import pickle
from nltk.corpus import stopwords
from collections import Counter
import pyodbc as odbc
from flask_sqlalchemy import sqlalchemy
from datetime import datetime

# ----------------------------------------------------------------
# Defining Connection
# -----------------------------------------------------------------


def connection():
    s = 'DESKTOP-B3U0GP9\SQLEXPRESS'  # Your server name
    d = 'Movies'
    cstr = 'DRIVER={SQL Server};SERVER='+s+';DATABASE='+d
    conn = odbc.connect(cstr)
    return conn


conn = connection()
cursor = conn.cursor()
trainedModel = pickle.load(open("./trainedModelNews", 'rb'))
vectorizer = pickle.load(open("vectorizer", 'rb'))

# ----------------------------------------------------------------
# Vectorization
# -----------------------------------------------------------------


def vectorization(preprocessedInput):
    preprocessedInput = vectorizer.transform(preprocessedInput).toarray()
    return preprocessedInput
# ----------------------------------------------------------------
# Web Scrapping Movie code and movie name
# -----------------------------------------------------------------


def webScrapping(userInput):
    safe_string = urllib.parse.quote_plus(userInput)
# Request Page Source for URL
    url = f"https://www.imdb.com/find?q={safe_string}&ref_=nv_sr_sm"
    page = requests.get(url)
# Displaying Page Source Code
    soup = BeautifulSoup(page.content, "html.parser")
    scraped_movies = soup.find('td', class_="result_text")
# scraped_movies
    if(scraped_movies == None):
        print("No Record Found")
    else:
        movieCode = scraped_movies.find('a')['href'].split('/')[2]
    url1 = f"https://www.imdb.com/title/{movieCode}/reviews/"
    pages = requests.get(url1)
# ---------------------------------------------------------
    soup = BeautifulSoup(pages.content, "html.parser")
    scraped_remarks = soup.find_all('div', class_="text show-more__control")
    reviews = []
    for scraped_remark in scraped_remarks:
        scraped_remark = scraped_remark.get_text().replace('\n', "")
        reviews.append(scraped_remark)
    return reviews, movieCode
# ----------------------------------------------------------------
# Showing Output
# -----------------------------------------------------------------


def ScrappReviews(userInput):
    scrapedMovieReviews, movieCode = webScrapping(userInput)
    if(scrapedMovieReviews == []):
        return "No movie Found please try again.", f"0 %", []
    afterVec = vectorization(scrapedMovieReviews)
    result1 = trainedModel.predict(afterVec)
    total = dict(Counter(result1))
    # calculate percentage
    totalPos = total['positive']
    totalNeg = total['negative']
    totalSum = totalPos + totalNeg
    if(totalPos >= totalNeg):
        overall = "Positive"
        totalPercentage = round((totalPos/totalSum)*100)
    else:
        overall = "Negative"
        totalPercentage = round((totalNeg/totalSum)*100)

    return overall, totalPercentage, movieCode


def getMessage(userInput):

    overall, totalPercentage, movieCode = ScrappReviews(userInput)
    movies = []
    cursor.execute(
        "Insert into dbo.movies(MovieID,MovieName) Values(?,?)", movieCode, userInput)
    cursor.execute(
        "Insert into dbo.prediction(MovieID,PredictionResult,Percentage,PredictedDate) values(?,?,?,GetDate())", movieCode, overall, totalPercentage)
    conn.commit()
    cursor.execute(
        "Select  Movies.MovieID,Movies.MovieName,Prediction.PredictionResult,Prediction.percentage ,Prediction.PredictedDate from Movies Join Prediction on Movies.MovieID=Prediction.MovieID ")
    for row in cursor.fetchall():
        movies.append({"MovieID": row[0], "MovieName": row[1],
                    "PredictionResult": row[2], "Percentage": row[3], "PredictedDate": row[4]})
        return f"Mostly Comments are: '{overall} '", f"\n Percentage: {totalPercentage} %", movies
