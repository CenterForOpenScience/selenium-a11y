flake:
	flake8

black:
	black -S api base components markers.py pages settings.py tests utils.py

isort:
	isort .

lintall: black isort flake
