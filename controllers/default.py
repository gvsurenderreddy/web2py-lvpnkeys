# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

import os
APP_DIR = 'applications/%s/' % request.application
STATIC_DIR = APP_DIR + 'static/'
HOSTS_DIR = APP_DIR + 'hosts/'

def mkhosts():
	""" Crea un fichero con la llave por cada usuario y lo empaqueta"""
	os.system('mkdir -p %s' % HOSTS_DIR)
	users = db(db.auth_user.id>0).select()
	for user in users:
		f = open(HOSTS_DIR + user.username, 'w')
		f.write(user.llave+'\n')
		f.close()
	os.system('tar -C %s -czf %shosts.tar.gz hosts/' % (APP_DIR, STATIC_DIR))
	_next = request.vars._next or URL('index')
	redirect(_next)

def index():
	nodos = db(db.auth_user.id>0).select()
	return dict(nodos=nodos)

def key():
	response.headers['Content-Type'] = 'text/plain; charset=utf-8'
	username = request.args(0)
	if not username:
		return T('Indique el usuario')
	user = db(db.auth_user.username==username).select()
	if not user:
		raise HTTP(404)
	user = user[0]
	return user.llave

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    form = auth()
    return dict(form=form)


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
