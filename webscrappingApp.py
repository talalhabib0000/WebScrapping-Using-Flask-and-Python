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
app = Flask(__name__)

DRIVER_NAME = 'SQL Server'
SERVER_NAME = 'DESKTOP-B3U0GP9\SQLEXPRESS'
DATABASE_NAME = 'school'
connection_string = f""" 

    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_connection=yes;
"""
conn = odbc.connect(connection_string)

trainedModel = pickle.load(open("trainedModelNews", 'rb'))
vectorizer = pickle.load(open("vectorizer", 'rb'))


def vectorization(preprocessedInput):
    preprocessedInput = vectorizer.transform(preprocessedInput).toarray()
    return preprocessedInput


def webScrapping(userInput):
    # userInput = "Planet Earth"
    # movieCode="tt0072000"
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
    return reviews


# def checkMovieExists():
#     conn = odbc.connect(connection_string)
#     SQL_QUERY= pd.read_sql_query('Select * from course', conn)
#     print(SQL_QUERY)
# conn.close()

def getMessage(userInput):
    scrapedMovieReviews = webScrapping(userInput)
    if(scrapedMovieReviews == []):
        return "No movie Found please try again."
    afterVec = vectorization(scrapedMovieReviews)
    result1 = trainedModel.predict(afterVec)
    total = dict(Counter(result1))
    # calculate percentage
    totalPos = total['positive']
    totalNeg = total['negative']
    totalSum = totalPos + totalNeg
    totalPercentagePos = (totalPos/totalSum)*100
    totalPercentageNeg = (totalNeg/totalSum)*100
    if total['positive'] >= total['negative']:
        return "Mostly Comments are ' Positive '", totalPercentagePos
    else:
        return "Mostly Comments are ' Negative '", totalPercentageNeg


@app.route('/', methods=['GET', 'POST'])
def index(): return render_template('main.html')


@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        userInput = request.form.get('inp')
        message, percentage = getMessage(userInput)
        return render_template('main.html', message=message, percentage=percentage)


if __name__ == '__main__':
    app.run(debug=True)
