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

# INSERT COMMAND ACTION FROM ADD COMMAND VIEW
@app.route('/insert_command', methods=['POST'])
def insert_command():
    # pdb.set_trace()
    add_app = request.form.get('app_name')
    add_distro = request.form.get('app_distro')
    existing_cmds = mongo.db.commands.find()
    if existing_cmds.retrieved:
      for commands in existing_cmds:
        if commands['app_name'] == add_app and commands['app_distro'] == add_distro:
          return render_template('find_command.html', req_type='insert_fail',
            results=mongo.db.commands.find({'app_name': {'$regex': add_app, '$options': 'ix'}, 'app_distro': add_distro}),
            distros=mongo.db.distros.find(), commands=mongo.db.commands.find())
    else:
      commands = mongo.db.commands
      commands.insert_one(request.form.to_dict())
      return render_template('find_command.html', req_type='insert_success',
        results=mongo.db.commands.find({'app_name': {'$regex': add_app, '$options': 'ix'}, 'app_distro': add_distro}),
        distros=mongo.db.distros.find(), commands=mongo.db.commands.find())
          

# FIND COMMAND VIEW
@app.route('/find_command', methods=['GET','POST']) 
def find_command():
  # pdb.set_trace()
  if request.method == 'GET':
    return render_template('find_command.html', req_type='find', distros=mongo.db.distros.find())
  else:
    if request.form.get('app_name') and request.form.get('app_distro'):
      find_app = request.form.get('app_name')
      find_distro = request.form.get('app_distro')
      return render_template('find_command.html', req_type='find', 
        distros=mongo.db.distros.find(),
        results=mongo.db.commands.find({'app_name': {'$regex': find_app, '$options': 'ix'}, 'app_distro': find_distro}))
    elif request.form.get('app_name'):
      find_app = request.form.get('app_name')
      return render_template('find_command.html', req_type='find', 
        distros=mongo.db.distros.find(),
        results=mongo.db.commands.find({'app_name': {'$regex': find_app, '$options': 'ix'}}))
    elif request.form.get('app_distro'):
      find_distro = request.form.get('app_distro')
      return render_template('find_command.html', req_type='find', 
        distros=mongo.db.distros.find(),
        results=mongo.db.commands.find({'app_distro': find_distro}))
    else:
      return render_template('find_command.html', req_type='empty', 
        distros=mongo.db.distros.find())


# EDIT COMMAND VIEW
@app.route('/edit/<command_id>')
def edit_command(command_id):
  cmd_to_update = mongo.db.commands.find_one({'_id': ObjectId(command_id)})
  distros = mongo.db.distros.find()
  return render_template('edit_command.html', cmd_to_update=cmd_to_update, distros=distros)

# UPDATE COMMAND ACTION FROM EDIT VIEW
@app.route('/update/<command_id>', methods=['POST'])
def update_command(command_id):
  commands = mongo.db.commands
  commands.update({'_id': ObjectId(command_id)},
  {
    'app_name': request.form.get('app_name'),
    'app_distro': request.form.get('app_distro'),
    'app_instruction': request.form.get('app_instruction'),
    'app_command': request.form.get('app_command')
  })
  return render_template('find_command.html', req_type='update',
          results=mongo.db.commands.find({'_id': ObjectId(command_id)}),
          distros=mongo.db.distros.find(), commands=mongo.db.commands.find())

@app.route('/confirm_delete/<command_id>')
def confirm_delete(command_id):
  cmd_to_delete = mongo.db.commands.find_one({'_id': ObjectId(command_id)})
  return render_template('delete_command.html', cmd_to_delete=cmd_to_delete, results=mongo.db.commands.find({'_id': ObjectId(command_id)}),
          distros=mongo.db.distros.find(), commands=mongo.db.commands.find())

# DELETE COMMAND VIEW
@app.route('/delete/<command_id>')
def delete_command(command_id):
  mongo.db.commands.remove({'_id': ObjectId(command_id)})
  return render_template('find_command.html', req_type='find', distros=mongo.db.distros.find())





# RUN Flask app
if __name__ == '__main__':
    app.run(debug=True)
    