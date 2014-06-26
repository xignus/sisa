 # -*- coding: utf-8 -*-

@auth.requires_login()
def certificados():

    cliente=db(db.clientes.id==request.args(1)).select()
    lugar=db(db.establecimientos.id==request.args(0)).select()
    response.subtitle+=" Certificados del cliente "+cliente[0].nombre.capitalize()+" "+cliente[0].apellido.capitalize()+" /  "+lugar[0].nombre
    certificados=db(db.certificados.establecimiento==request.args(0)).select()

    db.certificados.establecimiento.default=request.args(0)
    db.certificados.establecimiento.writable=False
    db.certificados.establecimiento.readable=False
    db.certificados.numero.requires=IS_NOT_IN_DB(db, 'certificados.numero')
    db.adicionales.certificado.readable=False
    db.adicionales.certificado.writable=False
    
    nCertificado=SQLFORM(db.certificados)

    if nCertificado.process().accepted:
        db.cobros.insert(certificado=nCertificado.vars.id, importe=0.0, pagado=0.0)
        db.adicionales.insert(certificado=nCertificado.vars.id)
        redirect(URL('consultas', 'certificados', args=(request.args(0), request.args(1))))
        session.flash='El certificado ha sido agregado'
        
    elif nCertificado.errors:
        response.flash='El certificado tiene errores'
        
    return dict(certificados=certificados, nCertificado=nCertificado)

@auth.requires_login()
def cobros():
    cliente=db(db.clientes.id==request.args(0)).select()
    response.subtitle+=" Cobros al cliente "+cliente[0].nombre.capitalize()+" "+cliente[0].apellido.capitalize()
    cobros=db((db.certificados.establecimiento==db.establecimientos.id)&(db.cobros.certificado==db.certificados.id)&(db.establecimientos.cliente==request.args(0))).select()

    return dict(cobros=cobros)
    
@auth.requires_login()
def establecimientos():

    cliente=db(db.clientes.id==request.args(0)).select()
    response.subtitle+=" Establecimientos del cliente "+cliente[0].nombre.capitalize()+" "+cliente[0].apellido.capitalize()

    db.establecimientos.cliente.default=request.args(0)
    db.establecimientos.cliente.writable=False
    db.establecimientos.cliente.readable=False
    
    sucursales=db(db.establecimientos.cliente==request.args(0)).select()
    
    nSucursal=SQLFORM(db.establecimientos)

    if nSucursal.process().accepted:
        redirect(URL('consultas','establecimientos', args=(request.args(0))))
        session.flash='Se ha registrado el nuevo establecimiento'
    elif nSucursal.errors:
        response.flash='Por favor, revise los datos ingresados'
    
    return dict(nSucursal=nSucursal, sucursales=sucursales)

@auth.requires_login()
def imprimircertificado():
    certificado=db((db.certificados.id==request.args(0))&(db.adicionales.certificado==db.certificados.id)&(db.certificados.establecimiento==db.establecimientos.id)&(db.clientes.id==db.establecimientos.cliente)).select()
    return dict(certificado=certificado)

def actualizarCobro():
    response.subtitle+='Actualizar cupon de pago'
    db.cobros.id.readable=False
    db.cobros.certificado.writable=False
    cupon=SQLFORM(db.cobros, request.args(0))
    cupon.add_button("Cancelar",URL('consultas','cobros', args=(request.args(1))))
    if cupon.process().accepted:
        redirect(URL('consultas','cobros', args=(request.args(1))))
        session.flash='Se ha actualizado el cupon'
    elif cupon.errors:
        response.flash='Por favor verifique los datos'
        
    return dict(cupon=cupon)
