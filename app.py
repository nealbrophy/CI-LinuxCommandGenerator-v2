import os 
from os import path
if path.exists("env.py"):
  import env 
from flask import Flask, render_template, redirect, request, url_for, abort, flash
from flask_pymongo import PyMongo
from flask_toastr import Toastr
from bson.objectid import ObjectId
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content, Email
import pdb
from form import AddCommandForm, csrf, EmailForm, SimpleSearch, DeleteForm, EditForm, AddDistroForm
import smtplib, ssl
import random

app = Flask(__name__)
# mongodb
app.config["MONGO_DBNAME"] = 'linuxCmdGen'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')
# csrf
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
csrf.init_app(app)
# recaptcha
app.config["RECAPTCHA_PUBLIC_KEY"] = '6LdiXPEUAAAAAK14HJzF9_m1YWsMHwhND5zUxq-9'
app.config["RECAPTCHA_PRIVATE_KEY"] = os.environ.get('RC_SECRETKEY')
# pymongo
mongo = PyMongo(app)
# flask_toastr
toastr = Toastr(app)
app.config['TOASTR_TIMEOUT'] = 4000

# =======================
# global vars & functions
# =======================
my_list = {}
distros_for_form = {distro['distro_name'] for distro in mongo.db.distros.find()}
header_images = [
  'https://i.imgur.com/Eazve8h.png',
  'https://i.imgur.com/6KB5U0y.png',
  'https://i.imgur.com/SlytyUz.png',
  'https://i.imgur.com/guFnrW5.png',
  'https://i.imgur.com/zwz1wla.png',
  'https://i.imgur.com/rh0SKoJ.png',
  'https://i.imgur.com/FvkUUea.png',
  'https://i.imgur.com/QFfaNxs.png',
  'https://i.imgur.com/rXIBDzI.png',
  'https://i.imgur.com/bwcn9Sq.png',
  'https://i.imgur.com/GpnCCcu.png',
  'https://i.imgur.com/wERzsMH.png'
]
footer_images = [
  'https://i.imgur.com/E8xv9bp.png',
  'https://i.imgur.com/bOJP0W5.png'
]
def random_image(list):
  for x in range(10):
    random_num = random.randint(1, 11)
  return list[random_num]

# ==========
#  Flask VIEWS
# ==========
@app.route('/')
def get_distros():
  form = SimpleSearch()
  choices = [('', 'select distro')]
  for distro in mongo.db.distros.find():
    choices.append((f"{distro['distro_name']}",f"{distro['distro_name']}"))
  form.search_distro.choices = choices
  distros=mongo.db.distros.find() 
  distro_counter = []
  cmd_counter = []
  for distro in distros:
    distro_counter.append(distro['distro_name'])
    cmd_counter.append(mongo.db.commands.count_documents({'app_distro': distro['distro_name']}))
  counter = {key:value for key, value in zip(distro_counter, cmd_counter)}
  empty_distros = {}
  for key, value in counter.items():
    if value == 0:
      empty_distros[key] = value
  return render_template('distros.html', header_images=header_images, random_image=random_image(header_images), counter=counter, empty_distros=empty_distros, form=form,
      distros=mongo.db.distros.find(), 
      commands=mongo.db.commands.find())

# DISTRO commands VIEW
@app.route('/distro_cmds/<distro_name>', methods=['GET', 'POST'])
def get_distro_cmds(distro_name):
  form = SimpleSearch()
  choices = [('', 'select distro')]
  for distro in mongo.db.distros.find():
    choices.append((f"{distro['distro_name']}",f"{distro['distro_name']}"))
  form.search_distro.choices = choices
  return render_template('find_command.html', req_type='find', form=form, find_distro=distro_name,
        distros=mongo.db.distros.find(),
        results=mongo.db.commands.find({'app_distro': distro_name}))

