from flask import Flask, render_template, request
from lib import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index(): return render_template('main.html')


@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':

        userInput = request.form.get('inp')
        # query1 = cursor.execute("SELECT Movies.MovieName FROM Movies WHERE MoviesName = @userInput", {"userInput": userInput}).fetchone()
        cursor.execute("SELECT * from movies where MovieName like '%'+?+'%'",[userInput])
        
        results=cursor.fetchall()
        if results:
            message, percentage, movies = getMessage(userInput)
        # cursor.execute(
        # "Insert into dbo.prediction(PredictionResult,PredictedDate) Values(?,getDate())",message)
            return render_template('main.html', message=message, percentage=percentage, movies=movies)
        else:
            print("error")

if __name__ == '__main__':
    app.run(debug=True)

conn.close()
