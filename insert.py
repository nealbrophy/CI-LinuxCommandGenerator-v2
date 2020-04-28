import pdb
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect, request, url_for, abort
import os
from os import path
if path.exists("env.py"):
    import env
from __main__ import app

mongo = PyMongo(app)

# INSERT COMMAND ACTION FROM ADD COMMAND VIEW
@app.route('/insert_command', methods=['POST'])
def insert_command():
    # pdb.set_trace()
    find_app = request.form.get('app_name')
    find_distro = request.form.get('app_distro')
    existing_cmds = mongo.db.commands.find({'app_name': {'$regex': find_app, '$options': 'ix'}, 'app_distro': find_distro})
    for docs in existing_cmds:
        return docs
            # if find_app in items and find_distro in items:
            #     return "Command already exists"
            # else:
            #     commands = mongo.db.commands
            #     commands.insert_one(request.form.to_dict())
            #     return render_template('distros.html', distros=mongo.db.distros.find(), commands=mongo.db.commands.find())