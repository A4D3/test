run:
	FLASK_ENV=development FLASK_APP=flask_engine.py flask run
clear:
	rm -r app/__pycache__
	rm -r __pycache__
