from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'secrete123'
client = MongoClient("mongodb://localhost:27017/")
db = client["localdb"]
collection = db["local"]
@app.route('/')
def form():
    return render_template('form.html', error=None)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    phone_number = request.form['phone_number']
    if not name or not email:
        error = "Name and Email are required."
        return render_template('form.html', error=error)
    collection.insert_one({'name': name, 'email': email})
    session["submitted"] = True
    return redirect(url_for('success'))
@app.route("/success")
def success():
    if not session.get("submitted"):
        return redirect(url_for("form"))  # redirect if refresh

    session.pop("submitted", None)  # remove flag after first load
    return render_template("success.html")
if __name__ == '__main__':
    app.run(debug=True)