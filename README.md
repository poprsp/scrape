# Installation

- Assignment 3 = search
- Project = scrape

```sh
$ git clone https://github.com/poprsp/search
$ pip3 install -r search/requirements.txt --user
$ git clone https://github.com/poprsp/scrape
$ pip3 install -r scrape/requirements.txt --user
```


# Run

First remove any old output directory:

```sh
$ cd search
$ rm -rf data
$ ../scrape/app.py --output-dir data/wikipedia https://en.wikipedia.org/wiki/Game_Programming
$ ./app.py
```
