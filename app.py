from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# sqlalchemy 설정
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask_db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# sqlalchemy 초기화
db = SQLAlchemy(app) 

migrate = Migrate(app,db)

class User(db.Model) :
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50))



@app.route("/") 
def hello():
    users = User.query.all()
    return render_template("index.html", users=users)
    
@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/create")
def create():
    name = request.args.get("name")
    email = request.args.get("email")
    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect("/")

@app.route("/post_new")
def post_new():
    return render_template("post_new.html")
    
@app.route("/post_create",methods=["post"])
def post_create():
    name = request.form.get("name")
    email = request.form.get("email")
    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect("/")
    
    
    
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)