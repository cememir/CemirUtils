
pip install twine setuptools


python setup.py sdist bdist_wheel

twine upload --repository-url https://test.pypi.org/legacy/ dist/*

twine upload dist/*


pip install cemirutils

