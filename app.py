import os 
from os import path
if path.exists("env.py"):
  import env 
from flask import Flask, render_template, url_for, redirect, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'linuxCmdGen'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)
form_info ={}
@app.route('/')
def get_distros():
    return render_template('distros.html', distros=mongo.db.distros.find(), form=form_info)

@app.route('/add')
def add_command():
  return render_template('add_commands.html', distros=mongo.db.distros.find())

@app.route('/insert_command', methods=['POST'])
def insert_command():
  form_info = request.form.to_dict()
  # distros = mongo.db.distros
  # distros.insert_one(request.form.to_dict())
  return redirect(url_for('get_distros', form=form_info))

if __name__ == '__main__':
    app.run(debug=True)
    