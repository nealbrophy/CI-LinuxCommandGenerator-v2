import os 
from os import path
if path.exists("env.py"):
  import env 
from flask import Flask, render_template, redirect, request, url_for, abort
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import pdb

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'linuxCmdGen'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

import find
import insert

mongo = PyMongo(app)

# HOME VIEW
@app.route('/')
def get_distros():
    return render_template('distros.html', 
      distros=mongo.db.distros.find(), 
      commands=mongo.db.commands.find())

# ADD COMMANDS VIEW
@app.route('/add')
def add_command():
    return render_template('add_command.html', distros=mongo.db.distros.find(), commands=mongo.db.commands.find())



# FIND COMMANDS VIEW
@app.route('/find', methods=['GET']) 
def find():
  return render_template('find_command.html', distros=mongo.db.distros.find(), commands=mongo.db.commands.find())


if __name__ == '__main__':
    app.run(debug=True)
    