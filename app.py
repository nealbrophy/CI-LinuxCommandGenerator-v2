import os 
from os import path
if path.exists("env.py"):
  import env 
from flask import Flask, render_template, redirect, request, url_for, abort
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import pyperclip
import pdb
from form import WTForm_with_ReCaptcha, csrf

# Flask
app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'linuxCmdGen'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config["RECAPTCHA_PUBLIC_KEY"] = '6LdiXPEUAAAAAK14HJzF9_m1YWsMHwhND5zUxq-9'
app.config["RECAPTCHA_PRIVATE_KEY"] = os.environ.get('RC_SECRETKEY')
csrf.init_app(app)

# ==========
# global vars
# ==========
mongo = PyMongo(app)

my_list = {}

# ==========
# HOME VIEW
# ==========
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

# =================
# ADD COMMANDS VIEW
# =================
@app.route('/add', methods=['GET','POST'])
def add_command():
  # pdb.set_trace()
  form = WTForm_with_ReCaptcha()
  if request.method == 'GET':
    return render_template('add_command.html', form=form, distros=mongo.db.distros.find(), commands=mongo.db.commands.find())
  else: 
    if form.validate():
      add_app = form.form_name.data.lower().replace(' ', '')
      add_distro = form.form_distro.data
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
          'app_url': form.form_url.data,
          'app_instruction': form.form_instruction.data,
          'app_command': form.form_command.data}
        mongo.db.commands.insert_one(cmd_to_insert)
        return render_template('find_command.html', req_type='insert_success',
          results=mongo.db.commands.find({'app_name': {'$regex': add_app, '$options': 'ix'}, 'app_distro': add_distro}),
          distros=mongo.db.distros.find(), commands=mongo.db.commands.find())
    elif 'response parameter is missing' in form.errors['form_recaptcha'][0]:
      return render_template('add_command.html', form=form, error='captcha missing', distros=mongo.db.distros.find(), commands=mongo.db.commands.find())

# =================
# FIND COMMAND VIEW
# =================
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

# =================
# EDIT COMMAND VIEW
# =================
@app.route('/edit/<command_id>', methods=['POST', 'GET'])
def edit_command(command_id):
  # pdb.set_trace()
  form = WTForm_with_ReCaptcha()
  commands = mongo.db.commands
  cmd_to_update = mongo.db.commands.find_one({'_id': ObjectId(command_id)})
  distros = mongo.db.distros.find()
  if request.method == 'GET':
    return render_template('edit_command.html', form=form, cmd_to_update=cmd_to_update, distros=distros)
  else:
    if form.validate():
      if form.form_submit:
        commands.update({'_id': ObjectId(command_id)}, 
        {
          'app_name': form.form_name.data,
          'app_distro': form.form_distro.data,
          'app_url': form.form_url.data,
          'app_instruction': form.form_instruction.data,
          'app_command': form.form_command.data
        })
        return render_template('find_command.html', req_type='update',
          results=mongo.db.commands.find({'_id': ObjectId(command_id)}),
          distros=mongo.db.distros.find(), commands=mongo.db.commands.find())
    else:
      return 'Error'
# ===================
# DELETE COMMAND VIEW
# ===================
@app.route('/confirm_delete/<command_id>', methods=['POST', 'GET'])
def confirm_delete(command_id):
  # pdb.set_trace()
  form = WTForm_with_ReCaptcha()
  cmd_to_delete = mongo.db.commands.find_one({'_id': ObjectId(command_id)})
  if request.method == 'GET':
    return render_template('delete_command.html', form=form, cmd_to_delete=cmd_to_delete, results=mongo.db.commands.find({'_id': ObjectId(command_id)}),
            distros=mongo.db.distros.find(), commands=mongo.db.commands.find())
  else:
    if form.validate():
      if form.form_submit:
        mongo.db.commands.remove({'_id': ObjectId(command_id)})
        return render_template('find_command.html', req_type='find', distros=mongo.db.distros.find(), commands=mongo.db.commands.find())
    elif form.errors:
      return render_template('delete_command.html', error=form.errors, form=form, cmd_to_delete=cmd_to_delete, results=mongo.db.commands.find({'_id': ObjectId(command_id)}),
            distros=mongo.db.distros.find(), commands=mongo.db.commands.find())

# =================
# ADD TO LIST VIEW
# =================
@app.route('/add_to_list/<command_id>')
def add_to_list(command_id):
  # pdb.set_trace()
  cmd_to_save = mongo.db.commands.find_one({'_id': ObjectId(command_id)})
  # formatted_name = f"{cmd_to_save['app_name']} ({cmd_to_save['app_distro']})"
  for key, value in my_list.items():
    if command_id in str(key):
      return 'app already in list'
  else:
    my_list[cmd_to_save['_id']] = {'app': cmd_to_save['app_name'], 'distro': cmd_to_save['app_distro'], 'url': cmd_to_save['app_url'], 'instruction': cmd_to_save['app_instruction'], 'command': cmd_to_save['app_command']}
    return redirect(url_for('my_list_func'))

# ============= 
# MY LIST VIEW
# =============
@app.route('/my_list')
def my_list_func():
  return render_template('my_list.html', my_list=my_list)

# remove action for MY LIST VIEW
@app.route('/remove_from_list/<command_id>')
def remove_from_list(command_id):
  for key, value in my_list.items():
    if str(key) == command_id:
      my_list.pop(key)
      return redirect(url_for('my_list_func'))
      

# ======================
# COPY COMMAND operation
# ======================
@app.route('/copy_command/<command_id>')
def copy_command(command_id):
  cmd_to_copy = mongo.db.commands.find_one({'_id': ObjectId(command_id)})
  pyperclip.copy(cmd_to_copy['app_command'])
  return 'copied to clipboard'




# RUN Flask app
if __name__ == '__main__':
    app.run(debug=True)
    