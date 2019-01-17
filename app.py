#!/usr/bin/env python3

import argparse
import sys

from scrape.scrape import recurse
from scrape.wikipedia import Wikipedia


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--pages", default=200, type=int)
    p.add_argument("--output-dir", required=True)
    p.add_argument("start_url")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    recurse(Wikipedia, args.start_url, args.output_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
