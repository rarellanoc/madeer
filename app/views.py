#FLASK
from flask import abort, render_template, Response, flash, redirect, session
from flask import url_for, g, request, send_from_directory
#FLASK EXTENSIONS
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import get_debug_queries
from flask.ext.mail import Mail
#LOCAL
from models import User, ROLE_USER, ROLE_ADMIN ,Metaindex, ListaUsuarios, ListaClientes
from forms import LoginForm
from forms import NewPass, ForgotPasswordForm, InscripcionUserForm, RegistrationForm
from email import user_notification, forgot_password
from config import DATABASE_QUERY_TIMEOUT
from app import app, db, lm, mail, models
from decorators import admin_required
#OTHER
from  datetime import date, timedelta
import uuid

from flask import make_response



		


@app.route('/crear_cuenta/' , methods=['GET','POST'])
def create_acct():
	meta = Metaindex.query.order_by(Metaindex.id.desc()).first()
	form = RegistrationForm(request.form)
	if form.validate_on_submit():

			
		user = User(email=form.email.data, password=form.password.data,
				oldPassword=form.password.data, userid=(str(uuid.uuid1())))
		db.session.add(user)
		db.session.commit()
		login_user(user)
		#user_notification(user)
		
		mailuser = form.email.data
		nusuario = mailuser.split('@')[0]
			
		return render_template ("dashboard.html", title="Panel", sector = sec, autor=aut, nusuario = nusuario, meta=meta)
	return render_template('create_acct.html', title = "Create Account", form=form, meta=meta)

@app.route('/nueva_clave/' , methods=['GET','POST'])
def new_pass():
	form = NewPass(request.form)
	meta = Metaindex.query.order_by(Metaindex.id.desc()).first()
	if form.validate_on_submit():
		user = g.user
		print form.data
		if user.password == form.data['password']:
				print 'I should raise a validation error'
				form.password.errors.append('You\'ve already used this password. Please choose a new password.')
		else:
				print 'user picked a different password'
				user.password = form.password.data
				user.changedPass = True
				db.session.commit()
				return redirect(url_for('index'))

	return render_template('new_pass.html', title='Update Password', form=form, meta=meta)

@app.route('/ingreso/',methods=['GET','POST'])
def login():
	meta = Metaindex.query.order_by(Metaindex.id.desc()).first()
	form = LoginForm(request.form)
	if form.validate_on_submit():
		user = form.get_user()
		login_user(user)
		user = g.user
		if current_user.is_admin():
			return redirect(url_for('admin2'))
		
		else:
			return redirect(request.args.get("next") or url_for("dashboard"))
	return render_template('login.html', title="Login", form=form, meta=meta)

@app.route('/olvido_clave/', methods=['GET', 'POST'])
def forgot_passwd():

	meta = Metaindex.query.order_by(Metaindex.id.desc()).first()
	form = ForgotPasswordForm(request.form)
	if form.validate_on_submit():
		user = request.form['email']
		if User.query.filter_by(email=user).first():
			q = User.query.filter_by(email=user).first()
			forgot_password(user, q.password)
			return redirect(request.args.get("next") or url_for("login"))
		else:
			flash('Usuario no enconstrado')
			return redirect(request.args.get("next") or url_for("login"))
	return render_template ("forgot_passwd.html",
		title="Recuperacion de contrase&ntide;a",
		form=form)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

	meta = Metaindex.query.order_by(Metaindex.id.desc()).first()



	form = InscripcionUserForm(request.form)
	if form.validate_on_submit():

		listausuarios = ListaUsuarios()
		form.populate_obj(listausuarios)
		db.session.add(listausuarios)
		db.session.commit()

		return redirect(url_for('gracias'))



		
	return render_template ("index.html", title="Home", form=form ,meta=meta)



