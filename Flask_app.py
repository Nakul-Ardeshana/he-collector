from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from emailsender import send_email
from sqlalchemy.sql import func

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgres://mndvfuvrbwocys:be7b8204109c9d7d8971b93608200995856b592b94c35b0d4573cc26ca4c058d@ec2-54-152-40-168.compute-1.amazonaws.com:5432/dbmn8jorjej9a6?sslmode=require'
db=SQLAlchemy(app)
print(db)

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120),unique=True)
    height_=db.Column(db.Integer)
    phoneno_=db.Column(db.String,unique=True)

    def __init__(self, email_, height_, phoneno_):
        self.email_=email_
        self.height_=height_
        self.phoneno_=phoneno_

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success",methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form["email_name"]
        height = request.form["height"]
        phoneno = request.form["phone_number"]
        if db.session.query(Data).filter(Data.email_ == email).count() == 0 :
            if db.session.query(Data).filter(Data.phoneno_ == phoneno).count() == 0 :
                data=Data(email,height,phoneno)
                db.session.add(data)
                db.session.commit()
                average_height=db.session.query(func.avg(Data.height_)).scalar()
                average_height= round(average_height,3)
                count=db.session.query(Data.height_).count()
                send_email(email,height,average_height,count)
                return render_template("success.html")
            else:
                return render_template("index.html", text="There was an Error <br> this error occured because you or someone else used the same phone number!!")
        else:
            return render_template("index.html", text="There was an Error <br> this error occured because you or someone else used the same email!!")


if __name__ == '__main__':
    app.debug=False
    app.run()