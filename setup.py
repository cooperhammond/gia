from setuptools import setup

setup(
    name =         'gia',
    version =      '1.0.0',
    description =  'A powerful image aggregator for data science projects.',
    url =          'https://github.com/cooperhammondg/gia',
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
