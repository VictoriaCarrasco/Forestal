from flask import render_template, request, session, redirect
from arboles_app.modelos.modelo_arboles import Arboles
from arboles_app import app 

@app.route('/arboles', methods=['GET'])
def desplegas_arboles():
    lista_arboles = Arboles.obtener_todas_con_usuario()
    if "id_usuario" not in session:
        return redirect ('/')
    else:
        lista_arboles = Arboles.obtener_todas_con_usuario()
        return render_template('arboles.html', lista_arboles=lista_arboles)

@app.route('/formulario/arboles', methods=['GET'])
def desplegas_formulario_arboles():
    if "id_usuario" not in session: 
        return redirect ('/')
    else:
        return render_template ('formulario_arbol.html')

@app.route('/crear/arboles', methods=['POST'])
def nueva_arboles():
    data = {
        **request.form,
        "id_usuario": session['id_usuario']
    }
    if Arboles.validar_formulario_arboles(data) == False:
        return redirect ('/formulario/arboles')
    else:
        id_arboles = Arboles.crear_uno(data)
        return redirect ('/arboles')
    
@app.route('/eliminar/arboles/<int:id>', methods=['POST'])
def eliminar_arboles (id):
    data = {
        "id": id
    }
    Arboles.eliminar_uno(data)
    return redirect (f'/usuario/cuenta/{id}')

@app.route('/arboles/<int:id>', methods=['GET'])
def desplegar_arboles (id):
    if "id_usuario" not in session:
        return redirect ('/')
    else: 
        data = {
            "id": id
        }
        arbol = Arboles.obtener_uno_con_usuario(data)
        return render_template ('arbol.html' , arbol = arbol)

@app.route('/formulario/editar/arboles/<int:id>', methods= ['GET'])
def desplegar_editar_arboles (id): 
    if "id_usuario" not in session:
            return redirect ('/')
    else:
        data = {
            "id": id
        }
        arbol = Arboles.obtener_uno(data)
        fecha_siembra = arbol.fecha_siembra.strftime('%Y-%m-%d')
        return render_template ('editar_arbol.html', arbol = arbol , fecha_siembra=fecha_siembra)

@app.route('/editar/arboles/<int:id>', methods= ['POST'])
def editar_arboles(id):
    if Arboles.validar_formulario_arboles (request.form) == False:
        return redirect (f'/formulario/editar/arboles/{id}')  
    else: 
        data = {
            **request.form,
            "id": id
        }
        Arboles.editar_uno(data)
        return redirect (f'/usuario/cuenta/{id}')
    

@app.route('/usuario/cuenta/<int:id>', methods= ['GET'])
def desplegar_mis_arboles(id):
    if "id_usuario" not in session:
        return redirect ('/')
    else: 
        data= {
            "id": id
        }
        lista_de_arboles = Arboles.obtener_arbol_con_usuario()
        return render_template ('mis_arboles.html' , lista_de_arboles = lista_de_arboles)
