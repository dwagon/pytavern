VENVDIR = ~/.venvs
PROJECT = pypub
PROJDIR = $(VENVDIR)/$(PROJECT)

all: venv

venv:
	python3 -m venv $(PROJDIR)
	$(PROJDIR)/bin/pip install -U -r requirements-dev.txt
	$(PROJDIR)/bin/pip install -U -r requirements.txt

clean:
	/bin/rm -r $(PROJDIR)

