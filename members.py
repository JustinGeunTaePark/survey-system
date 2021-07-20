from flask_login import UserMixin
class User(UserMixin):
    def __init__(self, id):
        self.id = id

class Admin(object):
	def __init__(self, username, password):
		self.username = username
		self.password = password

	def get_username(self):
		return self.username

	def get_password(self):
		return self.password

	def set_username(self, username):
		self.username = username

	def set_password(self, password):
		self.password = password

admin1 = Admin("admin_user", "password")

"""
from flask import Flask, redirect, render_template, request, url_for
from server import app
import csv

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        zID = int(request.form["zID"])
        description = request.form["desc"]
        write(name, zID, description)
        return redirect(url_for("hello"))
    return render_template("index.html")

@app.route("/Hello")
def hello():
    return render_template("hello.html", all_users = read())

def write(name, zID, desc):
    with open('example.csv','a') as csv_out:
        writer = csv.writer(csv_out)
        writer.writerow([name, zID, desc])

def read():
    return_dict = []
    with open('example.csv','r') as csv_in:
        reader = csv.reader(csv_in)
        for row in reader:
            new_dict = {}
            new_dict['name'] = row[0]
            new_dict['zid'] = row[1]
            new_dict['description'] = row[2]
            return_dict.append(new_dict)
            
    return return_dict
"""