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

@app.route('/find_commands', methods=['POST'])
def find_commands():
    find_app = request.form.get('app_name')
    find_distro = request.form.get('app_distro')
    return render_template('find_command.html',
                           results=mongo.db.commands.find({'app_name': {'$regex': find_app, '$options': 'ix'}, 'app_distro': find_distro}))