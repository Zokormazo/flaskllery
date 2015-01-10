#!flask/bin/python
from app import create_app, db
from flask.ext.script import Manager, Shell, Command, Option
from flask.ext.migrate import Migrate, MigrateCommand
from app.models import User, Role, Album, Directory, Photo, ExifData
import os

if os.path.exists('.env'):
	print('Importing environment from .env...')
	for line in open('.env'):
		var = line.strip().split('=')
		if len(var) == 2:
			os.environ[var[0]] = var[1]

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role,
			Album=Album, Directory=Directory,
			Photo=Photo, ExifData=ExifData)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
	"""Run the unit tests."""
	import coverage
	cov = coverage.coverage(branch=True, include='app/*')
	cov.start()
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)
	cov.stop()
	cov.save()
	print('Coverage Summary:')
	cov.report()
	cov.erase()

def _get_pybabel():
	import sys
	if sys.platform == 'win32':
		pybabel = 'flask\\Scripts\\pybabel'
	else:
		pybabel = 'flask/bin/pybabel'
	return pybabel

BabelCommand = Manager(usage='Perform pybabel related tasks')

@BabelCommand.command
def update(babel_cfg = 'app/babel.cfg', translations_dir = 'app/translations', pot_file='app/translations/messages.pot'):
	"""Update catalogs with new texts."""
	pybabel = _get_pybabel()
	os.system(pybabel + ' extract -F ' + babel_cfg + ' -k lazy_gettext -o ' + pot_file + ' app')
	os.system(pybabel + ' update -i ' + pot_file + ' -d ' + translations_dir)

@BabelCommand.command
def compile(translations_dir = 'app/translations'):
	"""Compile the catalogs."""
	pybabel = _get_pybabel()
	os.system(pybabel + ' compile -d ' + translations_dir)

@BabelCommand.command
def init(language, translations_dir = 'app/translations', pot_file='app/translations/messages.pot'):
	"""Init new language catalogs."""
	pybabel = _get_pybabel()
	os.system(pybabel + ' init -i ' + pot_file + ' -d ' + translations_dir + ' -l ' + language)

manager.add_command('babel', BabelCommand)

if __name__ == "__main__":
	manager.run()
