# setup.py

from setuptools import setup, find_packages

setup(
    name='cemirutils',
    version='0.2.2',
    packages=find_packages(),
    install_requires=[],
    author='Cem Emir / Muslu Yüksektepe',
    author_email='musluyuksektepe@gmail.com',
    description='Basit veri işleme yardımcıları',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/cememir/cemirutils',  # GitHub repo URL'si
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
