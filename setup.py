# setup.py

from setuptools import setup, find_packages

setup(
    name='cemirutils',
    version='2.1.0',
    packages=find_packages(),
    install_requires=[],
    author='Cem Emir Yüksektepe / Muslu Yüksektepe (musluyuksektepe@gmail.com)',
    author_email='cememir2017@gmail.com',
    description='Pythona yeni başlayanlar ve zaten kullananların yaptıkları işlerde vakit kazanmasını sağlayacak kütühane ve dekoratörler işlevlerini içeren bir Python yardımcı kütüphanesidir.',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/cememir/cemirutils',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
