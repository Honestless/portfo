from flask import Flask, render_template, request, redirect, url_for
import csv
app = Flask(__name__)

@app.route("/")
def rdr():
    return redirect("index.html")

@app.route("/index.html")
def my_home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("login.html", )

@app.route('/<usr>')
def user(usr):
    return f"<h1>{usr}</h1>"

def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        text = data['text']
        message = data['message']
        database_write = database.write(f"\n {email}, {text}, {message}")

def write_to_csv(data):
    with open('database.csv', mode='a', newline="") as database2:
        email = data['email']
        text = data['text']
        message = data['message']
        csv_writer = csv.writer(database2, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, text, message])

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('/thankyou.html')
        except:
            return 'Contact attempt did not save to database.'
    else:
        return 'Something went wrong, try again'


if __name__ == '__main__':
    app.run(debug=True)
