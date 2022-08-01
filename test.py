from flask import Flask,render_template,request
 
app = Flask(__name__)
 
@app.route('/form')
def main():
    return render_template('main.html')
 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'POST':
        inp=request.form.get('inp')
    # sid= preprocessing
    # vectorization
    
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug='True')