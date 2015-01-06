#!flask/bin/python
from app import create_app, db
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
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

if __name__ == "__main__":
	manager.run()
