from flask import render_template, request, session, redirect, flash
from arboles_app.modelos.modelo_usuario import Usuario
from arboles_app import app 
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt (app)

@app.route('/', methods=['GET'])
def desplegar_login_registro():
    return render_template ('login_registro.html')

@app.route('/crear/usuario', methods=['POST'])
def nuevo_usuario():
    data ={
        **request.form 
    }
    usuario_existe = Usuario.obtener_uno_con_email(data)
    if Usuario.validar_registro(data, usuario_existe) == False:
        return redirect ('/')
    else:
        password_escriptado = bcrypt.generate_password_hash(data['password'])
        data ['password'] = password_escriptado
        id_usuario = Usuario.crear_uno(data)     
        session ['nombre'] = data ['nombre']    
        session['apellido'] = data ['apellido']
        session ['id_usuario'] = id_usuario

        return redirect ("/arboles")
    
#Redireccionar al home
@app.route('/login', methods=['POST'])
def procesa_login():
    data = {
        "email": request.form ['email_login']
    }
    usuario_existe = Usuario.obtener_uno_con_email (data)
    if usuario_existe == None:
        flash("Este usuario no existe.", "error_email_login")
        return redirect ('/')
    else: 
        if not bcrypt.check_password_hash(usuario_existe.password, request.form['password_login']): 
            flash("Credenciales incorrectas.", "error_password_login")
            return redirect ('/')
        else: 
            session ['nombre'] = usuario_existe.nombre
            session['apellido'] = usuario_existe.apellido
            session ['id_usuario'] = usuario_existe.id
            return redirect ('/arboles')

@app.route('/logout', methods = ['POST'])
def procesa_logout():
    session.clear()
    return redirect ('/')