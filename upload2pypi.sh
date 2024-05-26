python -m pip install -U pip setuptools twine


python setup.py sdist bdist_wheel

#python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

python -m twine upload dist/*


python -m pip install -U cemirutils

