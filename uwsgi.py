from app import create_app, db

import os
if os.path.exists('.env'):
	print('Importing environment from .env...')
	for line in open('.env'):
		var = line.strip().split('=')
		if len(var) == 2:
			os.environ[var[0]] = var[1]
			os.putenv(var[0], var[1])

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
