#!/usr/bin/env python3

import argparse
import sys

from scrape.scrape import Scrape
from scrape.wikipedia import Wikipedia


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--output-dir", required=True)
    p.add_argument("--pages", default=200, type=int)
    p.add_argument("--threads", default=16, type=int)
    p.add_argument("start_url")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    s = Scrape(Wikipedia, args.output_dir, args.pages, args.threads)
    s.scrape(args.start_url)
    return 0


if __name__ == "__main__":
    sys.exit(main())
