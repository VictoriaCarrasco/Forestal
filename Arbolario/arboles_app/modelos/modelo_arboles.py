from arboles_app.config.mysqlconnection import connectToMySQL
from arboles_app.modelos.modelo_usuario import Usuario
from arboles_app import BASE_DATOS
from flask import flash
from datetime import datetime


class Arboles:
    def __init__(self,data):
        self.id = data['id']
        self.especies = data['especies']
        self.ubicacion = data['ubicacion']
        self.motivo = data['motivo']
        self.fecha_siembra = data['fecha_siembra']
        self.id_usuario = data['id_usuario']
        self.fecha_creacion = data['fecha_creacion']
        self.fecha_actualizacion = data['fecha_actualizacion']
        self.usuario = None

    def fecha_con_formato(self):
        fecha_formateada = self.fecha_siembra.strftime('%d-%m-%Y')
        return fecha_formateada


    @classmethod
    def crear_uno(cls,data):
        query = """
                INSERT INTO arboles ( especies , ubicacion , motivo , fecha_siembra, id_usuario)
                VALUES ( %(especies)s, %(ubicacion)s, %(motivo)s, %(fecha_siembra)s, %(id_usuario)s)
                """
        id_arboles = connectToMySQL(BASE_DATOS).query_db(query,data)
        return id_arboles

    @classmethod
    def obtener_todas_con_usuario(cls):
        query = """
                SELECT *
                FROM arboles a JOIN usuarios u
                ON a.id_usuario = u.id;
                """
        resultado = connectToMySQL(BASE_DATOS).query_db(query)
        lista_arboles = []
        for renglon in resultado:
            arbol = Arboles(renglon)
            data_usuario = {
                "id": renglon ['u.id'],
                "nombre": renglon ['nombre'],
                "apellido":renglon ['apellido'],
                "email":renglon ['email'],
                "password":renglon ['password'],
                "fecha_creacion": renglon ['u.fecha_creacion'],
                "fecha_actualizacion":renglon ['u.fecha_actualizacion']
            }
            usuario = Usuario(data_usuario)
            arbol.usuario = usuario 
            lista_arboles.append(arbol)

        return lista_arboles 
    
    @classmethod
    def eliminar_uno (cls,data):
        query = """
                DELETE FROM arboles
                WHERE id = %(id)s;
                """
        return connectToMySQL(BASE_DATOS).query_db(query,data)
    
    @classmethod
    def obtener_uno_con_usuario (cls,data):
        query = """
                SELECT *
                FROM arboles a JOIN usuarios u
                ON a.id_usuario = u.id
                WHERE a.id = %(id)s;
                """
        resultado = connectToMySQL(BASE_DATOS).query_db(query, data)
        renglon = (resultado[0])
        arbol = Arboles(renglon)
        data_usuario = {
            "id": renglon ['u.id'],
            "nombre": renglon ['nombre'],
            "apellido":renglon ['apellido'],
            "email":renglon ['email'],
            "password":renglon ['password'],
            "fecha_creacion": renglon ['u.fecha_creacion'],
            "fecha_actualizacion":renglon ['u.fecha_actualizacion']
            }
        arbol.usuario= Usuario (data_usuario)
        return arbol

    @classmethod
    def obtener_uno(cls,data):
        query = """
                SELECT *
                FROM arboles
                WHERE id = %(id)s;
                """
        resultado = connectToMySQL(BASE_DATOS).query_db(query,data)
        arbol= Arboles (resultado[0])
        return arbol
    
    @classmethod
    def editar_uno (cls, data):
        query = """
                UPDATE arboles
                SET especies = %(especies)s, ubicacion = %(ubicacion)s, motivo = %(motivo)s, fecha_siembra = %(fecha_siembra)s
                WHERE id= %(id)s;             
                """
        return connectToMySQL(BASE_DATOS).query_db( query, data)
    
    @classmethod
    def obtener_arbol_con_usuario(cls):
        query = """
                SELECT *
                FROM arboles a JOIN usuarios u
                ON a.id_usuario = u.id;
                """
        resultado = connectToMySQL(BASE_DATOS).query_db(query)
        lista_de_arboles = []
        for renglon in resultado:
            arbol = Arboles(renglon)
            data_usuario = {
                "id": renglon ['u.id'],
                "nombre": renglon ['nombre'],
                "apellido":renglon ['apellido'],
                "email":renglon ['email'],
                "password":renglon ['password'],
                "fecha_creacion": renglon ['u.fecha_creacion'],
                "fecha_actualizacion":renglon ['u.fecha_actualizacion']
            }
            usuario = Usuario(data_usuario)
            arbol.usuario = usuario 
            lista_de_arboles.append(arbol)

        return lista_de_arboles 
    
    @staticmethod
    def validar_formulario_arboles (data):
        es_valido=True
        if len(data['especies']) < 5:
            es_valido = False
            flash ("Debes proporcionar al menos 5 caracteres", "error_especies")

        if len(data['ubicacion']) < 2:
            es_valido = False
            flash ("Debes proporcionar la ubicacion del arbol, esta debe tener al menos 2 caracteres.", "error_ubicacion")

        if len(data['motivo']) > 50:
            es_valido = False
            flash ("Debes proporcionar maximo 50 caracteres", "error_motivo")


        return es_valido
