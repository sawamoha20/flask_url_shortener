from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///URLS.db'

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.sample(letters, length))
    return result_str


class URLS:
    id = db.Column(db.Integer, primary_key=True)
    URl = db.Column(db.Text, nullable=False)
    shrt_url = db.Column(db.Text,nullable=False)
    def __repr__(self):
        return 'url ' + str(self.id)


@app.route('/', methods = ['POST , GET'])
def home():
    if request.method == 'POST':
        link = request.form['main_url']
        short_url = get_random_string(5)
        

if __name__ == "__main__":
    app.run()