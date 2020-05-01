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

my_list = {}

# HOME VIEW
@app.route('/')
def get_distros():
  distros=mongo.db.distros.find() 
  distro_counter = []
  cmd_counter = []
  for distro in distros:
    distro_counter.append(distro['distro_name'])
    cmd_counter.append(mongo.db.commands.count_documents({'app_distro': distro['distro_name']}))
  counter = {key:value for key, value in zip(distro_counter, cmd_counter)}
  return render_template('distros.html', counter=counter, 
      distros=mongo.db.distros.find(), 
      commands=mongo.db.commands.find())

@app.route('/distro_cmds/<distro_name>', methods=['GET', 'POST'])
def get_distro_cmds(distro_name):
  return render_template('find_command.html', req_type='find', 
        distros=mongo.db.distros.find(),
        results=mongo.db.commands.find({'app_distro': distro_name}))

# ===============
# CRUD Operations
# ===============

# ADD COMMANDS VIEW
@app.route('/add')
def add_command():
    return render_template('add_command.html', distros=mongo.db.distros.find(), commands=mongo.db.commands.find())

# insert command action from ADD COMMAND VIEW
@app.route('/insert_command', methods=['POST'])
def insert_command():
    # pdb.set_trace()
    add_app = request.form.get('app_name').lower().replace(' ', '')
    add_distro = request.form.get('app_distro')
    existing_cmds = mongo.db.commands.count_documents({
      'app_name': {'$regex': add_app, '$options': 'ix'}, 
      'app_distro': {'$regex': add_distro, '$options': 'ix'}
      })
    if existing_cmds:
      return render_template('find_command.html', req_type='insert_fail',
        results=mongo.db.commands.find({'app_name': {'$regex': add_app, '$options': 'ix'}, 'app_distro': add_distro}),
        distros=mongo.db.distros.find(), commands=mongo.db.commands.find())
    else:
      cmd_to_insert = {
        'app_name': add_app,
        'app_distro': add_distro,
        'app_url': request.form.get('app_url'),
        'app_instruction': request.form.get('app_instruction'),
        'app_command': request.form.get('app_command')}
      mongo.db.commands.insert_one(cmd_to_insert)
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
      find_app = request.form.get('app_name').replace(' ', '')
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

# update command action FROM EDIT VIEW
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

# confirm delete action from DELETE COMMAND VIEW
@app.route('/confirm_delete/<command_id>')
def confirm_delete(command_id):
  cmd_to_delete = mongo.db.commands.find_one({'_id': ObjectId(command_id)})
  return render_template('delete_command.html', cmd_to_delete=cmd_to_delete, results=mongo.db.commands.find({'_id': ObjectId(command_id)}),
          distros=mongo.db.distros.find(), commands=mongo.db.commands.find())

# DELETE COMMAND VIEW
@app.route('/delete/<command_id>', methods=['POST'])
def delete_command(command_id):
  mongo.db.commands.remove({'_id': ObjectId(command_id)})
  return render_template('find_command.html', req_type='find', distros=mongo.db.distros.find(), commands=mongo.db.commands.find())

# ==================
# My List Operations
# ==================

# ADD TO LIST VIEW
@app.route('/add_to_list/<command_id>')
def add_to_list(command_id):
  # pdb.set_trace()
  cmd_to_save = mongo.db.commands.find_one({'_id': ObjectId(command_id)})
  formatted_name = f"{cmd_to_save['app_name']}_{cmd_to_save['app_distro']}"
  if formatted_name in my_list:
    return 'app already in list'
  else:
    my_list[formatted_name] = {'instructions': cmd_to_save['app_instruction'], 'command': cmd_to_save['app_command']}
    return redirect(url_for('my_list_func'))
  
# MY LIST VIEW
@app.route('/my_list')
def my_list_func():
  return render_template('my_list.html', my_list=my_list)

# remove action for MY LIST VIEW
@app.route('/remove_from_list/<command_id>')
def remove_from_list(command_id):
 return 'something'

# ===============
# other Operations
# ===============
# UPLOAD COMMANDS
# @app.route()



# RUN Flask app
if __name__ == '__main__':
    app.run(debug=True)
    