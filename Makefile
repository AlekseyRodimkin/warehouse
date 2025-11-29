lint:
	black .
	isort .
	pylint app/
