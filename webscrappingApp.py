## Importing Modules  
import pandas as pd
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
import numpy as np
import re # support regular expressions
from bs4 import BeautifulSoup
import requests
import urllib.parse
from flask import Flask,render_template, request
import pickle
from nltk.corpus import stopwords
from collections import Counter
app = Flask(__name__)

trainedModel=pickle.load(open("trainedModelNews", 'rb'))
vectorizer=pickle.load(open("vectorizer", 'rb'))
# def preprocessing(sentence):
#     sentence=re.sub(r'\W', ' ',str(sentence))
# # Remove single characters from the start   
#     sentence=re.sub(r'\^[a-zA-Z]\s+', ' ', sentence)
# # Substituting multiples spaces with single characters    
#     sentence=re.sub(r'\s+', ' ', sentence, flags=re.I)
# # Removing prefixed 'b'
#     sentence=re.sub(r'^b\s+', '', sentence)
# # Converting to Lowercase
#     sentence = sentence.lower()
#     return sentence

def vectorization(preprocessedInput): 
    preprocessedInput=vectorizer.transform(preprocessedInput).toarray()
    return preprocessedInput

def webScrapping(userInput):
# userInput = "Planet Earth"
# movieCode="tt0072000"
    safe_string = urllib.parse.quote_plus(userInput)

## Request Page Source for URL

    url=f"https://www.imdb.com/find?q={safe_string}&ref_=nv_sr_sm"
    page=requests.get(url)

## Displaying Page Source Code

    soup=BeautifulSoup(page.content,"html.parser")
    scraped_movies=soup.find('td',class_="result_text")
# scraped_movies
    if(scraped_movies==None):
            print("no movie found")
    else:
        movieCode=scraped_movies.find('a')['href'].split('/')[2]
    url1=f"https://www.imdb.com/title/{movieCode}/reviews/"
    pages=requests.get(url1)

#---------------------------------------------------------

    soup=BeautifulSoup(pages.content,"html.parser")
    scraped_remarks=soup.find_all('div',class_="text show-more__control")
    reviews=[]
    for scraped_remark in scraped_remarks: 
        scraped_remark=scraped_remark.get_text().replace('\n',"")
        reviews.append(scraped_remark)
    
    return reviews
    

@app.route('/',methods=['GET','POST'])
def index(): return render_template('main.html') 
@app.route('/data',methods=['GET','POST'])
def data():
    if request.method=='POST':
        inp=request.form.get('inp')
        if(inp==''):  return render_template('main.html',message="No Input Found.")
        result=webScrapping(inp)
        if(result==[]):   
            return render_template('main.html',message="No movie Found please try again.")
        afterVec=vectorization(result)
        result1=trainedModel.predict(afterVec)
        # print(accuracy_score(result1))
        total = dict(Counter(result1))
        # df = pd.value_counts(np.array(result1))
        
        #calculate percentage
        totalPos=total['positive']
        totalNeg=total['negative']
        totalSum=totalPos+ totalNeg
        totalPercentagePos=(totalPos/totalSum)*100
        totalPercentageNeg=(totalNeg/totalSum)*100
        if total['positive'] >= total['negative']:
            return render_template('main.html',message="Mostly Comments are ' Positive '", percentage=totalPercentagePos)
            
        else:
            return render_template('main.html',message="Mostly Comments are ' Negative '", percentage=totalPercentageNeg)
                
        totalPercent=(total['positive']) /total
        render_template('main.html',percentage=totalPercent)
        
        # if result1 > "negative":
        #     return render_template('main.html',message="negative")
        # else:
        #     return render_template('main.html',message="positive")
if __name__ == '__main__':
        app.run(debug=True)




