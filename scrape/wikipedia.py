import re
import string
from typing import Iterator

import bs4


# pylint: disable=W0223
class Wikipedia(bs4.BeautifulSoup):  # type: ignore
    # This is far from perfect.  Among others, 'string.punctuation'
    # contain the characters ',' and '.'.  This means that 'word,',
    # 'word.', and 'word' are treated as the same word (which is good),
    # but it also means that 2.15 is split into two elements.
    word_sep = re.compile(r"[\s{}]".format(string.punctuation))

    def links(self) -> Iterator[str]:
        """
        Yield all /wiki/ links for the current page.
        """
        for a in self.find_all("a"):
            href = a.get("href")
            if href and href.startswith("/wiki/") and ":" not in href:
                yield re.sub("#.*", "", href)

    def words(self) -> Iterator[str]:
        """
        Yeild all words for the current page.

        The content of an article may be wrapped in any number of
        attributes, which makes it difficult to grab all text in a clean
        manner.

        This is quite a crude implementation that grabs all text inside
        #bodyContent and splits on a somewhat fragile regex.
        """

        content = self.find(id="bodyContent")
        for word in re.split(self.word_sep, content.get_text()):
            if word != "":
                yield word.lower()
# pylint: enable=W0223
