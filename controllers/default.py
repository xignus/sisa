# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

@auth.requires_login()
def index():
    return dict()

@auth.requires_login()
def clientes():
    response.subtitle+=' Clientes'
    clientes=db(db.clientes.id>0).select()
    nCliente=SQLFORM(db.clientes)

    if nCliente.process().accepted:
        redirect(URL('default','clientes'))
    elif nCliente.errors:
        response.flash='Por favor, revise los datos ingresados'

    return dict(clientes=clientes, nCliente=nCliente)

@auth.requires_login()
def fumigadores():
    response.subtitle+=' Fumigadores'
    fumigadores=db(db.fumigadores.id>0).select()

    nFumigador=SQLFORM(db.fumigadores)

    if nFumigador.process().accepted:
        redirect(URL('default','fumigadores'))
    elif nFumigador.errors:
        response.flash='Por favor revise los datos ingresados'
    
    return dict(fumigadores=fumigadores, nFumigador=nFumigador)

@auth.requires_login()
def cobros():
    response.subtitle+= ' Cobros pendientes'
    cobros=db((db.cobros.id>0)&(db.cobros.certificado==db.certificados.id)&(db.establecimientos.cliente==db.clientes.id)&(db.establecimientos.id==db.certificados.establecimiento)).select()
    return dict(cobros=cobros)

@auth.requires_login()
def vencimientos():
    establecimientos=db((db.establecimientos.id>0)&(db.clientes.id==db.establecimientos.cliente)).select()
    return dict(establecimientos=establecimientos)
    
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
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
