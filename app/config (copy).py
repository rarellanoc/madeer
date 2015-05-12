import os
basedir = os.path.abspath(os.path.dirname(__file__))
script_dir = os.path.dirname(__file__)
CSRF_ENABLED = True
SECRET_KEY = 'xcvBy5aDdDE9lL2CtcPuDwtd6m0VRg9W'
if os.environ.get('DATABASE_URL') is None:
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
	SQLALCHEMY_RECORD_QUERIES = True
	DATABASE_QUERY_TIMEOUT = 0.5

DATABASE_QUERY_TIMEOUT = 0.5


ADMINS = ['ECITResearch@gmail.com']
