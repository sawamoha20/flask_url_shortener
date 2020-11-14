from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///URLS.db'
db = SQLAlchemy(app)

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.sample(letters, length))
    return result_str


class URLS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    URl = db.Column(db.String(200), nullable=False)
    shrt_value = db.Column(db.String(200),nullable=False,unique=True)
    
    def __init__(self,URl,shrt_value):
        self.URl = URl
        self.shrt_value = shrt_value


@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        URl = request.form['main-url']
        shrt_value = get_random_string(5)
        link = URLS(URl, shrt_value)
        db.session.add(link)
        db.session.commit()
    Data = URLS.query.all()
    print(Data)
    return render_template('index.html',Data = Data)

@app.route('/<value>')       
def unshorten(value):
    dblink = db.session.query(URLS).filter(URLS.shrt_value==value).first()
    print(dblink)
    link = dblink.URl
    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)