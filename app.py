# .\env\Scripts\activate.ps1
from unittest.mock import sentinel
from flask import Flask,render_template, request
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk 
import pickle
import numpy as np
import pandas as pd
import re # support regular expressions
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer  # Convert a collection of raw documents to a matrix of TF-IDF features.
from nltk.corpus import stopwords
# helps to plot graphs
# sets the backend of matplotlib to the 'inline' backend sets
# nltk.download('vader_lexicon')
app = Flask(__name__)
# routers mean endpoint
trainedModel=pickle.load(open("trainedModelNews", 'rb'))

vectorizer=pickle.load(open("vectorizer", 'rb'))

def preprocessing(sentence):
   sentence=re.sub(r'\W', ' ',str(sentence))
# Remove single characters from the start   
   sentence=re.sub(r'\^[a-zA-Z]\s+', ' ', sentence)
# Substituting multiples spaces with single characters    
   sentence=re.sub(r'\s+', ' ', sentence, flags=re.I)
# Removing prefixed 'b'
   sentence=re.sub(r'^b\s+', '', sentence)
# Converting to Lowercase
   sentence = sentence.lower()
   return sentence

def vectorization(preprocessedInput): 

   preprocessedInput=vectorizer.transform([preprocessedInput]).toarray()
   return preprocessedInput


@app.route('/',methods=['GET','POST'])
def index(): return render_template('main.html') 
   
@app.route('/data',methods=['GET','POST'])
def data():
   if request.method=='POST':
      inp=request.form.get('inp')
      inputs=preprocessing(inp)
      afterVec=vectorization([inp]).toarray()
      result=trainedModel.predict(afterVec)
      
      if result["neg"]!=0:
         return render_template('main.html',message="negative")
      else:
         return render_template('main.html',message="positive")
      
      
      
      return render_template('main.html')
#   return 'Hello, World!'

if __name__ == '__main__':
   app.run(debug=True)
   
   