from mixins import CRUDMixin
from flask.ext.login import UserMixin
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref

from app import db



ROLE_USER = 0
ROLE_ADMIN = 1


class User(UserMixin, CRUDMixin,  db.Model):
    id = db.Column(db.Integer, primary_key = True, unique=True)
    userid = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(20))
    oldPassword = db.Column(db.String(20))
    changedPass = db.Column(db.Boolean)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    lastSeen = db.Column(db.String(255))
    nuevouser0 = db.Column(db.String(100))

    def __init__(self, email=None, userid=None, password=None, oldPassword = None, changedPass=False,
        role=None, nuevouser0 = None):
        self.email = email
        self.userid = userid
        self.password = password
        self.oldPassword = oldPassword
        self.changedPass = changedPass

        self.role=role	
	self.nuevouser0 = nuevouser0

    def is_admin(self):
        if self.role == 1:
            return True
        else:
            return False

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.email)



class ListaUsuarios(db.Model):
	id = db.Column(db.Integer, primary_key = True)
 	email = db.Column(db.String(255), unique=True)
	joinedDate =db.Column(db.String(255))
	joined =db.Column(db.String(10))

	def __init__(self, email=None, joinedDate=None, joined=False):

		self.email = email
		self.joinedDate = joinedDate
		self.joined = joined

	def get_id(self):
        	return unicode(self.id)



class ListaClientes(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nombre = db.Column(db.String(100))
 	email = db.Column(db.String(255), unique=True)
	fono = db.Column(db.String(60))
	joinedDate =db.Column(db.String(255))
	joined =db.Column(db.String(10))

	def __init__(self, nombre=None, email=None, fono=None, joined=False):


		self.nombre = nombre
		self.email = email
		self.fono = fono
		self.joinedDate = joinedDate
		self.joined = joined

	def get_id(self):
        	return unicode(self.id)





class Metaindex(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	navbar = db.Column(db.String(50)) 
	titulo = db.Column(db.String(254)) 
	subtitulo = db.Column(db.String(254)) 
	motd = db.Column(db.String(254)) 
	fecha_motd = db.Column(db.String(50))

	def __init__(self, navbar='NavBar', titulo='Titulo', subtitulo='Subtitulo con contenido', motd='Noticia', fecha_motd='4 abr 2015'):

		self.navbar = navbar
		self.titulo = titulo
		self.subtitulo = subtitulo
		self.motd = motd
		self.fecha_motd = fecha_motd

	def get_id(self):
        	return unicode(self.id)
	
