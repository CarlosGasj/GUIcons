import flask
from flask import render_template, Flask
import GUI

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')