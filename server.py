from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

@app.route("/")
def rdr():
    return redirect("index.html")

@app.route("/index.html")
def my_home():
    return render_template('index.html')

@app.route('/dashboard.html')
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/blog.html")
def my_blog():
    return render_template('blog.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

@app.route("/login.html", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['email']
        passw = request.form['passw']
        try:
            data = User.query.filter_by(username=name, password=passw).first()
            if data is not None:
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return 'Dont Login'
        except:
            return "Dont Login"


@app.route("/register.html", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form['email']
        passw = request.form['passw']
        if User.query.filter_by(email=email) != None:
            register_user = User(email=email, password=passw)
            db.session.add(register_user)
            db.session.commit()

        else:
            print("Email already exists in the database", "error")

        return redirect(url_for("login"))
    return render_template("register.html")


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)