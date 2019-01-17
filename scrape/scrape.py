import os
import queue
import threading
import urllib.parse
import urllib.request

import bs4


class Scrape:
    def __init__(self,
                 scraper: bs4.BeautifulSoup,
                 output_dir: str,
                 pages: int,
                 threads: int) -> None:
        self.scraper = scraper
        self.output_dir = output_dir
        self.pages = pages
        self.threads = threads

        self.scraped = []  # type: List[str]
        self.queue = queue.Queue()  # type: queue.Queue
        self.lock = threading.Lock()

    def scrape(self, url: str) -> None:
        self.queue.put(url)

        threads = []
        for _ in range(self.threads):
            thread = threading.Thread(target=self.worker)
            thread.start()
            threads.append(thread)

        self.queue.join()
        for _ in range(self.threads):
            self.queue.put(None)

        for thread in threads:
            thread.join()

    def worker(self) -> None:
        while True:
            url = self.queue.get()
            if not url:
                break
            components = urllib.parse.urlsplit(url)

            print("{}: scraping {}".format(threading.get_ident(), url))
            with urllib.request.urlopen(url) as r:
                scrape = self.scraper(r, "html.parser")

                links = self.build_path("Links", components.path)
                with open(links, "w") as f:
                    for link in scrape.links():
                        f.write("{}\n".format(link))
                        with self.lock:
                            if self.pages > 0 and link not in self.scraped:
                                self.queue.put(self.build_url(
                                    components.scheme,
                                    components.netloc,
                                    link
                                ))
                                self.pages -= 1
                                self.scraped.append(link)

                words = self.build_path("Words", components.path)
                with open(words, "w") as f:
                    for word in scrape.words():
                        f.write("{} ".format(word))

            self.queue.task_done()

    def build_path(self, kind: str, path: str) -> str:
        basename = os.path.basename(path)
        if ".." in basename:
            raise ValueError("invalid basename: {}".format(basename))

        directory = os.path.join(self.output_dir, kind)
        os.makedirs(directory, exist_ok=True)

        return os.path.join(directory, basename)

    @staticmethod
    def build_url(scheme: str, netloc: str, path: str) -> str:
        return "{}://{}/{}".format(scheme, netloc, path.lstrip("/"))
