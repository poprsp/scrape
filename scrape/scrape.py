import os
import urllib.parse
import urllib.request

import bs4


def recurse(scraper: bs4.BeautifulSoup, url: str, output_dir: str) -> None:
    components = urllib.parse.urlsplit(url)

    with urllib.request.urlopen(url) as r:
        scrape = scraper(r, "html.parser")

        links = build_path(output_dir, "Links", components.path)
        with open(links, "w") as f:
            for link in scrape.links():
                f.write("{}\n".format(link))

        words = build_path(output_dir, "Words", components.path)
        with open(words, "w") as f:
            for word in scrape.words():
                f.write("{} ".format(word))


def build_path(output_dir: str, kind: str, path: str) -> str:
    basename = os.path.basename(path)
    if "." in basename:
        raise ValueError("invalid basename: {}".format(basename))

    directory = os.path.join(output_dir, kind)
    os.makedirs(directory, exist_ok=True)

    return os.path.join(directory, basename)
