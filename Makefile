.PHONY: clean-pyc

init:
	conda env create --file ml4t_conda.yml

clean:
	rm -rf `find . -name __pycache__ -type d`
	find . -name '*~' -exec rm --force {} +

