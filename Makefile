.PHONY: setup clean

all: setup run test clean

PYTHON = python3
PIP = pip3

setup:
	conda env update -f environment.yml

test:
	$(PYTEST) tests/

clean:
	rm -rf __pycache__
	rm -rf **/*.log

learn: semi-supervised supervised unsupervised

supervised: classification regression
	
regression:

classification: binary | multiclass

binary: pseudolabeling
	PYTHONPATH=. python scripts/model_class_bin.py

multiclass:
	PYTHONPATH=. python scripts/model_class_mult.py
	
semi-supervised: self-training

unsupervised: clustering ... ... ...?

self-training:
	PYTHONPATH=. python scripts/model_pseudo_label.py








