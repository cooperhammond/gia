from setuptools import setup

setup(
    name =         'ia',
    version =      '1.0.0',
    description =  'A powerful image aggregator for data science projects.',
    url =          'https://github.com/cooperhammond/ia',
    author =       'Cooper Hammond',
    author_email = 'kepoorh@gmail.com',
    license =      'GPL',
    packages = ['ia'],
    install_requires = [
        'selenium'
    ],
    entry_points = {
        'console_scripts': ['ia = ia.cli:main'],
    },
)
