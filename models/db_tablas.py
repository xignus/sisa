#-*- coding: utf-8 -*-
import datetime

db.define_table('clientes',
                Field('nombre'),
                Field('apellido'),
                Field('domicilio'),
                Field('telefono','integer'),
                format='%(nombre)s %(apellido)s'
)

db.clientes.nombre.requires=IS_NOT_EMPTY()
db.clientes.apellido.requires=IS_NOT_EMPTY()
db.clientes.domicilio.requires=IS_NOT_EMPTY()

db.define_table('establecimientos',
                Field('nombre'),
                Field('cliente',db.clientes),
                Field('domicilio'),
                Field('localidad'),
                Field('telefono','integer'),
                Field('rubro'),
                Field('superficie', 'float', comment='Expresado en M2'),
                format='%(nombre)s'
)

db.establecimientos.nombre.requires=IS_NOT_EMPTY()
db.establecimientos.domicilio.requires=IS_NOT_EMPTY()
db.establecimientos.localidad.requires=IS_NOT_EMPTY()
db.establecimientos.superficie.requires=IS_NOT_EMPTY()
db.establecimientos.rubro.requires=IS_IN_SET(['Comercial', 'Particular', 'Industrial', 'Educacional', 'Estatal'])

db.define_table('fumigadores',
                Field('nombre'),
                Field('apellido'),
                Field('domicilio'),
                Field('telefono','integer'),
                Field('foto'),
                format='%(nombre)s %(apellido)s'
)

db.fumigadores.nombre.requires=IS_NOT_EMPTY()
db.fumigadores.apellido.requires=IS_NOT_EMPTY()
db.fumigadores.domicilio.requires=IS_NOT_EMPTY()
db.fumigadores.telefono.requires=IS_NOT_EMPTY()

db.define_table('certificados',
                Field('numero', label='Certificado número'),
                Field('establecimiento', db.establecimientos),
                Field('tratamiento'),
                Field('vectTrat',label='Vect. Trat.'),
                Field('drogaUsada', label='Droga usada'),
                Field('venenoClase', label='Clase de veneno'),
                Field('fFumigacion','date', default=request.now, label='Fecha de fumigacion'),
                Field('hora','time', default=datetime.datetime.now().time()),
                Field('fVencimiento','date',label='Fecha de vencimiento'),
                Field('fumigador',db.fumigadores),
                format='%(numero)s'
)

db.certificados.tratamiento.requires=IS_IN_SET(['Aspersión', 'Humo', 'Niebla', 'Otro'], multiple=True)
db.certificados.vectTrat.requires=IS_IN_SET(['Insectos', 'Roedores', 'Voladores', 'Bacterias'], multiple=True)
db.certificados.vectTrat.comment='Mantenga Ctrl presionado para seleccionar mas de un item'
db.certificados.tratamiento.comment='Mantenga Ctrl presionado para seleccionar mas de un item'
db.certificados.drogaUsada.requires=IS_IN_SET(['Piretroydes', 'Bromadilone', 'Otra'])
db.certificados.venenoClase.requires=IS_IN_SET(['A','B','C'])

db.define_table('adicionales',
                Field('certificado',db.certificados),
                Field('antidoto','text'),
                Field('recomendaciones','text'),
                Field('observaciones','text')
)


db.define_table('cobros',
                Field('certificado',db.certificados),
                Field('importe', 'float'),
                Field('pagado','float'),
                Field('pago', 'double')
)
