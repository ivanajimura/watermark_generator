create-venv:
	@python -m venv venv

activate-venv:
	@source venv/bin/activate		#needs to be typed into terminal, does not work from within Make

set_path:
	@export PYTHONPATH='/home/ivan/Documents/Watermark_generator'

req-freeze:
	@pip freeze > requirements.txt

req-install:
	@pip install -r requirements.txt

docstring_coverage:
	@docstr-coverage /home/ivan/Documents/ensolvers_challenge_note_app/Ajimura-fcf59b -e ".*/(venv|tests|alembic)" --skip-file-doc

static-check-var-types:
	@mypy backend

server-start:
	@uvicorn main:app --reload