# FIND commands VIEW
@app.route('/find_command', methods=['GET','POST']) 
def find_command():
  form = SimpleSearch()
  choices = [('', 'select distro')]
  for distro in mongo.db.distros.find():
    choices.append((f"{distro['distro_name']}",f"{distro['distro_name']}"))
  form.search_distro.choices = choices
  if request.method == 'GET':
    return render_template('find_command.html', req_type='find', form=form, distros=mongo.db.distros.find())
  else:
    if form.search_app.data and form.search_distro.data:
      find_app = form.search_app.data.replace(' ', '')
      find_distro = form.search_distro.data
      return render_template('find_command.html', req_type='find', form=form, find_app=find_app, find_distro=find_distro,
        distros=mongo.db.distros.find(),
        results=mongo.db.commands.find({'app_name': {'$regex': find_app, '$options': 'ix'}, 'app_distro': find_distro}))
    elif form.search_app.data:
      find_app = form.search_app.data
      return render_template('find_command.html', req_type='find', form=form, find_app=find_app,
        distros=mongo.db.distros.find(),
        results=mongo.db.commands.find({'app_name': {'$regex': find_app, '$options': 'ix'}}))
    elif form.search_distro.data:
      find_distro = form.search_distro.data
      return render_template('find_command.html', req_type='find', form=form, find_distro=find_distro,
        distros=mongo.db.distros.find(),
        results=mongo.db.commands.find({'app_distro': find_distro}))
    else:
      return render_template('find_command.html', req_type='empty', form=form,
        distros=mongo.db.distros.find())

# COMMAND VIEW
@app.route('/command/<command_id>')
def command_view(command_id):
  command = mongo.db.commands.find_one({'_id': ObjectId(command_id)})
  return render_template('command.html', command=command)

