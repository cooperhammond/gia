# gia: General Image Aggregator

[![](https://img.shields.io/github/languages/code-size/cooperhammond/gia?color=green&style=flat-square)](https://saythanks.io/to/kepoorh%40gmail.com)
[![](https://img.shields.io/pypi/v/gia?color=blue&style=flat-square)](https://saythanks.io/to/kepoorh%40gmail.com)
[![](https://img.shields.io/badge/say-thanks-ff69b4?style=flat-square)](https://saythanks.io/to/kepoorh%40gmail.com)

> 🤖📷 A powerful image aggregator for data science projects

This is a CLI tool and/or library for automating/standardizing what images you download for a data science project.


## Installation

First, download the `chromedriver` binary [here](https://chromedriver.chromium.org/downloads), 
and point the environment variable `CHROME_DRIVER_LOC` to it.

### Pip
```bash
pip install gia
```

### From source
```bash
git clone https://github.com/cooperhammond/gia
cd gia
sudo python setup.py install
```


## Usage

### CLI Usage

```
usage: gia [-h] [--depth DEPTH] destination classes queries 

positional arguments:
  destination               ABSOLUTE path for where your images should be
                            downloaded
  classes                   a python list in a string of the classes for the        
                            queries
  queries                   a python list of lists in a string of the queries       
                            corresponding to each class

optional arguments:
  -h, --help                show this help message and exit
  --depth DEPTH, -d DEPTH   the default depth to go through queries for images 
```

The "depth" of a query literally indicates how far down the Google results page the scraper will scroll.
With a depth of 0, there will be no scrolling, a depth of 1 indicates that the `end` key will be passed
twice, a depth of two means two `end` presses, and so on. Each increment of depth means means 80 images will 
be downloaded from that query, but the exact number varies depending on Google's mood and your browser's cache. 
It's meant to be a general indicator of how much to weight queries.

The destination needs to be an _absolute_ path because it is being plugged into chromedriver as the default
download folder and chromedriver has no memory of the location it was spawned from.

Queries are plugged directly into the Google search bar, so you can use all of the fancy tricks you normally
can do with it.

Example usage:
```bash
$ gia ~/dev/data "['jeff bezos', 'bill gates']" "[['jeff bezos', 'jeff bezos face'], ['bill gates', 'bill gates face']]"
```
Output:
```bash
~/dev/data
+-- _jeff bezos
    +-- 00000.jpg
    +-- 00001.jpg
    +-- ...
+-- _bill gates
    +-- 00000.jpg
    +-- 00001.jpg
    +-- ...
+-- jeff bezos.csv
+-- bill gates.csv
```

By default there depth is 0, so there is no scroll, but the `--depth` parameter can set the default depth for every query.
If you don't want a query weighted so heavily, you can be more specific:
```
[[..., 'pepperoni pizza', ...], ...] => [[..., ['pepperoni', 5], ...]]
```

Example usage:
```bash
$ gia ~/dev/data --depth 3 "['pizza']" "[['pineapple pizza', 'pepperoni pizza', 'egg pizza']]"
```
Output:
```bash
~/dev/data
+-- _pizza # will have a much larger amount of images compared to above example
    +-- 00000.jpg
    +-- 00001.jpg
    +-- ...
+-- pizza.csv
```

### Module Usage

Everything that applies for the CLI applies to the library as well.
```python
from gia import ImageAggregator

destination = '~/dev/cool-data-science-project/data'
classes = ['steve jobs', 'jack black']
queries = [
    ["steve jobs' face", ['"steve jobs" -jack -black', 5]],
    ["jack black's face", ['"jack black" -steve -jobs', 4]],
]
depth = 2

ia = ImageAggregator(destination, classes, queries, default_depth=depth)
ia.aggregate()
```