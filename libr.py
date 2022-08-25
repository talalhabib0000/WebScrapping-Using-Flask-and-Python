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
trainedModel = pickle.load(open("trainedModelNews", 'rb'))
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
    # scraped_movies = soup.find('td', class_="result_text")
    # names = []
    # for scraped_names in scraped_movies:
    #     scraped_names = scraped_names.get_text().replace('\n', "")
    #     names.append(scraped_remark) 
# scraped_movies
    sections=soup.findAll('div', class_="findSection")
    for section in sections:
        sectionContent=section.contents
        sectionHeader=sectionContent[1].contents
        scrap_Movies=section.findAll('td', class_="result_text")
        if(scrap_Movies == None):return [],''
        else:
            if sectionHeader[1]=='Titles':
                movies=[]
        for movie in scrap_Movies:
            movie=movie.get_text().replace('\n',"")
            movie=movie.strip(" ")
            movies.append(movie)
        movieCode=[]
        for code in scrap_Movies:
            code =  code.find('a').get('href').split('/')[2]
            movieCode.append(code)
        url1 = f"https://www.imdb.com/title/{movieCode}/reviews/"
        pages = requests.get(url1)
        codes=[]
        for  movieCode in scrap_Movies:
            scraped_remark = scraped_remark.get_text().replace('\n', "")
        
        codes.append(movieCode)
# ---------------------------------------------------------
        soup = BeautifulSoup(pages.content, "html.parser")
        scraped_remarks = soup.find_all('div', class_="text show-more__control")
        reviews = []
    for scraped_remark in scraped_remarks:
        scraped_remark = scraped_remark.get_text().replace('\n', "")
        reviews.append(scraped_remark)
    return reviews, codes
# ----------------------------------------------------------------
# Showing Output
# -----------------------------------------------------------------


def ScrappReviews(userInput):
    scrapedMovieReviews, codes = webScrapping(userInput)
    if(scrapedMovieReviews == []):
        return "No movie Found please try again.",''
    afterVec = vectorization(scrapedMovieReviews)
    result1 = trainedModel.predict(afterVec)
    return result1,codes


def PredictPercentage(userInput):
    result1, codes = (ScrappReviews(userInput))
    total = dict(Counter(result1))
    if (codes== ''):
        return "No movie Found please try again.","0", []
    else:
        
        if (total.get('positive') == 0 or total.get('positive') == None):
            {
            total.update({'positive': 1})
            }
        elif(total.get('negative') == 0 or total.get('negative') == None):
            {
            total.update({'negative': 1})
            }
    totalPos = total['positive']
    totalNeg = total['negative']
    totalSum = totalPos + totalNeg
    if(totalPos >= totalNeg):
        overall = "Positive"
        totalPercentage = round((totalPos/totalSum)*100)
    else:
        overall = "Negative"
        totalPercentage = round((totalNeg/totalSum)*100)

        return overall, totalPercentage, codes

def getMessage(userInput):
    movies = []
    overall, totalPercentage, codes = PredictPercentage(userInput)
    if (codes== []):
        return f"'{overall} '", f"\n Percentage: {totalPercentage} %", movies
    else:
        cursor.execute(
        "Select Movies.MovieID,Movies.MovieName,Prediction.PredictionResult,Prediction.Percentage,Prediction.PredictedDate from Movies Join Prediction on Movies.MovieID=Prediction.MovieID WHERE DATEDIFF(day,GETDATE(),PredictedDate) <= 30  AND Movies.MovieName like '%'+?+'%'", [
            userInput]
    )
    for row in cursor.fetchall():
        movies.append({
                    "MovieID": row[0], "MovieName": row[1],
                    "PredictionResult": row[2], "Percentage": row[3], "PredictedDate": row[4]})
        return f"Mostly Comments are: '{overall} '", f"\n Percentage: {totalPercentage} %", movies
    
    cursor.execute("Update Prediction Set Prediction.PredictionResult=?,Prediction.Percentage=?,Prediction.PredictedDate=GetDate() from Prediction where DATEDIFF(day,GETDATE(),PredictedDate) >= 30 ", (overall, totalPercentage))
    cursor.execute(
        "Select Movies.MovieID,Movies.MovieName,Prediction.PredictionResult,Prediction.Percentage,Prediction.PredictedDate from Movies Join Prediction on Movies.MovieID=Prediction.MovieID WHERE DATEDIFF(day,GETDATE(),PredictedDate) <= 30 AND Movies.MovieName like '%'+?+'%'", [
            userInput]
    )
    for row in cursor.fetchall():
        movies.append({
                    "MovieID": row[0], "MovieName": row[1],
                    "PredictionResult": row[2], "Percentage": row[3], "PredictedDate": row[4]})
        return f"Mostly Comments are: '{overall} '", f"\n Percentage: {totalPercentage} %", movies
    cursor.execute(
        "Insert into dbo.movies(MovieID,MovieName) Values(?,?)", codes, userInput)
    cursor.execute(
        "Insert into dbo.prediction(MovieID,PredictionResult,Percentage,PredictedDate) values(?,?,?,GetDate())", codes, overall, totalPercentage)
    conn.commit()
    for row in cursor.fetchall():
        movies.append({
                    "MovieID": row[0], "MovieName": row[1],
                    "PredictionResult": row[2], "Percentage": row[3], "PredictedDate": row[4]})
        return f"Mostly Comments are: '{overall} '", f"\n Percentage: {totalPercentage} %", movies
    # Select  Movies.MovieID,Movies.MovieName,Prediction.PredictionResult,Prediction.percentage ,Prediction.PredictedDate from Movies Join Prediction on Movies.MovieID=Prediction.MovieID
    return f"Mostly Comments are: '{overall} '", f"\n Percentage: {totalPercentage} %", movies