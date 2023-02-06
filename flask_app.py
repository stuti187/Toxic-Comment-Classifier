import pickle
from flask import Flask,request,app,jsonify,url_for,render_template
import numpy as np
import pandas as pd
from NLP_model import predict_sentiment
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

regmodel = pickle.load(open('classmodel.pkl','rb'))
ps = pickle.load(open('porter.pkl','rb'))

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/toxic comment'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Details(db.Model):
    __tablename__ = 'userdetail'
    sno=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    comment = db.Column(db.String(100), nullable=False)
    result= db.Column(db.String(20), nullable=False)
@app.route('/')
def home():
    return render_template('feedback.html')

@app.route('/review')
def review():
    outputs = Details.query.all()
    return render_template('review.html',outputs = outputs)

@app.route('/adddetails',methods = ['POST'])
def adddetails():
    name = request.form['uname']
    email = request.form.get('email')
    comment = request.form.get('comment')
    output = predict_sentiment(comment)
    if output[0]==0:
        result = "false"
    if output[0]==1:
        result = "true"
    print(name,email,comment,result)
    entry = Details(name=name,email = email,comment=comment,result=result)
    db.session.add(entry)
    db.session.commit()
    return render_template('feedback.html')

# @app.route('/demo',methods = ['POST'])
# def demo():
#     name = request.form['uname']
#     mbno = request.form.get('mno')
#     email = request.form.get('email')
#     comment = request.form.get('comment')
#     print(name,mbno,email,comment)
#     return render_template('home.html')

# @app.route('/predict_api',methods = ['POST'])
# def predict_api():
#     name = request.form['uname']
#     comment = request.form.get('comment')
#     output = predict_sentiment(comment)
#     if output[0]==0:
#          result="Comment is Toxic."
#          class1 = "danger"
#         # {
#         #      "result" : "Comment is Toxic."
#         #  }
#     if output[0]==1:
#         result="Comment is not Toxic."
#         class1 = "success"
#         # {
#         #     "result" : "Comment is not Toxic."
#         # } 
#     return render_template("result.html",name=name,comment=comment,result=result,class1=class1)

if __name__  ==  "__main__":
    app.run(debug=True)
