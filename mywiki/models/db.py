# -*- coding: utf-8 -*-

from gluon.tools import Auth, Service, PluginManager
#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################
db = DAL('sqlite://storage.sqlite')
from gluon.tools import *

auth = Auth(db)
service = Service()
plugins = PluginManager()
db.define_table(
    auth.settings.table_user_name,
    Field('first_name', length=128, default=''),
    Field('last_name', length=128, default=''),
    Field('username',length=128,default='',unique=True),
    Field('email', length=128, default='', unique=True),
    Field('password', 'password', length=512,
        readable=False, label='Password'),
    Field('registration_key', length=512,
        writable=False, readable=False, default=''),
    Field('reset_password_key', length=512,
        writable=False, readable=False, default=''),
    Field('registration_id', length=512,
        writable=False, readable=False, default=''))

custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.first_name.requires =\
    IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.last_name.requires =\
    IS_NOT_EMPTY(error_message=auth.messages.is_empty)
custom_auth_table.password.requires = [IS_STRONG(min=8,upper=2,special=2), CRYPT()]
custom_auth_table.email.requires = [
    IS_EMAIL(error_message=auth.messages.invalid_email),
    IS_NOT_IN_DB(db, custom_auth_table.email)]
custom_auth_table.username.requires =IS_NOT_IN_DB(db, custom_auth_table.username)
auth.settings.table_user = custom_auth_table


## create all tables needed by auth if not custom tables
auth.define_tables(username=True,signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

auth.define_tables()
crud = Crud(db)

db.define_table('page',
Field('author'),
Field('recipe_name'),
Field('description', 'text'),
Field('full_recipe', 'text'),
Field('likes','integer',default=0),
Field('created_on', 'datetime', default=request.now),
Field('created_by', 'reference auth_user', default=auth.user_id),
Field('image','upload'))
db.define_table('post',
Field('page_id', 'reference page'),
Field('comment', 'text'),
Field('created_on', 'datetime', default=request.now),
Field('created_by', 'reference auth_user', default=auth.user_id))
db.page.author.requires = IS_NOT_EMPTY()
db.page.image.requires = IS_NOT_EMPTY()
db.page.recipe_name.requires = IS_NOT_IN_DB(db, 'page.recipe_name')
db.page.full_recipe.requires = IS_NOT_EMPTY()
db.page.description.requires = IS_NOT_EMPTY()
db.page.created_by.readable = db.page.created_by.writable = False
db.page.created_on.readable = db.page.created_on.writable = False
db.page.id.readable=False
db.page.image.requires = IS_NOT_EMPTY()
db.page.image.requires=IS_IMAGE(extensions=('bmp', 'gif', 'jpeg', 'png'), maxsize=(10000, 10000), minsize=(0, 0), error_message='invalid image!')
db.post.comment.requires = IS_NOT_EMPTY()
db.post.page_id.readable = db.post.page_id.writable = False
db.post.created_by.readable = db.post.created_by.writable = False
db.post.created_on.readable = db.post.created_on.writable = False
db.page.likes.readable = db.page.likes.writable = False
'''db.page.email.readable =True
db.page.email.writable =False'''
db.define_table('likes',
    Field('Username','text', readable=False, writable=False),
    Field('Dish', 'text', readable=False, writable=False))
