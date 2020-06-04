from setuptools import setup

setup(
    name =         'gia',
    version =      '1.0.1',
    description =  'A powerful image aggregator for data science projects.',
    url =          'https://github.com/cooperhammond/gia',
    author =       'Cooper Hammond',
    author_email = 'kepoorh@gmail.com',
    license =      'GPL',
    packages = ['gia'],
    install_requires = [
        'selenium'
    ],
    entry_points = {
        'console_scripts': ['gia = gia.cli:main'],
    },
)