@app.route('/panel/')
def dashboard():
	meta = Metaindex.query.order_by(Metaindex.id.desc()).first()

	if current_user.is_authenticated():
		g.user = current_user
		mailuser = User.query.filter_by(userid=g.user.userid).first().email
		surv1 = Survey1.query.filter_by(nuevouser1=mailuser).first()

		nusuario = mailuser.split('@')[0]

		if surv1 != None: 
			return render_template ("dashboard.html", title="Panel", sector = surv1.sector, autor=surv1.autor, nusuario = nusuario, meta=meta)
		else:
			return render_template ("dashboard.html", title="Panel", sector = '', autor='', meta=meta)

	else:
		return render_template ("dashboard.html", title="Panel", sector ='', autor='', meta=meta)

		

@app.route('/gracias/')
def gracias():
	meta = Metaindex.query.order_by(Metaindex.id.desc()).first()
	return render_template ("dashboard.html", title="Home", meta=meta)


@app.route('/informacion/')

def consent():
	meta = Metaindex.query.order_by(Metaindex.id.desc()).first()
	return render_template('consent.html', title = "Acuerdo", meta=meta)

@app.route('/propuesta/')

def propuesta():
	meta = Metaindex.query.order_by(Metaindex.id.desc()).first()
	return render_template('propuesta.html', title = "Propuesta", meta=meta)

@app.route('/logouthtml/')

def logouthtml():
	meta = Metaindex.query.order_by(Metaindex.id.desc()).first()
	return render_template('logout.html', title="Logout", meta=meta)

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user

@app.route('/salir')
def logout():
	logout_user()
	#return redirect(url_for('index'))

	resp = make_response(redirect(url_for('index')))
    	resp.set_cookie('autor', '', expires=0)
	resp.set_cookie('sector', '', expires=0)
	resp.set_cookie('uid', '', expires=0)
    	return resp

@app.errorhandler(404)
def internal_error(error):
	meta = Metaindex.query.order_by(Metaindex.id.desc()).first()
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.after_request
def after_request(response):
	for query in get_debug_queries():
		if query.duration >= DATABASE_QUERY_TIMEOUT:
			app.logger.warning("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" % (query.statement, query.parameters, query.duration, query.context))
	return response

def flash_errors(form):
	for field, errors in form.errors.items():
		for error in errors:
			flash(u"Error in the %s field - %s" % (
			getattr(form, field).label.text,error
		))


@app.route('/admin2')
@login_required
@admin_required
def admin2():
	meta = Metaindex.query.order_by(Metaindex.id.desc()).first()
	users = User.query.filter_by(role=0)
	return render_template('admin2/index.html', title="Admin", users=users, meta=meta)

@app.route('/admin_survey1/')
@login_required
@admin_required
def admin_survey1():
	meta = Metaindex.query.order_by(Metaindex.id.desc()).first()
	surveys = Survey1.query.all()
	return render_template('admin2/partials/survey1.html', title='Admin Survey-1', surveys=surveys, meta=meta)

@app.route('/admin_survey2/')
@login_required
@admin_required
def admin_survey2():
	meta = Metaindex.query.order_by(Metaindex.id.desc()).first()
	surveys = Survey2.query.all()
	return render_template('admin2/partials/survey2.html', title='Admin Survey-2', surveys=surveys, meta=meta)

@app.route('/admin_survey3/')
@login_required
@admin_required
def admin_survey3():
	meta = Metaindex.query.order_by(Metaindex.id.desc()).first()
	surveys = Survey3.query.all()
	return render_template('admin2/partials/survey3.html', title='Admin Survey-3', surveys=surveys, meta=meta)

@app.route('/admin_survey4/')
@login_required
@admin_required
def admin_survey4():
	meta = Metaindex.query.order_by(Metaindex.id.desc()).first()
	surveys = Survey4.query.all()
	return render_template('admin2/partials/survey4.html', title='Admin Survey-4', surveys=surveys, meta=meta)


@app.route('/admin_meta/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_metaedit():
	meta = Metaindex.query.order_by(Metaindex.id.desc()).first()

	form = MetaForm(request.form)

	if form.validate_on_submit():

		metaindex = Metaindex()
		form.populate_obj(metaindex)
		db.session.add(metaindex)
		db.session.commit()

		return redirect(url_for('admin'))
	
	
	return render_template('admin2/metaedit.html', title='Edit Index' , form=form, meta=meta)




