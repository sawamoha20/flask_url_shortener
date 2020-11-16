from flask import Flask, render_template, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import urllib.parse
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///URLS.db'
db = SQLAlchemy(app)

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.sample(letters, length))
    return result_str
def addhttp(url):
    p = urllib.parse.urlparse(url, 'http')
    netloc = p.netloc or p.path
    path = p.path if p.netloc else ''
    if not netloc.startswith('www.'):
        netloc = 'www.' + netloc
    p = urllib.parse.ParseResult('http', netloc, path, *p[3:])
    return p.geturl()

class URLS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    URl = db.Column(db.String(200), nullable=False)
    shrt_value = db.Column(db.String(200),nullable=False,unique=True)
    
    def __init__(self,URl,shrt_value):
        self.URl = URl
        self.shrt_value = shrt_value

#website views

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        URl = request.form['main-url']
        shrt_value = get_random_string(4) if request.form['short-url'] == '' else request.form['short-url']
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
    val = addhttp(dblink.URl)
    #print(addhttp(val)
    return redirect(val)


@app.route('/delete/<id>')
def delete(id):
    link = URLS.query.get_or_404(id)
    db.session.delete(link)
    db.session.commit()
    flash("URL Deleted!")
    return redirect('/')

#api endpoints

@app.route('/api/add' , methods = ['POST'])
def add():
    list_data = request.get_json(force = True)
    URl = list_data['URl']
    shrt_value = get_random_string(4) if list_data['short_value'] == '' else list_data['short_value']
    link = URLS(URl, shrt_value)
    db.session.add(link)
    db.session.commit()
    return 'Done', 201
@app.route('/api/list')
def list():
    url_list = URLS.query.all()
    links = []
    for link in url_list:
        links.append({"URl": link.URl , "short_value": link.shrt_value})
    return jsonify({'links' : links})

@app.route('/api/delete/<id>')
def api_delete(id):
    link = URLS.query.get_or_404(id)
    db.session.delete(link)
    db.session.commit()
    return 'deleted' ,202

if __name__ == "__main__":
    app.secret_key = 'SLrs5ThKt9z'
    app.run(host='0.0.0.0',debug = True)