# ADD command VIEW
@app.route('/add_command', methods=['GET','POST'])
def add_command():
  form = AddCommandForm()
  choices = [('', 'select distro')]
  for distro in mongo.db.distros.find():
    choices.append((f"{distro['distro_name']}",f"{distro['distro_name']}"))
  form.form_distro.choices = choices
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
        flash('command already exists!', 'warning')
        form=SimpleSearch()
        choices = [('', 'select distro')]
        for distro in mongo.db.distros.find():
          choices.append((f"{distro['distro_name']}",f"{distro['distro_name']}"))
        form.search_distro.choices = choices
        return render_template('find_command.html', form=form,
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
        flash('Command added!')
        form=SimpleSearch()
        choices = [('', 'select distro')]
        for distro in mongo.db.distros.find():
          choices.append((f"{distro['distro_name']}",f"{distro['distro_name']}"))
        form.search_distro.choices = choices
        return render_template('find_command.html', form=form,
          results=mongo.db.commands.find({'app_name': {'$regex': add_app, '$options': 'ix'}, 'app_distro': add_distro}),
          distros=mongo.db.distros.find(), commands=mongo.db.commands.find())
    elif form.form_recaptcha.data == None:
      flash('Please complete reCAPTCHA!')
      return render_template('add_command.html', form=form, error='captcha missing', distros=mongo.db.distros.find(), commands=mongo.db.commands.find())

# ADD DISTRO VIEW
@app.route('/add_distro', methods=['GET','POST'])
def add_distro():
  form = AddDistroForm()
  distros=mongo.db.distros.find() 
  distro_counter = []
  cmd_counter = []
  for distro in distros:
    distro_counter.append(distro['distro_name'])
    cmd_counter.append(mongo.db.commands.count_documents({'app_distro': distro['distro_name']}))
  counter = {key:value for key, value in zip(distro_counter, cmd_counter)}
  empty_distros = {}
  for key, value in counter.items():
    if value == 0:
      empty_distros[key] = value
  if request.method == 'GET':
    return render_template('add_distro.html', form=form)
  else:
    if form.validate():
      distro = form.distro_name.data
      logo = form.distro_logo.data
      existing_distro = mongo.db.distros.count_documents({
        'distro_name': {'$regex': distro, '$options': 'ix'}
        })
      if existing_distro:
        flash('distro already exists!', 'warning')
        return redirect(url_for('get_distros', header_images=header_images, random_image=random_image(header_images), empty_distros=empty_distros, counter=counter, form=form,
      distros=mongo.db.distros.find(), 
      commands=mongo.db.commands.find()))
      else:
        distro_to_add = {
            'distro_name': distro,
            'distro_logo': logo
          }
        mongo.db.distros.insert_one(distro_to_add)
        flash('distro added!')
        return redirect(url_for('get_distros', header_images=header_images, random_image=random_image(header_images), empty_distros=empty_distros, counter=counter, form=form,
      distros=mongo.db.distros.find(), 
      commands=mongo.db.commands.find()))
    elif form.form_recaptcha.data == None:
      flash('Please complete reCAPTCHA!')
      return render_template('add_distro.html', form=form, error='captcha missing')

      
# EDIT COMMAND VIEW
@app.route('/edit/<command_id>', methods=['POST', 'GET'])
def edit_command(command_id):
  form = EditForm()
  commands = mongo.db.commands
  cmd_to_update = mongo.db.commands.find_one({'_id': ObjectId(command_id)})
  distros = mongo.db.distros.find()
  if request.method == 'GET':
    return render_template('edit_command.html', form = AddCommandForm(), cmd_to_update=cmd_to_update, distros=distros)
  else:
    if form.validate():
      if form.form_submit:
        commands.update({'_id': ObjectId(command_id)}, 
        {
          'app_name': form.form_name.data,
          'app_distro': request.form.get('app_distro'),
          'app_url': form.form_url.data,
          'app_instruction': form.form_instruction.data,
          'app_command': form.form_command.data
        })
        flash('Command updated', 'info')
        form=SimpleSearch()
        choices = [('','select distro')]
        for distro in mongo.db.distros.find():
          choices.append((f"{distro['distro_name']}",f"{distro['distro_name']}"))
        form.search_distro.choices = choices
        return render_template('find_command.html', form=form,
          results=mongo.db.commands.find({'_id': ObjectId(command_id)}),
          distros=mongo.db.distros.find(), commands=mongo.db.commands.find())
    else:
      flash("ReCAPTCHA missing!", "warning")
      return redirect(request.referrer)

# DELETE COMMAND VIEW
@app.route('/confirm_delete/<command_id>', methods=['POST', 'GET'])
def confirm_delete(command_id):
  form = DeleteForm()
  cmd_to_delete = mongo.db.commands.find_one({'_id': ObjectId(command_id)})
  if request.method == 'GET':
    return render_template('delete_command.html', form=form, cmd_to_delete=cmd_to_delete, results=mongo.db.commands.find({'_id': ObjectId(command_id)}),
            distros=mongo.db.distros.find(), commands=mongo.db.commands.find())
  else:
    if form.validate():
      if form.form_submit:
        mongo.db.commands.remove({'_id': ObjectId(command_id)})
        flash('Command deleted!')
        form=SimpleSearch()
        choices = [('','select distro')]
        for distro in mongo.db.distros.find():
          choices.append((f"{distro['distro_name']}",f"{distro['distro_name']}"))
        form.search_distro.choices = choices
        return render_template('find_command.html', form=form, distros=mongo.db.distros.find(), commands=mongo.db.commands.find())
    elif form.errors:
      flash('reCAPTCHA missing!', 'error')
      return render_template('delete_command.html', error=form.errors, form=form, cmd_to_delete=cmd_to_delete, results=mongo.db.commands.find({'_id': ObjectId(command_id)}),
            distros=mongo.db.distros.find(), commands=mongo.db.commands.find())

# ADD TO MY_LIST operation
@app.route('/add_to_list/<command_id>')
def add_to_list(command_id):
  cmd_to_save = mongo.db.commands.find_one({'_id': ObjectId(command_id)})
  for key in my_list.keys():
    if command_id in str(key):
      flash('already in list!', 'warning')
      return redirect(request.referrer)
  else:
    my_list[cmd_to_save['_id']] = {'id': command_id, 'app': cmd_to_save['app_name'], 'distro': cmd_to_save['app_distro'], 'url': cmd_to_save['app_url'], 'instruction': cmd_to_save['app_instruction'], 'command': cmd_to_save['app_command']}
    flash('Command added!')
    return redirect(url_for('my_list_func'))

# MY_LIST VIEW
@app.route('/my_list')
def my_list_func():
  return render_template('my_list.html', my_list=my_list)

# remove action for MY LIST VIEW
@app.route('/remove_from_list/<command_id>')
def remove_from_list(command_id):
  for key in my_list.keys():
    if str(key) == command_id:
      my_list.pop(key)
      return redirect(url_for('my_list_func'))

# EMAIL MY_LIST operation
@app.route('/send_list', methods=['GET','POST'])
def send_list():
  form = EmailForm()
  if request.method == 'GET':
    return render_template('send_list.html', form=form)
  else:
    email_body = ""
    for value in my_list.values():
        email_body += f"""
        <h3>{value['app']}</h3>
        <p><strong>Distro:</strong> {value['distro']}.
        <br>
        <strong>Download URL (if available):</strong>{value['url']}.
        <br>
        <strong>Instruction:</strong>{value['instruction']}.
        <br>
        <strong>Command:</strong>{value['command']}
        <hr>
        """
    message = Mail(
        from_email='linuxcommandgen@gmail.com',
        to_emails=form.email_address.data,
        subject="Commands from Linux Command Generator",
        html_content=email_body
      )
    try:
      sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
      response = sg.send(message)
      print(response.status_code)
      print(response.body)
      print(response.headers)
      flash('Email sent', 'success')
      return redirect(request.referrer)
    except Exception as e:
      flash(f'{e}')
      return redirect(request.referrer)
      
# RUN Flask app
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
    