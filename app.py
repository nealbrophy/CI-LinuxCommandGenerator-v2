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

@app.route('/')
def get_distros():
    # _distros = mongo.db.distros.find()
    # distro_list = [dist for dist in _distros]
    return render_template('distros.html', distros=mongo.db.distros.find())

if __name__ == '__main__':
    app.run(debug=True)